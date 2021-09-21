import requests
from bs4 import BeautifulSoup
import pandas as pd
import data_requests
import os
import concurrent.futures as cf
import time
import sys
from datetime import date

#Algorithm parameters
checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, adults, number_of_cicles, threads = (int(value) for value in sys.argv[1:-1])
chosen_city = sys.argv[-1]
nights = int(str(date(checkout_year, checkout_month, checkout_monthday)-date(checkin_year, checkin_month, checkin_monthday)).split()[0])

cities_id = data_requests.json_load('./cities_id.txt')

css_data = data_requests.json_load('./css_data_min2.txt')
if(adults>2):
    css_data = data_requests.json_load('./css_data_over2.txt')
    
def server_request(offset):
    #Send a get request to the website and beautiful-soup it
    url = data_requests.url_builder(cities_id[str(chosen_city)], adults, checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset)
    html = requests.get(url, headers=data_requests.user_agent_random(), proxies=data_requests.proxies_random()).text
    data = BeautifulSoup(html, 'html5lib')
    
    #Create a support temporary dataframe
    df = pd.DataFrame(columns=['hotel_name','score','n_reviews','total_price','category','city_center_dist', 'neighborhood', 'free_cancellation'])
    hotels_name, points, reviews, prices, category, center_d, nbhood, free_canc= ([] for i in range(0,8))
    
    #Get data on 4 different lists: assing a '0' value if there is no data available
    for hotel in data.select('div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout'):
        for i, values in enumerate([hotels_name, points, reviews, prices, category, center_d, nbhood, free_canc]):
            single_cell = hotel.select(css_data[list(css_data)[i]])
            if(len(single_cell)==0):
                values.append(0)
            else:
                for plain_data in single_cell:
                    values.append(plain_data.text)
    
    #Assigning values to the previously created dataframe
    df['hotel_name'] = pd.Series(hotels_name, dtype='object')
    df['score'] = pd.Series(points, dtype='object')
    df['n_reviews'] = pd.Series(reviews, dtype='object')
    df['total_price'] = pd.Series(prices, dtype='object')
    df['category'] = pd.Series(category, dtype='object')
    df['city_center_dist'] = pd.Series(center_d, dtype='object')
    df['neighborhood'] = pd.Series(nbhood, dtype='object')
    df['free_cancellation'] = pd.Series(free_canc, dtype='object')
    
    return(df)

def main():
    t0 = time.time()
    
    #Create a main db where we are going to store data
    main_df = pd.DataFrame()
    
    #Added a while loop because sometimes the get requests returns an empty value, there is probabily a block
    url=''
    while(url==''):
        #How many structures do we have to find?
        url = data_requests.url_builder(cities_id[str(chosen_city)], adults, checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset = 25)
    n_structures = data_requests.structures_number(url, data_requests.user_agent_random(), data_requests.proxies_random())
    print('N. of structures to find:',n_structures)
    
    #Booking.com pages always have different structures listed, so in this way we make sure that every hotel is present our final database.
    #Obviously the more we want to be near to the real number of hotels listed, the more we have to pay in calculus terms (time and resources).
    #Added multithreading capabilities.
    with cf.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(0,number_of_cicles):
            try:
                dfs = {executor.submit(server_request, offset) for offset in range(25,n_structures+25,25)}
                for future in cf.as_completed(dfs):
                    main_df = main_df.append(future.result())
            except Exception as e:
                print("General error:\n",e)
                
    
    #Drop duplicates to reduce calculation time and reset index
    main_df = main_df.drop_duplicates(subset='hotel_name')
    main_df = main_df.reset_index(drop=True)
    
    #Get rid of some useless symbols
    main_df = main_df.replace(['\n', '€', 'recensioni','\.'],'', regex=True)
    main_df = main_df.replace(',','.', regex=True)
    
    #Convert some columns values to the right data type
    main_df = main_df.astype({'n_reviews': int, 'total_price': int, 'score': float})
    
    #Adding a new column with per night price
    main_df['price_per_night'] = main_df.apply(lambda row: row['total_price']/nights, axis=1)
    
    #Giving structures the right category name
    main_df['category'] = main_df.apply(data_requests.category_placer, axis=1)
    
    #Taking the first value of the city center distance string
    main_df['city_center_dist'] = main_df['city_center_dist'].apply(lambda row: row.split()[0]).astype('float')
    
    #Cleaning neighborhood string
    main_df['neighborhood'] = main_df['neighborhood'].apply(data_requests.nbhood_placer)
    
    #Convert free cancellation string to boolean
    main_df['free_cancellation'] = main_df['free_cancellation'].apply(data_requests.free_canc_placer).astype('bool')
   
    #Export the data just found to a csv file.
    where_am_i = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(where_am_i,'data',str(chosen_city)+'_'+str(checkin_month)+'.'+str(checkin_monthday)+'_'+str(checkout_month)+'.'+str(checkout_monthday)+'.A'+str(adults)+'.csv')
    main_df.to_csv(my_file, index=False)
    
    t1 = time.time()
    
    hotel_found = main_df.shape[0]
    algo_eff = round(main_df.shape[0]/n_structures*100,1)
    algo_time = round(t1-t0,1)
    print('Hotels found:',hotel_found)
    print('Algorithm efficiency:', algo_eff,'%')
    print('It took',algo_time,'seconds to run the algorithm')
    
    with open('log.txt', 'a') as f:
        f.write(str(checkin_month)+","+str(checkin_monthday)+","+str(checkin_year)+","+str(checkout_month)+","+str(checkout_monthday)+","+str(checkout_year)+","+str(adults)+","+str(number_of_cicles)+","+str(threads)+","+str(chosen_city)+","+str(n_structures)+","+str(hotel_found)+","+str(algo_eff)+","+str(algo_time)+'\n')
    
if __name__ == "__main__":
    main()
    
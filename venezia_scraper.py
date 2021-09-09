#Useful libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import data_requests

checkin_month = 9
checkin_monthday = 13
checkin_year = 2021
checkout_month = 9
checkout_monthday = 20
checkout_year = 2021
number_of_cicles = 3

#Url, user-agent and proxy definition
url = data_requests.url_builder(checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset = 25)
random_ua = data_requests.user_agent_random()
random_proxy = data_requests.proxies_random()

css_data={'hotel_name':'span.sr-hotel__name',
        'score':'div.bui-review-score__badge',
        'n_reviews':'div.bui-review-score__text',
        'price':'div.bui-price-display__value.prco-inline-block-maker-helper'}

#How many structures do we have to find?
n_structures = data_requests.structures_number(url, random_ua, random_proxy)
print('n. of structures to find:',n_structures)

#Create a main db where we are going to store data
main_df = pd.DataFrame()

#It's a nested for loop. Why? Because booking.com pages always have different structures listed, so in this way we make sure that every hotel is present our final database.
#Obviously this is not the most efficient solution, in fact the script takes a while to run. In the future i'm going to implement multithreading.
for offset in range(25,n_structures+25,25):
    for i in range(0,number_of_cicles):
        try:
            #Send a get request to the website and beautiful-soup it
            url = data_requests.url_builder(checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset)
            html = requests.get(url, headers=random_ua, proxies=random_proxy).text
            data = BeautifulSoup(html, 'html5lib')
            
            #Create a support temporary dataframe
            df = pd.DataFrame(columns=['hotel_name','score','n_reviews','price'])
            hotels_name, points, reviews, prices = ([] for i in range(0,4))
            
            #Get data on 4 different lists: assing a '0' value if there is no data available
            for hotel in data.select('div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout'):
                for i, values in enumerate([hotels_name, points, reviews, prices]):
                    single_cell = hotel.select(css_data[list(css_data)[i]])
                    if(len(single_cell)==0):
                        values.append(0)
                    else:
                        for plain_data in single_cell:
                            values.append(plain_data.text)
            
            #Assigning values to the previously created dataframe
            df['hotel_name'] = hotels_name
            df['score'] = points
            df['n_reviews'] = reviews
            df['price'] = prices
            
            #Get rid of some useless symbols
            df = df.replace(['\n','€', 'recensioni','\.'],'', regex=True)
            df = df.replace(',','.', regex=True)
            
            #Convert some columns values to the right data type
            df = df.astype({"n_reviews": int, "price": int, 'score':float})
            
            main_df = main_df.append(df)
            
        except ValueError as e:
            print("General error. Check code again\n",e)
    print('Loading...',round(offset/n_structures*100,1),'%')
            
#Final cleaning of the dataset: drop duplicates values and reset the index.
main_df = main_df.drop_duplicates(subset='hotel_name')
main_df = main_df.reset_index(drop=True)

#Export the data found to a csv file.
main_df.to_csv('data.csv')

print('Hotels found:',main_df.shape[0])

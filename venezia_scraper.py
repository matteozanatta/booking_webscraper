import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

checkin_month = 9
checkin_monthday = 7
checkin_year = 2021
checkout_month = 9
checkout_monthday = 10
checkout_year = 2021

#Set the target url
url = 'https://www.booking.com/searchresults.it.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaHGIAQGYARS4ARjIAQzYAQPoAQGIAgGoAgS4AqHeyYkGwAIB0gIkMjIxNGU0YmQtNzgwNC00ODRiLThjYjQtYzIzZGQ5MzBkMWUy2AIE4AIB&sid=354b17468fcb271e6d29d808e886f749&tmpl=searchresults&checkin_month='+str(checkin_month)+'&checkin_monthday='+str(checkin_monthday)+'&checkin_year='+str(checkin_year)+'&checkout_month='+str(checkout_month)+'&checkout_monthday='+str(checkout_monthday)+'&checkout_year='+str(checkout_year)+'&class_interval=1&dest_id=-132007&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&src_elem=sb&srpvid=96b4595e98bb0166&ss=Venezia&ss_all=0&ssb=empty&sshis=0&ssne=Venezia&ssne_untouched=Venezia&top_ufis=1&rows=25&offset=25&sr_ajax=1&b_gtt=dLYAeZFVJfNTBBSLFYdRdPcPVJBJZeBFZXNTfKe&_=1630759358757'

#Random picker of User-Agent for html requests
def user_agent_random():
    with open('./user_agent.txt') as f:
        lines = f.readlines()
        n_lines = len(lines)
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
            'User-Agent': lines[random.choice(range(0,n_lines))].replace('\n',''),
            'Accept': 'text/html, */*; q=0.01',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            }
        return(headers)
        
#Get a proxies list from proxylist.com and return a python dictionary
def proxies_random():
    proxies_url = 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc'
    proxies_json = requests.get(proxies_url).json()
    proxies_ip = {}
    for i, value in enumerate(proxies_json['data']):
        proxies_ip[''+str(i)] = {'http':value['ip']}
    return(proxies_ip[random.choice(list(proxies_ip))])

#Retrieve the number of structures listed on booking with specific criterias
def structures_number(url, headers, proxies):
    html = requests.get(url, headers=headers).text
    data = BeautifulSoup(html, 'html5lib')
    n_structures = data.select('div.sr_header')
    for value in n_structures:
        return(int(value.text.split(' ')[1]))

master_df = pd.DataFrame()

random_ua = user_agent_random()
random_proxy = proxies_random()
n_structures = structures_number(url, random_ua, random_proxy)

print('Strutture da trovare',n_structures)

#It's a nested for loop. Why? Because pages have always different structures listed, so in this way we make sure that everything is working properly.
for offset in range(25,n_structures+25,25):
    for i in range(0,3):
        try:
            #Send a get request to the website and beautiful-soup it
            url = 'https://www.booking.com/searchresults.it.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaHGIAQGYARS4ARjIAQzYAQPoAQGIAgGoAgS4AqHeyYkGwAIB0gIkMjIxNGU0YmQtNzgwNC00ODRiLThjYjQtYzIzZGQ5MzBkMWUy2AIE4AIB&sid=354b17468fcb271e6d29d808e886f749&tmpl=searchresults&checkin_month='+str(checkin_month)+'&checkin_monthday='+str(checkin_monthday)+'&checkin_year='+str(checkin_year)+'&checkout_month='+str(checkout_month)+'&checkout_monthday='+str(checkout_monthday)+'&checkout_year='+str(checkout_year)+'&class_interval=1&dest_id=-132007&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&src_elem=sb&srpvid=96b4595e98bb0166&ss=Venezia&ss_all=0&ssb=empty&sshis=0&ssne=Venezia&ssne_untouched=Venezia&top_ufis=1&rows=25&offset='+str(offset)+'&sr_ajax=1&b_gtt=dLYAeZFVJfNTBBSLFYdRdPcPVJBJZeBFZXNTfKe&_=1630759358757'
            html = requests.get(url, headers=random_ua, proxies=random_proxy).text
            data = BeautifulSoup(html, 'html5lib')
            
            #Create a support dataframe
            df = pd.DataFrame(columns=['nome_struttura','punteggio','n_recensioni','prezzo'])
            hotels_name, points, reviews, prices = ([] for i in range(0,4))
            
            #CSS dictionary and an index-list for the next 'for' cicle 
            css_data={'nome_struttura':'span.sr-hotel__name',
                        'punteggio':'div.bui-review-score__badge',
                        'n_recensioni':'div.bui-review-score__text',
                        'prezzo':'div.bui-price-display__value.prco-inline-block-maker-helper'}
            index_list=['nome_struttura','punteggio','n_recensioni','prezzo']
            
            #Get data on 4 different lists: assing a '0' value if there is no data available
            for hotel in data.select('div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout'):
                for i, values in enumerate([hotels_name, points, reviews, prices]):
                    single_cell = hotel.select(css_data[index_list[i]])
                    if(len(single_cell)==0):
                        values.append(0)
                    else:
                        for plain_data in single_cell:
                            values.append(plain_data.text)
            
            #Assigning values to the previously created dataframe
            df['nome_struttura'] = hotels_name
            df['punteggio'] = points
            df['n_recensioni'] = reviews
            df['prezzo'] = prices
            
            #Get rid of symbols
            df = df.replace(['\n','€', 'recensioni','\.'],'', regex=True)
            df = df.replace(',','.',regex=True)
            
            #Convert some columns values to the right dtype
            df = df.astype({"n_recensioni": int, "prezzo": int, 'punteggio':float})
            
            #Append the new database to the main one
            master_df = master_df.append(df)

        except ValueError as e:
            print("General error. Check details given below\n",e)

master_df = master_df.drop_duplicates(subset='nome_struttura')
master_df = master_df.reset_index(drop=True)
master_df.to_csv('data.csv')
print('Hotel trovati:',master_df.shape[0])
#print(master_df.shape[0], master_df['prezzo'].median())'''
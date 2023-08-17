import requests
import random
from bs4 import BeautifulSoup 
import json
import numpy as np

#Random picker of User-Agent for html requests
def user_agent_random():
    with open('./user_agent.txt') as f:
        lines = f.readlines()
        n_lines = len(lines)
        return({
            'Host': 'www.booking.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
            'User-Agent': lines[random.choice(range(0,n_lines))].replace('\n',''),
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            })
        
#Get a proxies list from proxylist.com and return a python dictionary
def proxies_random():
    proxies_url = 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=100&speed=fast'
    proxies_json = requests.get(proxies_url).json()
    proxies_ip = {}
    for i, value in enumerate(proxies_json['data']):
        proxies_ip[''+str(i)] = {'http':value['ip']}
    return(proxies_ip[random.choice(list(proxies_ip))])

#Return the number of structures listed on booking with specific criterias
def structures_number(url, headers, proxies):
    html = requests.get(url, headers=headers, proxies=proxies).text
    data = BeautifulSoup(html, 'html5lib')
    n_structures = data.select('div.sr_header')
    for value in n_structures:
        return(int(value.text.split(' ')[1].replace(".","")))

#Return a booking.com url with given parameters
def url_builder(city_id, adults, checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset):
    room=''
    for count in range(0,adults-1):
        room+='A,'
    room+='A'
    return('https://www.booking.com/searchresults.it.html?tmpl=searchresults&checkin_month='+str(checkin_month)+'&checkin_monthday='+str(checkin_monthday)+'&checkin_year='+str(checkin_year)+'&checkout_month='+str(checkout_month)+'&checkout_monthday='+str(checkout_monthday)+'&checkout_year='+str(checkout_year)+'&class_interval=1&dest_id='+str(city_id)+'&dest_type=city&dtdisc=0&from_sf=1&group_adults='+str(adults)+'&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1='+str(room)+'&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset='+str(offset)+'&sr_ajax=1&changed_currency=1&selected_currency=EUR&top_currency=1')
   
#Load the requested json structure
def json_load(path):
    with open(path) as f:
        return(json.load(f))
    f.close()
 
def category_placer(row):
    structure_type = row['category'].split()[:3]
    if('B&B' in row['hotel_name']) or ('B&b' in row['hotel_name']):
        return 'Bed&Breakfast'
    elif('Camera' in structure_type) or ('Junior' in structure_type) or ('Suite' in structure_type):
        return 'Hotel'
    elif('Appartamento' in structure_type) or ('Monolocale' in structure_type) or ('Loft' in structure_type):
        return 'Apartment'
    elif('Casa' in structure_type):
        return 'Holiday Home'
    else:
        return 'Other'
        
def nbhood_placer(row):
    nbhood = row.split('.')[0]
    if ('sulla' in nbhood.split()) and ('mappa' in nbhood.split()):
        return 'Not specified'
    else:
        return nbhood
        
def free_canc_placer(row):
    splitted = str(row).split()
    if('Cancellazione' in splitted) and ('GRATUITA' in splitted):
        return True
    else:
        return False
        
def log_marks_creator(dataframe, variable, decimal):        
    marks = {}
    for i,value in enumerate(np.linspace(0,1,num=6)):
        quantile_value = dataframe[variable].quantile(value)
        #Logarithmic calculus
        if(quantile_value==0):
            log_value=-1
        else:
            log_value=np.log10(quantile_value)
        #added this check because there's a display bug on the first value if mark key=-1.0
        if(log_value==-1): 
            marks[int(log_value)]=round(quantile_value, decimal)
        else:
            marks[log_value]=round(quantile_value, decimal)
    return marks
    
def marks_creator(dataframe, variable, decimal):        
    marks = {}
    for i,value in enumerate(np.linspace(0,1,num=6)):
        quantile_value = dataframe[variable].quantile(value)
        #added this check because there's a display bug on the first and the last value
        if((i==0) | (i==5)): 
            marks[int(quantile_value)]=round(quantile_value, decimal)
        else:
            marks[quantile_value]=round(quantile_value, decimal)
    return marks
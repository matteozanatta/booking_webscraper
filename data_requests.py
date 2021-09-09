import requests
import random
from bs4 import BeautifulSoup 

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

#Return the number of structures listed on booking with specific criterias
def structures_number(url, headers, proxies):
    html = requests.get(url, headers=headers).text
    data = BeautifulSoup(html, 'html5lib')
    n_structures = data.select('div.sr_header')
    for value in n_structures:
        return(int(value.text.split(' ')[1]))

#Return a booking url with given parameters
def url_builder(checkin_month, checkin_monthday, checkin_year, checkout_month, checkout_monthday, checkout_year, offset):
    return('https://www.booking.com/searchresults.it.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaHGIAQGYARS4ARjIAQzYAQPoAQGIAgGoAgS4AqHeyYkGwAIB0gIkMjIxNGU0YmQtNzgwNC00ODRiLThjYjQtYzIzZGQ5MzBkMWUy2AIE4AIB&sid=354b17468fcb271e6d29d808e886f749&tmpl=searchresults&checkin_month='+str(checkin_month)+'&checkin_monthday='+str(checkin_monthday)+'&checkin_year='+str(checkin_year)+'&checkout_month='+str(checkout_month)+'&checkout_monthday='+str(checkout_monthday)+'&checkout_year='+str(checkout_year)+'&class_interval=1&dest_id=-132007&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&src_elem=sb&srpvid=96b4595e98bb0166&ss=Venezia&ss_all=0&ssb=empty&sshis=0&ssne=Venezia&ssne_untouched=Venezia&top_ufis=1&rows=25&offset='+str(offset)+'&sr_ajax=1&b_gtt=dLYAeZFVJfNTBBSLFYdRdPcPVJBJZeBFZXNTfKe&_=1630759358757')
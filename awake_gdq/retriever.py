#\usr\bin\python3

import urllib3
from bs4 import BeautifulSoup
import re
import datetime

from awake_gdq.schedule import *

## retrieve the schedule from the official website ##

sc_url = 'https://gamesdonequick.com/schedule'
http = urllib3.PoolManager()
sc_table_id = 'runTable'

def get_date(date_str) :
    # format used : 'AAAA-MM-DDThh:mm:ssZ'

    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date

def get_estimate(estimate_str) :
    # format used : (h)h:mm:ss
    estimate = datetime.datetime.strptime(estimate_str, '%H:%M:%S')
    estimate = datetime.timedelta(hours=estimate.hour, minutes=estimate.minute, seconds=estimate.second)
    return estimate

def get_schedule(sc, path = '') :
    sc_page_data = None
    if path == '' :
        sc_page = http.request('GET', sc_url, headers={})
        sc_page_data = BeautifulSoup(sc_page.data, 'html.parser')
    else :
        sc_page = open(path, 'r')
        sc_page_data = BeautifulSoup(sc_page.read(), 'lxml')
        sc_page.close()

    sc_table = sc_page_data.find('table', attrs={'id':sc_table_id}).find('tbody')

    sc_info_1 = sc_table.find_all('tr', attrs={'class':''})
    sc_info_2 = sc_table.find_all('tr', attrs={'class':'second-row'})
    sc_info = None
    for (entry_1, entry_2) in zip(sc_info_1, sc_info_2) :
        data_1 = entry_1.find_all('td')
        data_2 = entry_2.find_all('td')

        sc.add_sc(date = get_date(data_1[0].text), \
                title = data_1[1].text, \
                runners = data_1[2].text, \
                estimate = get_estimate(data_2[0].text.strip()), \
                category = data_2[1].text)

## --- ##

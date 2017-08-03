# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:30:40 2017

@author: ndoannguyen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:33:56 2017

@author: ndoannguyen
"""
# Get the first 5 hits for "google 1.9.1 python" in Google Pakistan
#
import requests, re
import time
import urllib
from bs4 import BeautifulSoup

from google import search

def ask_sinovietnamese_word(word):

    r = requests.get('http://www.google.com.vn/search',
            params={'q': '%s' % (urllib.quote(word).replace("%20", "+")), 'start': pos})
    soup = BeautifulSoup(r.text)

    print soup
    text = soup.find('div',{'id':'resultStats'}).text
    if text == "":
        return 0

    text = text.replace('.', '')
    number_list = re.findall(r'\d+', text)
    nb_results = number_list[-1]
    return int(nb_results)

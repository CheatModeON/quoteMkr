#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import time
import json

def countword(str):
    count = 0;
    words = str.split()
    for word in words:
        count += 1
    return count

def fetchQuotes(max_words, keyword):
    #resp = requests.get('http://www.quotationspage.com/search.php?Search='+keyword+'&startsearch=Search&Author=&C=mgm&C=motivate&C=classic&C=coles&C=poorc&C=lindsly&page=1')

    f = open("json/"+keyword+".json", "w")

    html_data = ''
    count = 1
    oldQuotes =""
    final=[]
    while True:
        resp = requests.get('https://www.goodreads.com/quotes/search?commit=Search&page='+str(count)+'&q='+keyword+'&utf8=✓')
        if resp.ok:
            html_data = resp.text
        else:
            print ("Error! {}".format(resp.status_code))
            print (resp.text)
                

        soup = BeautifulSoup(html_data, 'html.parser')

        test = soup.find_all('div', class_='mediumText')[0].text.split()[0]
        if(test=='Sorry,'):
            print(json.dumps(final, sort_keys=True, indent=2))
            
            f.write(json.dumps(final, sort_keys=True, indent=2))
            f.close()
            exit()

        #quotes = soup.find_all('dt', class_ = 'quote')
        #authors = soup.find_all('dd', class_ = 'author')

        quotes = soup.find_all('div', class_ = 'quoteText')
        authors = soup.find_all('span', class_ = 'authorOrTitle')
        
        output =[]
        newQuotes =[]
        for t in range(len(quotes)):
            data={}
            if(countword(quotes[t].text) < max_words):
                test = quotes[t].text.encode('utf-8')
                
                data['quote'] = test.split("―",1)[0].replace('      ','').replace('\n','').replace('“','').replace('”','').replace('    ','')
                data['author'] = authors[t].text.replace('\n','').replace('    ','').replace('  ','').replace('    ','')
                
                output.append(data)
                final.append(data.copy())

            test = quotes[t].text.encode('utf-8')
            data['quote'] = test.split("―",1)[0].replace('      ','').replace('\n','').replace('“','').replace('”','').replace('    ','')
            data['author'] = authors[t].text.replace('\n','').replace('    ','').replace('  ','').replace('    ','')
            newQuotes.append(data)

        if(oldQuotes==newQuotes):
            print(json.dumps(final, sort_keys=True, indent=2))
            
            f.write(json.dumps(final, sort_keys=True, indent=2))
            f.close()
            exit()

        #if(output!={}):
        #    print(json.dumps(output, sort_keys=True, indent=2))
        count += 1
        oldQuotes = newQuotes


    print(json.dumps(final, sort_keys=True, indent=2))

    f.write(json.dumps(final, sort_keys=True, indent=2))
    f.close()


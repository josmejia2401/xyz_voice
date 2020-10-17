#!/usr/bin/python3
#Scraping wikipedia page according to your command line input
import sys
import requests
import bs4
res = requests.get('https://es.wikipedia.org/wiki/colombia')

res.raise_for_status()
#Just to raise the status code
wiki = bs4.BeautifulSoup(res.text,"lxml")
elems = wiki.select('p')
for i in range(len(elems)):
    if elems[i].getText().strip():
        print(elems[i].getText().strip())
        break
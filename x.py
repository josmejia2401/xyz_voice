#!/usr/bin/env python3
import requests

r1 = requests.get('http://api.ipstack.com/check?access_key=5aec9b31b13f035849b504b3eb632ec0&format=1')
if r1.status_code == 200:
    result = r1.json()
    country_name = result['country_name']
    region_name = result['region_name']
    city = result['city']
    print(result)
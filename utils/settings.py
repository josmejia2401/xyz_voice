"""
Open weather map API settings
Create key: https://openweathermap.org/appid
"""
WEATHER_API = {
    "URL" : "http://api.openweathermap.org/data/2.5/weather?q={0}&units={1}&lang={2}&appid={3}",
    "KEY" : "d504c812d3974c7628d4475c4eb74ff5",
    "CITY": "BOGOTA",
    "UNITS": "metric",
    "LANG": "es"
}

IPSTACK_API = {
    "URL" : "http://api.ipstack.com/check?access_key={}&format=1",
    "KEY" : "5aec9b31b13f035849b504b3eb632ec0"
}
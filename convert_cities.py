import requests
import json
import sys
from collections import defaultdict

API_KEY = ''
METRO_ARTIST_PREFIX =  'http://ws.audioscrobbler.com//2.0/?method=geo.getmetroartistchart'
METRO_ARTIST_POSTFIX = '&limit=10&' + API_KEY + '&format=json'


cities = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key=0ea35acc68848f320352bfa76c4c6494&format=json').json

city_file = defaultdict(dict)

f = open("city_country_conversion.json", "w")
for city in cities['metros']['metro']:
    city_file[city['name']] = city['country']
    
f.write(json.dumps(city_file))
f.close()

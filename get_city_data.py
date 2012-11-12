import requests
import json

METRO_ARTIST_PREFIX =  'http://ws.audioscrobbler.com//2.0/?method=geo.getmetroartistchart'
METRO_ARTIST_POSTFIX = '&api_key=0ea35acc68848f320352bfa76c4c6494&format=json'


cities = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key=0ea35acc68848f320352bfa76c4c6494&format=json').json

for city in cities['metros']['metro']:
    city_string = METRO_ARTIST_PREFIX + '&country=' + city['country'] + '&metro=' + city['name'] + METRO_ARTIST_POSTFIX
    print "CITY: " + str(city['name'])
    top_artists = requests.get(city_string).json
    for artist in top_artists['topartists']['artist']:
        print artist['name']

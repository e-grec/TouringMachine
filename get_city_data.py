import requests
import json

METRO_ARTIST_PREFIX =  'http://ws.audioscrobbler.com//2.0/?method=geo.getmetroartistchart'
METRO_ARTIST_POSTFIX = '&limit=500&api_key=0ea35acc68848f320352bfa76c4c6494&format=json'


cities = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key=0ea35acc68848f320352bfa76c4c6494&format=json').json

file = open("artist_dump.json", "w")
for city in cities['metros']['metro']:
    city_string = METRO_ARTIST_PREFIX + '&country=' + city['country'] + '&metro=' + city['name'] + METRO_ARTIST_POSTFIX
    top_artists = requests.get(city_string)
    print city['country']
    file.write(json.dumps(top_artists.json))


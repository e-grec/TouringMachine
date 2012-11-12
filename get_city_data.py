import requests

METRO_ARTIST_PREFIX =  '/2.0/?method=geo.getmetroartistchart'
METRO_ARTIST_POSTFIX = 'api_key=0ea35acc68848f320352bfa76c4c6494&format=json'


cities = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&api_key=0ea35acc68848f320352bfa76c4c6494&format=json')
print r.text
#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import time

import bottle
from recommender import Recommender
from settings import settings

_searcher = None

MAPS_PREFIX = 'http://maps.googleapis.com/maps/api/staticmap?size=768x380'
MAPS_MARKERS = '&markers=size:mid%7Ccolor:red%7Clabel:'
MAPS_POSTFIX = '&sensor=false'
STYLE_TYPE = '7C'

@bottle.route('/bandsearch')
def search(name='World'):
    global _searcher
    query = bottle.request.query.q.lower()
    start_time = time.time()
    cities = _searcher.get_city_rankings(query)
    end_time = time.time()
    
    #Construct Google Maps image
    gmurl = MAPS_PREFIX
    city_num = 1
    for city in cities:
        gmurl += MAPS_MARKERS + str(city_num) + '%' + STYLE_TYPE + city['city_name'].replace(' ', '+') + '%'
        city_num += 1
    gmurl += MAPS_POSTFIX
    print "gmurl: " + gmurl
    #Return dict
    return dict(
            cities = cities,
            count = len(cities),
            time = end_time - start_time,
            google_maps_url = gmurl
            )


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


if __name__=="__main__":
    _searcher = Recommender()
    bottle.run(host=settings['http_host'],
               port=settings['http_port'],
               reloader=True)

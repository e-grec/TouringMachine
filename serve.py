#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import time

import bottle
from recommender import Recommender
from settings import settings

_searcher = None

@bottle.route('/search')
def search(name='World'):
    global _searcher
    query = bottle.request.query.q
    start_time = time.time()
    tweets = _searcher.search_results(query)
    end_time = time.time()

    return dict(
            tweets = tweets,
            author = settings['author'],
            agree_to_honor_code = settings['agree_to_honor_code'],
            count = len(tweets),
            time = end_time - start_time,
            )

@bottle.route('/bandsearch')
def search(name='World'):
    global _searcher
    query = bottle.request.query.q
    start_time = time.time()
    cities = _searcher.get_city_rankings(query)
    end_time = time.time()

    return dict(
            cities = cities,
            author = settings['author'],
            agree_to_honor_code = settings['agree_to_honor_code'],
            count = len(cities),
            time = end_time - start_time,
            )


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')

@bottle.route('/test.html')
def favicon():
    
    return bottle.static_file('/test.html', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


if __name__=="__main__":
    _searcher = Recommender()
    bottle.run(host=settings['http_host'],
               port=settings['http_port'],
               reloader=True)

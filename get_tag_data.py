#!/usr/bin/env python
import requests
import json
import sys
import time

file = open("artist_dump.json")
artist_set = set()

for line in file:
    if len(line) < 200:
        continue

    top_artists = json.loads(line)
    top_artists = top_artists['topartists']
    ranked_artists = top_artists['artist']
    for artist in ranked_artists:
        artist_set.add(artist['name'].replace(' ','%20'))
API_KEY = ''
TAG_PREFIX =  'http://ws.audioscrobbler.com//2.0/?method=artist.gettoptags'
TAG_POSTFIX = '&api_key=' + API_KEY + '&format=json'
file = open("tag_dump.json", "w")
i = 0
for artist in artist_set: 
    i += 1
    print "[" + str(i) + "]Requesting " + artist + " ......"
    tag_string = TAG_PREFIX + '&artist=' + artist + TAG_POSTFIX
    top_tags = requests.get(tag_string)
    file.write(json.dumps(top_tags.json) + '\n')
    time.sleep(1)   # last.fm recommends limiting to 1 call/second

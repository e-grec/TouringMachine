#!/usr/bin/env python
import requests
import json
import sys

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

TAG_PREFIX =  'http://ws.audioscrobbler.com//2.0/?method=artist.gettoptags'
TAG_POSTFIX = '&api_key=fee41939e7b3fb451b45351ff55a0514&format=json'

file = open("tag_dump.json", "w")
for artist in artist_set: 
    tag_string = TAG_PREFIX + '&artist=' + str(artist) + TAG_POSTFIX
    top_tags = requests.get(tag_string)
    file.write(json.dumps(top_tags.json))

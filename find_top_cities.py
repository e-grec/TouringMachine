#!/usr/bin/env python
import json
import sys
from collections import defaultdict


"""
To use, run 'python find_top_cities.py bandName'
The program will print every city that the band is ranked in (in order)
"""

# For each metro, store a list of bands ordered by popularity (from most to least)
# metro_artist_chart['seattle'] = ['band1', 'band2', ...]
metro_artist_chart = defaultdict( list )

# For each artist, store a (city, ranking) pair
# artist_rankings['Muse'] =  [('boston', 4), (dallas, 41), ...]
artist_rankings = defaultdict( list )


# Open the file
file = open("artist_dump.json")

# Sets to see number of unique items
artist_set = set()
metros = set()

# Read the data city by city
for line in file:
    if len(line) < 200:
        continue    # In some cases, metros have no artists
                    # Which causes errors in the process

    top_artists = json.loads(line) # The top artist in a metro
    top_artists = top_artists['topartists']
    metro = top_artists['@attr']['metro']
    metros.add(metro)
    ranked_artists = top_artists['artist']
    for artist in ranked_artists:
        artist_name = artist['name'].lower() # TODO Remove special characters
        artist_rank = int(artist['@attr']['rank'])

        metro_artist_chart[metro].append(artist_name)	
        artist_rankings[artist_name].append( (metro, artist_rank) )

# For each number one artist, store a counter of their popularity
# number_one_artist['Muse'] =  5
number_one_artists = defaultdict(int)
for metro in metros:
    number_one_artists[metro_artist_chart[metro][0]] += 1
    #print metro + " : " + metro_artist_chart[metro][0]

# Sort based on most popular
for key, value in sorted(number_one_artists.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)

#print "Total cities: " + str(len(metros))
#print "Total artists: " + str( len(artist_set) )

# Lookup a band given as a parameter
if len(sys.argv) > 1:
    search_term = sys.argv[1]
else:
    search_term = 'queen'


# Search and sort by rank
search_rankings = sorted(artist_rankings[search_term], key=lambda city:city[1])

print "--- Top Cities for " + search_term + " (in order) ---"
print "City: rank"

for city in search_rankings:
    print city[0] + ": " + str(city[1])




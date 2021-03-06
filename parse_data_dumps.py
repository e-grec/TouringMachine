#!/usr/bin/env python

import json
import sys
from collections import defaultdict


class ParseDataDumps(object):   
    """
    ParseDataDumps is a class of helper functions that given a block of json 
    text, will parse the json and put any relevant information into a 
    dictionary of only necessary information (or another appropriate data
    structure)
    """

    def __init__(self):

        # For each metro, store a list of bands ordered by popularity (from most to least)
        # metro_artist_chart['seattle'] = ['band1', 'band2', ...]
        self.metro_artist_chart = defaultdict( list )

        # For each artist, store a (city, ranking) pair
        # artist_rankings['Muse'] =  [('boston', 4), (dallas, 41), ...]
        self.artist_rankings = defaultdict( list )

        # Store each unique artist
        self.artists = set()

        # Store a list of (tag, count) pairs for each artist
        # artist_tags['Queen'] = [('rock', 75), ('classic', 55), ...]
        self.artist_tags = defaultdict( list )
        

    def parse_metro_artist_chart(self, file_name):
        """
        Given the JSON dump of geo.getmetroartistchart calls for every metro, 
        store for each artist the list of ranks and cities they're ranked in

        file_name - location of the file that contains the last.fm dump

        self.artist_rankings - a dictionary whose key is an artist that contains 
        a list of (city, rank) tuples 
        """

        # Open the file
        file = open(file_name)

        # Read the data city by city
        for line in file:
            if len(line) < 200:
                continue    # In some cases, metros have no artists
                            # Which causes errors in the process

            top_artists = json.loads(line) # The top artists in a metro

            top_artists = top_artists['topartists']
            metro = top_artists['@attr']['metro']
            ranked_artists = top_artists['artist']
            for artist in ranked_artists:

                artist_name = artist['name'].lower() # TODO Remove special characters
                artist_rank = int(artist['@attr']['rank'])

                self.artists.add( artist_name )
                self.metro_artist_chart[metro].append(artist_name)	
                self.artist_rankings[artist_name].append( (metro, artist_rank) )
            for artist in self.artist_rankings:
                self.artist_rankings[artist] = sorted(self.artist_rankings[artist], key=lambda city:city[1])

        
    def parse_top_tags(self, file_name):
        """
        Given the JSON dump of artist.getTopTags for every ranked artist, store for 
        each artist each of their tags and the count of each tag as a (tag, count)
        pair.

        file_name - location of the file that contains the last.fm dump
        """        

        file = open(file_name)

        for line in file:
            if len(line) < 10 or line == 'null':
                continue
    
            top_tags = json.loads(line)

            if "message" in top_tags or "#text" in top_tags['toptags']:
                continue

            artist_name = top_tags['toptags']['@attr']['artist'].lower()
            top_tags = top_tags['toptags']['tag']
            for tag in top_tags:

                # JSON has different format if only one tag
                if type(tag) is not dict:    
                    tag_name = top_tags['name']
                    tag_count = top_tags['count']
                    break
                else:               
                    tag_name = tag['name']
                    tag_count = int( tag['count'] )

                self.artist_tags[artist_name].append( (tag_name, tag_count) )

    def sendToFile(self):
        self.parse_metro_artist_chart("artist_dump.json")
        self.parse_top_tags("tag_dump.json")
        f = open('city_rankings.json', 'wb')
        f.write(json.dumps(self.metro_artist_chart))
        f.close()
        f = open('artist_rankings.json', 'wb')
        f.write(json.dumps(self.artist_rankings))
        f.close()
        f = open('artist_tags.json', 'wb')
        f.write(json.dumps(self.artist_tags))
        f.close()
        
        #data = json.load(open('city_rankings.json'))
        #for city in data:
            #print "city: " + str(city)
            #print "bands in city: " + str(data[city])

if __name__=="__main__":
    # Lookup a band given as a parameter
    #if len(sys.argv) > 1:
     #   search_term = sys.argv[1]
    #else:
    #    search_term = 'queen'
    parser = ParseDataDumps()
    parser.sendToFile()



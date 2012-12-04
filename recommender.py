#!/usr/bin/env python

import json
import sys
from parse_data_dumps import ParseDataDumps
from collections import defaultdict
# make sure you have installed: sudo apt-get install python-numpy python-scipy
from scipy.stats.stats import pearsonr
from math import sqrt 

#cosine similarity helper functions
def scalar(collection): 
    total = 0 
    for coin, count in collection.items(): 
        total += count * count 
    return sqrt(total) 

def similarity(A,B):
    total = 0 
    for kind in A: 
        if kind in B: 
            total += A[kind] * B[kind] 
    return float(total) / (scalar(A) * scalar(B))


class Recommender(object):
    """
    This Recommender class takes a json of tagged artists, parses them,
    takes a user (defaulted to an account made for the demo: DrCaverlee)
    and gives a percentage recommendation based on a new artist given
    """

    def __init__(self):
        # parser for the user data
        self.user_parser = ParseDataDumps()

        # parser for the artists
        self.artist_parser = ParseDataDumps()

        # Pearson coefficient represented as:
        # Pearson_coeff['pop'] = 0.344
        self.Pearson_coeff = defaultdict(float)

        # set of unique tags found in both the users data
        # as well as the artists' data
        self.tags = set()
        
        # maps an artist to their tags and tag weight
        # artists['psy'] = {'guilty pleasure': 46, 'awesome': 100, 'auto tuned': 99}
        self.artists = defaultdict(list)

        # maps tags to summed weighted average unique to the user
        # weighted_user_vec['awesome'] = -76.79
        self.weighted_user_vec = defaultdict(float)
    
        # loads city_rankings.json, which is a serialized list of artists from each city.  The type maps cities as strings to a *ranked* list of artists within each city.
        self.city_rankings = json.load(open('city_rankings.json'))
        self.artist_rankings = json.load(open('artist_rankings.json'))
        self.artist_tags = json.load(open('artist_tags.json'))
        self.recommendations = json.load(open('artist_recommendation.json'))
    
    #TODO: change to use the api http://ws.audioscrobbler.com/2.0/?method=user.gettoptags&user=DrCaverlee
    def get_user(self):
        # will give self.parser.artist_tags Caverlee's user tags
        self.user_parser.parse_top_tags( "DrCaverlee.json" )
        self.artist_parser.parse_top_tags( "demo.json" )   
        self.tags = self.user_parser.tags.union(self.artist_parser.tags)

    #calc_Pearson calculates the Pearson correlation of an artist to the user
    def calc_Pearson(self):
        a = set(self.user_parser.tags)        
        user_dict = defaultdict(float)
        for tag_name, tag_count in self.user_parser.artist_tags['drcaverlee']:
                user_dict[tag_name] = tag_count

        for artist in self.artist_parser.artist_tags:
            user_list = []
            artist_list = []
            b = set()
                    
            artist_dict = defaultdict(float)
            for tag_name, tag_count in self.artist_parser.artist_tags[artist]:
                b.add(tag_name)
                artist_dict[tag_name] = tag_count          

            if a.intersection(b):
                for tag in a.intersection(b):
                    user_list.append(user_dict[tag])
                    artist_list.append(artist_dict[tag])
            self.artists[artist] = artist_dict
            self.Pearson_coeff[artist] = pearsonr(user_list,artist_list)[0]

    # calculeted the unique summed weighted vector for the user
    # to be used in calculating a recommendation
    def calc_user_tag_vector(self):
        for tag in self.tags:
            weight = 0
            for artist in self.artists: 
                if self.artists[artist][tag] != 0:
                    weight += self.artists[artist][tag] * self.Pearson_coeff[artist]  
            self.weighted_user_vec[tag] = weight
            
    # this function returns the cosine similarity of the weighted
    # vector to an unknown artist, tagged by last.fm users
    # and converted to a percentage for the user to see how
    # "likely" they are to enjoy the band
    def calc_recommendation(self, artist):
        parser = ParseDataDumps()
        #TODO: change to read from tag_data.json on large scale
        parser.parse_top_tags( artist + ".json" )
        user_dict = defaultdict(float)
        for tag_name, tag_count in parser.artist_tags['one direction']:
                user_dict[tag_name] = tag_count
        print "Caverlee is " + str(similarity(user_dict,self.weighted_user_vec)*100) + "% likely to enjoy the band One Direction"

    def get_city_rankings(self, search_term):
        
        if not search_term in self.artist_rankings:
            return []

        for sim_artist in self.recommendations[search_term]:
                self.recommendations[search_term] = sorted(self.recommendations[search_term], key=lambda recommendation:recommendation[1], reverse=True)

        result = []
        counter = 0
        for pair in self.artist_rankings[search_term]:
            i = 0
            similar_artists = []
            similarity = []
            for i in range(5):
                similar_artists.append(self.recommendations[search_term][i][0])
                similarity.append(str(round(self.recommendations[search_term][i][1]*100,2)))
            counter+=1
            result.append({'city_name':pair[0], 'relative_rank':counter,'similar_artists':similar_artists,'similarity':similarity,'band_name':search_term})
               
        return result
        

if __name__=="__main__":
    recom = Recommender()
    recom.get_city_rankings("queen")
    #recom.get_user()
    #recom.calc_Pearson()
    #recom.calc_user_tag_vector()
    #recom.calc_recommendation('one_direction')

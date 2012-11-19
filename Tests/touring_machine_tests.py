#!/usr/bin/env python
# script to test Touring Machine operations
import unittest
from parse_data_dumps import ParseDataDumps


class TestClustering(unittest.TestCase):
    def setUp(self):
    
        # Parse data dumps
        self.search_term = "kanye west"
        self.parser = ParseDataDumps()
        self.parser.parse_metro_artist_chart( "test_artist_dump.json" )
        self.parser.parse_top_tags( "tag_dump.json" )

        self.artist_rankings = self.parser.artist_rankings
        self.search_rankings = sorted(self.artist_rankings[self.search_term], key=lambda city:city[1])

        self.artist_tags = self.parser.artist_tags[self.search_term]
        #print artist_tags

    
    def test_rank(self):
        artist_rankings = self.parser.artist_rankings
        search_rankings = sorted(self.artist_rankings[self.search_term], key=lambda city:city[1])

        #self.artist_tags = self.parser.artist_tags[self.search_term]
        #print artist_tags
        self.assertEqual(self.search_rankings[0][1],1)

    def test_top_tag(self):
        artist_tags = self.parser.artist_tags[self.search_term]
        print artist_tags
        self.assertEqual(self.artist_tags[0][0], "Hip-Hop")
        self.assertEqual(self.artist_tags[0][1], 100)
        

if __name__ == '__main__':
    unittest.main()

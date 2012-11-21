TouringMachine
==============

CSCE 470 Project which allows you to construct a euler tour of the cities that
like your band/artist the most! It will also recommend similar artists to play
with in each city.


To run the main code, type in the following command:

python parse_data_dumps.py "dream theater"

Where "dream theater" may be your favorite band (include quotes).  After entering the command, the script will 
output the band's most popular cities and its tags.  To run tests, use nosetests.

To run the recommender, run:
python recommender.py

This will run the recommendation algorithm on a small set of data and output a recommendation.

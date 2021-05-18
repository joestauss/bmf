import unittest
from ffwen.extractors import IMDbPY_Context
from collections import namedtuple

class Test_Identifiers( unittest.TestCase):

    def setUp( self):
        KnownFilm = namedtuple( 'KnownFilm', [ 'title', 'year', 'id'])
        self.films = [
            KnownFilm( 'Doctor Zhivago', 1965, '0059113'),
            KnownFilm( 'Caddyshack'    , 1980, '0080487')
        ]

    def test_film_identifier( self):
        imdb = IMDbPY_Context()
        for title, year, known_id in self.films:
            self.assertEqual( imdb.get_movie_id( title, year), known_id)

if __name__ == "__main__":
    unittest.main()

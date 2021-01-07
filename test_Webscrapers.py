from UnitTest_Resources import *
from webscrapers import *
from utility_methods import *
import unittest

class TestWebscrapers( unittest.TestCase):
    def test_ActingFilmographySearch( self):
        with self.assertRaises( ValueError):
            Webscraper.IMDB.Person.acting_filmography('I am not a valid person ID')

        for person_id, known_film_ids in TestCases.Webscrapers.filmography_search:
            filmography = Webscraper.IMDB.Person.acting_filmography( person_id)
            for film in known_film_ids:
                self.assertTrue( film in filmography)

        filmography = Webscraper.IMDB.Person.acting_filmography( PersonID.renee_zellweger )
        self.assertTrue( 'tt0045888' not in filmography)  # house of wax came out before she was born.

if __name__ == '__main__':
    unittest.main()

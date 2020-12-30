from UnitTest_Resources import *
from webscrapers import *
import unittest

class TestWebscrapers( unittest.TestCase):

    def test_ActingFilmographySearch( self):
        for author_id, known_film_ids in TestCases.Webscrapers.filmography_search:
            filmography = Webscraper.IMDB.Actor.acting_filmography( author_id)
            for film in known_film_ids:
                self.assertTrue( film in filmography)
        filmography = Webscraper.IMDB.Actor.acting_filmography( ActorID.renee_zellweger )
        self.assertTrue( 'tt0045888' not in filmography)  # house of wax came out before she was born.

if __name__ == '__main__':
    unittest.main()

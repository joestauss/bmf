from UnitTest_Resources import *
from webscrapers import *
import unittest

class TestSearch( unittest.TestCase):
    def test_SearchForTitleAndYear( self):
        for imdb_id, title, year in TestCases.Webscrapers.validated_films:
            self.assertEqual( Webscraper.IMDB.Search.for_title_and_year(imdb_id), (title, year))

    def test_SearchByTitleAndYear( self):
        for imdb_id, title, year in TestCases.Webscrapers.validated_films:
            self.assertEqual( Webscraper.IMDB.Search.by_title_and_year(title, year), (imdb_id, year))

    def test_SearchForPersonName( self):
        for actor_id, actor_name in TestCases.Webscrapers.validated_actor_ids:
            self.assertEqual( Webscraper.IMDB.Search.for_person_name(actor_id), actor_name)

    def test_SearchByPersonName( self):
        for actor_id, actor_name in TestCases.Webscrapers.validated_actor_ids:
            self.assertEqual( Webscraper.IMDB.Search.by_person_name(actor_name), actor_id)

if __name__ == '__main__':
    unittest.main()

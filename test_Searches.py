from test_Resources import *
from webscrapers import *
import unittest

class TestSearch( unittest.TestCase):
    def test_SearchForTitleAndYear( self):
        for film_id, title, year in TestCases.Webscrapers.validated_films:
            self.assertEqual( Webscraper.IMDB.Search.for_title_and_year(film_id), (title, year))

    def test_SearchByTitleAndYear( self):
        for film_id, title, year in TestCases.Webscrapers.validated_films:
            self.assertEqual( Webscraper.IMDB.Search.by_title_and_year(title, year), (film_id, year))

    def test_SearchForPersonName( self):
        for person_id, person_name in TestCases.Webscrapers.validated_person_ids:
            self.assertEqual( Webscraper.IMDB.Search.for_person_name(person_id), person_name)

    def test_SearchByPersonName( self):
        for person_id, person_name in TestCases.Webscrapers.validated_person_ids:
            self.assertEqual( Webscraper.IMDB.Search.by_person_name(person_name), person_id)

if __name__ == '__main__':
    unittest.main()

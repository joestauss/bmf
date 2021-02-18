from bmb.extractors import MyWebscraper
import unittest

class Test_MyWebscraper_Search( unittest.TestCase):
    def setUp( self):
        self.validated_films = [
            ('tt0087892', "A Passage to India", 1984),
            ('tt0045888', "House of Wax", 1953),
            ('tt0397065', "House of Wax", 2005)
        ]

        self.validated_person_ids = [
            ('nm0000246', "Bruce Willis"),
            ('nm0001637', "Vincent Price")
        ]

    def test_Search_ForTitleAndYear( self):
        for film_id, title, year in self.validated_films:
            self.assertEqual( MyWebscraper.IMDB_Search.for_title_and_year(film_id), (title, year))

    def test_Search_ByTitleAndYear( self):
        for film_id, title, year in self.validated_films:
            self.assertEqual( MyWebscraper.IMDB_Search.by_title_and_year(title, year), (film_id, year))

    def test_Search_ForPersonName( self):
        for person_id, person_name in self.validated_person_ids:
            self.assertEqual( MyWebscraper.IMDB_Search.for_person_name(person_id), person_name)

    def test_Search_ByPersonName( self):
        for person_id, person_name in self.validated_person_ids:
            self.assertEqual( MyWebscraper.IMDB_Search.by_person_name(person_name), person_id)

if __name__ == '__main__':
    unittest.main()

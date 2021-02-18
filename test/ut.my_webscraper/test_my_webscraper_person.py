from bmb.extractors import MyWebscraper
import unittest

class Test_MyWebscraper_Person( unittest.TestCase):
    def setUp( self):
        self.known_filmography_entries = [
            ( 'nm0001637', ['tt0099487', 'tt0045888', 'tt0081178'] ), # Vincent Price: Ed S'hands, house of wax, monster club
            ( 'nm0000246',  ['tt0095016']) # Bruce Willis: Die Hard
        ]

    def test_Person_FullName( self):
        self.assertEqual( 'Bruce Willis', MyWebscraper.IMDB_Person.full_name( 'nm0000246'))

    def test_Person_ActingFilmography( self):
        with self.assertRaises( ValueError):
            MyWebscraper.IMDB_Person.acting_filmography('I am not a valid person ID')

        for person_id, known_film_ids in self.known_filmography_entries:
            filmography = MyWebscraper.IMDB_Person.acting_filmography( person_id)
            for film in known_film_ids:
                self.assertTrue( film in filmography)

        filmography = MyWebscraper.IMDB_Person.acting_filmography(  'nm0000250' ) # renee zelwegger
        self.assertTrue( 'tt0045888' not in filmography)  # house of wax came out before she was born.

if __name__ == '__main__':
    unittest.main()

from ffwen.extractors import MyWebscraper
import unittest

class Test_MyWebscraper_Film( unittest.TestCase):
    def setUp( self):
        self.known_metadata = {
            'tt0247745' : {
                'title'    : 'Super Troopers',
                'year'     : 2001,
                'genres'   : {'Comedy', 'Crime', 'Mystery'},
                'taglines' : {"Altered State Police"},
                'prod co'  : "Broken Lizard Industries"
            }
        }
        self.false_metadata = {
            'tt0247745' : {
                'title' : 'NOT Super Troopers',
                'year'  : 2002
            }
        }


    def test_Film_TitleAndYear( self):
        for film_id, known_dd in self.known_metadata.items():
            if 'title' in known_dd and 'year' in known_dd:
                search_dd = MyWebscraper.IMDB_Film.title_and_year( film_id)
                self.assertTrue( search_dd['title'] == known_dd['title'])
                self.assertTrue( search_dd['year' ] == known_dd['year' ])

        for film_id, false_dd in self.false_metadata.items():
            if 'title' in false_dd and 'year' in false_dd:
                search_dd = MyWebscraper.IMDB_Film.title_and_year( film_id)
                self.assertTrue( search_dd['title'] != false_dd['title'])
                self.assertTrue( search_dd['year' ] != false_dd['year' ])

    def test_Film_Genres( self):
        for film_id, known_dd in self.known_metadata.items():
            if 'genres' in known_dd:
                search_dd = MyWebscraper.IMDB_Film.main_page( film_id)
                for genre in known_dd['genres']:
                    self.assertTrue( genre in search_dd['genres'])

    def test_Film_Taglines( self):
        for film_id, known_dd in self.known_metadata.items():
            if 'taglines' in known_dd:
                search_result = MyWebscraper.IMDB_Film.taglines( film_id)
                for tagline in known_dd['taglines']:
                    self.assertTrue( tagline in search_result)

    def test_Film_ProdCos( self):
        for film_id, known_dd in self.known_metadata.items():
            if 'prod co' in known_dd:
                self.assertTrue( known_dd['prod co'] in MyWebscraper.IMDB_Film.production_companies( film_id))

if __name__ == '__main__':
    unittest.main()

from locators import StringLocator
from webscrapers import *

class BaseFilmRecord():
    def __init__(self, imdb_id):
        self.imdb_id, self.title, self.year = StringLocator.film_identity( imdb_id)
        self.details = []

    def __str__(self):
        r_val = self.imdb_id
        if self.title:
            r_val = r_val + f" : {self.title}"
        if self.year:
            r_val = r_val + f" ({'; '.join([str(self.year)] + self.details)})"
        return r_val

    def __eq__(self, other):
        return self.imdb_id == other.imdb_id

    def __hash__(self):
        return hash( self.imdb_id)

    def identify( self):
        self.title, self.year = Webscraper.IMDB.Film.title_and_year( self.imdb_id)

    def scrape_data( self):
        self.identify()

class TaglineFilmRecord( BaseFilmRecord):
    def scrape_data(self):
        super().scrape_data()
        self.taglines = Webscraper.IMDB.Film.taglines( self.imdb_id)
        self.details.append( f'{len(self.taglines)} taglines')

class ProductionFilmRecord( BaseFilmRecord):
    def scrape_data(self):
        super().scrape_data()
        self.production_cos = Webscraper.IMDB.Film.production_companies( self.imdb_id)
        self.details.append( f'{len(self.production_cos)} production companies')

class DetailedFilmRecord(TaglineFilmRecord, ProductionFilmRecord):
    def scrape_data(self):
        super().scrape_data()
        ttl_yr, sm_cst, detail, genres = Webscraper.IMDB.Film.main_page( self.imdb_id)
        self.title, self.year          = ttl_yr
        self.genres                    = genres
        self.actors, self.directors,  self.writers = sm_cst
        self.budget, self.box_office, self.runtime = detail
        self.details.append('detailed record')

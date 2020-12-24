from utility_methods import StringUtil
from webscrapers import IMDB_Scraper

class BaseFilmRecord():
    def __init__(self, id_string):
        self.imdb_id, self.title, self.year = StringUtil.film_identity( id_string)
        self.scrape_all()

    def __str__(self):
        return f"{self.imdb_id} : {self.title} ({self.year})"

    def scrape_all(self):
        pass

class TaglineFilmRecord( BaseFilmRecord):
    def scrape_all(self):
        super().scrape_all()
        self.taglines = IMDB_Scraper.taglines( self.imdb_id)

    def __str__(self):
        return  super().__str__() + f"\n\t({len( self.taglines)} taglines)"

class ProductionFilmRecord( BaseFilmRecord):
    def scrape_all(self):
        super().scrape_all()
        self.production_cos = IMDB_Scraper.production_companies( self.imdb_id)

    def __str__(self):
        return  super().__str__() + f"\n\t({len( self.production_cos)} production companies)"

class DetailedFilmRecord(TaglineFilmRecord, ProductionFilmRecord):
    def __str__(self):
        return super().__str__() + "\n\t(detailed record)"

    def scrape_all(self):
        super().scrape_all()
        dd = IMDB_Scraper.scrape_main_page( self.imdb_id)
        self.title  , self.year       = dd['title']  , dd['year']
        self.budget , self.box_office = dd['budget'] , dd['box_office']
        self.runtime, self.genres     = dd['runtime'], dd['genres']
        self.actors , self.directors  = dd['actors'] , dd['directors']
        self.writers                  = dd['writers']

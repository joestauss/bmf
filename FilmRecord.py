from utility_methods import StringUtil
from webscrapers import IMDB_Scraper

class BaseFilmRecord():
    def __init__(self, id_string):
        self.imdb_id, self.title, self.year = StringUtil.film_identity( id_string)
        self.details = []

    def __str__(self):
        return f"{self.imdb_id} : {self.title} ({'; '.join([str(self.year)] + self.details)})"

    def identify( self, VERBOSE=False):
        if self.imdb_id:
            self.validate_by_id( VERBOSE=VERBOSE)
        else:
            self.validate_by_title( VERBOSE=VERBOSE)

    def validate_by_title( self, VERBOSE=False):
        if VERBOSE:
            print( f"{self.title} Identification")
        imdb_id, year = IMDB_Scraper.search_by_title_and_year( self.title, self.year)
        if VERBOSE and not imdb_id:
            print( f"{self.title} Identification: Unable to locate title.")
        elif VERBOSE and imdb_id != self.imdb_id:
            print( f"{self.title} Identification: Updating IMDB ID to {imdb_id}.")
        if VERBOSE and year != self.year:
            print( f"{self.title} Identification: Year updated to {year}.")
        self.imdb_id, self.year = imdb_id, year

    def validate_by_id( self, VERBOSE=False):
        title, year = IMDB_Scraper.title_and_year( self.imdb_id)
        if VERBOSE:
            print( f"{self.imdb_id} Identification")
        if VERBOSE and not title:
            print( f"{self.imdb_id} Identification: Unable to locate IMDB ID.")
        elif VERBOSE and title != self.title:
            print( f"{self.imdb_id} Identification: Updating title to {title}.")
        if VERBOSE and year != self.year:
            print( f"{self.imdb_id} Identification: Year updated to {year}.")
        self.title, self.year = title, year

class TaglineFilmRecord( BaseFilmRecord):
    def __init__(self, id_string):
        super().__init__( id_string)
        self.taglines = IMDB_Scraper.taglines( self.imdb_id)
        self.details.append( f'{len(self.taglines)} taglines')

class ProductionFilmRecord( BaseFilmRecord):
    def __init__(self, id_string):
        super().__init__( id_string)
        self.production_cos = IMDB_Scraper.production_companies( self.imdb_id)
        self.details.append( f'{len(self.production_cos)} production companies')

class DetailedFilmRecord(TaglineFilmRecord, ProductionFilmRecord):
    def __init__(self, id_string):
        super().__init__( id_string)
        ttl_yr, sm_cst, detail, genres = IMDB_Scraper.scrape_main_page( self.imdb_id)
        self.title, self.year          = ttl_yr
        self.genres                    = genres
        self.actors, self.directors,  self.writers = sm_cst
        self.budget, self.box_office, self.runtime = detail
        self.details.append('detailed record')

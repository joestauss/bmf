from locators import StringLocator
from webscrapers import *
import os

class FilmRecord():
    ''' A FilmRecord encapsulates all the data about a particular film.

    Initialization Parameters
    -------------------------
    film_id: str, beginning with "tt"
        Corresponds to IMDB's title id.  Used as the hash value.

    metadata_flags: set of str (optional; see class variables for available values)
        Metadata flags indicate which data have been scraped/ should be scraped.

    Data Variables
    --------------
    Under actively development.  Soon just one data dictionary.

    Class Variables
    ---------------
    FilmRecord.IDENTITY_FLAG : str
    FilmRecord.TAGLINES_FLAG : str
    FilmRecord.PROD_COS_FLAG : str
    FilmRecord.DETAILED_FLAG : str
    FilmRecord.POSTERS_FLAG  : str
        Each flag is a string that indictes which data extraction methods a performed by default.

    FilmRecord.data_extraction : dict
        The data_extraction dictionary maps each metadata flag to tbe corresponding data extraction method.

    Methods
    -------
        __init__
        __eq__ and __hash__ - based on film_id.
        __str__

    Data Extraction Methods
    -----------------------
        load_metadata - calls the other extraction methods (that are flagged for).
        identify
        load_details
        load_poster_urls
        load_production_companies
        load_taglines
    '''
    def __init__(self, film_id, metadata_flags=[]):
        self.film_id = film_id
        self.metadata_flags = {metadata for metadata in metadata_flags}
        self.metadata = {}
        self.poster_urls = None

    def __eq__(self, other):
        return self.film_id == other.film_id

    def __hash__(self):
        return hash( self.film_id)

    def __str__(self):
        if len(self.metadata) == 0:
            return self.film_id
        str_lines = []
        header = self.film_id
        if 'title' in self.metadata:
            header = self.metadata['title']
        if self.poster_urls:
            header = header + f" ({len(self.poster_urls)} poster images found)"
        str_lines.append(header + " :")
        str_lines.append("="*len(str_lines[0]))
        max_width = 0
        for metadata_field in self.metadata:
            if (len(metadata_field) + 3) > max_width:
                max_width = (len(metadata_field) + 3)
        for metadata_field in self.metadata:
            if metadata_field == 'taglines':
                str_lines.append('taglines:')
                for tagline in self.metadata['taglines']:
                    str_lines.append(f"     {tagline}")
            else:
                spaces = ' ' * (max_width - len(metadata_field) + 2)
                str_lines.append(f"{metadata_field}:{spaces}{self.metadata[metadata_field]}")
        return "\n".join(str_lines) + "\n"

    ''' Data extraction methods must be defined before being used in the data_extraction dictionary definition below. '''

    def load_metadata(self):
        for metadata_flag in self.metadata_flags:
            self.data_extraction[ metadata_flag]( self)

    def identify(self):
        self.metadata.update( Webscraper.IMDB_Film.title_and_year( self.film_id))

    def load_details( self):
        self.metadata.update( Webscraper.IMDB_Film.main_page( self.film_id) )

    def load_poster_urls(self):
        self.poster_urls = Webscraper.IMDB_Film.poster_urls( self.film_id)

    def load_production_companies(self):
        self.metadata.update( {'production companies' : Webscraper.IMDB_Film.production_companies( self.film_id)})

    def load_taglines(self):
        self.metadata.update( {'taglines': Webscraper.IMDB_Film.two_taglines_at_random( self.film_id)})

    IDENTITY_FLAG = "identity"
    TAGLINES_FLAG = "taglines"
    PROD_COS_FLAG = "production companies"
    DETAILED_FLAG = "detailed record"
    POSTERS_FLAG  = "movie posters"

    data_extraction = {
        IDENTITY_FLAG: identify,
        TAGLINES_FLAG: load_taglines,
        PROD_COS_FLAG: load_production_companies,
        DETAILED_FLAG: load_details,
        POSTERS_FLAG : load_poster_urls
    }

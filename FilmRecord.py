from locators import StringLocator
from webscrapers import *
import json
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
    metadata: dict
        Contains information about the film.

    poster_urls: list
        Contains URLS to online resources for movie posters.

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

    Basic Methods
    -------------
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
        self.images = set()

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

    def as_json( self):
        json_dict = self.metadata
        for key, value in json_dict.items():
            if isinstance( value, set):
                json_dict[key] = list( value)
        json_dict['film_id'] = self.film_id
        return json_dict

    def from_json( json_dict):
        filmrecord = FilmRecord(json_dict.pop('film_id'))
        filmrecord.metadata = json_dict
        return filmrecord

    ''' Data extraction methods must be defined before being used in the data_extraction dictionary definition below. '''

    def load_metadata(self):
        '''Loads all metadata that metadata_flags indicates is necessary.'''
        for metadata_flag in self.metadata_flags:
            self.data_extraction[ metadata_flag]( self)

    def identify(self):
        '''Adds a film's title and year to the metadata dictionary.'''
        self.metadata.update( Webscraper.IMDB_Film.title_and_year( self.film_id))

    def load_details( self):
        '''Adds to the metadata dictionary the film's identity, genre(s), budget, box office ticket sales, runtime, and partial cast.'''
        self.metadata.update( Webscraper.IMDB_Film.main_page( self.film_id) )

    def load_poster_urls(self):
        '''Gets the URLs for movie posters.  The results are NOT stored in the metadata dictionary.'''
        self.poster_urls = Webscraper.IMDB_Film.poster_urls( self.film_id)

    def load_production_companies(self):
        '''Adds production companies to the metadata dictionary.'''
        self.metadata.update( {'production companies' : Webscraper.IMDB_Film.production_companies( self.film_id)})

    def load_taglines(self):
        '''Adds taglines to the metadata dictionary.'''
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

    def as_json_for_twitter( self):
        def camel_case(string):
            string = re.sub(r"[\.,!_-]+", " ", string).title().replace(" ", "")
            return string[0].upper() + string[1:]

        data_dictionary = {}
        data_dictionary['Subject'] = f"{self.metadata['title']} ({self.metadata['year']})"
        data_dictionary['Content'] = self.metadata['taglines']
        data_dictionary['Hashtags'] = [camel_case( self.metadata['title'])]
        data_dictionary['Images'] = sorted(list( self.images))

        return json.dumps( data_dictionary)

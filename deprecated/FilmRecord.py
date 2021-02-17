from webscrapers import Webscraper
from utility import JSONable, ActionThreadsMixin
import json
import os
import collections

class FilmRecord( ActionThreadsMixin, collections.UserDict, JSONable):
    ''' A FilmRecord encapsulates all the data about a particular film.

    Initialization Parameters
    -------------------------
    film_id: str, beginning with "tt"
        Corresponds to IMDB's title id.  Used as the hash value.

    metadata_tags: set of str (optional; see class variables for available values)
        Metadata flags indicate which data have been scraped/ should be scraped.

    Class Variables
    ---------------
    FilmRecord.IDENTITY_TAG : str
    FilmRecord.TAGLINES_TAG : str
    FilmRecord.PROD_COS_TAG : str
    FilmRecord.DETAILED_TAG : str
    FilmRecord.POSTERS_TAG  : str
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

    def __init__(self, film_id, tags=set()):
        super().__init__({'film_id' : film_id}, tags=set(tags))

    def __str__( self):
        if 'title' in self and 'year' in self:
            return f"{self['title']} ({self['year']})"
        elif 'film_id' in self:
            return self['film_id']
        return "FilmRecord"

    def __repr__( self):
        return f"FilmRecord({self.data})"

    def pretty_print( self):
        lines = [ str( self)]
        lines.append("="*len(lines[0]))
        for key, value in self.data.items():
            lines.append( f"  {key} --- {value}")
        return "\n".join( lines)

    ''' Data extraction methods must be defined before being used in the data_extraction dictionary definition below. '''


    def identify(self):
        '''Adds a film's title and year to the metadata dictionary.'''
        self.data.update( Webscraper.IMDB_Film.title_and_year( self.data['film_id']))

    def load_details( self):
        '''Adds to the metadata dictionary the film's identity, genre(s), budget, box office ticket sales, runtime, and partial cast.'''
        self.data.update( Webscraper.IMDB_Film.main_page( self.data['film_id']) )

    def load_poster_urls(self):
        '''Gets the URLs for movie posters.  The results are NOT stored in the metadata dictionary.'''
        self.data['poster_urls'] = Webscraper.IMDB_Film.poster_urls( self.data['film_id'])

    def load_production_companies(self):
        '''Adds production companies to the metadata dictionary.'''
        self.data.update( {'production companies' : Webscraper.IMDB_Film.production_companies( self.data['film_id'])})

    def load_taglines(self):
        '''Adds taglines to the metadata dictionary.'''
        self.data.update( {'taglines': Webscraper.IMDB_Film.two_taglines_at_random( self.data['film_id'])})

    def load_recommendations( self):
        self.data.update( {'recommendations': Webscraper.IMDB_Film.recommendations( self.data['film_id'])})

    IDENTITY_TAG = hash( "identity --- ACTION TAG")
    TAGLINES_TAG = hash( "taglines --- ACTION TAG")
    PROD_COS_TAG = hash( "production companies --- ACTION TAG")
    DETAILED_TAG = hash( "detailed record --- ACTION TAG")
    POSTERS_TAG  = hash( "movie posters --- ACTION TAG")
    RECCS_TAG    = hash( "recommendations --- ACTION TAG")

    regular_action_tags = {
        IDENTITY_TAG: identify,
        TAGLINES_TAG: load_taglines,
        PROD_COS_TAG: load_production_companies,
        DETAILED_TAG: load_details,
        POSTERS_TAG : load_poster_urls
    }
    batch_action_tags = {
        RECCS_TAG : load_recommendations
    }

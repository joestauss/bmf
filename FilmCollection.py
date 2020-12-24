from FilmRecord import *

class BaseFilmCollection():
    def __init__(self, input_list, VERBOSE=False):
        self.movies = set()
        for i, input_item in enumerate(input_list, 1):
            if VERBOSE:
                print( f"Adding record {i} of {len(input_list)}")
            self.add_record( input_item)

    def __str__(self):
        r = [ StringUtil.section_header("Film Collection")]
        for item in self.movies:
            r.append( str(item))
        return "\n".join(r)

    def add_record( self, item):
        self.movies.add( BaseFilmRecord( item))

class TaglineFilmCollection( BaseFilmCollection):
    def add_record( self, item):
        self.movies.add( TaglineFilmRecord( item))

class DetailedFilmCollection( BaseFilmCollection):
    def add_record( self, item):
        self.movies.add( DetailedFilmRecord( item))
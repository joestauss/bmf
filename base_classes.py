from utility_methods import StringUtil, SQLUtil

class BaseFilmRecord():
    def __init__(self, id_string):
        self.imdb_id, self.title, self.year = StringUtil.film_identity(id_string )

    def __str__(self):
        r = ""
        if self.imdb_id:
            r = r + f"{self.imdb_id} : "
        if self.title:
            r = r + self.title
        if self.year:
            r = r + f" ({self.year})"
        return r

    def as_dict( self):
        return {
            'movie_id'    : self.imdb_id,
            'movie_title' : self.title,
            'movie_year'  : self.year
        }

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

class BaseFilmDatabase():
    load_order = ['Movie']

    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.tables = {}
        self.load_movie_table()
        temp_needs_pk = self.needs_primary_key()
        for table_name in self.needs_primary_key():
            self.tables[table_name] = SQLUtil.add_primary_key(
                self.get_pk_col( table_name),
                temp_needs_pk[ table_name])

    def needs_primary_key(self):
        needs_pk = {}
        return needs_pk

    def get_pk_col(self, s):
        return None

    def load_movie_table(self):
        self.tables['Movie'] = []
        for movie in self.movies:
            self.tables['Movie'].append(movie.as_dict())

    def as_sql(self):
        all_tables = []
        for table_name in self.load_order:
            temp = []
            for dd in self.tables[table_name]:
                temp.append(SQLUtil.insert_from_dd(table_name, dd))
            all_tables.append( '\n'.join(temp))
        return "\n\n".join( all_tables)

from utility_methods import SQLUtil
from FilmCollection import *

class BaseJSONExport():
    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.json = []
        for film in movies.self:
            self.json.append( "\n".join(["{", json_internals_for_movie_data( film), "}"]))

    def json_internals_for_movie_data( self, film):
        #   By "JSON Internals", I mean everything except the leading and trailing {} brackets.
        #   By NOT adding these in this method, the child class' implementation can call their supers' version
        #   and then append any new data without having to worry about re-opening the record .
        if isinstance( film, BaseFilmRecord):
            json_lines = [ f'"imdb_id": "{film.imdb_id}"']
            if film.title:
                json_lines.append( f'"title": "{film.title}"')
            if film.year:
                json_lines.append( f'"year": "{film.year}"')
            return ",\n".join( json_lines)

    def __str__(self):
        return "\n".join( self.json)


class BaseSQLExport():
    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.initialize_tables()

    def __str__(self):
        return "\n\n".join([ self.tables[table_name].InsertAllInto(table_name) for table_name in self.load_order])

    def initialize_tables( self):
        self.tables = {}
        self.tables['Movie'] = SQLUtil.Table( self.unprocessed_movie_data)
        self.load_order = ['Movie']

    @property
    def unprocessed_movie_data(self):
        return [ self.movie_data_as_row( movie) for movie in self.movies if isinstance(movie, BaseFilmRecord)]

    def movie_data_as_row(self, movie):
        return { 'movie_id'    : movie.imdb_id,
                 'movie_title' : movie.title,
                 'movie_year'  : movie.year }

class TaglineSQLExport( BaseSQLExport):
    def initialize_tables( self):
        super().initialize_tables()
        self.tables['Tagline'] = SQLUtil.Table( self.unprocessed_tagline_data)
        self.tables['Tagline'].AddPrimaryKey( 'tagline_id')
        self.load_order = self.load_order + ['Tagline']

    @property
    def unprocessed_tagline_data( self):
        dat = []
        for movie in self.movies:
            if isinstance(movie, TaglineFilmRecord):
                dat = dat + [{
                    'movie_id'   : movie.imdb_id,
                    'tagline_text': SQLUtil.text_field_m( tagline)}
                for tagline in movie.taglines ]
        return dat

class ProductionSQLExport( BaseSQLExport):
    def initialize_tables( self):
        super().initialize_tables()
        self.tables['MovieProduction'] = SQLUtil.Table( self.unprocessed_production_data)
        self.tables['Production'] = self.tables['MovieProduction'].NormalizeColumn( 'production_name', 'production_id')
        self.load_order = self.load_order +  ['Production', 'MovieProduction']

    @property
    def unprocessed_production_data( self):
        dat = []
        for movie in self.movies:
            if isinstance(movie, ProductionFilmRecord):
                dat = dat + [{
                    'movie_id'   : movie.imdb_id,
                    'production_name': SQLUtil.text_field_s( prod_co)}
                for prod_co in movie.production_cos ]
        return dat

class GenreSQLExport( BaseSQLExport):
    def initialize_tables( self):
        super().initialize_tables()
        self.tables['MovieGenre'] = SQLUtil.Table( self.unprocessed_genre_data)
        self.tables['Genre'] = self.tables['MovieGenre'].NormalizeColumn( 'genre_name', 'genre_id')
        self.load_order = self.load_order +  ['Genre', 'MovieGenre']

    @property
    def unprocessed_genre_data( self):
        dat = []
        for movie in self.movies:
            if isinstance(movie, DetailedFilmRecord):
                dat = dat + [{
                    'movie_id'   : movie.imdb_id,
                    'genre_name': SQLUtil.text_field_s( genre)}
                for genre in movie.genres ]
        return dat

class SmallCastSQLExport( BaseSQLExport):
    def initialize_tables( self):
        super().initialize_tables()
        self.tables['RoleCode'] = SQLUtil.Table( [ {'role_name' : role } for role in ['Director', 'Writer', 'Actor'] ])
        self.tables['RoleCode'].AddPrimaryKey('role_code')
        self.tables['Role'] = SQLUtil.Table( self.unprocessed_small_cast_data)
        self.tables['Person'] = self.tables['Role'].NormalizeColumn( 'person_name', 'person_id')
        self.load_order = self.load_order + ['Person', 'RoleCode', 'Role']

    @property
    def unprocessed_small_cast_data( self):
        dat = []
        for movie in self.movies:
            if isinstance(movie, DetailedFilmRecord):
                for person in movie.directors:
                    dat.append( {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':0})
                for person in movie.writers:
                    dat.append( {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':1})
                for person in movie.actors:
                    dat.append({'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':2})
        return dat

class DetailedSQLExport(TaglineSQLExport, ProductionSQLExport, GenreSQLExport, SmallCastSQLExport):
    def movie_data_as_row(self, movie):
        dat = super().movie_data_as_row(movie)
        if isinstance(movie, DetailedFilmRecord):
            dat.update({
                'movie_budget' : movie.budget,
                'movie_boxoffice' : movie.box_office,
                'movie_runtime': movie.runtime
            })
        else:
            dat.update({
                'movie_budget' : None,
                'movie_boxoffice' : None,
                'movie_runtime': None
            })
        return dat

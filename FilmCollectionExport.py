from utility_methods import SQLUtil
from FilmCollection import *

class BaseSQLExport():
    load_order = ['Movie']
    mn_tuples = []
    pk_only = []

    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.tables = { table_name : [] for table_name in self.load_order }
        self.load_data()
        self.normalize_MN_relationships()
        self.add_primary_keys()

    def load_data( self):
        for movie in self.movies:
            self.tables['Movie'].append( self.movie_data_as_row( movie))

    def add_primary_keys(self):
        for (table_name, pk_col) in self.pk_only:
            self.tables[table_name] = SQLUtil.add_primary_key( pk_col, self.tables[ table_name])

    def normalize_MN_relationships(self):
        for (terminal_table_name, connecting_table_name, col_names) in self.mn_tuples:
            (self.tables[terminal_table_name  ],
             self.tables[connecting_table_name]) = SQLUtil.normalize_many_to_many(
                col_names,
                self.tables[terminal_table_name] )

    def movie_data_as_row(self, movie):
        return { 'movie_id'    : movie.imdb_id,
                 'movie_title' : movie.title,
                 'movie_year'  : movie.year }

    def as_sql(self):
        all_tables = []
        for table_name in self.load_order:
            temp = []
            for dd in self.tables[table_name]:
                temp.append(SQLUtil.insert_from_dd(table_name, dd))
            all_tables.append( '\n'.join(temp))
        return "\n\n".join( all_tables)

    def __str__(self):
        return self.as_sql()

class TaglineSQLExport( BaseSQLExport):
    load_order = ['Movie', 'Tagline']

    @property
    def pk_only( self):
        return super().pk_only + [ ('Tagline', 'tagline_id')]

    def load_data( self):
        super().load_data()
        self.load_taglines_table()

    def load_taglines_table( self):
        self.tables['Tagline'] = []
        for movie in self.movies:
            for tagline in movie.taglines:
                self.tables['Tagline'].append({
                    'movie_id'   : movie.imdb_id,
                    'tagline_text': SQLUtil.text_field_m( tagline)
                } )

class ProductionSQLExport( BaseSQLExport):
    load_order = ['Movie', 'Production', 'MovieProduction']

    @property
    def mn_tuples( self):
        return super().mn_tuples + [('Production', 'MovieProduction', ('production_name', 'production_id'))]

    def load_data( self):
        super().load_data()
        self.load_normalized_production_tables()

    def load_normalized_production_tables( self):
        for movie in self.movies:
            for prod_co in movie.production_cos:
                self.tables['Production'].append(
                    {'movie_id': movie.imdb_id,
                    'production_name':  SQLUtil.text_field_s(prod_co) })

class GenreSQLExport( BaseSQLExport):
    load_order = ['Movie', 'Production', 'MovieProduction']

    @property
    def mn_tuples( self):
        return super().mn_tuples + [('Genre', 'MovieGenre', ('genre_name', 'genre_id') )]

    def load_data( self):
        super().load_data()
        self.load_genre_tables()

    def load_genre_tables( self):
        for movie in self.movies:
            for genre in movie.genres:
                self.tables['Genre'].append(
                    {'movie_id': movie.imdb_id, 'genre_name':  SQLUtil.text_field_s(genre)})

class SmallCastSQLExport( BaseSQLExport):
    load_order = ['Movie', 'Person', 'RoleCode', 'Role']

    @property
    def mn_tuples(self):
        return super().mn_tuples + [('Person', 'Role', ('person_name', 'person_id')) ]

    @property
    def pk_only( self):
        return super().pk_only + [ ('RoleCode', 'role_code')]

    def load_data(self):
        super().load_data()
        self.load_small_cast()

    def load_small_cast( self):
        self.tables['RoleCode'] = [ {'role_name' : role } for role in ['Director', 'Writer', 'Actor'] ]
        for movie in self.movies:
            for person in movie.directors:
                self.tables['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':0})
            for person in movie.writers:
                self.tables['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':1})
            for person in movie.actors:
                self.tables['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':2})

class DetailedSQLExport(TaglineSQLExport, ProductionSQLExport, GenreSQLExport, SmallCastSQLExport):
    load_order = ['Movie', 'Genre', 'MovieGenre', 'Production', 'MovieProduction', 'Person', 'RoleCode', 'Role',  'Tagline']

    def movie_data_as_row(self, movie):
        dd = super().movie_data_as_row(movie)
        dd.update({
            'movie_budget' : movie.budget,
            'movie_boxoffice' : movie.box_office,
            'movie_runtime': movie.runtime
        })
        return dd

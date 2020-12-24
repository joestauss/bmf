from utility_methods import SQLUtil
from FilmCollection import *

class BaseFilmDatabase():
    load_order = ['Movie']
    mn_tuples = []

    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.tables = { table_name : [] for table_name in self.load_order }
        self.load_data()

    def load_data( self):
        for movie in self.movies:
            self.tables['Movie'].append( self.film_as_dd( movie))

        temp_needs_pk = self.needs_primary_key()
        for table_name in self.needs_primary_key():
            self.tables[table_name] = SQLUtil.add_primary_key(
                self.get_pk_col( table_name),
                temp_needs_pk[ table_name])

        self.load_MN_relationships()
        self.normalize_MN_relationships()

    def needs_primary_key(self):
        needs_pk = {}
        return needs_pk

    def get_pk_col(self, s):
        return None

    def film_as_dd(self, movie):
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

    def load_MN_relationships(self):
        self.unnormalized_data = {}

    def normalize_MN_relationships(self):
        for (terminal_table_name, connecting_table_name, col_names) in self.mn_tuples:
            (self.tables[terminal_table_name  ],
             self.tables[connecting_table_name]) = SQLUtil.normalize_many_to_many(
                col_names,
                self.unnormalized_data[terminal_table_name] )

class DetailedFilmDatabase(BaseFilmDatabase):
    load_order = ['Movie', 'Genre', 'MovieGenre', 'Production', 'MovieProduction', 'Person', 'RoleCode', 'Role',  'Tagline']
    primary_key = {'RoleCode': 'role_code', 'Tagline' : 'tagline_id'}

    mn_tuples = [
        ('Genre', 'MovieGenre', ('genre_name', 'genre_id') ),
        ('Production', 'MovieProduction', ('production_name', 'production_id')),
        ('Person', 'Role', ('person_name', 'person_id')) ]

    def film_as_dd(self, movie):
        dd = super().film_as_dd(movie)
        dd.update({
            'movie_budget' : movie.budget,
            'movie_boxoffice' : movie.box_office,
            'movie_runtime': movie.runtime
        })
        return dd

    def needs_primary_key(self):
        needs_pk = super().needs_primary_key()
        needs_pk['RoleCode'] = [ {'role_name' : role } for role in ['Director', 'Writer', 'Actor'] ]
        tagline_entries = []
        for movie in self.movies:
            for tagline in movie.taglines:
                tagline_entries.append( {
                    'movie_id'   : movie.imdb_id,
                    'tagline_text': SQLUtil.text_field_m( tagline)
                })
        needs_pk['Tagline'] = tagline_entries
        return needs_pk

    def get_pk_col(self, s):
        if s == 'RoleCode':
            return 'role_code'
        if s == 'Tagline':
            return 'tagline_id'
        return 'ERROR_CODE'

    def load_MN_relationships(self):
        unnormalized_data = {'Genre' : [] , 'Production' : [], 'Person' : []}
        for movie in self.movies:
            for genre in movie.genres:
                unnormalized_data['Genre'].append(
                    {'movie_id': movie.imdb_id, 'genre_name':  SQLUtil.text_field_s(genre)})
            for prod_co in movie.production_cos:
                unnormalized_data['Production'].append(
                    {'movie_id': movie.imdb_id, 'production_name':  SQLUtil.text_field_s(prod_co)})
            for person in movie.directors:
                unnormalized_data['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':0})
            for person in movie.writers:
                unnormalized_data['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':1})
            for person in movie.actors:
                unnormalized_data['Person'].append(
                    {'movie_id': movie.imdb_id, 'person_name': SQLUtil.text_field_s(person), 'role_code':2})
            self.unnormalized_data = unnormalized_data

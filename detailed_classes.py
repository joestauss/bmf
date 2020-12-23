from webscrapers import IMDB_Scraper
from utility_methods import SQLUtil
from base_classes import *

class DetailedFilmRecord(BaseFilmRecord):
    def __init__(self, imdb_id):
        super().__init__( imdb_id)
        self.scrape_all()

    def __str__(self):
        return "\n".join([
            super().__str__(),
            f" Budget\t\t: {self.budget}",
            f" Box Office\t: {self.box_office}",
            f" Runtime\t: {self.runtime}",
            f" Director(s)\t: {self.directors}",
            f" Actor(s)\t: {self.actors}",
            f" Writer(s)\t: {self.writers}",
            f" Genres\t\t: {self.genres}", "\n"
        ])

    def as_dict(self):
        dd = super().as_dict()
        dd.update({
            'movie_budget' : self.budget,
            'movie_boxoffice' : self.box_office,
            'movie_runtime': self.runtime
        })
        return dd

    def scrape_all(self):
        dd = IMDB_Scraper.scrape_main_page( self.imdb_id)
        self.title  , self.year       = dd['title']  , dd['year']
        self.budget , self.box_office = dd['budget'] , dd['box_office']
        self.runtime, self.genres     = dd['runtime'], dd['genres']
        self.actors , self.directors  = dd['actors'] , dd['directors']
        self.writers                  = dd['writers']
        self.taglines       = IMDB_Scraper.taglines( self.imdb_id)
        self.production_cos = IMDB_Scraper.production_companies( self.imdb_id)

class DetailedFilmCollection(BaseFilmCollection):
    def add_record( self, item):
        self.movies.add( DetailedFilmRecord( item))

    def normalize_taglines(self):
        tagline_entries = []
        for movie in self.movies:
            for tagline in movie.taglines:
                tagline_entries.append( {
                    'movie_id'   : movie.imdb_id,
                    'tagline_text': SQLUtil.text_field_m( tagline)
                })

class DetailedFilmDatabase(BaseFilmDatabase):
    load_order = ['Movie', 'Genre', 'MovieGenre', 'Person', 'RoleCode', 'Role', 'Production', 'MovieProduction', 'Tagline']
    primary_key = {'RoleCode': 'role_code', 'Tagline' : 'tagline_id'}

    def __init__(self, movie_collection):
        super().__init__(movie_collection)
        self.normalize_MN_relationships()

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

    def normalize_MN_relationships(self):
        unnormalized_data = {'Genre' : [] , 'Production' : [], 'Person' : []}
        for movie in self.movies:
            for genre in movie.genres:
                unnormalized_data['Genre'].append((movie.imdb_id, SQLUtil.text_field_s(genre)))
            for prod_co in movie.production_cos:
                unnormalized_data['Production'].append((movie.imdb_id, SQLUtil.text_field_s(prod_co)))
            for person in movie.directors:
                unnormalized_data['Person'].append((movie.imdb_id, 0, SQLUtil.text_field_s(person)))
            for person in movie.writers:
                unnormalized_data['Person'].append((movie.imdb_id, 1, SQLUtil.text_field_s(person)))
            for person in movie.actors:
                unnormalized_data['Person'].append((movie.imdb_id, 2, SQLUtil.text_field_s(person)))

        MN_relationship = {
            # a:b where
            #  a is key for the raw, unnormalized data
            #  b is the name for the new intermediate table
            #
            'Genre' : 'MovieGenre',
            'Production' : 'MovieProduction',
            'Person': 'Role'
        }
        cols = {
            'Genre' : ['genre_id', 'genre_name'],
            'MovieGenre' : ['movie_id', 'genre_id'],
            'Production' : ['production_id', 'production_name'],
            'MovieProduction' : ['movie_id', 'production_id'],
            'Role': ['movie_id', 'role_code', 'person_id'],
            'Person': ['person_id', 'person_name']
        }
        for term, conn in MN_relationship.items():
            self.tables[term], self.tables[conn] = SQLUtil.normalize_many_to_many(
            unnormalized_data[term],
            cols[term],
            cols[conn]
        )

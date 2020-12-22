import my_utility
import my_webscraping as wbsp

class MovieCollection():
    def __init__(self, imdb_ids, VERBOSE=False):
        self.movies = set()
        i = 1
        n = len(imdb_ids)
        for imdb_id in imdb_ids:
            if VERBOSE:
                print(f"Scraping from {imdb_id}...\t({i} of {n})")
            self.movies.add( wbsp.IMDB_Data( imdb_id))
            i = i+1

    def __str__(self):
        r = []
        for m in self.movies:
            if hasattr( m, 'title') and hasattr( m, 'year'):
                r.append( f"{m.year} - {m.title}")
        r.sort()
        return my_utility.section_header('Movie List') + "\n" + "\n".join( r)

class NormalizedMovieDatabase():
    def __init__(self, movie_collection):
        self.movies = movie_collection.movies
        self.tables = {}

        self.normalize_movies()
        self.normalize_taglines()
        self.normalize_rolecodes()
        self.normalize_MN_relationships()

    def normalize_movies(self):
        self.tables['Movie'] = []
        for movie in self.movies:
            self.tables['Movie'].append(movie.as_dict())

    def normalize_MN_relationships(self):
        unnormalized_data = {'Genre' : [] , 'Production' : [], 'Person' : []}
        for movie in self.movies:
            for genre in movie.genres:
                unnormalized_data['Genre'].append((movie.imdb_id, my_utility.text_field_s(genre)))
            for prod_co in movie.production_cos:
                unnormalized_data['Production'].append((movie.imdb_id, my_utility.text_field_s(prod_co)))
            for person in movie.directors:
                unnormalized_data['Person'].append((movie.imdb_id, 0, my_utility.text_field_s(person)))
            for person in movie.writers:
                unnormalized_data['Person'].append((movie.imdb_id, 1, my_utility.text_field_s(person)))
            for person in movie.actors:
                unnormalized_data['Person'].append((movie.imdb_id, 2, my_utility.text_field_s(person)))

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
            self.tables[term], self.tables[conn] = my_utility.normalize_many_to_many(
            unnormalized_data[term],
            cols[term],
            cols[conn]
        )

    def normalize_rolecodes(self):
        self.tables['RoleCode'] = [
            {'role_code': 0, 'role_name': 'Director'},
            {'role_code': 1, 'role_name': 'Writer'},
            {'role_code': 2, 'role_name': 'Actor'}
        ]

    def normalize_taglines(self):
        # Tagline normalization is separate from the others, because it has a many-to-one
        # relationship with movies.
        #
        tagline_entries = []
        tagline_counter = 0
        for movie in self.movies:
            for tagline in movie.taglines:
                tagline_entries.append( {
                    'tagline_id' : tagline_counter,
                    'movie_id'   : movie.imdb_id,
                    'tagline_text': my_utility.text_field_m( tagline)
                })
                tagline_counter = tagline_counter + 1
        self.tables['Tagline'] = tagline_entries

    def as_sql(self):
        load_order = [
            'Movie',
            'Genre',
            'MovieGenre',
            'Person',
            'RoleCode',
            'Role',
            'Production',
            'MovieProduction',
            'Tagline'
        ]

        all_tables = []
        for table_name in load_order:
            temp = []
            for dd in self.tables[table_name]:
                temp.append(my_utility.sql_insert_from_dd(table_name, dd))
            all_tables.append( '\n'.join(temp))

        return "\n\n".join( all_tables)

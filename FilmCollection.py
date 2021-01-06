from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *

class BaseFilmCollection():
    RECORD_TYPE = BaseFilmRecord

    def __init__(self, input_list, VERBOSE=False):
        self.movies = set()
        for i, input_item in enumerate(input_list, 1):
            if VERBOSE:
                print( f"Adding record {i} of {len(input_list)}:\t{input_item}")
            self.add_record( input_item)

    def __str__(self):
        r = [ StringUtil.section_header("Film Collection")]
        sorted_movies = sorted( self.movies, key=lambda m:m.year if m.year else 0)
        for item in sorted_movies:
            r.append( str(item))
        return "\n".join(r)

    def add_record( self, item):
        if isinstance(item, BaseFilmRecord):
            self.movies.add( item)
        else:
            imdb_id, title, year = StringLocator.film_identity( item)
            if not imdb_id:
                imdb_id, _ = Webscraper.IMDB.Search.by_title_and_year( title, year)
            self.movies.add( self.RECORD_TYPE( imdb_id))

    def identify_all( self):
        threads = {}
        for movie in self.movies:
            threads[movie] = threading.Thread( target=movie.identify)
            threads[movie].start()
        for movie in self.movies:
            threads[movie].join()

    def scrape_all( self):
        threads = {}
        counter = 0
        for movie in self.movies:
            counter = counter + 1
            print(f"Creating thread {counter}.")
            threads[movie] = threading.Thread( target=movie.scrape_data)
            threads[movie].start()
        for movie in self.movies:
            print(f"Waiting for {counter} threads..")
            threads[movie].join()
            counter = counter - 1

    def full_recommendation_expansion(self):
        imdb_ids = { movie.imdb_id for movie in self.movies }
        recs = DataExtraction.Recommendations.all(imdb_ids)
        for rec in recs:
            self.add_record( rec)

        num_old = len( imdb_ids )
        num_new = len( recs - imdb_ids )
        print(f"From {num_old} films, there were {num_new} unique recommendations")
        self.identify_all()

    def multiple_adjacency_recommendation_expansion( self):
        imdb_ids = { movie.imdb_id for movie in self.movies }
        recs = DataExtraction.Recommendations.multiple_adjacency(imdb_ids)

        for rec in recs:
            self.add_record( rec)

        num_old = len( imdb_ids )
        num_new = len( recs - imdb_ids )
        print(f"From {num_old} films, there were {num_new} films recommended multiple times.")
        self.identify_all()

class TaglineFilmCollection( BaseFilmCollection):
    RECORD_TYPE = TaglineFilmRecord

    def manual_tagline_selection( self):
        def get_user_choices( input_list):
            explanation_prompt = "Please enter the number of the tagline(s) you would like, separated by a comma."
            print( explanation_prompt)

            choices_prompt = "\n".join(
                [f'{i}:{" "*(4-len(str(i)))}{choice}' for i, choice in enumerate( input_list)]
                + [">>> "] )
            user_input = input( choices_prompt)

            print( f"User wants {user_input}.  This corresponds to the following taglines:")
            selections = [s.strip() for s in user_input.split(",")]
            valid_selections = []
            for selection in selections:
                try:
                    valid_selections.append( input_list[ int(selection)])
                    print(  "\t" + valid_selections[-1])
                except:
                    print( "\t" + f"{selection} was not a valid choice.")
            return valid_selections

        for film in self.movies:
            all_taglines = Webscraper.IMDB.Film.taglines( film.imdb_id)
            film.taglines  = get_user_choices( list(all_taglines))
            film.details.append( f'{len(film.taglines)} taglines')

class DetailedFilmCollection( BaseFilmCollection):
    RECORD_TYPE = DetailedFilmRecord

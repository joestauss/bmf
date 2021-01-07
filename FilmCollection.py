from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *

class BaseFilmCollection():
    RECORD_TYPE = BaseFilmRecord

    def __init__(self, input_list, VERBOSE=False):
        self.films = set()
        for i, input_item in enumerate(input_list, 1):
            if VERBOSE:
                print( f"Adding record {i} of {len(input_list)}:\t{input_item}")
            self.add_record( input_item)

    def __str__(self):
        r = [ StringUtil.section_header("Film Collection")]
        sorted_films = sorted( self.films, key=lambda m:m.year if m.year else 0)
        for item in sorted_films:
            r.append( str(item))
        return "\n".join(r)

    def add_record( self, item):
        if isinstance(item, BaseFilmRecord):
            self.films.add( item)
        else:
            film_id, title, year = StringLocator.film_identity( item)
            if not film_id:
                film_id, _ = Webscraper.IMDB.Search.by_title_and_year( title, year)
            self.films.add( self.RECORD_TYPE( film_id))

    def identify_all( self):
        threads = {}
        for film in self.films:
            threads[film] = threading.Thread( target=film.identify)
            threads[film].start()
        for film in self.films:
            threads[film].join()

    def scrape_all( self):
        threads = {}
        counter = 0
        for film in self.films:
            counter = counter + 1
            print(f"Creating thread {counter}.")
            threads[film] = threading.Thread( target=film.scrape_data)
            threads[film].start()
        for film in self.films:
            print(f"Waiting for {counter} threads..")
            threads[film].join()
            counter = counter - 1

    def full_recommendation_expansion(self):
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.all(film_ids)
        for rec in recs:
            self.add_record( rec)

        num_old = len( film_ids )
        num_new = len( recs - film_ids )
        print(f"From {num_old} films, there were {num_new} unique recommendations")
        self.identify_all()

    def multiple_adjacency_recommendation_expansion( self):
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.multiple_adjacency(film_ids)

        for rec in recs:
            self.add_record( rec)

        num_old = len( film_ids )
        num_new = len( recs - film_ids )
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

        for film in self.films:
            all_taglines = Webscraper.IMDB.Film.taglines( film.film_id)
            film.taglines  = get_user_choices( list(all_taglines))
            film.details.append( f'{len(film.taglines)} taglines')

class DetailedFilmCollection( BaseFilmCollection):
    RECORD_TYPE = DetailedFilmRecord

from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *

class FilmCollection():
    def __init__(self, input_list, default_metadata=[FilmRecord.IDENTITY_FLAG], name='FilmCollection'):
        self.default_metadata = {flag for flag in default_metadata}
        self.films = set()
        for i, input_item in enumerate(input_list, 1):
            self.add_record( input_item)
        self.name=name

    def __str__(self):
        r = [ PrintUtil.section_header(self.name)]
        sorted_films = sorted( self.films, key=lambda m:m.metadata['year'] if 'year' in m.metadata else 0)
        for item in sorted_films:
            r.append( str(item))
        return "\n".join(r)

    def add_record(self, item):
        if isinstance(item, FilmRecord):
            self.films.add( item)
        else:
            film_id, title, year = StringLocator.film_identity( item)
            if not film_id:
                film_id, _ = Webscraper.IMDB_Search.by_title_and_year( title, year)
            self.films.add( FilmRecord( film_id, metadata_flags=self.default_metadata))

    def load_all_metadata( self):
        threads = {}
        for film in self.films:
            threads[film] = threading.Thread( target=film.load_metadata)
            threads[film].start()
        for film in self.films:
            threads[film].join()

    def full_recommendation_expansion(self):
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.all(film_ids)
        for rec in recs:
            self.add_record( rec)
        num_old = len( film_ids )
        num_new = len( recs - film_ids )
        print(f"From {num_old} films, there were {num_new} unique recommendations")

    def multiple_adjacency_recommendation_expansion( self):
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.multiple_adjacency(film_ids)

        for rec in recs:
            self.add_record( rec)

        num_old = len( film_ids )
        num_new = len( recs - film_ids )
        print(f"From {num_old} films, there were {num_new} films recommended multiple times.")

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
            if FilmRecord.TAGLINES_FLAG in film.metadata_flags:
                print(PrintUtil.section_header(str(film).split('\n')))
                all_taglines = Webscraper.IMDB_Film.taglines( film.film_id)
                film.metadata['taglines']  = get_user_choices( list(all_taglines))

    @property
    def images_dir(self):
        return self.__images_dir

    @images_dir.setter
    def images_dir(self, folder_name):
        base_dir  = os.getcwd()
        image_dir =  os.path.join(base_dir, folder_name)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.__images_dir = image_dir

    def download_posters(self):
        self.images_dir = "New_Poster_Folder_2"
        for film in self.films:
            i = 0
            if FilmRecord.POSTERS_FLAG in film.metadata_flags:
                for url in film.poster_urls:
                    i = i + 1
                    target_filename = f'{film.film_id} Poster {i}.jpg'
                    target_file_location = os.path.join( self.images_dir, target_filename)
                    Webscraper.image(url, target_file_location)

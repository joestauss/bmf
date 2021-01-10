from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *
from tqdm import tqdm
from time import sleep
from parsers import FilmParser

class FilmCollection():
    ''' A FilmCollection groups together several FilmRecords.

    Recommendations and images are managed at the FilmCollection level, and not by the FilmRecord class,
    because extracting those data requires an automated browser interest, not just a simple HTML request.

    Initialization Parameters
    -------------------------
    input_list: list of (str and FilmRecord)
        Strings should be either an IMDB film id, a title, or a "title (year)" combinations.

    default_metadata: a list of FilmRecord flags (optional)
        See FilmRecord for a list of available metadata flags.  Defaults to [FilmRecord.IDENTITY_FLAG]

    name: str (optional)
        Defaults to 'FilmCollection'.

    Optional Variables
    ------------------
    images_dir: str
        The folder name of where images are to be saved to.

    Methods
    -------
        __init__
        __str__
        __add__
        add_record
        load_all_metadata
        full_recommendation_expansion
        multiple_adjacency_recommendation_expansion
        manual_tagline_selection
        download_posters
        images_dir.setter
    '''
    def __init__(self, input_list, default_metadata=[FilmRecord.IDENTITY_FLAG], name='FilmCollection', VERBOSE=False):
        self.default_metadata = {flag for flag in default_metadata}
        self.films = set()
        for i, input_item in enumerate(input_list, 1):
            self.add_record( input_item)
        self.name=name
        self.VERBOSE=VERBOSE

    def __str__(self):
        r = [ PrintUtil.section_header(self.name)]
        sorted_films = sorted( self.films, key=lambda m:m.metadata['year'] if 'year' in m.metadata else 0)
        for item in sorted_films:
            r.append( str(item))
        return "\n".join(r)

    def add_record(self, item):
        '''If item is a FilmRecord, it is added to self.films. If item is a string, a record is created with ONLY the IMDB film id,
        so if a title (with optional year) is given, that information is lost when the FilmRecord is created.'''
        if isinstance(item, FilmRecord):
            self.films.add( item)
        else:
            film_id, title, year = FilmParser.identify( item)
            if not film_id:
                film_id, _ = Webscraper.IMDB_Search.by_title_and_year( title, year)
            self.films.add( FilmRecord( film_id, metadata_flags=self.default_metadata))

    def load_all_metadata( self):
        '''Creates a thread for each film that loads its metadata.  Waits 0.1 seconds after starting each new thread.

        If VERBOSE, there will be TQDM progess bars for creating and waiting for threads.
        '''
        threads = {}
        films = self.films
        if self.VERBOSE:
            films = tqdm( films)
        for film in films:
            if self.VERBOSE:
                films.set_description(f"Starting thread for {film.film_id}")
            threads[film] = threading.Thread( target=film.load_metadata)
            threads[film].start()
            sleep(0.1)
        if self.VERBOSE:
            films = tqdm( films)
        for film in films:
            if self.VERBOSE:
                films.set_description(f"Waiting for {film.film_id}")
            threads[film].join()

    def full_recommendation_expansion(self):
        '''Adds to the collection all films that were recommended on other films' IMDB page.'''
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.all(film_ids)
        for rec in recs:
            self.add_record( rec)
        num_old = len( film_ids )
        num_new = len( recs - film_ids )
        print(f"From {num_old} films, there were {num_new} unique recommendations")

    def multiple_adjacency_recommendation_expansion( self):
        '''Checks the recommendation of all films in the database, and adds movies that were recommended more than once.'''
        film_ids = { film.film_id for film in self.films }
        recs = ExtractData.ExtractRecommendations.multiple_adjacency(film_ids)

        for rec in recs:
            self.add_record( rec)

        num_old = len( film_ids )
        num_new = len( recs - film_ids )
        print(f"From {num_old} films, there were {num_new} films recommended multiple times.")

    def manual_tagline_selection( self):
        '''An interactive prompt that allows a user select the taglines that will be added to the database.'''
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
        '''When images_dir is set, a folder called images_dir is created in the current directory if it does not exist.'''
        base_dir  = os.getcwd()
        image_dir =  os.path.join(base_dir, folder_name)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.__images_dir = image_dir

    def download_posters(self):
        '''Downloads all movie posters to NewPosterFolder.'''
        self.images_dir = "NewPosterFolder"
        for film in self.films:
            i = 0
            if FilmRecord.POSTERS_FLAG in film.metadata_flags:
                for url in film.poster_urls:
                    i = i + 1
                    target_filename = f'{film.film_id} Poster {i}.jpg'
                    target_file_location = os.path.join( self.images_dir, target_filename)
                    Webscraper.image(url, target_file_location)

    def __add__( self, other, name='MergedTable'):
        '''Use A + B to merge two FilmCollections.  The default name is MergedTable.'''
        return FilmCollection( self.films | other.films, name=name)

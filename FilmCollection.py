from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *
from tqdm import tqdm
from time import sleep
from parsers import FilmParser
import json

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

    Variables
    ----------
    images_dir: str
        The folder name of where images are to be saved to.  Not necessary if no image-work is to be done.

    keywords: dict
        A dict of sets.

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

    Properties
    ----------
        imdb_ids
    '''
    def __init__(self, input_list, default_metadata=[FilmRecord.IDENTITY_FLAG], name='FilmCollection', VERBOSE=False):
        self.default_metadata = {flag for flag in default_metadata}
        self.films = set()
        for i, input_item in enumerate(input_list, 1):
            self.add_record( input_item)
        self.name=name
        self.VERBOSE=VERBOSE
        self.keywords={}

    def __str__(self):
        r = [ PrintUtil.section_header(self.name)]
        sorted_films = sorted( self.films, key=lambda m:m.metadata['year'] if 'year' in m.metadata and m.metadata['year'] else 0)
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
        for film in self.films:
            i = 0
            if FilmRecord.POSTERS_FLAG in film.metadata_flags:
                for url in tqdm(film.poster_urls):
                    if url != 'https://m.media-amazon.com/images/M/MV5BZGI5OTZhYjAtMGYwMS00ZmFiLWI3ODAtYjk1OWRiNWExNWNiXkEyXkFqcGdeQXVyNzI4MDMyMTU@._V1_.jpg':
                        i = i + 1
                        target_filename = f"{film.metadata['title']} ({film.metadata['year']}), Poster {i}.jpg"
                        target_file_location = os.path.join( self.images_dir, target_filename)
                        Webscraper.image(url, target_file_location)
                        film.images.add( target_filename)

    @property
    def film_ids( self):
        return {film.film_id for film in self.films}

    def __add__( self, other, name='MergedTable'):
        '''Use A + B to merge two FilmCollections.  The default name is MergedTable.'''
        merged_collection = FilmCollection( self.films | other.films, name=name)
        title1 = self.name
        title2 = other.name
        if title1 == title2:
            title1 = title1 + "_1"
            title2 = title2 + "_2"
        merged_collection.keywords = {
            title1 : self.film_ids,
            title2 : other.film_ids
        }
        merged_collection.keywords.update( self.keywords)
        merged_collection.keywords.update( other.keywords)
        return merged_collection

    def export_metadata_as_json(self):
        return json.dumps({'FilmRecords':[film.as_json() for film in self.films]}, indent=2)

    def initialize_from_json(json_string, name='Collection Loaded from JSON'):
        return FilmCollection([FilmRecord.from_json( filmrecord_dict) for filmrecord_dict in json.loads( json_string)['FilmRecords']], name=name)

    def export_film_structure(self):
        lines = list(self.film_ids)
        for keyword in self.keywords:
            lines.append( keyword + " : {")
            for film_id in self.keywords[ keyword]:
                lines.append( f"       {film_id}")
            lines.append( "}")
        return "\n".join(lines)

    def flag_all(self, flag):
        for film in self.films:
            film.metadata_flags.add( flag)


    def as_json_for_twitter( self):
        data_dictionary = { 'ContentRecords': []}
        for film in self.films:
            data_dictionary['ContentRecords'].append( json.loads( film.as_json_for_twitter()))
        return json.dumps( data_dictionary, indent=2)

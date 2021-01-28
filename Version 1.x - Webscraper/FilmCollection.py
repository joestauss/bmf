from FilmRecord import *
import threading
from webscrapers import *
from tqdm import tqdm
from time import sleep
from chopping_block import FilmParser
import json
from utility import PatientThreadManager, ActionThreadsMixin, boxed_text, select_from_list
import pyparsing as pp

class FilmCollection(ActionThreadsMixin):
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
    def __init__( self, *args, default_metadata=[FilmRecord.IDENTITY_TAG], **kwargs):
        self.default_metadata = default_metadata
        self.films = set()
        if len(args) > 0:
            init_data = set(args[0])
            for record in init_data:
                self.add( record)
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "Nameless BaseCollection"

    def __repr__( self):
        return( f"{type(self).__name__}( {repr( self.data)}, default_metadata={repr( self.default_metadata)}, name={self.name})")


    def __str__( self):
        return f"This is a {type(self).__name__} with {len( self)} items."
    #
    #   Start of MutableSet methods
    #
    def __contains__(self, item):
        return item in self.films

    def __iter__(self):
        return iter(self.films)

    def __len__(self):
        return len(self.films)

    def add(self, item):
        if isinstance( item, FilmRecord):
            self.films.add(item)
        elif isinstance( item, str):
            search_result = pp.Regex("tt\d+").searchString( item)
            if search_result:
                self.films.add( FilmRecord(search_result[0][0], tags=self.default_metadata))
        else:
            raise ValueError( "Tried to add a non-FilmRecord item to a FilmCollection.")

    def discard(self, item):
        self.films.pop(item)
    #
    #   End of MutableSet methods
    #


    def manual_tagline_selection( self):
        '''An interactive prompt that allows a user select the taglines that will be added to the database.'''
        for film in self.films:
            if FilmRecord.TAGLINES_TAG in film.tags:
                print( boxed_text(str(film)))
                all_taglines = Webscraper.IMDB_Film.taglines( film['film_id'])
                film['taglines']  = select_from_list( list(all_taglines))

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
            if FilmRecord.POSTERS_FLAG in film.tags:
                for url in tqdm(film.poster_urls):
                    if url != 'https://m.media-amazon.com/images/M/MV5BZGI5OTZhYjAtMGYwMS00ZmFiLWI3ODAtYjk1OWRiNWExNWNiXkEyXkFqcGdeQXVyNzI4MDMyMTU@._V1_.jpg':
                        i = i + 1
                        target_filename = f"{film.metadata['title']} ({film.metadata['year']}), Poster {i}.jpg"
                        target_file_location = os.path.join( self.images_dir, target_filename)
                        Webscraper.image(url, target_file_location)
                        film.images.add( target_filename)

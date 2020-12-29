from utility_methods import StringUtil
from filmsets import *
from FilmCollection import *
from webscrapers import *

TEST_FIND_FILMOGRAPHY = False
TEST_IDENTIFY_ALL     = False
TEST_SECTION_HEADER   = False
TEST_FILM_IDENTITY    = False

if TEST_FIND_FILMOGRAPHY:
    BRUCE_WILLIS_ID  = 'nm0000246'
    VINCENT_PRICE_ID = 'nm0001637'
    print(", ".join( [f'"{film}"' for film in IMDB_Scraper.films_acted_in( VINCENT_PRICE_ID)]))

if TEST_IDENTIFY_ALL:
    coll = BaseFilmCollection( TestSets.MixedFormat.medium)
    coll.identify_all( VERBOSE=True)

if TEST_SECTION_HEADER:
    test_string = 'one line'
    lines = ['uno' , '2', 'trestrestrestrestrestrestres']
    print( StringUtil.section_header( test_string))
    print( StringUtil.section_header( lines))
    print( StringUtil.section_header( 12))

if TEST_FILM_IDENTITY:
    test_strs = [
        'tt2347386', # a valid imdb_id
        'Terminator (1492)', # a valid film-and-date
        'I am the muffin man.', # neither of the above, assumed to be a title.
        'Deltron(3030)', # No space, should still work.
        'Beastmaster 2000 (1982)' # something like this started this whole fix
    ]
    for s in test_strs:
        imdb_id, title, year = StringUtil.film_identity( s)
        print(f"Test String: {s}")
        print(f"IMDB ID: {imdb_id}")
        print(f"Title: {title}")
        print(f"Year: {year}\n\n")

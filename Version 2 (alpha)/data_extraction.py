from cli_utility import cli_selector
import imdb

def find_person( person_name, mode='first'):
    if mode == 'first':
        ia = imdb.IMDb()
        return ia.search_person( person_name)[0]
    if mode == 'many':
        ia = imdb.IMDb()
        return cli_selector( ia.search_person( person_name))

    raise ValueError( "imdb_search_person can only be called in 'first' mode.")

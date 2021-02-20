from py_util.collections import BaseSet
from bmb.collections     import FilmRecord

class FilmSet( BaseSet):
    def __str__(self):
        lines = [ 'FilmSet']
        lines.append( '='*len( lines[0]))
        sorted_films = sorted( self, key=lambda m:m['year'] if 'year' in m and m['year'] else 0)
        for item in sorted_films:
            lines.append( str( item))
        return "\n".join( lines)

    def add(self, item):
        if isinstance( item, FilmRecord):
            self.data.add(item)
        elif isinstance( item, str):
            self.data.add( FilmRecord.from_id_string( item))
        else:
            raise ValueError( "Only a FilmRecord or an identification string can be added to a FilmSet.")

    @classmethod
    def from_movie_list( cls, movie_list):
        temp = cls()
        for movie in movie_list:
            temp.add( movie)
        return temp

    @classmethod
    def from_actor( cls, actor_name):
        ia = imdb.IMDb()
        film_strings = []
        person = ia.get_person( ia.search_person( actor_name)[0].personID)
        for film in person[ 'filmography'][ 'actor']:
            film_string = film['title']
            if 'year' in film.data:
                film_string = film_string + f" ({film.data['year']})"
            film_strings.append( film_string)
        return cls.from_movie_list( film_strings)

    @classmethod
    def from_director( cls, director_name):
        ia = imdb.IMDb()
        film_strings = []
        person = ia.get_person( ia.search_person( director_name)[0].personID)
        for film in person[ 'filmography'][ 'director']:
            film_string = film['title']
            if 'year' in film.data:
                film_string = film_string + f" ({film.data['year']})"
            film_strings.append( film_string)
        return cls.from_movie_list( film_strings)

    @classmethod
    def from_producer( cls, producer_name):
        ia = imdb.IMDb()
        film_strings = []
        person = ia.get_person( ia.search_person( producer_name)[0].personID)
        for film in person[ 'filmography'][ 'producer']:
            film_string = film['title']
            if 'year' in film.data:
                film_string = film_string + f" ({film.data['year']})"
            film_strings.append( film_string)
        return cls.from_movie_list( film_strings)

    @classmethod
    def from_prod_co( cls, writer_id):
        return cls()

    @classmethod
    def from_imdb_list( cls, writer_id):
        return cls()

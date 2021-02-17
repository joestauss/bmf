import utility
import collections
import pyparsing as pp
import imdb

class FilmRecord( collections.UserDict, utility.JSONableMapping):
    __repr__ = utility.JSONableMapping.__repr__

    def __str__( self):
        if 'title' in self:
            if 'year' in self:
                return f"{self[ 'title']} ({ self[ 'year']})"
            else:
                return self['title']
        else:
            return "FilmRecord"

    @classmethod
    def from_id_string( cls, id_string):
        try:
            MOVIE_ID = pp.Word( pp.nums)
            MOVIE_ID.parseString( id_string)
            return FilmRecord( {'movie_id' : id_string})
        except pp.ParseException:
            YEAR_PAREN     = pp.Suppress("(") + pp.Word(pp.nums).setResultsName('year') + pp.Suppress(")")
            TITLE          = pp.OneOrMore( pp.Word(pp.printables, excludeChars='()')).setParseAction(' '.join).setResultsName("title")
            TITLE_AND_YEAR = pp.Group(TITLE + pp.Optional(YEAR_PAREN))
            result         = TITLE_AND_YEAR.parseString(id_string)[0]
            if len(result) == 1:
                return FilmRecord({'title' : result.title})
            return FilmRecord({'title' : result.title, 'year' : int( result.year) })

class FilmSet( utility.BaseSet):
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


if __name__ == "__main__":
    ia = imdb.IMDb()
    company = ia.get_company( ia.search_company('Hammer Films')[0].companyID)
    print( company.summary())

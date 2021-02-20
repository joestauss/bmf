from py_util.collections import BaseMapping, JSONableMapping
from py_util.parsers     import extract_film_identity

class FilmRecord( BaseMapping, JSONableMapping):
    def __init__(self, film_title, release_year):
        data_dictionary = { 'title' : film_title, 'year' : release_year}
        super().__init__( data_dictionary)

    def __str__( self):
        return f"{self['title']} ({self['year']})"

    def __repr__( self):
        return f'{type(self).__name__}({self["title"]!r}, {self["year"]!r})'

    @classmethod
    def from_id_string( cls, id_string):
        title, year, _ = extract_film_identity( id_string)
        if year:
            return cls({'title' : title, 'year' : year })
        else:
            return cls({'title' : title})

    def pretty_print( self):
        lines = [ str( self)]
        lines.append("="*len(lines[0]))
        for key, value in self.data.items():
            lines.append( f"  {key} --- {value}")
        return "\n".join( lines)

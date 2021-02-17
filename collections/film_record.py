from py_util.collections import BaseMapping, JSONableMapping
from py_util.parsers     import extract_film_identity

class FilmRecord( BaseMapping, JSONableMapping):
    def __str__( self):
        if 'title' in self and 'year' in self:
            return f"{self[ 'title']} ({ self[ 'year']})"
        elif 'title' in self:
            return self['title']
        else:
            return "FilmRecord"

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

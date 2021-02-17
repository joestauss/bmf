from py_util.collections import BaseSet

class FilmSet( BaseSet):
    def __eq__( self, other):
        print( [obj in other.data for obj in self.data])
        return all( obj in other.data for obj in self.data)

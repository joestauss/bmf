from py_util.collections import BaseMapping
import collections.abc

class FilmRecord( collections.abc.Hashable, BaseMapping):
    global_counter = 0

    def __init__( self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hash = FilmRecord.global_counter
        FilmRecord.global_counter = FilmRecord.global_counter + 1

    def __hash__( self):
        return self._hash

    def __eq__( self, other):
        return self.data == other.data

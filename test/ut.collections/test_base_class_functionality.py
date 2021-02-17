import unittest
from bmb.collections import FilmRecord, FilmSet
from collections import namedtuple

class Test_BaseClass_Functionality( unittest.TestCase):
    def setUp( self):
        InitTestCase = namedtuple( 'InitTestCase', [ 'input', 'object'])
        dicts = [
            { 'a' : 'A', 'b' : 'B'},
            { f"key_{i}" : f"value_{i}" for i in range( 10)}
        ]

        self.records = [ InitTestCase(dict, FilmRecord( dict)) for dict in dicts]
        self.sets = [
            InitTestCase( {self.records[0].object},         FilmSet( {self.records[0].object})),
            InitTestCase( {self.records[1].object},         FilmSet( {self.records[1].object})),
            InitTestCase( {r.object for r in self.records}, FilmSet( {r.object for r in self.records}))
        ]

    def test_BaseMapping_through_FilmRecord( self):
        for test_case in self.records:
            self.assertEqual( test_case.object, FilmRecord( test_case.input))
            self.assertEqual( test_case.object, eval( repr( test_case.object)))

    def test_BaseSet_through_FilmSet( self):
        for test_case in self.sets:
            self.assertEqual( test_case.object, FilmSet( test_case.input))

if __name__ == "__main__":
    unittest.main()

import unittest
from test_Resources import TestCases
from parsers import TableParser, FilmParser

class TestTableParser( unittest.TestCase):
    def test_TableParser( self):
        for input, expected_output in TestCases.TableParser.validated_correct:
            self.assertEqual( TableParser.parse( input), expected_output)

    def test_FilmParser_identify( self):
        for input, expected_output in TestCases.FilmParser.validated_identities:
            self.assertEqual( FilmParser.identify(input), expected_output)

    def test_FilmParser_collection_structure( self):
        for input, expected_ids, expected_groups in TestCases.FilmParser.validated_collection_structures:
            self.assertEqual( FilmParser.collection_structure( input), (expected_ids, expected_groups))

if __name__ == '__main__':
    unittest.main()

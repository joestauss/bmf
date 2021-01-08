import unittest
from test_Resources import TestCases
from parsers import Parser

class TestTableParser( unittest.TestCase):
    def test_table_parser( self):
        for input, expected_output in TestCases.TableParser.validated_correct:
            self.assertEqual( Parser.table_parser( input), expected_output)

if __name__ == '__main__':
    unittest.main()

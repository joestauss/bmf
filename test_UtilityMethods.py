import unittest
from utility_methods import *
from test_Resources import *
from parsers import TableParser

class TestExportUtil( unittest.TestCase):
    def test_TableEquality( self):
        for table1_str, table2_str in TestCases.TableClass.same_tables:
            table1 = TableParser.parse( table1_str)
            table2 = TableParser.parse( table2_str)
            self.assertEqual(table1, table2)

    def test_Normalization( self):
        for known_case in TestCases.TableClass.validated_normalizations:
            base_table = TableParser.parse(known_case['base_table'])
            terminal_table = base_table.NormalizeColumn('col2', 'col3')
            self.assertEqual( terminal_table, TableParser.parse(known_case['expected_terminal_table']))
            self.assertEqual( base_table, TableParser.parse(known_case['expected_connecting_table']))

if __name__ == '__main__':
    unittest.main()

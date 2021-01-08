import unittest
from locators import StringLocator
from utility_methods import *
from test_Resources import *

class TestStringLocator( unittest.TestCase):
    def test_FilmIdentity( self):
        for input, output in TestCases.UtilityMethods.FilmIdentity:
            self.assertEqual( StringLocator.film_identity(input), output)

class TestExportUtil( unittest.TestCase):
    def test_TableEquality( self):
        table1 = ExportUtil.Table([
            {'col1' : 'a', 'col2' : 'A'},
            {'col1' : 'b', 'col2' : 'B'}])
        table2 = ExportUtil.Table([
            {'col1' : 'a', 'col2' : 'A'},
            {'col1' : 'b', 'col2' : 'B'}])
        self.assertEqual(table1, table2)

    def test_Normalization( self):
        for known_case in TestCases.TableClass.validated_normalizations:
            base_table = known_case['base_table']
            terminal_table = base_table.NormalizeColumn('col2', 'col3')
            self.assertEqual( terminal_table, known_case['expected_terminal_table'])
            self.assertEqual( base_table, known_case['expected_connecting_table'])


if __name__ == '__main__':
    unittest.main()

import unittest
from utility_methods import *
from UnitTest_Resources import *

class TestStringUtil( unittest.TestCase):
    def test_FilmIdentity( self):
        for input, output in TestCases.UtilityMethods.FilmIdentity:
            self.assertEqual( StringUtil.film_identity(input), output)

class TestSQLUtil( unittest.TestCase):
    def test_TableEquality( self):
        table1 = SQLUtil.Table([
            {'col1' : 'a', 'col2' : 'A'},
            {'col1' : 'b', 'col2' : 'B'}])
        table2 = SQLUtil.Table([
            {'col1' : 'a', 'col2' : 'A'},
            {'col1' : 'b', 'col2' : 'B'}])
        self.assertEqual(table1, table2)

    def test_Normalization( self):
        base_table = SQLUtil.Table( [
            {'col1' : 'a1', 'col2' : 'A'},
            {'col1' : 'b' , 'col2' : 'B'},
            {'col1' : 'a2', 'col2' : 'A'} ])
        terminal_table = base_table.NormalizeColumn('col2', 'col3')
        true_terminal  = SQLUtil.Table( [
            {'col2' : "A", 'col3': 0},
            {'col2' : "B", 'col3': 1} ])
        true_transformed_base = SQLUtil.Table( [
            {'col1' : 'a1', 'col3' : 0},
            {'col1' : 'b' , 'col3' : 1},
            {'col1' : 'a2', 'col3' : 0} ])
        self.assertEqual(true_transformed_base, base_table)
        self.assertEqual(true_transformed_base, base_table)


if __name__ == '__main__':
    unittest.main()

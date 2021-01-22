''' The code in the utility module was taken from the "my-python-utilities" repository.

Contains
--------
    boxed_text : v1
    SQLTable   : v1
'''
import pyparsing as pp

def boxed_text( *args, BUFFER_SPACE=5 ):
    '''boxed_text   is a function that pretty-prints its args in a box.

Parameters
-----------
    args
        Each arg in args will be interpretted as a string, unless it's a non-string iterable, in which case it will be unpacked.

    BUFFER_SPACE: int
        The number of spaces between the longest text and the left/ right borders.

    ''' #v1
    def unpack_strings( obj):
        if isinstance( obj, str) or not hasattr(obj, '__iter__'):
            return [ str (obj)]
        else:
            lines = []
            for item in obj:
                lines = lines + unpack_strings( item)
    lines = unpack_strings( args)

    MAX_LEN         = max( map( lambda s: len(s), lines))
    HORIZONTAL_LINE = '='* (MAX_LEN + 2*BUFFER_SPACE + 4)
    GAP             = '||' + ' '*(MAX_LEN + 2*BUFFER_SPACE) +'||'
    RIGHT_BORDER    = '||' + ' '*BUFFER_SPACE
    LEFT_BORDER     =  ' '*BUFFER_SPACE + '||'
    TOP_BORDER      = (HORIZONTAL_LINE, GAP)
    BOTTOM_BORDER   = (GAP, HORIZONTAL_LINE)
    return "\n".join([*TOP_BORDER, *map( lambda l: RIGHT_BORDER + l + ' '*(MAX_LEN - len(l))+ LEFT_BORDER, lines), *BOTTOM_BORDER])

class SQLTable():
    """SQLTable performs basic operations for relational data.

Attributes
----------
    rows : [dict]
        Each row is represented by a dictionary { column_name : cell_value}.  No schema is enforced.

Dunder Methods
--------------
    __init__
    __eq__
    __str__
    __repr__

Instance Methods
----------------
    add_primary_key
    contains_row
    insert_all
    normalize_column

Other Methods in the Namespace
------------------------------
    insert_from_dd
    _text_field
    text_field_s
    text_field_m
    text_field_l
    parse
    """ #v1

# Dunder Methods

    def __init__( self, rows):
        self.rows = rows

    def __eq__(self, other):
        return len(self.rows) == len(other.rows) and all( map( other.contains_row, self.rows))

    def __str__(self):
        return "\n".join( [str(row) for row in self.rows])

    def __repr__( self):
        return f"SQLTable( {repr( self.rows)})"

# Instance Methods

    def add_primary_key( self, primary_key_name):
        """ Add a primary key to the table.  The name of the primary key must be supplied, and its values are the integers 0 -- len( self.rows). """
        self.rows = [ { primary_key_name : i, **row} for i, row in enumerate( self.rows)  ]

    def contains_row( self, search_row):
        """ Return True if this table contains search_row"""
        return any( map (lambda row: len(row) == len( [c for c in row if c in search_row and row[c] == search_row[c]]), self.rows))

    def insert_all( self, target_table):
        """ Return a string containing INSERT INTO statements for every row in the table. """
        return "\n".join(  [SQLTable.insert_from_dd( target_table, row) for row in self.rows])

    def normalize_column( self, normalization_column, connecting_column):
        """ Normalize a column of this table and return the newly-created terminal table.

        Parameters
        ----------
            normalization_column : str
                The name of the column that is to normalized by.

            connecting_column : str
                The name for the newly-created common column between the tables.

        Returns
        -------
            An SQLTable containing the unqiue values in normalization_column.
            This table will be modified to reflect the normalization procedure.
        """
        # Begin by finding the unique values in the normalization column, and using it to construct the terminal table.
        unique_norm_col_values = []
        for row in self.rows:
            norm_col_value = row[ normalization_column]
            if norm_col_value not in unique_norm_col_values:
                unique_norm_col_values.append( norm_col_value)
        terminal_table = [ { connecting_column : i, normalization_column: value} for i, value in enumerate(unique_norm_col_values)]
        # Next use a lookup table to put new values in rows of the connecting table, and return the terminal table.
        lookup = { value: i for i, value in enumerate(unique_norm_col_values)}
        for row in self.rows:
            row[ connecting_column] = lookup[ row[ normalization_column]]
            row.pop( normalization_column)
        return SQLTable( terminal_table)

# Other Methods

    def insert_from_dd( table_name, dd):
        """ Create a statement to INSERT INTO table_name the row represented by the dd dictionary. """
        def transform_cell( c):
            if isinstance( c, str):
                return  f'"{c}"'
            elif c == None:
                return 'Null'
            return str( c)
        k_s = []
        v_s = []
        for k, v in dd.items():
            k_s.append( k)
            v_s.append( transform_cell( v))
        return f'INSERT INTO {table_name} ({", ".join(k_s)}) VALUES ({", ".join(v_s)});'

    def _text_field(input_string, text_length):
        """Replace quotation marks and, if len(input_string) > text_length, truncate with an ellipsis."""
        if len(input_string) > text_length:
            input_string = input_string[:text_length-3] + '...'
        return input_string.lstrip().replace( '"', "'")

    def text_field_l(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 400)

    def text_field_m(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 200)

    def text_field_s(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 45)

    def parse( table_string):
        """ Interprets markdown-style tables, with the first row as a header:
            | column 1 | column 2 | column 3|
            | a        | b        | c       |
            | 1        | 2        | 3       |
        Columns don't have to line up; all that matters is that each row is "|"-delimited.

        Parameters
        ----------
        table_string: string
          A string multi-line string of "|"-delimited rows.  There can be blank rows, but comments are not yet supported.

        Returns
        -------
        An SQLTable containing the same data as test_string.
        """

        INTEGER = pp.Word(pp.nums).setParseAction(lambda x: int(x[0]))
        STRING  = pp.OneOrMore(pp.Word(pp.alphanums, pp.alphanums+'_'))
        CELL    = INTEGER | STRING
        ROW  = pp.Suppress("|") + pp.delimitedList(CELL, delim='|').setParseAction(lambda x: [x]) + pp.Suppress("|")
        ROW_LINE = ROW + pp.Suppress(pp.LineEnd())
        TABLE   = ROW_LINE.setResultsName("header") + pp.OneOrMore(ROW_LINE).setResultsName("data") + pp.StringEnd()

        result = TABLE.parseString( table_string)
        header = result.header[0]
        data   = result.data
        return  SQLTable( [{header[i]: row[i] for i in range( len( header))} for row in data])

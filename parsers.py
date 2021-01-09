import pyparsing as pp
from utility_methods import ExportUtil

class Parser:
    def table_parser( table_string):
        ''' Interprets markdown-style tables, with the first row as a header:
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
        An ExportUtil.Table containing the same data as test_string.
        '''

        INTEGER = pp.Word(pp.nums).setParseAction(lambda x: int(x[0]))
        STRING  = pp.OneOrMore(pp.Word(pp.alphanums, pp.alphanums+'_'))
        CELL    = INTEGER | STRING
        ROW  = pp.Suppress("|") + pp.delimitedList(CELL, delim='|').setParseAction(lambda x: [x]) + pp.Suppress("|")
        ROW_LINE = ROW + pp.Suppress(pp.LineEnd())
        TABLE   = ROW_LINE.setResultsName("header") + pp.OneOrMore(ROW_LINE).setResultsName("data") + pp.StringEnd()
        
        search_result = TABLE.parseString( table_string)
        header = search_result.header[0]
        data   = search_result.data
        return ExportUtil.Table( [{header[i]: row[i] for i in range( len( header))} for row in data])

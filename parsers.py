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
        CELL_ENTRY     = pp.OneOrMore(pp.Word(pp.alphanums, pp.alphanums+'_'))
        INTEGER_ENTRY  = pp.Word(pp.nums)
        WORD_ENTRY     = pp.Word(pp.alphas)
        ROW_GRAMMAR    = pp.delimitedList(CELL_ENTRY, delim='|')

        state   = "HEADER"
        data    = []
        columns = []
        for line in table_string.split('\n'):
            search_result =  ROW_GRAMMAR.searchString(line)
            if search_result:
                row = search_result[0]
                if state == "HEADER":
                    columns = row
                    state = "BODY"
                else:
                    for i in range(len(row)):
                        if INTEGER_ENTRY.searchString( row[i]) and not WORD_ENTRY.searchString(row[i]):
                            row[i] = int(row[i])
                    data.append( row)

        return ExportUtil.Table([ {col_name: dat[i] for i, col_name in enumerate(columns)} for dat in data ])

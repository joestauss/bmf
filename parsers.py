import pyparsing as pp
from utility_methods import ExportUtil

class FilmParser():
    YEAR_PAREN     = pp.Suppress("(") + pp.Word(pp.nums).setParseAction( lambda x: int(x[0]) ).setResultsName('year') + pp.Suppress(")")
    TITLE          = pp.OneOrMore( pp.Word( pp.alphanums, pp.alphanums+'.:')).setParseAction(lambda x: ' '.join(x)).setResultsName("title")
    TITLE_AND_YEAR = TITLE + pp.Optional(YEAR_PAREN)
    IMDB_FILM_ID   = pp.Regex("tt\d+")

    def identify( s):
        ''' Identify is the swiss army knife of identifing films.

        Input
        -----
        s: str
            A single film to be identified.  Currently supported formats:
            - Title (Year)

        Returns
        -------
        A tuple of (IMDB Film ID, title, year).
        If any of these are not in "s", None will be in its place.
        '''
        
        film_id = FilmParser.IMDB_FILM_ID.searchString(s)
        if film_id:
            return (film_id[0][0], None, None)
        result = FilmParser.TITLE_AND_YEAR.parseString(s)
        if not result.year:
            return (None, result.title, None)
        return ( None, result.title, result.year)

class TableParser():
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

    def parse( table_string):
        result = TableParser.TABLE.parseString( table_string)
        header = result.header[0]
        data   = result.data
        return  ExportUtil.Table( [{header[i]: row[i] for i in range( len( header))} for row in data])

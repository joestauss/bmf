import pyparsing as pp
from utility_methods import ExportUtil

class FilmParser():
    YEAR_PAREN     = pp.Suppress("(") + pp.Word(pp.nums).setParseAction( lambda x: int(x[0]) ).setResultsName('year') + pp.Suppress(")")
    TITLE          = pp.OneOrMore( pp.Word(pp.printables, excludeChars='()')).setParseAction(lambda x: ' '.join(x)).setResultsName("title")
    TITLE_AND_YEAR = pp.Group(TITLE + YEAR_PAREN).setResultsName('Title and Year Pairs', listAllMatches=True)
    IMDB_FILM_ID   = pp.Regex("tt\d+")

    END_ENTRY            = pp.Suppress(pp.Literal(";") | pp.StringEnd() | pp.LineEnd())
    FILM_ENTRY           = (IMDB_FILM_ID | TITLE_AND_YEAR) + END_ENTRY
    GROUP_ENTRY          = (pp.OneOrMore( pp.Word( pp.alphanums)).setParseAction(lambda x: ' '.join(x)) + pp.Suppress(":") + pp.Suppress("{") + pp.ZeroOrMore( FILM_ENTRY) + pp.Suppress("}") + END_ENTRY).setParseAction(lambda x: [x])
    COLLECTION_STRUCTURE = pp.OneOrMore( FILM_ENTRY | GROUP_ENTRY)

    def collection_structure( structure_string):
        ''' Reads a list of film entries and their category strucutre.

        Input
        -----
        structure_string: str
            Contains entries that are either categories or "loose" films.

            Categories are structured like:

            <CATEGORY NAME> : {
                <DATA 1>
                {DATA 2>
            }

            Entries are ended by either a semicolon or a newline so, for now at least,
            one of these must come between the final entry in a category and "}".

        Returns
        -------
        A tuple of (
            set of all film ids,
            dict of keywords
        )
        '''
        parse_results = FilmParser.COLLECTION_STRUCTURE.parseString( structure_string)
        films = set()
        groups = {}
        for title, year in parse_results['Title and Year Pairs']:
            films.add( f"{title} ({year})")
        for entry in parse_results:
            if FilmParser.IMDB_FILM_ID.searchString( entry):
                films.add( entry)
        return films, groups

    def identify( s):
        ''' Identify is the swiss army knife of identifing films.

        Input
        -----
        s: str
            A single film to be identified.  Currently supported formats:
            - Title (Year)
            - Title (without a year)
            - IMDB film ID (can be anywhere, meaning this enables...)
            - a URL that contains an IMDB film ID

        Returns
        -------
        A tuple of (IMDB Film ID, title, year).
        If any of these are not in "s", None will be in its place.
        '''
        s = s.replace(u'\xa0', ' ')
        film_id = FilmParser.IMDB_FILM_ID.searchString(s)
        if film_id:
            return (film_id[0][0], None, None)
        result = FilmParser.TITLE_AND_YEAR.parseString(s)
        if len(result[0]) == 1:
            return (None, result[0][0], None)
        return ( None, result[0][0], result[0][1])

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

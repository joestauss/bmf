from utility_methods import ExportUtil

class PersonID:
    vincent_price = 'nm0001637'
    bruce_willis  = 'nm0000246'
    renee_zellweger = 'nm0000250'

class TestCases:
    class FilmParser:
        validated_identities = [
            ('tt2347386', ('tt2347386', None, None)), # a valid imdb id
            ('Terminator (1492)', ( None, 'Terminator', 1492)), # a valid film-and-date.
            ('I am the muffin man', (None, 'I am the muffin man', None)), # neither of the above, assumed to be a title.
            ('Deltron(3030)', (None, 'Deltron', 3030)), # No space, should still work.
            ('Beastmaster 2000 (1982)', (None, 'Beastmaster 2000', 1982)), # something like this started this whole fix
            ('/embedded/link/tt234/j/', ('tt234', None, None)) # this should locate the film_id
        ]

    class TableParser:
        validated_correct = [(
        '''
        | col_1 | col_2 |
        | a     | b     |
        ''',
        ExportUtil.Table([{'col_1':'a', 'col_2': 'b'}])),
        ('''| col |
        | 1 |
        | 2 |''',
        ExportUtil.Table([{'col':i} for i in [1, 2]])
        )]

    class TableClass:
        validated_normalizations = [{
        'base_table' : '''
        | col1 | col2 |
        | a1   | A    |
        | b    | B    |
        | a2   | A    |''',
        'expected_terminal_table': '''
        | col2 | col3 |
        | A    | 0    |
        | B    | 1    |''',
        'expected_connecting_table': '''
        | col1 | col3 |
        | a1   | 0    |
        | b    | 1    |
        | a2   | 0    |''' }]

        same_tables = [ ('''
        | col_0 | col_1 | col_2 |
        | 0     | 1     | 2     |
        | Blah  | Blah  | Blah  |
        ''', '''
        | col_0 | col_1 | col_2 |
        | 0     | 1     | 2     |
        | Blah  | Blah  | Blah  |
        '''
        )]

    class Webscrapers():
        filmography_search = [
            (PersonID.vincent_price, ['tt0099487', 'tt0045888', 'tt0081178'] ), # Ed S'hands, house of wax, monster club
            (PersonID.bruce_willis,  ['tt0095016']) # Die Hard
        ]
        validated_films = [
            ('tt0087892', "A Passage to India", 1984),
            ('tt0045888', "House of Wax", 1953),
            ('tt0397065', "House of Wax", 2005)
        ]

        validated_person_ids = [
            (PersonID.bruce_willis, "Bruce Willis"),
            (PersonID.vincent_price, "Vincent Price")
        ]

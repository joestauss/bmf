from utility import SQLTable

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

        validated_collection_structures = [ # (input, output film ids, output keywords)
            ('''
            tt1
            tt2
            tt3
            ''', {'tt1', 'tt2', 'tt3'}, {} ),
            (''' tt4; tt5;
            tt6
            tt7;''', {'tt4', 'tt5', 'tt6', 'tt7'}, {} ),
            (''' Category : { tt20; tt21;} ''',
            {'tt20', 'tt21'}, {'Category' : {'tt20', 'tt21'} }),
            ('''tt10
            Category 1 : {tt11; tt12;}
            tt13
            Category 2 : {
            tt14; tt15
            tt16
            }
            tt17
            ''',
            {'tt10', 'tt11', 'tt12', 'tt13', 'tt14', 'tt15', 'tt16', 'tt17'},
            { 'Category 1': {'tt11', 'tt12'}, 'Category 2': {'tt14', 'tt15', 'tt16'}})
        ]


class ActorID():
    vincent_price = 'nm0001637'
    bruce_willis  = 'nm0000246'
    renee_zellweger = 'nm0000250'

class TestCases():
    class UtilityMethods():
        FilmIdentity = [
            ('tt2347386', ('tt2347386', None, None)), # a valid imdb id
            ('Terminator (1492)', ( None, 'Terminator', 1492)), # a valid film-and-date.
            ('I am the muffin man.', (None, 'I am the muffin man.', None)), # neither of the above, assumed to be a title.
            ('Deltron(3030)', (None, 'Deltron', 3030)), # No space, should still work.
            ('Beastmaster 2000 (1982)', (None, 'Beastmaster 2000', 1982)), # something like this started this whole fix
            ('/embedded/link/tt234/j/', ('tt234', None, None)) # this should locate the imdb_id
        ]

    class Webscrapers():
        filmography_search = [
            (ActorID.vincent_price, ['tt0099487', 'tt0045888', 'tt0081178'] ), # Ed S'hands, house of wax, monster club
            (ActorID.bruce_willis,  ['tt0095016']) # Die Hard
        ]
        validated_films = [
            ('tt0087892', "A Passage to India", 1984),
            ('tt0045888', "House of Wax", 1953),
            ('tt0397065', "House of Wax", 2005)
        ]

        validated_actor_ids = [
            (ActorID.bruce_willis, "Bruce Willis"),
            (ActorID.vincent_price, "Vincent Price")
        ]


class TestSet:
    class MixedFormat:
        tiny   = {'tt0042376', 'Tommy Boy (1995)'}
        medium = {'tt0042376', 'Tommy Boy (1995)', 'The Matrix (1984)', 'The Ice Pirates', 'beep boop im not a real movie', 'tt4'}

    one_unreleased = {'tt8820258', 'tt0859635', 'tt0247745'}
    # super troopers 1-3. the third has not been released yet (it miiiight be out sometime in 2021).

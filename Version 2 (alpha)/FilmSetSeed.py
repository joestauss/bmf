from FilmSet import FilmSet

import pyparsing as pp

class FilmSetSeed:

    @staticmethod
#
# ACTOR		Vincent Price # Mostly after 1953, though his career always included other genres.
# DIRECTOR	Roger Corman  # Known as "King of the B's".  Get his whole Poe series.
# PRODUCER	Val Lewton	  # Made several B-Horror films for RKO in the 40's (maybe more RKO?)
# ACTOR		Boris Karloff # Maybe a little bit older-school than I'm going for?
# PROD_CO		Hammer Film Productions # and variants?
# DIRECTOR	Herschell Gordon Lewis  # The Godfather of Gore
# DIRECTOR	Lucio Fulci   # Also AKA The Godfather of Gore
# DIRECTOR	Mario Bava    # The Master of Italian Horror
# DIRECTOR	George A. Romero
# DIRECTOR	David Cronenberg
#
# # The Ultimate Anthology Horror List, by theNomad
# IMDB_LIST	https://www.imdb.com/list/ls000742940/
#
# # Check out the "Poverty Row" studios.
#
# # I think that the B-Movie Era can be said to have gone from 1948-1980:
# #
# # Beginning in 1948 with the Paramount Decrees.
# #
# # By 1961, the average production cost of an American feature film was still only $2 million—
# # after adjusting for inflation, less than 10% more than it had been in 1950.
# #
# # It had taken a decade and a half, from 1961 to 1976, for the production cost of the average
# # Hollywood feature to double from $2 million to $4 million—a decline if adjusted for inflation.
# # In just four years it more than doubled again, hitting $8.5 million in 1980
#
#
# Deathdream (1974) # AKA Dead of Night; is a Vietnam protest film
# Fright Night (1985)
# One Dark Night (1982)
# The House of Seven Corpses (1974)
# The House that Dripped Blood (1971)
# The Mephisto Waltz (1971)
#
    def parse_string( input_string):
        pp.ParserElement.setDefaultWhitespaceChars(' \t')

        YEAR_PAREN = pp.Literal("(") + pp.Word(pp.nums) + pp.Literal(")")
        TEXT       = pp.Combine( pp.OneOrMore( pp.Word( pp.printables, excludeChars='(){}\n')), adjacent=False, joinString=' ')
        FILM_ENTRY = (pp.Combine(TEXT + YEAR_PAREN, adjacent=False, joinString=' '))('films*')

        DIRECTOR_CMD = pp.Literal( "DIRECTOR" )
        PRODUCER_CMD = pp.Literal( "PRODUCER" )
        PROD_CO_CMD  = pp.Literal( "PROD_CO"  )
        ACTOR_CMD    = pp.Literal( "ACTOR"    )
        LIST_CMD     = pp.Literal( "IMDB_LIST")
        COMMAND = DIRECTOR_CMD | PRODUCER_CMD | PROD_CO_CMD | ACTOR_CMD | LIST_CMD
        COMMAND_ENTRY = (COMMAND + TEXT)('commands*')

        ENTRY = (COMMAND_ENTRY | FILM_ENTRY) + pp.LineEnd()
        SEED_STRUCTURE = pp.ZeroOrMore( ENTRY)

        result = SEED_STRUCTURE.parseString( input_string)

        if 'films' in result:
            film_strings = [str( film) for film in result[ 'films']]
            filmset = FilmSet.from_movie_list( film_strings)
        else:
            filmset = FilmSet()

        if 'commands' in result:
            for command_type, command_detail in result[ 'commands']:
                if DIRECTOR_CMD.searchString( command_type):
                    filmset = filmset | FilmSet.from_director( command_detail)

                if PRODUCER_CMD.searchString( command_type):
                    filmset = filmset | FilmSet.from_producer( command_detail)

                if PROD_CO_CMD.searchString( command_type):
                    filmset = filmset | FilmSet.from_prod_co( command_detail)

                if ACTOR_CMD.searchString( command_type):
                    filmset = filmset | FilmSet.from_actor( command_detail)

                if LIST_CMD.searchString( command_type):
                    filmset = filmset | FilmSet.from_imdb_list( command_detail)

        return filmset

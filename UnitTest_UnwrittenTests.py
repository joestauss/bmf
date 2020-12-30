#   Explaination of this Module
#
#   One of the benefits of unit testing (other than catching bugs, of course) is
#   to help organize a code-base; an easily-unit-testable method is probably
#   well-defined, has a clear interface to the rest of the program, etc.
#
#   However, I don't unit test everything - I just sort of add new tests as I
#   feel they are are helpful.  This module is a place for comments about parts
#   of the code that either haven't been tested yet or won't be tested at all.
#
#   This script is structured like another UnitTest_ module: each test is one
#   that might be written, containing the relevant comments  to it
#   and an always true assertion:
#       self.assertTrue( True)
#
#
import unittest

class UnwrittenTest( unittest.TestCase):

    def test_RecommendationSearch( self):
        #   I'm not sure that recommendations are deterministic.  Find that out
        #   before attempting to test recommendation search.
        #
        self.assertTrue( True)

    def test_TaglineScraper( self):
        #   Before this can be written, the tagline scraper needs to be properly
        #   refactored to deal with the "2 random" condition.
        #
        self.assertTrue( True)

    def test_ProductionCompanyScraper( self):
        #   Don't worry about until writing a more thorough company credits scraper.
        #
        self.assertTrue( True)

    def test_MainPageScraper( self):
        #   Write this when revamping details and cast locators.
        #
        self.assertTrue( True)

    def test_BaseFilmCollection( self):
        #   Start testing if I make any chagned to "add_record" (it has enough edge cases to be worth it).
        #
        self.assertTrue( True)

if __name__ == '__main__':
    unittest.main()

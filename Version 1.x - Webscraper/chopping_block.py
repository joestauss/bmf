''' The chopping block is for code that is going to be depricated, but can't be yet because something else that is going to be changed soon depends on it.

Contains
--------
    FilmParser
    SoupUtil.search_in_soup
    StringLocator.*
'''

import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pyparsing as pp
from utility import *

class FilmParser():
    YEAR_PAREN     = pp.Suppress("(") + pp.Word(pp.nums).setParseAction( lambda x: int(x[0]) ).setResultsName('year') + pp.Suppress(")")
    TITLE          = pp.OneOrMore( pp.Word(pp.printables, excludeChars='()')).setParseAction(lambda x: ' '.join(x)).setResultsName("title")
    TITLE_AND_YEAR = pp.Group(TITLE + YEAR_PAREN).setResultsName('Title and Year Pairs', listAllMatches=True)
    IMDB_FILM_ID   = pp.Regex("tt\d+")
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

class SoupUtil:
    def search_in_soup(soup, tag_type, search_text):
        candidates = soup.find_all(tag_type)
        for c in candidates:
            tag_text = c.text
            if re.search(search_text, tag_text):
                return c
        return None

class StringLocator:
    def dollar_amount( s):
        dollar_amounts = re.findall(r'\$[0-9,]+', s)
        for d in dollar_amounts:
            return int(d[1:].replace(',', ''))
        return None

    def minute_amount( s):
        minute_amounts = re.findall(r'[0-9]+ min', s)
        for m in minute_amounts:
            return int(m[:-4])
        return None

    def person_id( s):
        if re.search("nm\d+", s):
            return re.findall("nm\d+", s)[0]
        return None

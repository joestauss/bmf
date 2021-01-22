''' The chopping block is for code that is going to be depricated, but can't be yet because something else that is going to be changed soon depends on it.

Contains
--------
    SoupUtil.search_in_soup
    SeleniumContext.BasicChromeDriver
    StringLocator.*
'''

import re
from bs4 import BeautifulSoup
from selenium import webdriver

class SoupUtil:
    def search_in_soup(soup, tag_type, search_text):
        candidates = soup.find_all(tag_type)
        for c in candidates:
            tag_text = c.text
            if re.search(search_text, tag_text):
                return c
        return None

class SeleniumContext:
    class BasicChromeDriver():
        def __init__( self, url):
            self.url = urlweb

        def __enter__(self):
            self.driver = webdriver.Chrome()
            self.driver.get(self.url)
            return self.driver

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.driver.quit()

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

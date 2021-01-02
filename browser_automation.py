from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import SeleniumLocator
from threading import Thread
from utility_methods import *
from webscrapers import *
import time

def BatchExtraction( dataExtractionThread, inputs):
    results = {}
    threads = {}
    BATCH_SIZE = 10
    THREAD_COUNT = 0
    item_groups = [[]]
    i = 0
    for item in inputs:
        THREAD_COUNT = THREAD_COUNT + 1
        item_groups[i].append( item)

        if THREAD_COUNT == BATCH_SIZE:
            i = i + 1
            THREAD_COUNT = 0
            item_groups.append([])

    for item_group in item_groups:
        thread_pool = { item: dataExtractionThread( item, results) for item in item_group }
        for item in item_group:
            thread_pool[item].start()
        for item in item_group:
            thread_pool[item].join()

    return results

class IMDBExtractionThread():
    class BaseIMDBExtractionThread( Thread):
        def __init__(self, imdb_id, output_dict):
            super().__init__()
            self.imdb_id = imdb_id
            self.output_dict = output_dict

        def run( self):
            self.output_dict[ self.imdb_id] =  self.extract( self.imdb_id)

        def extract( self, imdb_id):
            return []

    class Recommendations( BaseIMDBExtractionThread):
        def extract(self, imdb_id):
            url = f"https://www.imdb.com/title/{imdb_id}/"
            recs = []
            with SeleniumContext.BasicChromeDriver( url) as driver:
                recs_temp = WebDriverWait(driver, 1).until( EC.presence_of_element_located(SeleniumLocator.IMDB.RECS_LIST))
                recs = recs_temp.find_elements(By.CLASS_NAME, 'rec_item')
                for rec in recs:
                    rec_str = rec.get_attribute("data-tconst")
                    if rec_str != imdb_id:
                        recs.append(rec_str)
            return recs

class DataExtraction():
    class Recommendations():
        def all( imdb_ids):
            recs = set()
            recs_dictionary = BatchExtraction( IMDBExtractionThread.Recommendations, imdb_ids)
            for imdb_id in recs_dictionary:
                recs = recs | {rec for rec in recs_dictionary[imdb_id]}
            return recs

        def multiple_adjacency( imdb_ids):
            rec_count = {}
            recs_dictionary = BatchExtraction( IMDBExtractionThread.Recommendations, imdb_ids)
            for imdb_id in recs_dictionary:
                for rec in recs_dictionary[ imdb_id]:
                    if rec not in rec_count:
                        rec_count[ rec] = 0
                    rec_count[ rec] = rec_count[ rec] + 1
            return {rec for rec in rec_count if rec_count[ rec] > 1}


class TwitterArtBot():
    def __init__( self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://twitter.com/"

    def text_post( self, post_text):
        with SeleniumContext.BasicChromeDriver( self.base_url) as self.driver:
            self._login()
            self._form_text_post( post_text)
            time.sleep(10)
                # I'm not ready to start posting yet.

    def _form_text_post(self, post_text):
        post_text_box = WebDriverWait(self.driver, 2).until( EC.presence_of_element_located(SeleniumLocator.Twitter.POST_TEXT_BOX))
        post_text_box.send_keys( post_text)

    def _login( self):
        username_box = WebDriverWait(self.driver, 2).until( EC.presence_of_element_located(SeleniumLocator.Twitter.USERNAME_BOX))
        username_box.send_keys( self.username)
        password_box = WebDriverWait(self.driver, 2).until( EC.presence_of_element_located(SeleniumLocator.Twitter.PASSWORD_BOX))
        password_box.send_keys( self.password)
        login_button = WebDriverWait(self.driver, 2).until( EC.presence_of_element_located(SeleniumLocator.Twitter.LOGIN_BUTTON))
        login_button.click()

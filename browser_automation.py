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
    ''' Multi-threaded data extraction in batches of 10.

    Parameters
    ----------
    dataExtractionThread: Thread class
        A thread to perform the desired data extraction a single time.

    inputs: list
        Desired inputs to dataExtractionThread.

    Returns
    -------
    A set of all the data extractions.
    '''
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

class IMDBExtractionThread:
    class BaseIMDBExtractionThread( Thread):
        def __init__(self, film_id, output_dict):
            super().__init__()
            self.film_id = film_id
            self.output_dict = output_dict

        def run( self):
            self.output_dict[ self.film_id] =  self.extract( self.film_id)

        def extract( self, film_id):
            return []

    class RecommendationsExtractionThread( BaseIMDBExtractionThread):
        def extract(self, film_id):
            url = f"https://www.imdb.com/title/{film_id}/"
            recs = []
            with SeleniumContext.BasicChromeDriver( url) as driver:
                recs_temp = WebDriverWait(driver, 1).until( EC.presence_of_element_located(SeleniumLocator.IMDB.RECS_LIST))
                recs = recs_temp.find_elements(By.CLASS_NAME, 'rec_item')
                for rec in recs:
                    if isinstance( rec, str):
                        rec_str = rec
                    else:
                        rec_str = rec.get_attribute("data-tconst")
                    if rec_str != film_id:
                        recs.append(rec_str)
            return recs

class ExtractData:
    class ExtractRecommendations:
        def all( film_ids):
            recs = set()
            recs_dictionary = BatchExtraction( IMDBExtractionThread.RecommendationsExtractionThread, film_ids)
            for film_id in recs_dictionary:
                recs = recs | {rec for rec in recs_dictionary[film_id]}
            return recs

        def multiple_adjacency( film_ids):
            rec_count = {}
            recs_dictionary = BatchExtraction( IMDBExtractionThread.RecommendationsExtractionThread, film_ids)
            for film_id in recs_dictionary:
                for rec in recs_dictionary[ film_id]:
                    if rec not in rec_count:
                        rec_count[ rec] = 0
                    rec_count[ rec] = rec_count[ rec] + 1
            return {rec for rec in rec_count if rec_count[ rec] > 1}

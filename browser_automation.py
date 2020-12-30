from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import SeleniumLocator
from threading import Thread
from utility_methods import *
from webscrapers import *

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
            return SeleniumLocator.IMDB.recommendations( imdb_id)

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

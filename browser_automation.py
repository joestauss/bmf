from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import SeleniumLocator
from threading import Thread
from utility_methods import *
from webscrapers import *

def ParallelExtraction( dataExtractionThread, inputs):
    results_set = set()
    threads = {}
    MAX_THREADS = 10
    THREAD_COUNT = 0
    item_groups = [[]]
    i = 0
    for item in inputs:
        THREAD_COUNT = THREAD_COUNT + 1
        item_groups[i].append( item)

        if THREAD_COUNT == MAX_THREADS:
            i = i + 1
            THREAD_COUNT = 0
            item_groups.append([])

    for item_group in item_groups:
        thread_pool = {
            item: dataExtractionThread( item, results_set)
            for item in item_group }
        for item in item_group:
            thread_pool[item].start()
        for item in item_group:
            thread_pool[item].join()

    return results_set

class IMDBExtractionThread():
    class BaseIMDBExtractionThread( Thread):
        def __init__(self, imdb_id, output_set):
            super().__init__()
            self.imdb_id = imdb_id
            self.output_set = output_set

        def run( self):
            temp_return = self.extract( self.imdb_id)
            for item in temp_return:
                self.output_set.add( item)

        def extract( self, imdb_id):
            return []

    class Recommendations( BaseIMDBExtractionThread):
        def extract(self, imdb_id):
            return SeleniumLocator.IMDB.recommendations( imdb_id)

class DataExtraction():
    class Recommendations():
        def all( imdb_ids):
            return ParallelExtraction( IMDBExtractionThread.Recommendations, imdb_ids)

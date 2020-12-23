import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IMDB_Tools():
    def recursive_recommendations( imdb_ids, recs_per_film, num_layers):
        # The number of recommendation grows with recs_per_film^num_layers.
        #
        assert type( num_layers) is int
        assert num_layers >= 0

        all_movies = set( imdb_ids)
        if num_layers == 0:
            # Not really necessary, but makes the recursion more explicit.
            #
            return all_movies
        else:
            print( f"{num_layers} recursive layers remain.")

            new_movies = set([])

            for movie in imdb_ids:
                print( f"\t\tGetting recs from {movie}")
                recs = IMDB_Tools.get_recomendations( movie, recs_per_film)

                for rec in recs:
                    if rec not in all_movies:
                        new_movies.add( rec)
                        all_movies.add( rec)
            print( f"\t...{len( new_movies)} new items.")
            all_movies = all_movies | IMDB_Tools.recursive_recommendations( new_movies, recs_per_film, num_layers - 1)

        return all_movies

    def get_recomendations( imdb_id, num_recs):
        URL = f"https://www.imdb.com/title/{imdb_id}/"

        driver = webdriver.Chrome()
        driver.get( URL)

        selected_recs = []
        try:
            recs_div = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "titleRecs"))
            )
            recs_temp = recs_div.find_elements(By.CLASS_NAME, 'rec_item')
            recs = []
            for rec in recs_temp:
                rec_str = rec.get_attribute("data-tconst")
                if rec_str != imdb_id:
                    recs.append(rec_str)

            try:
                #   Catches the case where
                #       num_recs > len (recs)
                #
                selected_recs = random.sample(recs, num_recs)
            except:
                selected_recs = recs

        finally:
            driver.quit()
            return selected_recs

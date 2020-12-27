from utility_methods import SoupUtil
from locators import SoupLocator

class IMDB_Scraper():
    def scrape_main_page( imdb_id):
        url = f'https://www.imdb.com/title/{imdb_id}'
        soup = SoupUtil.soup_from_url( url)
        ttl_yr = SoupLocator.IMDB.MainPage.title_and_year( soup)
        sm_cst = SoupLocator.IMDB.MainPage.small_credits( soup)
        detail = SoupLocator.IMDB.MainPage.details(soup)
        genres = SoupLocator.IMDB.MainPage.genres(soup)
        return ttl_yr, sm_cst, detail, genres

    def title_and_year( imdb_id):
        url  = f'https://www.imdb.com/title/{imdb_id}'
        soup = SoupUtil.soup_from_url( url)
        return SoupLocator.IMDB.MainPage.title_and_year( soup)

    def taglines(imdb_id, NUM_TAGLINES = 2):
        url = f'https://www.imdb.com/title/{imdb_id}/taglines'
        soup = SoupUtil.soup_from_url( url)
        return SoupLocator.IMDB.Taglines.get_two_at_random( soup)

    def production_companies( imdb_id):
        url = f'https://www.imdb.com/title/{imdb_id}/companycredits'
        soup = SoupUtil.soup_from_url( url)
        return SoupLocator.IMDB.CompanyCredits.production_cos( soup)

    def search_by_title_and_year( search_title, search_year):
        url = f"https://www.imdb.com/find?q={search_title}"
        soup = SoupUtil.soup_from_url( url)
        candidates = SoupLocator.IMDB.Search.films( soup)

        smallest_difference = 2000
        return_id   = None
        return_year = None
        for imdb_id, title, year in candidates:
            if search_year is None:
                return imdb_id, year
            if title == search_title:
                if abs(year - search_year) < smallest_difference:
                    return_id, return_year = imdb_id, year
        return return_id, return_year

# Data Scraping & Browser Automation
The repository contains tools for building a collection of movies and extract information about the films from the internet using webscraping and browser automation techniques.  I have two goals for this project:
* The first goal is to build a Twitter Art Bot that can post a movie poster along with a tagline for the film.  I'll automate the operation of a few bots for different niches and see if anybody enjoys them.
* The second goal is to build a movie recommendation system that is NOT based on collaborative filtering.  Almost every streaming company uses collaborative filtering for their recommendation system, and I'd like to look at other possibilities.

# FilmRecords and FilmCollections

The user-facing classes are found in __FilmRecord.py__ and  __FilmCollection.py__.  A FilmRecord encapsulates movie information at a specific level of detail, and a FilmCollection is a set-based container for a group of FilmRecords.  The hash-value for a FilmRecord is based on the IMDB ID of the film in question, so there is only one FilmRecord for any movie within a collection.  For both FilmRecord and FilmCollection, there is a base class and several sub-classes that represent various levels of detail.

# Webscraping

Webscraping is implemented across three modules: __webscraping_context_mangers.py__ handles all of the set-up and tear-down including, for example, checking that an IMDB film identification code is valid; __locators.py__ helps find specific web elements; and __webscrapers.py__ contains the methods that should be used to actually extract data.  I have used the BeautifulSoup python module for webscraping.

# Browser Automation

Not everything can be handled webscraping alone; in particular, recommendations on IMDB are added by Javascript after the initial HTML request has been served, so a functioning browser window is needed to find them.  The __browser_automation.py__ module uses the Selenium automation framework to initialize and control a Chrome window to extract movie recommendations.  Waiting for a server response can take a while, so the recommendation-extraction methods are multi-threaded, and create browser windows in batches of ten.

This method also contains the TwitterArtBot class.  The functionality is still pretty limited, but it can log in to a Twitter account from their website and enter text in the post field.

# Exporting Data

Exporting is handled in __FilmCollectionExport.py__.  The module contains a base class and several sub-classes that specify the format and level of detail for the data export.  Each of the classes takes a FilmCollection object as an initialization parameter.  Currently, the only export-format is SQL, although JSON will be added soon.  Most data-normalization methods are found in the SQLTable() class (see "Utility Methods").

# Unit testing

Unit tests can be found in the  __test_*.py__ modules, in addition to two auxiliary modules: __test_Resources.py__, which contains known values, and __test_UnwrittenTests.py__, which has notes regarding tests that I haven't written yet.  So far, these tests have all been added when I refactored the relevant section of code, but I will be aiming to use test-driven development principals going forward.

# Utility Methods

Miscellaneous other operations are supported in __utility_methods.py__.  There are currently three classes of methods: _SoupUtil_, _SQLTable_, and _PrintUtil_.  Previously, there was a _SeleniumUtil_ class as well, but its functionality has been completely taken over by webscraping_context_mangers.py, which is the eventual goal for this entire module; I would prefer if all of these methods were in other, more-purposeful modules, but at this stage in development I am okay with having an "other" module like this.

# Future Work

* _Add JSON as a supported export-format.  This will probably involve re-factoring the existing FilmCollectionExport, but is a better data-format than SQL for the planned TwitterArtBot data._
* _Add support for scraping movie posters.  This will be the first data extracted that is not text._
* _Add methods for TwitterArtBot to post an image.  When this, JSON support, and poster-scraping are implemented, the first ArtBot can go into operation._
* _Add support to associate keywords with FilmRecords at the FilmCollection level._

# Data Scraping & Browser Automation
The repository contains a collection of methods for automating web tasks.
My current goal is to build a Twitter ArtBot, which I expect should be done by about the New Year.

# Files

* **user_facing_classes** is the front end, what might eventually become an API.  It currently contains three classes:
 - _BaseFilmRecord_, which contains the data for a single film.
 - _BaseFilmCollection_ is a collection of film records.  It is set-based, unilke...
 - _BaseFilmDatabase_ is the interface to export a film collection to SQL.
* **webscrapers** contains methods for tasks that require only HTML parsing; it uses BeautifulSoup.
* **broswer_automation** is for more complex tasks, where with a bot is used to communicate with a server; it uses Selenium.
* **utility_methods** contains methods for string searching, data formatting, etc.  Eventually many of the methods in this module will be refactored into...
* _locators_ (not yet created) will contain methods for locating specific web elements.  It'll be pretty messy, but that's the point- hopefully by putting the worst of the "plumbing" here, the other modules will be short and easily readable.
* **filmsets** just groups of movies used for testing and evaluation.  Currently all IMDB_IDs.
* **Create Movie Database.sql** defines the data format for the BaseFilmDatabase.

## Files --- Example Notebooks

* **IMDB Webscraping Example** --- construction of a dataset based on six classic films directed by David Lean.
* **Recursive Recomendations Example** --- automated IMDB crawling to find recommendations, recommendations-of-recommendations, etc.

# DevLog

1. __12/22/20__ --- Repository created; first version of files uploaded.  Began a refactor.
1. __12/23/20__ --- Completed refactor, no new functionality but a better foundation to grow.
 - The code organization scheme is totally different than it was before.
 - All of the modules are now class-based.  I'm still deciding on a format for some of the classes, but on the whole it's been a great change, and it's especially nice in that it applies to the whole codebase.
  - Production companies and taglines are now scraping correctly.

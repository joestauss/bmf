# Data Scraping & Browser Automation
The repository contains a collection of methods for automating web tasks.
My current goal is to build a Twitter ArtBot, which I expect should be done by about the New Year.

# Files

* There are currently three _user facing classes_ that constitute the API: a __FilmRecord__, which contains the data for a single film; a _FilmCollection_, which contains a set of film records; and a __FilmDatabase__, which interface for a SQL representation of the data.  There are currently several types of records, collections, databases- I'm still deciding on the final arrangement of them.
* **webscrapers** contains methods for tasks that require only HTML parsing; it uses BeautifulSoup.
* **broswer_automation** is for more complex tasks, where with a bot is used to communicate with a server; it uses Selenium.
* **utility_methods** contains methods for string searching, data formatting, etc.  Eventually many of the methods in this module will be refactored into...
* _locators_ (not yet created) will contain methods for locating specific web elements.  It'll be pretty messy, but that's the point- hopefully by putting the worst of the "plumbing" here, the other modules will be short and easily readable.
* **filmsets** just groups of movies used for testing and evaluation.  Currently all IMDB_IDs.
* **Create Movie Database.sql** defines the data format for the BaseFilmDatabase.

## Files --- Example Notebooks

* **Film Collection Classes** --- demonstrates the difference between Base, Tagline, and Detailed classes.
* **Recursive Recomendations Example** --- automated IMDB crawling to find recommendations, recommendations-of-recommendations, etc.

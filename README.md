# Data Scraping & Browser Automation
The repository contains a collection of methods for automating web tasks.
My current goal is to build a Twitter ArtBot, which I expect should be done by about the New Year.

# Files

* A database is implemented as a group of three **User Facing Classes**: a _FilmRecord_, which contains the data for a single film; a _FilmCollection_, which contains a set of film records; and a _FilmDatabase_, which interface for a SQL representation of the data.  There are currently two types of databases: _Base_ classes (which don't try to find any data) and _Detailed_ classes (which do).
* **webscrapers** contains methods for tasks that require only HTML parsing; it uses BeautifulSoup.
* **broswer_automation** is for more complex tasks, where with a bot is used to communicate with a server; it uses Selenium.
* **utility_methods** contains methods for string searching, data formatting, etc.  Eventually many of the methods in this module will be refactored into...
* _locators_ (not yet created) will contain methods for locating specific web elements.  It'll be pretty messy, but that's the point- hopefully by putting the worst of the "plumbing" here, the other modules will be short and easily readable.
* **filmsets** just groups of movies used for testing and evaluation.  Currently all IMDB_IDs.
* **Create Movie Database.sql** defines the data format for the BaseFilmDatabase.

## Files --- Example Notebooks

* **Detailed Film Collections vs Base** --- demonstrates the difference between Base and Detailed objects with SQL INSERT INTO statements.
* **Recursive Recomendations Example** --- automated IMDB crawling to find recommendations, recommendations-of-recommendations, etc.

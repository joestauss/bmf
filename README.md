# Data Scraping & Browser Automation
The repository contains a collection of methods for automating web tasks.
My current goal is to build a Twitter ArtBot, which I expect should be done by about the New Year.

# Files

* There are currently three _user facing classes_ that constitute the API: a __FilmRecord__, which contains the data for a single film; a __FilmCollection__, which contains a set of film records; and a __FilmCollectionExport__, which is an interface for exporting a film collection, currently just as a normalized SQL database.  There are currently several types of records, collections, databases- I'm still deciding on the final arrangement of them.
* **webscrapers** contains methods for tasks that require only HTML parsing; it uses BeautifulSoup.
* **broswer_automation** is for more complex tasks, where with a bot is used to communicate with a server; it uses Selenium.
* **utility_methods** contains methods for string searching, data formatting, etc.  It's a little bit messy, but that's the point; by keeping most of the "plumbing" here, the code in the other modules can be more directly focused on the problem at hand.
* **filmsets** just groups of movies used for testing and evaluation.  Currently all IMDB_IDs.
* **Create Movie Database.sql** defines the data format for the DetailedFilmDatabase.

## Files --- Example Notebooks

* **Film Collection Classes** --- demonstrates the difference between Base, Tagline, and Detailed classes.
* **Recursive Recomendations Example** --- automated IMDB crawling to find recommendations, recommendations-of-recommendations, etc.

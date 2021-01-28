# My Requirements for Version 1.0

* __Test-driven development.__  I want to give TDD a shot, and this seems like a decent place to do it.

* __Data extraction.__ All data extraction should all be handled through an API, and all of the methods should be in a single data_extraction.py module (no more "browser_automation.py", "locators.py", "webscraping.py", "webscraping_contexts.py", etc.).

* __More, smaller, more abstract classes.__  With some of what I know now about dunder methods, I'd like to take a different approach to OOP.

* __Human-writable input.__  It should be possible to create a movie collection with a file that can be written in a text document.

* __Account and data resource Management.__ Nothing fancy; just a way to synchronize film lists with data files with image folders, etc.

* __Data source agnostic.__  v1.0 won't be IMDB-based; it will be a more general tool that may or may not have an IMDB mode.

* __All JSON, no SQL.__  Although I may want to use SQLite if I ever make this an App, for now everything will be JSON-based.

* __Key design patterns.__  Keep an eye out for opportunities to use context managers, generators, and decorators.

# Key Design Patterns

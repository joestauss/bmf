# ffwen

## About

I have used the code in this repository to help me with two projects, but the purpose of the codebase has become a little muddled by some of the additional functionality I have added in.  I am in the process of changing the data model for this project and using the opportunity to pin down the scope of this project more exactly.

## Installation & Dependencies

To use `ffwen`, just copy this repository to a location in your Python Path.

* **py\_util** - my collection of Python utility code; before `ffwen` is real-deal published, I will be relocating the `py_util` code to this repository.  Objects in `py_util` are named as transparently as possible (no points for guessing what the *@time_this* decorator does), so you should be able to read through and understand this repository without referring to the `py_util` source code, which is available on my GitHub if needed.
* **pyparsing**
* **tqdm**
* **IMDbPY**
* **Beautiful Soup**

## Repository Contents

### Source Code

The following directories contain source code for the `ffwen` package.

* **collections**  - any and all data structures.
* **extractors** - data acquisition hooks.
* **parsers** - extract information from text.
* **run** - scripts to execute high-level functionality.  If you don't want to mess around with webscrapers or algorithms or any of the internal junk and just want to do stuff , this is the folder for you.

### Development Resources

The following directories contain development resources, and do not contribute to package functionality.

* **data** - information about specific movies or movie collections.
* **deprecated** - old code that doesn't fit into the current architecture; kept around to revisit later.
* **docs** - written in Jupyter and Markdown.
* **sample** - sample code; some things, like interactive tools and pretty-print functions, can't easily be unit tested and should be demonstrated instead.
* **test** - unit tests.
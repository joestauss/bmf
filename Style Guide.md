
# Naming Data Structures and Methods

I've been working on this project for a while now, and found that I sometimes alternate between word-choices in a few contexts.  In the interest of having a consistent interface, the following words will be used for this project:
+ "Film" instead of "Movie".
+ "Person" instead of "Actor", although "actors" is OK as an attribute for a small-cast FilmRecord and "ActorSet" is OK in filmsets.py.
+ "film_id" or "person_id" instead of "imdb_id" or "actor_id".  In BaseSQLExport, "movie_id" is used to be consistent with the convention for naming SQL columns.

# Organizing Variants of Classes

When there are variants of a class (for example,  BaseSQLExport and DetailedSQLExport), they should be all be enclosed in a class called ClassName, and the name of each variant should be include ClassName.  For example:
```python
class SQLExport:
  class BaseSQLExport():
    pass
  class DetailedSQLExport( BaseSQLExport):
    pass
```
The following modules are exempt from this guideline, on account of impending refactor: FilmCollection, FilmRecord, ImageCollection, webscrapers, webscraping_context_managers.  This also does not apply to classes that are only used to encapsulate functions, such as SoupLocator.IMDB.Search.

# VERBOSE

Some methods have an optional VERBOSE flag that can set to see a tqdm progress bar.  It is set at the FilmCollection level, and is probably a good idea for large FilmCollections (there are HTTP requests involved for each film, and not much to be done about speeding them up). 

# Commenting Templates

Most methods can get away with a one-line docstring, but each reasonably complex method should have the following:

```python
''' Summary.

Parameters
----------
name: datatype
  description

Returns
-------
'''
```

Each class should have the following:

```python
''' Summary.

Attributes
----------
name: datatype
  description

Methods
-------
  name (no parameters)
'''
```

Child classes should explain any new attributes or methods, but can otherwise leave it at:
```python
'''See ParentClass documentation.

Attributes
----------

Methods
-------
'''
```

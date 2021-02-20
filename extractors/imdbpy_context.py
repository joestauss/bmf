from imdb import IMDb

class IMDbPY_Context:
    """This class is a wrapper for data extraction functions that use IMDbPY."""
    def __init__( self):
        self.ia = IMDb()

    def get_movie_id( self, search_title, search_year):
        movies = self.ia.search_movie( search_title)
        for movie in movies:
            self.ia.update( movie, info='main')
            if ('year' in movie) and (movie['year'] == search_year):
                return movie.movieID

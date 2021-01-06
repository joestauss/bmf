import os
from FilmCollection import BaseFilmCollection
from webscrapers import *

class FilmImageCollection( BaseFilmCollection):

    @property
    def images_dir(self):
        return self.__images_dir

    @images_dir.setter
    def images_dir(self, folder_name):
        base_dir  = os.getcwd()
        image_dir =  os.path.join(base_dir, folder_name)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.__images_dir = image_dir

    def get_poster_urls(self):
        self.poster_urls = {}
        for film in [m.imdb_id for m in self.movies]:
            return_vals = []
            imdb_viewer_urls = Webscraper.IMDB.Film.poster_urls( film)
            for viewer_url in imdb_viewer_urls:
                with SoupContext.Base(viewer_url) as soup:
                    return_vals.append([img['src'] for img in soup.find_all('img') if 'peek' not in img['class']][0])
            self.poster_urls[ film] = return_vals

    def download_posters(self):
        for film, urls in self.poster_urls.items():
            print( f"{film}\n---------\n{'        '.join(urls)}\n\n")
            i = 0
            for url in urls:
                i = i + 1
                target_filename = f'{film} Poster {i}.jpg'
                target_file_location = os.path.join( self.images_dir, target_filename)
                Webscraper.image(url, target_file_location)
                

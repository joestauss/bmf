from data_extraction import find_person
import imdb

result = find_person( 'Vincent Price')
#
# ia = imdb.IMDb()
# ia.get_person_filmography( result)

print( result['name id'])

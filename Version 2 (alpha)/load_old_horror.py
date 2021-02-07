from FilmSetSeed import FilmSetSeed
from pathlib     import Path

seed_string = Path( 'OldHorror.simple.FilmSetSeed.txt').read_text()

filmset = FilmSetSeed.parse_string( seed_string)

print( f"This filmset has {len( filmset)} items.")

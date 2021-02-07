from FilmSet import FilmRecord, FilmSet
from cli_utility import MenuLoop

class FilmSetBuilder( MenuLoop):

    def __init__( self, filmset=FilmSet()):
        self.filmset = filmset
        MenuLoop.__init__( self)

    @property
    def action_options( self):
        """ The action_options parameter returns a dictionary:
            <OPTION TEXT> : <OPTION ACTION>
        Option Actions should be implemented as functions in the namespace of
        this method.
        """
        def exit():
            self.exit_status = True
        def trim():
            raise NotImplementedError
        def actor_menu():
            raise NotImplementedError
        def director_menu():
            raise NotImplementedError
        def prodco_menu():
            raise NotImplementedError
        return {
            "Sub-menu: Actors" : actor_menu,
            "Remove some films from the collection." : trim,
            "Save the collection." : save,
            "Exit (does not save)" : exit

        }

if __name__ == "__main__":
    builder = FilmSetBuilder()

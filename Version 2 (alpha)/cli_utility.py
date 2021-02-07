def boxed_text( *args, BUFFER_SPACE=5 ):
    """boxed_text is a function that pretty-prints its args in a box.

    Parameters
    -----------
        args
            Each arg in args will be interpretted as a string.
            Non-string iterables will be unpacked.

        BUFFER_SPACE: int
            Number of spaces surrounding the longest text.
    """ #v1
    def unpack_strings( obj):
        """Unpack parameter into a list of strings.  Recursive function."""
        if isinstance( obj, str) or not hasattr(obj, '__iter__'):
            return [ str (obj)]
        else:
            lines = []
            for item in obj:
                lines = lines + unpack_strings( item)
            return lines

    lines = unpack_strings( args)

    MAX_LEN         = max( map( lambda s: len(s), lines))
    GAP             = '||' + ' '*(MAX_LEN + 2*BUFFER_SPACE) +'||'
    HORIZONTAL_LINE = '='* (MAX_LEN + 2*BUFFER_SPACE + 4)
    RIGHT_BORDER    = '||' + ' '*BUFFER_SPACE
    LEFT_BORDER     =  ' '*BUFFER_SPACE + '||'
    TOP_BORDER      = (HORIZONTAL_LINE, GAP)
    BOTTOM_BORDER   = (GAP, HORIZONTAL_LINE)
    return "\n".join([*TOP_BORDER, *map( lambda l: RIGHT_BORDER + l + ' '*(MAX_LEN - len(l))+ LEFT_BORDER, lines), *BOTTOM_BORDER])

def cli_selector( option_list, mode='single'):
    """Prompts the user to select from a list of options.

    Supports two modes of operation:
        -   'single'   : select a single option.
        -   'multiple' : can select several options, separated by a comma.
    """
    def select_single( option_list):
        """Prompts the user to select a single option from a list."""
        explanation_prompt = "Enter the number for your choice."
        choices_prompt = "\n".join(
            [f'{i}:{" "*(4-len(str(i)))}{option}' for i, option in enumerate( option_list)]
            + [">>> "] )
        failure_prompt = f"TRY AGAIN: Your input must be a single integer between 0 and {(len( option_list))-1}."

        print( explanation_prompt)
        while True:
            user_input = input( choices_prompt)
            try:
                return option_list[ int( user_input)]
            except:
                print( failure_prompt)

    def select_multiple( option_list):
        """Prompts the user to select one or more from among a list of options.""" #v1
        explanation_prompt = "Enter the number for your choice(s), separated by a comma."
        choices_prompt = "\n".join(
            [f'{i}:{" "*(4-len(str(i)))}{option}' for i, option in enumerate( option_list)]
            + [">>> "] )
        failure_prompt = 'There were no valid selections.  Please try again.'

        print( explanation_prompt)
        while True:
            valid_selections = []
            user_input = input( choices_prompt)
            selections = [s.strip() for s in user_input.split(",")]
            for selection in selections:
                try:
                    valid_selections.append( option_list[ int(selection)])
                except:
                    print( "\t" + f'"{selection}" was not a valid selection.')
            if valid_selections:
                return valid_selections
            print( failure_prompt)

    if mode == 'single':
        return select_single( option_list)
    elif mode == 'multiple':
        return select_multiple( option_list)
    else:
        raise ValueError( "CLI Selector can only be called in 'single' or 'many' modes.")

class MenuLoop:
    """MenuLoop is a framework for a basic, repeating CLI menu.

SubClasses should override, at minimum, the action_options property to add the
desired functionality. All implementations should leave the exit action/ option.
    """
    def __init__( self, *args, **kwargs):
        """Run the main loop.

Subclasses can load their parameters and then call MenuLoop's init to start.
        """
        self.exit_status = False
        while not self.exit_status:
            self.main_loop()

    def main_loop( self):
        """Read user's selection into a local variable, then execute it."""
        print( "Please select one of the following actions.")
        self.selection = cli_selector( list( self.action_options))
        self.action_options[ self.selection]()

    @property
    def action_options( self):
        """ The action_options parameter returns a dictionary:
            <OPTION TEXT> : <OPTION ACTION>
        Option Actions should be implemented as functions in the namespace of
        this method.
        """
        def exit():
            self.exit_status = True
        def nop():
            print( "You have selected: " + self.selection)
        return {
            "Do something."      : nop ,
            "Do something else." : nop ,
            "Exit."              : exit #exit should be in every main loop.
        }

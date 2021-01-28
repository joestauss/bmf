''' The code in the utility module was taken from the "my-python-utilities" repository.

Contains
--------
    boxed_text
    PatientThreadManager
    BatchThreadManager
    JSONAble           : v1
    Taggable           : v1
    ActionThreadsMixin : v1
    SQLTable           : v1
'''

import abc
import collections
import collections.abc
import threading
import pyparsing as pp
import json
from time import sleep

def select_from_list( input_list):
    """Prompts the user to select one or more from among a list of options.""" #v1
    explanation_prompt = "Enter the number for the selection(s) you would like, separated by a comma."
    print( explanation_prompt)

    valid_selections = []
    while not valid_selections:
        choices_prompt = "\n".join(
            [f'{i}:{" "*(4-len(str(i)))}{choice}' for i, choice in enumerate( input_list)]
            + [">>> "] )
        user_input = input( choices_prompt)

        print( f"User wants {user_input}.  This corresponds to the following selection(s):")
        selections = [s.strip() for s in user_input.split(",")]
        for selection in selections:
            try:
                valid_selections.append( input_list[ int(selection)])
                print(  "\t" + valid_selections[-1])
            except:
                print( "\t" + f"{selection} was not a valid choice.")
        if not valid_selections:
            print('There were no valid selections.  Please try again:\n' + explanation_prompt.upper())
    return valid_selections

def boxed_text( *args, BUFFER_SPACE=5 ):
    """boxed_text   is a function that pretty-prints its args in a box.

    Parameters
    -----------
        args
            Each arg in args will be interpretted as a string, unless it's a non-string iterable, in which case it will be unpacked.

        BUFFER_SPACE: int
            The number of spaces between the longest text line and the left/ right borders.
    """ #v1
    def unpack_strings( obj):
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


class PatientThreadManager:
    def __init__( self, threads):
        self.threads = threads

    def __call__(self, VERBOSE=False):
        if VERBOSE:
            n = len( self.threads)
            i = 0
            self.threads = tqdm(self.threads)
        for thread in self.threads:
            thread.start()
            sleep(0.1)
            if VERBOSE:
                i = i + 1
                self.threads.set_description( f"Starting threads {i} of {n}.")
        if VERBOSE:
            self.threads = tqdm(self.threads)
            n = len( self.threads)
            i = 0
        for thread in self.threads:
            if VERBOSE:
                i = i + 1
                self.threads.set_description( f"Waiting for thread {i} of {n}.")
            thread.join()

class BatchThreadManager:
    def __init__( self, threads):
        self.threads = threads

    def __call__( self, VERBOSE=False, BATCH_SIZE=10):
        THREAD_COUNT = 0
        thread_groups = [[]]
        if VERBOSE:
            self.threads = tqdm( self.threads)
            n = len( self.threads)
            i = 0
        for thread in self.threads:
            if VERBOSE:
                i = i + 1
                self.threads.set_description( f"Starting threads {i} of {n}.")
                thread_groups[-1].append( thread)
            THREAD_COUNT = THREAD_COUNT + 1
            if THREAD_COUNT == BATCH_SIZE:
                THREAD_COUNT = 0
                thread_groups.append([])
        if VERBOSE:
            i = 0
            n = len( thread_groups)
            thread_groups = tqdm( thread_groups)

        for thread_group in thread_groups:
            if VERBOSE:
                i = i + 1
                thread_group.set_description( f"Processing thread group {i} of {n}.")
            for thread in thread_group:
                thread.start()
            for thread in thread_group:
                thread.join()

class JSONable( collections.abc.Mapping, collections.abc.Hashable, abc.ABC):
    """A JSONable mapping can be represented in JSON or initialized from json.

    A JSONable class must be initializable with ClassName( data_dictionary).  In return it gets...
    * obj.json                    : a property thay returns the object as a JSON string
    * cls.from_json( json_string) : a method that initializes the object from the string.
    * The object is also made hashable by the result of obj.json.

    This is an abstract class and should work with any implementation of Mapping.
    """ #v1
    @abc.abstractmethod
    def __init__( self, data_dictionary, *args, **kwargs):
        """An __init__ method must be callable in this format for cls.from_json."""
        raise NotImplementedError

    @property
    def json( self):
        """Return a JSON representation of the object."""
        def replace_empty_with_none( item):
            if not item:
                return None
            return item
        return json.dumps( { k: replace_empty_with_none(v) for k, v in self.items()})

    def __hash__(self):
        """Return a hash value based on the JSON representation of the object."""
        return hash( self.json)

    @classmethod
    def from_json( cls, json_string):
        """Create an instance of the object from a JSON string."""
        return cls( json.loads(json_string))

class Taggable():
    """A Taggable object can can be given temporary tags, or be a container for Taggable objects.

    Methods for All Taggables
    -------------------------
        Taggable__init__ --- adds the "tags" attribute to the object.
        Taggable.tag( tag_string)

    Methods and Properties for Taggable Collections
    -----------------------------------------------
        Taggable.taggable_records
        Taggable.all_tags
        Taggable.tag_all( tag_string)
    """ #v
    def __init__( self, *args, tags=set(), **kwargs):
        """Add the tags attribute."""
        super().__init__(*args, **kwargs)
        self.tags = tags

    def tag( self, tag_string):
        """Add the parameter to this TaggableRecord's "tags" set."""
        self.tags.add( tag_string)

    @property
    def taggable_records( self):
        """Return any taggable objects, but raise an error if its not a collection."""
        if not isinstance( self, collections.abc.Collection):
            raise TypeError("The taggable_records property is only available for collections.")
        for record in self:
            if isinstance( record, Taggable):
                yield record

    @property
    def all_tags( self):
        """Return all the tags that are on any record."""
        all_tags = set()
        for record in self.taggable_records:
            all_tags = all_tags | record.tags
        return all_tags

    def tag_all( self, tag_string):
        """Apply a tag to each of the records."""
        for record in self.taggable_records:
            record.tag( tag_string)

class ActionThreadsMixin( Taggable):
    """ActionThreadsMixin enables thead-based actions, such as updating records.  Actions can be flagged to be batched.

    To make an ActionThreads perform an action:
    1)  Choose a tag for that action (EXAMPLE_ACTION_TAG below).
    2)  Write a method to perform the action ( example_method( seld) below).
    3)  Add the following key-value pair:
            ACTION_TAG : CORRESPONDING_METHOD_NAME
        to either the regular_action_tags or batch_action_tags dictionary.
    """ #v1
    @property
    def action_threads(self):
        """Property to return a pair of lists: regular action threads, batched action threads."""
        regular_threads  = []
        batch_threads    = []
        for tag in self.tags:
            if tag in self.regular_action_tags.keys():
                regular_threads.append( threading.Thread( target=self.regular_action_tags[ tag]( self)))
            if tag in self.batch_action_tags.keys():
                batch_threads.append( threading.Thread( target=self.batch_action_tags[ tag]( self)))
        return regular_threads, batch_threads

    def act_on_self( self, VERBOSE=False):
        """Do all available actions for this object."""
        regular_threads, batch_threads = self.action_threads
        PatientThreadManager(regular_threads)(VERBOSE=VERBOSE)
        BatchThreadManager(batch_threads)(VERBOSE=VERBOSE)

    @property
    def updatable_records( self):
        """Return any updatable objects, but raise an error if the object is not a collection."""
        if not isinstance( self, collections.abc.Collection):
            raise TypeError("The updatable_records property is only available for collections.")
        for record in self:
            if isinstance( record, ActionThreadsMixin):
                yield record

    def act_on_records( self, VERBOSE=False):
        """Do all actions on all records in this object."""
        regular_threads = []
        batch_threads   = []
        for record in self.updatable_records:
            regular, batch = record.action_threads
            regular_threads.extend( regular)
            batch_threads.extend( batch)
        PatientThreadManager(regular_threads)(VERBOSE=VERBOSE)
        BatchThreadManager(batch_threads)(VERBOSE=VERBOSE)

    #   Subclasses must implement the following:
    #
    def example_method( self):
        pass

    EXAMPLE_ACTION_TAG = hash( "ACTION TAG - Example.") # a hash to avoid accidental collision

    regular_action_tags = {
        EXAMPLE_ACTION_TAG : example_method
    }
    batch_action_tags = {
    }
    #
    #   End of subclass requirements.


class SQLTable():
    """SQLTable performs basic operations for relational data.

Attributes
----------
    rows : [dict]
        Each row is represented by a dictionary { column_name : cell_value}.  No schema is enforced.

Dunder Methods
--------------
    __init__
    __eq__
    __str__
    __repr__

Instance Methods
----------------
    add_primary_key
    contains_row
    insert_all
    normalize_column

Other Methods in the Namespace
------------------------------
    insert_from_dd
    _text_field
    text_field_s
    text_field_m
    text_field_l
    parse
    """ #v1

# Dunder Methods

    def __init__( self, rows):
        self.rows = rows

    def __eq__(self, other):
        return len(self.rows) == len(other.rows) and all( map( other.contains_row, self.rows))

    def __str__(self):
        return "\n".join( [str(row) for row in self.rows])

    def __repr__( self):
        return f"SQLTable( {repr( self.rows)})"

# Instance Methods

    def add_primary_key( self, primary_key_name):
        """ Add a primary key to the table.  The name of the primary key must be supplied, and its values are the integers 0 -- len( self.rows). """
        self.rows = [ { primary_key_name : i, **row} for i, row in enumerate( self.rows)  ]

    def contains_row( self, search_row):
        """ Return True if this table contains search_row"""
        return any( map (lambda row: len(row) == len( [c for c in row if c in search_row and row[c] == search_row[c]]), self.rows))

    def insert_all( self, target_table):
        """ Return a string containing INSERT INTO statements for every row in the table. """
        return "\n".join(  [SQLTable.insert_from_dd( target_table, row) for row in self.rows])

    def normalize_column( self, normalization_column, connecting_column):
        """ Normalize a column of this table and return the newly-created terminal table.

        Parameters
        ----------
            normalization_column : str
                The name of the column that is to normalized by.

            connecting_column : str
                The name for the newly-created common column between the tables.

        Returns
        -------
            An SQLTable containing the unqiue values in normalization_column.
            This table will be modified to reflect the normalization procedure.
        """
        # Begin by finding the unique values in the normalization column, and using it to construct the terminal table.
        unique_norm_col_values = []
        for row in self.rows:
            norm_col_value = row[ normalization_column]
            if norm_col_value not in unique_norm_col_values:
                unique_norm_col_values.append( norm_col_value)
        terminal_table = [ { connecting_column : i, normalization_column: value} for i, value in enumerate(unique_norm_col_values)]
        # Next use a lookup table to put new values in rows of the connecting table, and return the terminal table.
        lookup = { value: i for i, value in enumerate(unique_norm_col_values)}
        for row in self.rows:
            row[ connecting_column] = lookup[ row[ normalization_column]]
            row.pop( normalization_column)
        return SQLTable( terminal_table)

# Other Methods

    def insert_from_dd( table_name, dd):
        """ Create a statement to INSERT INTO table_name the row represented by the dd dictionary. """
        def transform_cell( c):
            if isinstance( c, str):
                return  f'"{c}"'
            elif c == None:
                return 'Null'
            return str( c)
        k_s = []
        v_s = []
        for k, v in dd.items():
            k_s.append( k)
            v_s.append( transform_cell( v))
        return f'INSERT INTO {table_name} ({", ".join(k_s)}) VALUES ({", ".join(v_s)});'

    def _text_field(input_string, text_length):
        """Replace quotation marks and, if len(input_string) > text_length, truncate with an ellipsis."""
        if len(input_string) > text_length:
            input_string = input_string[:text_length-3] + '...'
        return input_string.lstrip().replace( '"', "'")

    def text_field_l(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 400)

    def text_field_m(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 200)

    def text_field_s(s):
        """ See _text_field docstring."""
        return SQLTable._text_field(s, 45)

    def parse( table_string):
        """ Interprets markdown-style tables, with the first row as a header:
            | column 1 | column 2 | column 3|
            | a        | b        | c       |
            | 1        | 2        | 3       |
        Columns don't have to line up; all that matters is that each row is "|"-delimited.

        Parameters
        ----------
        table_string: string
          A string multi-line string of "|"-delimited rows.  There can be blank rows, but comments are not yet supported.

        Returns
        -------
        An SQLTable containing the same data as test_string.
        """

        INTEGER = pp.Word(pp.nums).setParseAction(lambda x: int(x[0]))
        STRING  = pp.OneOrMore(pp.Word(pp.alphanums, pp.alphanums+'_'))
        CELL    = INTEGER | STRING
        ROW  = pp.Suppress("|") + pp.delimitedList(CELL, delim='|').setParseAction(lambda x: [x]) + pp.Suppress("|")
        ROW_LINE = ROW + pp.Suppress(pp.LineEnd())
        TABLE   = ROW_LINE.setResultsName("header") + pp.OneOrMore(ROW_LINE).setResultsName("data") + pp.StringEnd()

        result = TABLE.parseString( table_string)
        header = result.header[0]
        data   = result.data
        return  SQLTable( [{header[i]: row[i] for i in range( len( header))} for row in data])

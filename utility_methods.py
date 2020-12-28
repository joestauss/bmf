import re
import requests
from bs4 import BeautifulSoup

class SoupUtil():
    def soup_from_url( url):
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def search_in_soup(soup, tag_type, search_text):
        candidates = soup.find_all(tag_type)
        for c in candidates:
            tag_text = c.text
            if re.search(search_text, tag_text):
                return c
        return None

    def filmography_filter( full_filmography):
        r_vals = []
        illegal_patterns = [
            "(Video Game)", "(TV Series)", "uncredited", "(TV Movie)",
            "(Video short)", "(Video)", "(TV Special)", "(Short)", "(scenes deleted)",
            "(TV Mini-Series)", "(Documentary)", "(Concert Feature)", "(voice)"
        ]
        for item in full_filmography:
            REGULAR_FILM = True
            for illegal_pattern in illegal_patterns:
                if re.search(illegal_pattern, item.text) :
                    REGULAR_FILM = False

            if REGULAR_FILM:
                r_vals.append( item.find('a')["href"].split('/')[2])
        return r_vals

class SQLUtil():
    class Table():
        def __init__( self, rows):
            self.rows = rows

        def InsertAllInto( self, target_table):
            return "\n".join(  [SQLUtil.insert_from_dd( target_table, row) for row in self.rows])

        def AddPrimaryKey( self, primary_key_name):
            counter = 0
            for row in self.rows:
                row[ primary_key_name] = counter
                counter = counter + 1

        def NormalizeColumn( self, normalization_column, connecting_column):
            terminal_table_data, self.rows = SQLUtil.normalize_many_to_many( (normalization_column, connecting_column), self.rows )
            return SQLUtil.Table( terminal_table_data)

    def insert_from_dd( table_name, dd):
        return_string = f'INSERT INTO {table_name}'
        k_s = []
        v_s = []
        for k, v in dd.items():
            k_s.append(k)
            if isinstance( v, str):
                v_s.append( f'"{v}"')
            elif v == None:
                v_s.append('Null')
            else:
                v_s.append(str(v))
        return f'{return_string} ({", ".join(k_s)}) VALUES ({", ".join(v_s)});'

    def normalize_many_to_many ( names, record_list):
        #   names should be a 2-tuple:
        #       (column to normalize off of,
        #        name for new intermediate column)
        #
        (norm_col, connecting_col) = names
        unique_norm_col_values = []
        for record in record_list:
            norm_col_value = record[ norm_col]
            if norm_col_value not in unique_norm_col_values:
                unique_norm_col_values.append( norm_col_value)

        terminal_table = [
            {norm_col : i, connecting_col: value}
            for i, value in enumerate(unique_norm_col_values)]
        lookup = { value: i for i, value in enumerate(unique_norm_col_values)}

        for record in record_list:
            record[ connecting_col] = lookup[ record[ norm_col]]
            record.pop( norm_col)

        return terminal_table, record_list

    def _text_field(s, l):
        TEXT_LENGTH = l
        t = s.lstrip().replace( '"', "'")
        if len(t) > TEXT_LENGTH:
            t = t[:TEXT_LENGTH-3] + '...'
        return t

    def text_field_l(s):
        return SQLUtil._text_field(s, 400)

    def text_field_m(s):
        return SQLUtil._text_field(s, 200)

    def text_field_s(s):
        return SQLUtil._text_field(s, 45)



class StringUtil():
    def dollar_amount( s):
        dollar_amounts = re.findall(r'\$[0-9,]+', s)
        for d in dollar_amounts:
            return int(d[1:].replace(',', ''))
        return None

    def minute_amount( s):
        minute_amounts = re.findall(r'[0-9]+ min', s)
        for m in minute_amounts:
            return int(m[:-4])
        return None

    def film_identity( s):
        imdb_id, title, year = None, None, None
        if re.match("tt\d+", s):
            imdb_id = s
        elif re.search("\(\d\d\d\d\)$", s):
            year, title  = int(s[-5:-1]), s[:-6].strip()
        else:
            title = s
        return imdb_id, title, year

    def section_header( input_item):
        #   input_item can be either a string or a list of strings.
        #
        if isinstance( input_item, str):
            title  = f'||     {input_item}     ||'
            gap = '||' + ' '*(len(title) - 4) + '||'
            h_line = '=' * len(title)

        if isinstance( input_item, list):
            title_strings = []
            longest_string_length = 0
            for item in input_item : #   Find the longest header string.
                title_string = f'||     {item}     ||'
                current_string_length = len(title_string)
                if current_string_length > longest_string_length:
                    longest_string_length = current_string_length
            for item in input_item: # Find the string that will actually be used.
                title_string = f'||     {item}' + ' '*(longest_string_length - len(item) - 9) + '||'
                title_strings.append(title_string)
            h_line = "=" * longest_string_length
            gap = '||' + ' '*(longest_string_length - 4) + '||'
            title = "\n".join(title_strings)

        try:
            print_objects = [ h_line, gap, title, gap, h_line]
            return "\n".join(print_objects)
        except:
            return "||    ERROR PRINTING HEADER"

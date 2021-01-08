import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class SoupUtil:
    def search_in_soup(soup, tag_type, search_text):
        candidates = soup.find_all(tag_type)
        for c in candidates:
            tag_text = c.text
            if re.search(search_text, tag_text):
                return c
        return None

class ExportUtil:
    class Table():
        def __init__( self, rows):
            self.rows = rows

        def __eq__(self, other):
            for row in other.rows:
                if not self.contains_row(row):
                    return False
            return len(self.rows) == len(other.rows)

        def contains_row( self, search_row):
            for row in self.rows:
                shared_cols = [ col for col in row if col in search_row and row[col] == search_row[col]]
                if len(shared_cols) == len(row):
                    return True
            return False

        def InsertAllInto( self, target_table):
            return "\n".join(  [ExportUtil.insert_from_dd( target_table, row) for row in self.rows])

        def __str__(self):
            return "\n".join( [str(row) for row in self.rows])

        def AddPrimaryKey( self, primary_key_name):
            counter = 0
            for row in self.rows:
                row[ primary_key_name] = counter
                counter = counter + 1

        def NormalizeColumn( self, normalization_column, connecting_column):
            unique_norm_col_values = []
            for row in self.rows:
                norm_col_value = row[ normalization_column]
                if norm_col_value not in unique_norm_col_values:
                    unique_norm_col_values.append( norm_col_value)

            terminal_table = [ { connecting_column : i, normalization_column: value} for i, value in enumerate(unique_norm_col_values)]
            lookup = { value: i for i, value in enumerate(unique_norm_col_values)}

            for row in self.rows:
                row[ connecting_column] = lookup[ row[ normalization_column]]
                row.pop( normalization_column)

            return ExportUtil.Table( terminal_table)

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

    def _text_field(s, l):
        TEXT_LENGTH = l
        t = s.lstrip().replace( '"', "'")
        if len(t) > TEXT_LENGTH:
            t = t[:TEXT_LENGTH-3] + '...'
        return t

    def text_field_l(s):
        return ExportUtil._text_field(s, 400)

    def text_field_m(s):
        return ExportUtil._text_field(s, 200)

    def text_field_s(s):
        return ExportUtil._text_field(s, 45)

class PrintUtil:
    def section_header( input_item):
        #   input_item can be either a string or a list of strings.
        #
        if isinstance( input_item, str):
            title  = f'||     {input_item}     ||'
            gap    =  '||' + ' '*(len(title) - 4) + '||'
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

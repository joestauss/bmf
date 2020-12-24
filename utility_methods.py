import re
import requests
from bs4 import BeautifulSoup

class SoupUtil():
    def soup_from_url( url):
        r       =   requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def search_in_soup(soup, tag_type, search_text):
        candidates = soup.find_all(tag_type)

        for c in candidates:
            tag_text = c.text
            if re.search(search_text, tag_text):
                return c
        return None

class SQLUtil():
    def add_primary_key( primary_key_name, records):
        counter = 0
        for record in records:
            record[ primary_key_name] = counter
            counter = counter + 1
        return records

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

    def normalize_many_to_many ( names, data_dictionary):
        #   names should be a 2-tuple:
        #       (column to normalize off of,
        #        name for newly normalized column)
        #
        (norm_col, connecting_col) = names
        unique_norm_col_values = []
        for record in data_dictionary:
            norm_col_value = record[ norm_col]
            if norm_col_value not in unique_norm_col_values:
                unique_norm_col_values.append( norm_col_value)

        terminal_table = [
            {norm_col : i, connecting_col: value}
            for i, value in enumerate(unique_norm_col_values)]
        lookup = { value: i for i, value in enumerate(unique_norm_col_values)}

        for record in data_dictionary:
            record[ connecting_col] = lookup[ record[ norm_col]]
            record.pop( norm_col)

        return terminal_table, data_dictionary

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
        if re.match("tt\d+", s):
            imdb_id = s
            title   = None
            year    = None
        else:
            imdb_id = None
            title   = s
            year    = None
        return imdb_id, title, year


    def section_header( s):
        fancy_title  = f'||     {s}     ||'
        fancy_break = '||' + ' '*(len(fancy_title) - 4) + '||'
        fancy_line = '=' * len(fancy_title)
        return '\n'.join([
            fancy_line,
            fancy_break,
            fancy_title,
            fancy_break,
            fancy_line
        ])

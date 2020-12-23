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

    def normalize_many_to_many(
        unnormalized_data,
            # The data will be normalized off of the final column.
            #
        terminal_table_cols,
        intermediate_table_cols
    ):
        unique_values = []
        for record in unnormalized_data:
            final_val = record[-1]
            if final_val not in unique_values:
                unique_values.append(final_val)

        terminal_table = []
        lookup_val = {}
        for i in range( len(unique_values)):
            val = unique_values[i]
            terminal_table.append({
                terminal_table_cols[0]: i,
                terminal_table_cols[1]: val
            })
            lookup_val[val] = i

        intermediate_table = []
        for record in unnormalized_data:
            dd = {}
            n = len(record)
            for i in range(n - 1):
                dd[intermediate_table_cols[i]] = record[i]
            dd[intermediate_table_cols[n-1]] = lookup_val[record[n-1]]
            intermediate_table.append(dd)
        return terminal_table, intermediate_table

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

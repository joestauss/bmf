def search_in_soup(soup, tag_type, search_text):
    candidates = soup.find_all(tag_type)
    for c in candidates:
        tag_text = c.text
        if re.search(search_text, tag_text):
            return c
    return None

from itertools import groupby
import re

class Entry:
    def __init__(self,lines):
        self.book = clean_line(lines[0])
        m = re.search(r"- Ihre Markierung bei Position (.*)-(.*) | Hinzugefügt am (.*)",lines[1])
        self.position = (m.group(1), m.group(2))
        self.timestamp = m.group(3)
        self.text = clean_line("".join(lines[2:]))

class Book:
    def __init__(self,title,entries):
        self.title = title
        self.entries = entries


def load_kindle(file_path):
    with open(file_path, 'r') as clippings:
        return load_book(load_entries(clippings))

def load_entries(clippings):
    entries = []
    current_entry = None
    return [Entry(list(group)) for key, group in groupby(clippings, lambda line: line == '==========\n') if not key]

def clean_line(line):
    return line.replace('\ufeff','').strip()

def load_book(entries):
    return [Book(title,entries) for title, entries in groupby(entries,lambda entry: entry.book)]

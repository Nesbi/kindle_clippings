from itertools import groupby
import re

class Entry:
    def __init__(self,entry_id,lines):
        self.id = entry_id
        self.book = clean_line(lines[0])
        m = re.search(r"- Ihre Markierung bei Position (.*)-(.*) \| Hinzugefügt am (.*)",lines[1])
        self.position = (m.group(1), m.group(2))
        self.timestamp = m.group(3)
        self.text = clean_line("".join(lines[2:]))


class Book:
    def __init__(self,title,entries):
        self.title = title
        self.entries = entries

    def get_text(self):
        return "\n\n".join(e.text for e in self.entries)


def load_kindle(file_path):
    delimiter = '==========\n'

    with open(file_path, 'r') as clippings:
        line_groups = enumerate((list(group) 
                for key, group in groupby(clippings, lambda line: line == delimiter) if not key))
        entries = [Entry(entry_id, entry_lines) for entry_id, entry_lines in line_groups]

        return [Book(title,clean_entries(list(book_entries))) 
                for title, book_entries in groupby(entries,lambda entry: entry.book)]


def clean_entries(entries):
    filtered = [e for e in entries if 
            len([p for p in entries if p.id != e.id and e.text in p.text]) == 0]

    return sorted(filtered, key=lambda e: [e.position,len(e.text)])


def is_subentry(entry_id, entry, entries):
    parents = [p for p in entries if p.id != entry.id and entry.text in p.text]
    return len(parents) > 0


def clean_line(line):
    return line.replace('\ufeff','').strip()


def save_book(book,file_path):
    with open(file_path, 'w+') as notes:
        notes.write(book.get_text())



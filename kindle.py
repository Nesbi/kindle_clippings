from itertools import groupby
import re
import datetime

class Entry:
    def __init__(self,entry_id,book,position,timestamp,text):
        self.id = entry_id
        self.book = book
        self.position = position
        self.timestamp = timestamp
        self.text = text


class Book:
    def __init__(self,title,entries):
        self.title = title
        self.entries = sorted(entries, key=lambda e: [e.position,len(e.text)])

    def get_text(self):
        return "\n\n".join(e.text for e in self.clean_entries())

    def clean_entries(self):
        return [e for e in self.entries if len([p for p in self.entries if p.id != e.id and e.text in p.text]) == 0]

    def export(self,file_path):
        with open(file_path, 'w+') as notes:
            notes.write(self.title+'\n')
            notes.write("=" * len(self.title) + "\n\n")

            notes.write(self.get_text())


class Kindle:
    def load(file_path):
        delimiter = '==========\n'

        with open(file_path, 'r') as clippings:
            line_groups = enumerate((list(group) 
                    for key, group in groupby(clippings, lambda line: line == delimiter) if not key))
            entries = [Kindle.entry_from_lines(entry_id, entry_lines) for entry_id, entry_lines in line_groups]

            return [Book(title,list(book_entries)) 
                    for title, book_entries in groupby(entries,lambda entry: entry.book)]


    def entry_from_lines(entry_id, lines):
        # TODO use locale instead of hard coded german
        m = re.search(r"- Ihre Markierung bei Position (.*)-(.*) \| Hinzugefügt am (.*)",lines[1])
        months = {
                "Januar":1,
                "Februar":2,
                "März":3,
                "April":4,
                "Mai":5,
                "Juni":6,
                "Juli":7,
                "August":8,
                "September":9,
                "Oktober":10,
                "November":11,
                "Dezember":12
               } 

        d = re.search(r".*, (.*)\. (.*) (.*) (.*):(.*):(.*)",m.group(3))

        date = datetime.datetime(
                int(d.group(3)),
                months[d.group(2)],
                int(d.group(1)),
                int(d.group(4)),
                int(d.group(5)),
                int(d.group(6)))

        return Entry(entry_id, Kindle.clean_line(lines[0]), (m.group(1), m.group(2)), date, Kindle.clean_line("".join(lines[2:])))


    def clean_line(line):
        return line.replace('\ufeff','').strip()



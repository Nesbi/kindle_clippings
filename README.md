Kindle Clippings
================

This is a simple parser for (german) kindle clippings files.
The clipping notes will be loaded in multiple `Entry` objects, that provide a simple way to access the notes text, timestamp and more.
Every `Entry` is bundled within a `Book`.
Entries and books can easily be edited, saved and exported.

Requirements
------------
- python3 

Usage
-----
### import
```python3
from kindle import *
```

### Load clippings file
Load all clipping notes as entries bundled in books:
```python3
books = Kindle.load('My Clippings.txt') 
```

### Save notes to file
Save all clipping notes of a specific book into a textfile:
```python3
books[0].export(books[0].title+".txt") 
```

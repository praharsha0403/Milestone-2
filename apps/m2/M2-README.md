# Milestone-2 README

## Source Code References


| API Function      | File                 | Line | Description                        |
|------------------|----------------------|------|------------------------------------|
| BeautifulSoup     | bs4/__init__.py       | 133  | Main parser class                  |
| SoupStrainer      | bs4/soupstrainer.py   | 15   | Selective parsing class            |
| find_all()        | bs4/element.py        | 2715 | Find multiple tags                 |
| find()            | bs4/element.py        | 2684 | Find single tag                    |
| prettify()        | bs4/element.py        | 2601 | Format HTML structure              |
| get()             | bs4/element.py        | 2160 | Get attribute from tag             |
| string (property) | bs4/element.py        | 1866 | Access tag string content          |
| text (property)   | bs4/element.py        | 1882 | Text content of tag                |

---

## Custom API – `SoupReplacer`

Added a new API called `SoupReplacer` to replace tags **during parsing**, rather than after.

### Usage

```python
from bs4.soupreplacer import SoupReplacer
from bs4 import BeautifulSoup

replacer = SoupReplacer("b", "blockquote")
soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)
print(soup.prettify())
```

### Constructor

```python
SoupReplacer(og_tag, alt_tag)
```

### Integration

Modified the constructor of `BeautifulSoup` in `bs4/__init__.py` to accept a `replacer` argument and injected tag-replacement logic in the parsing phase.

---

## Files Added/Modified

- `bs4/soupreplacer.py`: Defines SoupReplacer
- `bs4/__init__.py`: Modified to accept `replacer`
- `bs4/tests/test_replacer.py`: Unit tests
- `apps/m2/task6.py`: Application using `SoupReplacer`
- `apps/m2/task2.py`, `task3.py`, `task4.py`: Use `SoupStrainer`


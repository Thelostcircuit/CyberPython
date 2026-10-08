# 34 // SOUP KITCHEN

```
[CHEESE SHOP] purchase: beautifulsoup4 ── target: Ouroboros staff directory (27 pages of tag soup)
```

**Package:** [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), imported as `bs4`: parse and search HTML.

The Ouroboros staff directory is an internal web page first built in 2061 and patched by
hand ever since. It's unclosed tags, tables inside tables, inline styles, and a script that
does nothing but show a snowflake in December. The name of whoever holds physical access to
wing C is in there somewhere.

> **WENSLEYDALE:** Beautiful Soup doesn't care how ugly the page is, sir. It builds a tidy
> tree out of anything, and then you ask it questions: "all the rows in this table", "the
> link that says *Next*", "everything with class `engineer`". Like asking a librarian instead of
> reading every book.
>
> **MONTY:** `html.parser` from ch 27 gave us events. This gives us a *tree* we can search.

---

## ▓ TECH BRIEFING

### Making soup

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")   # the stdlib parser; "lxml" and "html5lib" are optional extras
soup.title.string                             # the <title> text
soup.prettify()                               # re-indented HTML
```

### Finding things

```python
soup.find("table")                            # the first match, or None
soup.find_all("a")                            # all matches (a list)
soup.find_all("td", class_="clearance")       # class_ because `class` is a Python keyword
soup.find("a", attrs={"rel": "next"})
soup.find_all(["h1", "h2"])                   # any of these tags
soup.find("td", string="I. Vale")             # by exact text
soup.find_all("a", href=True)                 # only anchors that HAVE an href

# CSS selectors
soup.select("table#staff tr.engineer td")     # a list
soup.select_one("div.card > a[href^='/staff/']")
```

### Tags

```python
tag = soup.find("a")
tag.name, tag.attrs, tag["href"], tag.get("title", "none")
tag.get_text(strip=True)                      # all the text inside: each piece trimmed, then glued together
tag.get_text(" ", strip=True)                 # ...glued with spaces instead (usually what you want)
tag.string                                    # the text, if the tag holds exactly one string
tag.parent, tag.children, tag.find_next_sibling("td"), tag.find_parent("tr")
tag.decompose()                               # remove it from the tree completely
soup.get_text(" ", strip=True)                # the whole page's visible text, space-joined
```

`class` is a multi-valued attribute, so `tag["class"]` is a **list** (`["row", "engineer"]`).

### Being a good citizen

Real scraping means fetching pages (requests, ch 33), respecting `robots.txt` (ch 26),
rate-limiting yourself, and handling missing elements (`find` returns `None`, and
`None.get_text()` raises `AttributeError`). And scrape only what you're allowed to.

---

## ▓ THE JOB

The tests feed you HTML strings (no network). In `job.py`, using **Beautiful Soup**:

1. **`page_title(html)`**: the stripped `<title>` text, or `None`.
2. **`staff_rows(html)`**: the `#staff` table's rows as dicts keyed by the header cells.
3. **`absolute_links(html, base)`**: every `href`, resolved against `base`, in order.
4. **`texts_with_class(html, cls)`**: the space-joined text of every element with that class.
5. **`select_texts(html, selector)`**: the texts matched by a CSS selector.
6. **`clearance_of(html, name)`**: find the cell with exactly that name, and return the text of its row's `.clearance` cell.
7. **`visible_text(html)`**: the page text without `<script>`/`<style>` contents, space-joined.
8. **`meta_tags(html)`**: `{name: content}` for every `<meta name=...>`.
9. **`next_page(html)`**: the `href` of the link with `rel="next"`, or `None`.

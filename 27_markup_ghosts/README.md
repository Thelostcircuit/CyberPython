# 27 // MARKUP GHOSTS

```
[PYTHIA-9] input: receipt_7.pdf → embedded rack_manifest.xml ── schema: OURO-MANIFEST/2 ── also: portal HTML
```

**Modules:** `html`, `html.parser`, `xml.etree.ElementTree`, `xml.dom.minidom`, `xml.sax`, `pyexpat`

The receipt's embedded manifest is XML, the kind that's been passed through six generations
of corporate systems, each adding its own attributes and never removing any. And the Orders
Portal's pages are old-fashioned HTML, full of `&nbsp;` and links you'll need to follow.

> **MONTY:** Markup is text with structure: elements inside elements, each with attributes and
> content. Python ships a whole family of parsers. There are tree builders that load everything
> (`ElementTree`, `minidom`), streaming parsers that fire events as they read (`sax`, `pulldom`,
> `expat`), and a forgiving HTML tokenizer. Choose the tree when the document is small, and a
> stream when it's huge.
>
> And one warning: never feed untrusted XML to a parser without thinking about it. XML has
> features that can be turned against you.

---

## ▓ TECH BRIEFING

### `html`: escaping

```python
import html
html.escape('<a href="x">Iris & co</a>')   # '&lt;a href=&quot;x&quot;&gt;Iris &amp; co&lt;/a&gt;'
html.unescape("caf&eacute; &lt;3 &#128013;")  # 'café <3 🐍'

from html.entities import name2codepoint, html5
chr(name2codepoint["eacute"])                 # 'é'
```

Escape anything you insert into HTML. (That's what ch 10's t-string renderer did by hand.)

### `html.parser`: an event-driven HTML tokenizer

```python
from html.parser import HTMLParser
class Links(HTMLParser):
    def __init__(self):
        super().__init__()                    # convert_charrefs=True by default: &amp; → &
        self.links = []
    def handle_starttag(self, tag, attrs):    # attrs is a list of (name, value) pairs
        if tag == "a":
            self.links.append(dict(attrs).get("href"))
    def handle_endtag(self, tag): ...
    def handle_data(self, data): ...          # the text between tags

p = Links(); p.feed(page); p.close(); p.links
```

It's forgiving about broken HTML, but it's low-level. BeautifulSoup (ch 34) sits on top of
parsers like this one.

### `xml.etree.ElementTree`: the everyday XML API

```python
import xml.etree.ElementTree as ET
root = ET.fromstring(xml_text)                # or ET.parse("file.xml").getroot()
root.tag, root.attrib, root.text
root.get("version"), root.get("missing", "default")
for rack in root.findall("rack"): ...         # direct children
root.findall(".//subject")                    # anywhere below
root.find("rack[@id='C-17']")                 # a limited XPath subset: [@attr='v'], [tag], [1]
root.iter("subject")                          # every matching element, depth-first
root.findtext("title", default="")

new = ET.Element("manifest", version="2")
rack = ET.SubElement(new, "rack", id="C-17")
ET.indent(new)                                # pretty-print in place
ET.tostring(new, encoding="unicode")          # a str (the default gives bytes)
for event, elem in ET.iterparse(path, events=("end",)): ...; elem.clear()   # stream big files
```

### `xml.dom.minidom` and `xml.dom.pulldom`

The W3C DOM API, which is familiar from JavaScript:

```python
from xml.dom import minidom
doc = minidom.parseString(xml_text)
doc.getElementsByTagName("subject")[0].getAttribute("id")
doc.toprettyxml(indent="  ")

from xml.dom import pulldom                   # stream of events, expand only what you need
for event, node in pulldom.parseString(xml_text):
    if event == pulldom.START_ELEMENT and node.tagName == "subject":
        node.getAttribute("id")
```

### `xml.sax` and `xml.parsers.expat`

```python
import xml.sax
class Counter(xml.sax.ContentHandler):
    def startElement(self, name, attrs): ...    # attrs.get("id")
    def characters(self, content): ...
    def endElement(self, name): ...
xml.sax.parseString(xml_bytes, Counter())

from xml.parsers import expat                   # the fast C parser under all of the above
p = expat.ParserCreate()                        # (the C module itself is `pyexpat`)
p.StartElementHandler = lambda name, attrs: ...
p.Parse(xml_text, True)
```

### Security

XML supports entity expansion and external entities. A malicious document can expand to
gigabytes ("billion laughs"), or try to pull in local files. Python's expat has had protections
added over time, and the docs have a table of which parser is vulnerable to what. For
documents from strangers, the third-party `defusedxml` package gives hardened drop-in
replacements.

---

## ▓ THE JOB

In `job.py`:

1. **`escape_for_page(text)`** / **`unescape_page(text)`**: `html`.
2. **`entity(name)`**: the character for an HTML entity name.
3. **`PortalScraper`** and **`scrape(page)`**: collect the page `<title>` text and every `<a href>`.
4. **`manifest_racks(xml)`**: `{rack_id: [subject ids]}` via `ElementTree`.
5. **`rack_of(xml, subject_id)`**: which rack holds a subject (use an XPath predicate).
6. **`build_manifest(racks, version)`**: build the XML with `ElementTree`.
7. **`pretty(xml)`**: `minidom` pretty-printing.
8. **`sax_count(xml, tag)`**: count elements with a SAX handler.
9. **`pull_subjects(xml)`**: subject ids via `pulldom`.
10. **`expat_tags(xml)`**: every start-tag name, in order, via `expat`.

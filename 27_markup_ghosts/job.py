"""27 // MARKUP GHOSTS: HTML and XML, trees and streams."""

import html
import xml.etree.ElementTree as ET
import xml.sax
from html.entities import name2codepoint
from html.parser import HTMLParser
from xml.dom import minidom, pulldom
from xml.parsers import expat

# A manifest looks like:
# <manifest version="2">
#   <rack id="C-17"><subject id="OS-ENG-4471"/><subject id="OS-OPS-1111"/></rack>
#   <rack id="A-02"><subject id="OS-FIN-0042"/></rack>
# </manifest>


def escape_for_page(text: str) -> str:
    """html.escape (quotes included)."""
    raise NotImplementedError("TODO")


def unescape_page(text: str) -> str:
    raise NotImplementedError("TODO")


def entity(name: str) -> str:
    """entity("eacute") -> "é", via html.entities.name2codepoint. Unknown -> KeyError."""
    raise NotImplementedError("TODO")


class PortalScraper(HTMLParser):
    """Collects .title (the text inside <title>, stripped) and .links (the href of every <a>
    that has one, in order)."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links: list[str] = []
        raise NotImplementedError("TODO")

    pass  # TODO: handle_starttag, handle_endtag, handle_data


def scrape(page: str) -> tuple[str, list[str]]:
    """Feed the page to a PortalScraper; return (title, links)."""
    raise NotImplementedError("TODO")


def manifest_racks(xml_text: str) -> dict[str, list[str]]:
    """{rack id: [subject ids in document order]} using ElementTree."""
    raise NotImplementedError("TODO")


def rack_of(xml_text: str, subject_id: str) -> str | None:
    """The id of the rack containing that subject, or None. Use
    rack.find(f"subject[@id='{subject_id}']") on each rack."""
    raise NotImplementedError("TODO")


def build_manifest(racks: dict[str, list[str]], version: int = 2) -> str:
    """Build <manifest version="..."> with a <rack id> per key and an empty <subject id> per
    subject. Return ET.tostring(root, encoding="unicode") (no indentation)."""
    raise NotImplementedError("TODO")


def pretty(xml_text: str) -> str:
    """minidom.parseString(xml_text).toprettyxml(indent="  ")"""
    raise NotImplementedError("TODO")


def sax_count(xml_text: str, tag: str) -> int:
    """Count elements named `tag` with an xml.sax ContentHandler."""
    raise NotImplementedError("TODO")


def pull_subjects(xml_text: str) -> list[str]:
    """Subject ids in document order, streaming with xml.dom.pulldom."""
    raise NotImplementedError("TODO")


def expat_tags(xml_text: str) -> list[str]:
    """Every start-tag name in order, using xml.parsers.expat.ParserCreate()."""
    raise NotImplementedError("TODO")

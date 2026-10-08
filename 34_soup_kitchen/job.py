"""34 // SOUP KITCHEN: pick the staff directory apart with Beautiful Soup."""

from urllib.parse import urljoin

from bs4 import BeautifulSoup


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def page_title(html: str) -> str | None:
    """The <title> text, stripped, or None if there's no title."""
    raise NotImplementedError("TODO")


def staff_rows(html: str) -> list[dict[str, str]]:
    """The table with id="staff": its first row holds <th> header cells; every later row
    becomes {header text: cell text}, all stripped."""
    raise NotImplementedError("TODO")


def absolute_links(html: str, base: str) -> list[str]:
    """urljoin(base, href) for every <a> that has an href, in document order."""
    raise NotImplementedError("TODO")


def texts_with_class(html: str, cls: str) -> list[str]:
    """The text of every element (any tag) whose class list contains cls, with its pieces
    joined by single spaces: tag.get_text(" ", strip=True)."""
    raise NotImplementedError("TODO")


def select_texts(html: str, selector: str) -> list[str]:
    """get_text(" ", strip=True) of every element matching the CSS selector."""
    raise NotImplementedError("TODO")


def clearance_of(html: str, name: str) -> str | None:
    """Find the <td> whose text is exactly `name`, go to its <tr>, and return the stripped text
    of the <td class="clearance"> in that row. None if the name isn't there."""
    raise NotImplementedError("TODO")


def visible_text(html: str) -> str:
    """Remove every <script> and <style> element (decompose), then
    soup.get_text(" ", strip=True)."""
    raise NotImplementedError("TODO")


def meta_tags(html: str) -> dict[str, str]:
    """{name: content} for every <meta> that has a name attribute."""
    raise NotImplementedError("TODO")


def next_page(html: str) -> str | None:
    """The href of the <a> whose rel includes "next" (rel is multi-valued, like class)."""
    raise NotImplementedError("TODO")

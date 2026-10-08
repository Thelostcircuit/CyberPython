# HINTS // 27 MARKUP GHOSTS

## PortalScraper
<details><summary>Hint 1</summary>

Keep a flag, `self._in_title`. Set it in `handle_starttag` when `tag == "title"`, clear it in
`handle_endtag`, and in `handle_data` add text to `self.title` while it's set.
</details>
<details><summary>Hint 2</summary>

`HTMLParser` lower-cases tag and attribute names for you, so `<A HREF=...>` arrives as `"a"`
with `("href", ...)`. `dict(attrs).get("href")` is `None` for an anchor without one. Strip the
title when it ends.
</details>

## manifest_racks
<details><summary>Hint</summary>

`root = ET.fromstring(xml_text)`, then a dict comprehension over `root.findall("rack")` with
`rack.get("id")` and `[s.get("id") for s in rack.findall("subject")]`.
</details>

## rack_of
<details><summary>Hint</summary>

For each rack in `root.iter("rack")`: `rack.find(f"subject[@id='{subject_id}']") is not None`.
</details>

## build_manifest
<details><summary>Hint</summary>

`ET.Element("manifest", version=str(version))` and `ET.SubElement(parent, "rack", id=...)`.
Attribute values must be strings.
</details>

## sax_count
<details><summary>Hint</summary>

Define a `ContentHandler` subclass *inside* the function, so it can see `tag`, and count in
`startElement`. `xml.sax.parseString` wants bytes, so encode first.
</details>

## pull_subjects / expat_tags
<details><summary>Hint</summary>

`for event, node in pulldom.parseString(xml_text): if event == pulldom.START_ELEMENT and
node.tagName == "subject": ...`. For expat: `p = expat.ParserCreate()`,
`p.StartElementHandler = lambda name, attrs: tags.append(name)`, then `p.Parse(xml_text, True)`.
</details>

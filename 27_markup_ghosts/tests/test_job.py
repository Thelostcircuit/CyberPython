import unittest
import xml.etree.ElementTree as ET

import job

MANIFEST = """<manifest version="2">
  <rack id="C-17"><subject id="OS-ENG-4471"/><subject id="OS-OPS-1111"/></rack>
  <rack id="A-02"><subject id="OS-FIN-0042"/></rack>
  <rack id="Z-99"/>
</manifest>"""

PAGE = """<!doctype html><html><head><title>  Orders &amp; Releases </title></head>
<body><p>Hi&nbsp;engineer</p><a href="/orders">orders</a> <a name="top">x</a>
<A HREF="/logout">bye</A></body></html>"""


class Html(unittest.TestCase):
    def test_escape(self):
        s = '<a href="x">Iris & co</a>'
        self.assertEqual(job.escape_for_page(s),
                         "&lt;a href=&quot;x&quot;&gt;Iris &amp; co&lt;/a&gt;")
        self.assertEqual(job.unescape_page(job.escape_for_page(s)), s)
        self.assertEqual(job.unescape_page("caf&eacute; &#128013;"), "café 🐍")

    def test_entity(self):
        self.assertEqual(job.entity("eacute"), "é")
        self.assertEqual(job.entity("amp"), "&")
        with self.assertRaises(KeyError):
            job.entity("nonsense")

    def test_scrape(self):
        self.assertEqual(job.scrape(PAGE), ("Orders & Releases", ["/orders", "/logout"]))


class Xml(unittest.TestCase):
    def test_manifest_racks(self):
        self.assertEqual(job.manifest_racks(MANIFEST), {
            "C-17": ["OS-ENG-4471", "OS-OPS-1111"], "A-02": ["OS-FIN-0042"], "Z-99": []})

    def test_rack_of(self):
        self.assertEqual(job.rack_of(MANIFEST, "OS-FIN-0042"), "A-02")
        self.assertEqual(job.rack_of(MANIFEST, "OS-ENG-4471"), "C-17")
        self.assertIsNone(job.rack_of(MANIFEST, "NOBODY"))

    def test_build_manifest(self):
        out = job.build_manifest({"C-17": ["OS-ENG-4471"], "B-01": []}, version=3)
        self.assertEqual(out, '<manifest version="3"><rack id="C-17"><subject id="OS-ENG-4471" />'
                              '</rack><rack id="B-01" /></manifest>')
        racks = {"C-17": ["a", "b"], "A-02": ["c"]}
        self.assertEqual(job.manifest_racks(job.build_manifest(racks)), racks)

    def test_pretty(self):
        out = job.pretty('<m><r id="1"><s/></r></m>')
        self.assertEqual(out.splitlines()[1:4], ["<m>", '  <r id="1">', "    <s/>"])

    def test_streams(self):
        self.assertEqual(job.sax_count(MANIFEST, "subject"), 3)
        self.assertEqual(job.sax_count(MANIFEST, "rack"), 3)
        self.assertEqual(job.pull_subjects(MANIFEST), ["OS-ENG-4471", "OS-OPS-1111", "OS-FIN-0042"])
        self.assertEqual(job.expat_tags("<a><b/><c><b/></c></a>"), ["a", "b", "c", "b"])

    def test_bad_xml(self):
        with self.assertRaises(ET.ParseError):
            job.manifest_racks("<manifest><rack></manifest>")


if __name__ == "__main__":
    unittest.main()

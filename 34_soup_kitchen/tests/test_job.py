import unittest

import job

DIRECTORY = """<html><head>
<title>
  Ouroboros Staff Directory
</title>
<meta name="generator" content="StaffDir 2061">
<meta name="robots" content="noindex">
<meta charset="utf-8">
<style>.x { color: red }</style>
<script>showSnowflake();</script>
</head><body>
<h1 class="banner">Staff <b>Directory</b></h1>
<table id="nav"><tr><td>ignore me</td></tr></table>
<table id="staff">
 <tr><th>Name</th><th>Wing</th><th>Clearance</th></tr>
 <tr class="row engineer"><td> I. Vale </td><td>C</td><td class="clearance">IV</td></tr>
 <tr class="row"><td>H. Voss</td><td>*</td><td class="clearance"> VII </td></tr>
 <tr class="row engineer"><td>K. Lin</td><td>C</td><td class="clearance">II</td>
</table>
<p class="note">Updated <span class="note">weekly</span></p>
<a href="/staff/vale">Vale</a> <a name="anchor">no href</a>
<a href="https://ouro.corp/help">Help</a>
<a href="?page=2" rel="next nofollow">Next</a>
</body></html>"""


class SoupKitchen(unittest.TestCase):
    def test_title(self):
        self.assertEqual(job.page_title(DIRECTORY), "Ouroboros Staff Directory")
        self.assertIsNone(job.page_title("<p>no title</p>"))

    def test_staff_rows(self):
        self.assertEqual(job.staff_rows(DIRECTORY), [
            {"Name": "I. Vale", "Wing": "C", "Clearance": "IV"},
            {"Name": "H. Voss", "Wing": "*", "Clearance": "VII"},
            {"Name": "K. Lin", "Wing": "C", "Clearance": "II"}])

    def test_links(self):
        self.assertEqual(job.absolute_links(DIRECTORY, "http://portal.ouro/dir/index.html"), [
            "http://portal.ouro/staff/vale", "https://ouro.corp/help",
            "http://portal.ouro/dir/index.html?page=2"])

    def test_class_and_select(self):
        self.assertEqual(job.texts_with_class(DIRECTORY, "note"), ["Updated weekly", "weekly"])
        self.assertEqual(job.texts_with_class(DIRECTORY, "engineer"),
                         ["I. Vale C IV", "K. Lin C II"])
        self.assertEqual(job.select_texts(DIRECTORY, "tr.engineer td:first-child"), ["I. Vale", "K. Lin"])
        self.assertEqual(job.select_texts(DIRECTORY, "h1.banner b"), ["Directory"])

    def test_clearance(self):
        self.assertEqual(job.clearance_of(DIRECTORY, "H. Voss"), "VII")
        self.assertEqual(job.clearance_of(DIRECTORY, "K. Lin"), "II")
        self.assertIsNone(job.clearance_of(DIRECTORY, "Nobody"))

    def test_visible_text(self):
        text = job.visible_text(DIRECTORY)
        self.assertNotIn("showSnowflake", text)
        self.assertNotIn("color", text)
        self.assertTrue(text.startswith("Ouroboros Staff Directory Staff Directory"))

    def test_meta(self):
        self.assertEqual(job.meta_tags(DIRECTORY), {"generator": "StaffDir 2061", "robots": "noindex"})

    def test_next(self):
        self.assertEqual(job.next_page(DIRECTORY), "?page=2")
        self.assertIsNone(job.next_page("<a href='x'>x</a>"))


if __name__ == "__main__":
    unittest.main()

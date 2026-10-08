import unittest

from job import (ascii_fold, clean_block, closest_command, edits, fill_blanks, pretty,
                 safe_markup, short_repr, similarity, unrot, wrap_quote)


class TextForge(unittest.TestCase):
    def test_fill_blanks(self):
        self.assertEqual(fill_blanks("Meet $who at ${place}.", who="Adder"),
                         "Meet Adder at ${place}.")
        self.assertEqual(fill_blanks("$a$b", a="1", b="2"), "12")

    def test_safe_markup(self):
        name = "<b>Iris & co</b>"
        self.assertEqual(safe_markup(t"<p>{name}</p>"), "<p>&lt;b&gt;Iris &amp; co&lt;/b&gt;</p>")
        quote = "it's"
        self.assertEqual(safe_markup(t"<i>{quote!r}</i>"), '<i>&quot;it&#x27;s&quot;</i>')
        n = 3.14159
        self.assertEqual(safe_markup(t"<{n:.2f}>"), "<3.14>")
        self.assertEqual(safe_markup(t"plain"), "plain")

    def test_wrap_quote(self):
        text = "the parrot is not dead it is resting"
        self.assertEqual(wrap_quote(text, 14),
                         "> the parrot is\n> not dead it is\n> resting")

    def test_clean_block(self):
        block = "\n\n    def f():\n        return 1\n\n"
        self.assertEqual(clean_block(block), "def f():\n    return 1")

    def test_closest_command(self):
        cmds = ["scan", "lock", "jack-in", "replay"]
        self.assertEqual(closest_command("scna", cmds), "scan")
        self.assertEqual(closest_command("jackin", cmds), "jack-in")
        self.assertIsNone(closest_command("zzzzzz", cmds))

    def test_edits(self):
        old = "Ouroboros serves the city.\nArchival is voluntary.\nWe care."
        new = "Ouroboros serves the city.\nArchival is mandatory.\nWe care.\nWe watch."
        self.assertEqual(edits(old, new), ["-Archival is voluntary.", "+Archival is mandatory.",
                                           "+We watch."])
        self.assertEqual(edits("same", "same"), [])

    def test_similarity(self):
        self.assertEqual(similarity("abcd", "abcd"), 1.0)
        self.assertEqual(similarity("abcd", "wxyz"), 0.0)
        self.assertEqual(similarity("voluntary", "mandatory"), 0.33)

    def test_ascii_fold(self):
        self.assertEqual(ascii_fold("Ｉｒíｓ ﬁle"), "Iris file")
        self.assertEqual(ascii_fold("café crème"), "cafe creme")

    def test_unrot(self):
        self.assertEqual(unrot("Vevf Inyr"), "Iris Vale")

    def test_short_repr_and_pretty(self):
        self.assertEqual(short_repr(list(range(10))), "[0, 1, 2, ...]")
        self.assertEqual(short_repr("abcdefghijklmnop"), "'abc...mnop'")
        self.assertEqual(pretty({"b": [1, 2], "a": "x" * 20}),
                         "{'a': 'xxxxxxxxxxxxxxxxxxxx',\n 'b': [1, 2]}")


if __name__ == "__main__":
    unittest.main()

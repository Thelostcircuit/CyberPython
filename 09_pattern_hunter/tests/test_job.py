import unittest

from job import (censor, iso_dates, parse_line, redact_emails, split_fields, squash_ws,
                 strong_passphrase, subject_ids, tokens)

LOG = """2091-03-14 22:10:05 [WARN] rack=C-17 subject=OS-ENG-4471 msg=priority hold
2091-03-14 22:10:06 [INFO] rack=A-2 subject=OS-FIN-0042 msg=
coffee machine 4 fault: XOS-ENG-12345 is not an ID
2091-03-14 22:11:00 [DEBUG] rack=B-1 subject=OS-OPS-1111 msg=bad level
"""


class PatternHunter(unittest.TestCase):
    def test_subject_ids(self):
        self.assertEqual(subject_ids(LOG), ["OS-ENG-4471", "OS-FIN-0042", "OS-OPS-1111"])
        self.assertEqual(subject_ids("none here"), [])

    def test_parse_line(self):
        lines = LOG.splitlines()
        self.assertEqual(parse_line(lines[0]), {
            "timestamp": "2091-03-14 22:10:05", "level": "WARN", "rack": "C-17",
            "subject": "OS-ENG-4471", "msg": "priority hold"})
        self.assertEqual(parse_line(lines[1])["msg"], "")
        self.assertIsNone(parse_line(lines[2]))
        self.assertIsNone(parse_line(lines[3]))
        self.assertIsNone(parse_line("junk " + lines[0]))

    def test_redact_emails(self):
        t = "mail i.vale+work@ouro.corp.os or dex@pit.net, not @nobody or a@b"
        self.assertEqual(redact_emails(t), "mail [REDACTED] or [REDACTED], not @nobody or a@b")

    def test_squash_ws(self):
        self.assertEqual(squash_ws("  a \t b\n\n c  "), "a b c")
        self.assertEqual(squash_ws(""), "")

    def test_iso_dates(self):
        self.assertEqual(iso_dates("from 14/03/2091 to 01/04/2091."),
                         "from 2091-03-14 to 2091-04-01.")
        self.assertEqual(iso_dates("1/3/2091 stays"), "1/3/2091 stays")

    def test_strong_passphrase(self):
        self.assertTrue(strong_passphrase("Ouroboros4471x"))
        for bad in ("short1A", "alllowercase123", "ALLUPPERCASE123", "NoDigitsAtAllHere",
                    "Has Space 1234a"):
            self.assertFalse(strong_passphrase(bad), bad)

    def test_tokens(self):
        self.assertEqual(tokens("rack_count*2 + 17.5"), ["rack_count", "*", "2", "+", "17.5"])
        self.assertEqual(tokens("(a1-b)/3"), ["(", "a1", "-", "b", ")", "/", "3"])

    def test_split_fields(self):
        self.assertEqual(split_fields(" a , b;c ;  d "), ["a", "b", "c", "d"])
        self.assertEqual(split_fields("solo"), ["solo"])

    def test_censor(self):
        self.assertEqual(censor("BASILISK sees basilisks. Basilisk!", ["basilisk"]),
                         "******** sees basilisks. ********!")
        self.assertEqual(censor("cost is 1.5+x today", ["1.5+x"]), "cost is ***** today")
        self.assertEqual(censor("code c++ and C", ["c"]), "code *++ and *")
        self.assertEqual(censor("nothing", []), "nothing")


if __name__ == "__main__":
    unittest.main()

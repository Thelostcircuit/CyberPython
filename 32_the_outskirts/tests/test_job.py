import contextlib
import io
import locale
import math
import tempfile
import unittest
import wave
from array import array
from pathlib import Path

import job


def write_stego(path, message, rate=8000):
    bits = []
    for byte in message.encode() + b"\x00":
        bits += [(byte >> k) & 1 for k in range(7, -1, -1)]
    bits += [1] * 16   # junk after the terminator
    samples = array("h")
    for i, bit in enumerate(bits):
        noise = int(3000 * math.sin(i * 0.37)) & ~1
        samples.append(noise | bit)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(samples.tobytes())


class Sound(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_tone(self):
        p = self.d / "tone.wav"
        job.write_tone(p, 440, 0.5, 8000)
        self.assertEqual(job.wav_info(p), (1, 2, 8000, 4000))
        with wave.open(str(p)) as w:
            s = array("h")
            s.frombytes(w.readframes(10))
        self.assertEqual(s[0], 0)
        self.assertEqual(s[1], int(12000 * math.sin(2 * math.pi * 440 / 8000)))

    def test_hidden_message(self):
        p = self.d / "voicemail.wav"
        write_stego(p, "the parrot is resting. C-17. — I")
        self.assertEqual(job.hidden_message(p), "the parrot is resting. C-17. — I")


class Colour(unittest.TestCase):
    def test_palette(self):
        self.assertEqual(job.neon_palette(3), ["#ff0000", "#00ff00", "#0000ff"])
        self.assertEqual(job.neon_palette(6)[1], "#ffff00")

    def test_hue(self):
        self.assertEqual(job.hue_degrees("#ff00ff"), 300)
        self.assertEqual(job.hue_degrees("#00ffff"), 180)
        self.assertEqual(job.hue_degrees("#ff0000"), 0)


class Language(unittest.TestCase):
    def test_catalog(self):
        t = job.CatalogTranslations({"Release": "Kaihō",
                                     ("%d rack", "%d racks"): ("%d raku", "%d rakku")})
        self.assertEqual(t.gettext("Release"), "Kaihō")
        self.assertEqual(t.gettext("Unknown"), "Unknown")
        self.assertEqual(t.ngettext("%d rack", "%d racks", 1) % 1, "1 raku")
        self.assertEqual(t.ngettext("%d rack", "%d racks", 5) % 5, "5 rakku")
        self.assertEqual(t.ngettext("door", "doors", 2), "doors")

    def test_locale(self):
        before = locale.setlocale(locale.LC_NUMERIC)
        self.assertEqual(job.decimal_point_in("C"), ".")
        self.assertEqual(locale.setlocale(locale.LC_NUMERIC), before)
        with self.assertRaises(locale.Error):
            job.decimal_point_in("xx_NOPE.UTF-8")
        self.assertEqual(locale.setlocale(locale.LC_NUMERIC), before)


class Odds(unittest.TestCase):
    def test_spiral(self):
        self.assertEqual(job.spiral(4, 10, 90), [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)])
        pts = job.spiral(3, 5, 120)
        self.assertEqual(pts[-1], (0.0, 0.0))
        self.assertEqual(pts[1], (5.0, 0.0))

    def test_tk_status(self):
        self.assertIn(job.tk_status(), ("available", "missing"))

    def test_zen(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            first = job.zen(0)
            third = job.zen(2)
        self.assertEqual(first, "The Zen of Python, by Tim Peters")
        self.assertEqual(third, "Beautiful is better than ugly.")
        self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main()

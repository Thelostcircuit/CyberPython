import unittest

from job import (callsign, cell_voltage, is_safe_level, mask_card, parse_reading,
                 signal_label, split_credits, status_line)


class BootChecks(unittest.TestCase):
    def test_cell_voltage(self):
        self.assertEqual(cell_voltage(11.1, 3), 3.7)
        self.assertEqual(cell_voltage(10, 3), 3.33)
        self.assertIsInstance(cell_voltage(8, 2), float)

    def test_split_credits(self):
        self.assertEqual(split_credits(340, 3), (113, 1))
        self.assertEqual(split_credits(100, 4), (25, 0))
        self.assertEqual(split_credits(2, 5), (0, 2))

    def test_is_safe_level(self):
        for lvl in (20, 50, 95):
            self.assertIs(is_safe_level(lvl), True, lvl)
        for lvl in (19, 96, 0, -5, 100):
            self.assertIs(is_safe_level(lvl), False, lvl)

    def test_callsign(self):
        self.assertEqual(callsign("  iris", "vale "), "VALE, Iris")
        self.assertEqual(callsign("MONTY", "python"), "PYTHON, Monty")

    def test_status_line(self):
        self.assertEqual(status_line("core", 7, 36.456), "core    |  7%|  36.5C")
        self.assertEqual(status_line("coolant", 100, -4.04), "coolant |100%|  -4.0C")

    def test_parse_reading(self):
        self.assertEqual(parse_reading("  36.6C "), 36.6)
        self.assertEqual(parse_reading("36.6 c"), 36.6)
        self.assertEqual(parse_reading("-2c"), -2.0)

    def test_mask_card(self):
        self.assertEqual(mask_card("4929123456781234"), "************1234")
        self.assertEqual(mask_card("12345"), "*2345")
        self.assertEqual(mask_card("123"), "123")

    def test_signal_label(self):
        self.assertEqual(signal_label(None), "no signal")
        self.assertEqual(signal_label(0), "weak (0)")
        self.assertEqual(signal_label(29), "weak (29)")
        self.assertEqual(signal_label(30), "fair (30)")
        self.assertEqual(signal_label(69), "fair (69)")
        self.assertEqual(signal_label(70), "strong (70)")


if __name__ == "__main__":
    unittest.main()

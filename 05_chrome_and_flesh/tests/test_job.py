import unittest

from job import Chassis, Credits, Implant, Weapon


class CreditsTests(unittest.TestCase):
    def test_repr_str(self):
        self.assertEqual(repr(Credits(1200)), "Credits(1200)")
        self.assertEqual(str(Credits(1200)), "¢1,200")
        self.assertEqual(f"{Credits(5)}", "¢5")

    def test_eq_hash_order(self):
        self.assertEqual(Credits(5), Credits(5))
        self.assertNotEqual(Credits(5), Credits(6))
        self.assertNotEqual(Credits(5), 5)
        self.assertEqual(len({Credits(1), Credits(1), Credits(2)}), 2)
        self.assertLess(Credits(1), Credits(2))
        self.assertEqual(sorted([Credits(3), Credits(1), Credits(2)]),
                         [Credits(1), Credits(2), Credits(3)])
        self.assertEqual(max([Credits(3), Credits(9)]), Credits(9))

    def test_arithmetic(self):
        self.assertEqual(Credits(5) + Credits(3), Credits(8))
        self.assertEqual(Credits(5) - Credits(3), Credits(2))
        self.assertEqual(Credits(5) * 3, Credits(15))
        self.assertEqual(3 * Credits(5), Credits(15))
        total = Credits(0)
        total += Credits(4)
        self.assertEqual(total, Credits(4))
        with self.assertRaises(TypeError):
            Credits(5) + 5
        with self.assertRaises(TypeError):
            Credits(5) * 1.5
        with self.assertRaises(TypeError):
            Credits(5) * Credits(2)

    def test_bool(self):
        self.assertFalse(Credits(0))
        self.assertTrue(Credits(-1))


class ImplantTests(unittest.TestCase):
    def test_basics(self):
        arm = Implant("Gorilla Arm", "arm", 40)
        self.assertEqual(arm.describe(), "Gorilla Arm [arm] 40W")
        self.assertEqual(repr(arm), "Implant('Gorilla Arm', 'arm', 40)")
        with self.assertRaises(ValueError):
            Implant("Tail", "tail", 5)

    def test_from_spec_and_valid_slot(self):
        eye = Implant.from_spec("Kiroshi Optics:eye:12")
        self.assertIsInstance(eye, Implant)
        self.assertEqual((eye.name, eye.slot, eye.power), ("Kiroshi Optics", "eye", 12))
        self.assertTrue(Implant.valid_slot("spine"))
        self.assertFalse(Implant.valid_slot("wing"))
        w = Weapon.from_spec("Blade:arm:9")
        self.assertIsInstance(w, Weapon)

    def test_weapon(self):
        w = Weapon("Mantis Blades", "arm", 30, damage=80)
        self.assertIsInstance(w, Implant)
        self.assertEqual(w.describe(), "Mantis Blades [arm] 30W DMG 80")
        self.assertEqual(repr(w), "Weapon('Mantis Blades', 'arm', 30)")
        with self.assertRaises(ValueError):
            Weapon("Tail Gun", "tail", 1, damage=1)


class ChassisTests(unittest.TestCase):
    def setUp(self):
        self.c = Chassis(budget=100)
        self.arm = Weapon("Mantis Blades", "arm", 30, damage=80)
        self.eye = Implant("Kiroshi Optics", "eye", 12)
        self.c.install(self.arm)
        self.c.install(self.eye)

    def test_container(self):
        self.assertEqual(len(self.c), 2)
        self.assertEqual(list(self.c), [self.arm, self.eye])
        self.assertIn("Kiroshi Optics", self.c)
        self.assertNotIn("Heart", self.c)
        self.assertIs(self.c["arm"], self.arm)
        with self.assertRaises(KeyError):
            self.c["spine"]

    def test_power(self):
        self.assertEqual(self.c.power_draw, 42)
        with self.assertRaises(AttributeError):
            self.c.power_draw = 0
        with self.assertRaises(ValueError):
            self.c.install(Implant("Heavy Spine", "spine", 59))
        self.c.install(Implant("Spine", "spine", 58))
        self.assertEqual(self.c.power_draw, 100)

    def test_slot_taken(self):
        with self.assertRaises(ValueError):
            self.c.install(Implant("Spare Eye", "eye", 1))
        self.assertEqual(len(self.c), 2)

    def test_budget_property(self):
        self.c.budget = 500
        self.assertEqual(self.c.budget, 500)
        with self.assertRaises(ValueError):
            self.c.budget = -1
        with self.assertRaises(ValueError):
            Chassis(budget=-5)


if __name__ == "__main__":
    unittest.main()

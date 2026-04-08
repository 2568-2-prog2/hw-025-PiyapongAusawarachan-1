import unittest
from dice import Dice

class TestDice(unittest.TestCase):
    def test_valid(self):
        d = Dice([0.1,0.2,0.3,0.1,0.2,0.1])
        result = d.roll(5)
        self.assertEqual(len(result), 5)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Dice([0.1,0.2])

    def test_invalid_sum(self):
        with self.assertRaises(ValueError):
            Dice([1,1,1,1,1,1])

if __name__ == "__main__":
    unittest.main()
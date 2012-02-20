import unittest

from kasner import KasnerSequence


class TestKasnerSequence(unittest.TestCase):

    def test_2(self):
        expected = [(0, 1), (0, 2)]
        actual = list(KasnerSequence(2))
        self.assertEqual(actual, expected)

    def test_3(self):
        expected = [(0, 1, 0), (0, 1, 2), (0, 2, 0), (0, 2, 1)]
        actual = list(KasnerSequence(3))
        self.assertEqual(actual, expected)

    def test_4(self):
        expected = [(0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 0), (0, 1, 2, 1),
                    (0, 2, 0, 1), (0, 2, 0, 2), (0, 2, 1, 0), (0, 2, 1, 2)]
        actual = list(KasnerSequence(4))
        self.assertEqual(actual, expected)

    def test_5(self):
        expected = [(0, 1, 0, 1, 0), (0, 1, 0, 1, 2), (0, 1, 0, 2, 0), (0, 1, 0, 2, 1),
                    (0, 1, 2, 0, 1), (0, 1, 2, 0, 2), (0, 1, 2, 1, 0), (0, 1, 2, 1, 2),
                    (0, 2, 0, 1, 0), (0, 2, 0, 1, 2), (0, 2, 0, 2, 0), (0, 2, 0, 2, 1),
                    (0, 2, 1, 0, 1), (0, 2, 1, 0, 2), (0, 2, 1, 2, 0), (0, 2, 1, 2, 1)]
        actual = list(KasnerSequence(5))
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()

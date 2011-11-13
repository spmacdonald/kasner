import unittest

from kasner import KasnerPath

class TestKasnerPath(unittest.TestCase):

    def test_path_3(self):
        expected = [[0, 1, 2], [0, 2, 1]]
        paths = KasnerPath(3)
        self.assertEqual(list(paths), expected)

    def test_path_4(self):
        expected = [[0, 1, 0, 2], [0, 1, 2, 1], [0, 2, 1, 2]]
        paths = KasnerPath(4)
        self.assertEqual(list(paths), expected)

    def test_path_5(self):
        expected = [[0, 1, 0, 1, 2], [0, 1, 0, 2, 1], [0, 1, 2, 0, 2],
                    [0, 1, 2, 1, 2], [0, 2, 0, 2, 1], [0, 2, 1, 2, 1]]
        paths = KasnerPath(5)
        self.assertEqual(list(paths), expected)

if __name__ == "__main__":
    unittest.main()

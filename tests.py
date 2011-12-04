import unittest

from kasner import KasnerPath, Point, circle_line_intersection


class TestKasnerRange(unittest.TestCase):

    def test_intersection(self):
        p1 = Point(0.963525, -0.267617)
        p2 = Point(-1, 1.7320508075688772)
        p = circle_line_intersection(p1, p2)
        self.assertTrue(p == Point(-0.250000279, 0.968245764))


class TestKasnerPath(unittest.TestCase):

    def test_path_3(self):
        expected = [(0, 1, 2), (0, 2, 1)]
        paths = KasnerPath(3)
        self.assertEqual(list(paths), expected)

    def test_path_4(self):
        expected = [(0, 1, 0, 2), (0, 1, 2, 1), (0, 2, 1, 2)]
        paths = KasnerPath(4)
        self.assertEqual(list(paths), expected)

    def test_path_5(self):
        expected = [(0, 1, 0, 1, 2), (0, 1, 0, 2, 1), (0, 1, 2, 0, 2),
                    (0, 1, 2, 1, 2), (0, 2, 0, 2, 1), (0, 2, 1, 2, 1)]
        paths = KasnerPath(5)
        self.assertEqual(list(paths), expected)

if __name__ == "__main__":
    unittest.main()

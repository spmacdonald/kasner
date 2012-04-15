import unittest

from kasner import KasnerSequence, KasnerPath, refine_path


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


class TestKasnerPath(unittest.TestCase):

    def test_3(self):
        expected = [(0, 1, 2), (0, 2, 1)]
        actual = list(KasnerPath(3))
        self.assertEqual(actual, expected)

    def test_4(self):
        expected = [(0, 1, 0, 2), (0, 1, 2, 1), (0, 2, 1, 2)]
        actual = list(KasnerPath(4))
        self.assertEqual(actual, expected)

    def test_5(self):
        expected = [(0, 1, 0, 1, 2), (0, 1, 0, 2, 1),
                    (0, 1, 2, 0, 2), (0, 1, 2, 1, 2),
                    (0, 2, 0, 2, 1), (0, 2, 1, 2, 1)]
        actual = list(KasnerPath(5))
        self.assertEqual(actual, expected)

    def test_primes(self):
        self.assertEqual(2, len(KasnerPath(3)))
        self.assertEqual(6, len(KasnerPath(5)))
        self.assertEqual(18, len(KasnerPath(7)))
        self.assertEqual(186, len(KasnerPath(11)))
        self.assertEqual(630, len(KasnerPath(13)))

    def test_refine_path(self):
        self.assertAlmostEqual(0.270918521455, refine_path((0, 1, 2)))
        self.assertAlmostEqual(-0.27091852145, refine_path((0, 2, 1)))

        self.assertAlmostEqual(-4.386261286, refine_path((0, 1, 0, 2)))
        self.assertAlmostEqual(2.2918661857, refine_path((0, 1, 2, 1)))
        self.assertAlmostEqual(-2.291866185, refine_path((0, 2, 1, 2)))

        self.assertAlmostEqual(2.23630658934, refine_path((0, 1, 0, 1, 2)))
        self.assertAlmostEqual(-2.4158117875, refine_path((0, 1, 0, 2, 1)))
        self.assertAlmostEqual(0.25179872406, refine_path((0, 1, 2, 0, 2)))
        self.assertAlmostEqual(-2.5902541268, refine_path((0, 1, 2, 1, 2)))
        self.assertAlmostEqual(-2.2363065893, refine_path((0, 2, 0, 2, 1)))
        self.assertAlmostEqual(2.59025412688, refine_path((0, 2, 1, 2, 1)))



if __name__ == "__main__":
    unittest.main()

import unittest

from kasner import KasnerTree

class TestKasnerTree(unittest.TestCase):

    def setUp(self):
        tree = KasnerTree()

        tree.add({'a':0})
        tree.add({'ab':1})
        tree.add({'ac':2})
        tree.add({'aba':3})
        tree.add({'abc':4})
        tree.add({'aca':5})
        tree.add({'acb':6})
        tree.add({'abab':7})
        tree.add({'abac':8})
        tree.add({'abca':9})
        tree.add({'abcb':10})
        tree.add({'acab':11})
        tree.add({'acac':12})
        tree.add({'acba':13})
        tree.add({'acbc':14})

    def test_get_items(self):
        print tree.items()

if __name__ == '__main__':
    unittest.main()

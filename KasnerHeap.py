from math import floor

class KasnerHeap(object):
    """
    """

    def __init__(self):
        self.storage = []

    def __getitem__(self, key):
        return self.storage[key]
        
    def add(self, d):
        self.storage.append(d)

    def items(self):
        return self.storage

    def get_child_index(self, n):
        return range(2**(n-1)-1, 2**n-1)

    def _parent(self, ix):
        return int(floor((ix+1)/2)-1) 
    
    def follow(self, ix):
        trail = [ix]
        while True:
            if ix == 0:
                break
            ix = self._parent(ix)
            trail.append(ix)
        return trail


def test():

    heap = KasnerHeap()

    heap.add({'a':0})
    heap.add({'ab':1})
    heap.add({'ac':2})
    heap.add({'aba':3})
    heap.add({'abc':4})
    heap.add({'aca':5})
    heap.add({'acb':6})
    heap.add({'abab':7})
    heap.add({'abac':8})
    heap.add({'abca':9})
    heap.add({'abcb':10})
    heap.add({'acab':11})
    heap.add({'acac':12})
    heap.add({'acba':13})
    heap.add({'acbc':14})

    print heap.items()
    print heap.get_child_index(3)
    print heap.follow(234)

    print heap[12]

    for i in heap.get_child_index(3):
        print heap[i]


if __name__ == '__main__': test()

from math import floor


class KasnerTree(object):
    """Structure to hold periodic paths."""

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

    def follow(self, ix):
        trail = [ix]
        while True:
            if ix == 0:
                break
            trail.append(self._parent(ix))
        return trail

    def _parent(self, ix):
        return int(floor((ix+1)/2)-1)

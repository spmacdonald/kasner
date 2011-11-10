import sys

class KasnerPath:
    """ """

    def __init__(self, n):
        self.n = n
        self.data = [i % 2 for i in range(n)]
        self.seen_paths = set()

    def __iter__(self):
        for i in range(2**(self.n - 1)):
            path = self.circular_min(self.data)
            if tuple(path) not in self.seen_paths and self.is_periodic(path):
                self.seen_paths.add(tuple(path))
                yield path
            self._next_path(self.n - 1)

    def _next_path(self, i):
        self.data[i] += 1
        if self.data[i] > 2:
            self.data[i] = 0
            self._next_path(i - 1)
        if self.data[i - 1] == self.data[i]:
            self._next_path(i)

    def is_periodic(self, path):
        return self.is_path_terminating(path) and self.is_path_balanced(path)

    def is_path_terminating(self, path):
        try:
            path.index(0)
            path.index(1)
            path.index(2)
            return True
        except ValueError:
            return False

    def is_path_balanced(self, path):
        for i in range(self.n - 1):
            if path[i] == path[i + 1]:
                return False
        return True

    def circular_min(self, path):
        """
        This algorithm is from Lothaire's Applied Combinatorics on Words, pg.
        14
        """
        (i,j,k) = (0,1,0)
        m = len(self.data)
        b = [0] * (2*m+1)
        b[0] = -1
        while k+j < 2*m:
            if j-i == m:
                break
            b[j] = i
            while i >= 0 and self.data[(k+j) % m] != self.data[(k+i) % m]:
                if self.data[(k+j) % m] < self.data[(k+i) % m]:
                    (k, j) = (k+j-i, i)
                i = b[i]
            (i, j) = (i+1, j+1)

        # Rotate to least conjugate.
        if k == 0:
            return path

        result = self.n * [0]
        i = k
        j = 0
        for _ in range(self.n):
            if i >= self.n:
                i = 0
            result[j] = self.data[i]
            j += 1
            i += 1
        return result


if __name__ == "__main__":

    paths = KasnerPath(int(sys.argv[1]))
    for p in paths:
        continue
        # print "Periodic path:", p

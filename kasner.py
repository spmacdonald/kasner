import sys

class KasnerSequence:

    def __init__(self, n):
        self.n = n
        self.num_iter = 2 ** (n - 1)
        self.sequence = [i % 2 for i in range(n)]

    def __iter__(self):
        for i in range(self.num_iter):
            yield tuple(self.sequence)
            self._next_sequence(self.n - 1)

    def _next_sequence(self, i):
        self.sequence[i] += 1
        if self.sequence[i] > 2:
            self.sequence[i] = 0
            self._next_sequence(i - 1)
        if self.sequence[i - 1] == self.sequence[i]:
            self._next_sequence(i)


class KasnerPath:

    def __init__(self, n):
        self.n = n
        self.seen_paths = set()
        self._add_all_paths()

    def __iter__(self):
        return iter(sorted(self.seen_paths))

    def __len__(self):
        return len(self.seen_paths)

    def _add_all_paths(self):
        for s in KasnerSequence(self.n):
            self._add_path(s)

    def _add_path(self, s):
        rotations = [s[i:] + s[:i] for i in range(len(s))]
        least_rotation = sorted(rotations)[0]
        if self._valid_path(least_rotation):
            self.seen_paths.add(least_rotation)

    def _valid_path(self, path):
        try:
            path.index(0)
            path.index(1)
            path.index(2)
        except ValueError:
            return False

        for i in range(len(path) - 1):
            if path[i] == path[i + 1]:
                return False

        return True

if __name__ == "__main__":

    n = int(sys.argv[1])

    print len(KasnerPath(n))

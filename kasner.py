import sys
from math import pi, acos, cos, sin


class KasnerSequence(object):

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


class KasnerPath(object):

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
        if self._is_periodic(least_rotation):
            self.seen_paths.add(least_rotation)

    def _is_periodic(self, path):
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


def refine_path(path):

    path_range = [-pi/3, pi/3]

    i = 0
    while abs(path_range[0] - path_range[1]) > 1e-8:
        idx = i % len(path)
        path_range[0] = last_angle(path_range[0], path[idx])
        path_range[1] = last_angle(path_range[1], path[idx])
        i += 1

    return (path_range[0] + path_range[1]) / 2


def last_angle(th, i):
    if th < 0:
        th += 2 * pi

    if th >= pi / 3 and th < pi:
        if i == 0:
            return acos((5 * cos(th) - 4) / (4 * cos(th) - 5))
        elif i == 1:
            return -acos((5 * cos(th + 2 * pi / 3) - 4) / (4 * cos(th + 2 * pi / 3) - 5) ) - 2 * pi / 3
        else:
            return th

    elif th >= pi and th < 5 * pi / 3:
        if i == 0:
            return -acos((5 * cos(th) - 4) / (4 * cos(th) - 5))
        elif i == 2:
            return acos((5 * cos(th - 2 * pi / 3) - 4) / (4 * cos(th - 2 * pi / 3) - 5)) + 2 * pi / 3
        else:
            return th

    else:
        if i == 1:
            return acos((5 * cos(th + 2 * pi / 3) - 4) / (4 * cos(th + 2 * pi / 3) - 5)) - 2 * pi / 3
        elif i == 2:
            return -acos((5 * cos(th + 4 * pi / 3) - 4) / (4 * cos(th + 4 * pi / 3) - 5)) - 4 * pi / 3
        else:
            return th


if __name__ == "__main__":

    n = int(sys.argv[1])

    for path in KasnerPath(n):
        theta = refine_path(path)
        print path, theta, cos(theta), sin(theta)

import sys
from math import sqrt
from collections import namedtuple

class Point(namedtuple("Point", "x y")):

    def __eq__(self, other):
        return almost_equal(self.x, other.x) and almost_equal(self.y, other.y)

    def __ne__(self, other):
        return not almost_equal(self.x, other.x) or not almost_equal(self.y, other.y)

TOL = 1e-12
SQRT3 = 1.7320508075688772
FIXED_POINTS = {0: Point(2.0, 0.0),
                1: Point(-1.0, SQRT3),
                2: Point(-1.0, -SQRT3)}


def refine_path(path):
    p1 = Point(0.5, sqrt(3) / 2.0)
    p2 = Point(0.5, -sqrt(3) / 2.0)
    dist = sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    path = list(path)
    path.reverse()
    while dist > TOL:
        for v in path:
            p1 = circle_line_intersection(p1, FIXED_POINTS[v])
            p2 = circle_line_intersection(p2, FIXED_POINTS[v])
        dist = sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    # XXX: Check the order of points matches path string.
    path.reverse()
    for v in path:
        p1 = circle_line_intersection(p1, FIXED_POINTS[v])
        p2 = circle_line_intersection(p2, FIXED_POINTS[v])

def circle_line_intersection(point, vertex):

    dx = vertex.x - point.x
    dy = vertex.y - point.y
    dr = dx*dx + dy*dy
    d = point.x*vertex.y - vertex.x*point.y
    discriminant = dr - d*d

    if discriminant < 0:
        return None
    else:
        discriminant = sqrt(discriminant)

        x0 = ( d*dy + sgn(dy)*dx*discriminant ) / dr
        y0 = ( -d*dx + abs(dy)*discriminant ) / dr
        p0 = Point(x0, y0)
        if p0 != point:
            return p0

        x1 = ( d*dy - sgn(dy)*dx*discriminant ) / dr
        y1 = ( -d*dx - abs(dy)*discriminant ) / dr
        p1 = Point(x1, y1)
        if p1 != point:
            return p1

        return None


def almost_equal(x, y):
    if abs(x - y) < TOL:
        return True
    return False

def sgn(x):
    """
    Implements the mathematical sgn*(x) function.

    See:
        http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    if x < 0.0:
        return -1.0
    return 1.0

class KasnerPath:
    """ """

    def __init__(self, n):
        self.n = n
        self.data = [i % 2 for i in range(n)]
        self.seen_paths = set()

    def __iter__(self):
        path = self.data
        for i in range(2**(self.n - 1)):
            path = self.next_path(path, self.n - 1)
            least_path = tuple(self.circular_min(path))
            if least_path not in self.seen_paths and self.is_periodic(least_path):
                self.seen_paths.add(least_path)
                yield least_path

    def next_path(self, path, i):
        path[i] += 1
        if path[i] > 2:
            path[i] = 0
            self.next_path(path, i - 1)
        if path[i - 1] == path[i]:
            self.next_path(path, i)
        return path

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
        refine_path(p)


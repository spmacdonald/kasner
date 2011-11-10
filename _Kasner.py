from math import fabs, sqrt, cos, sin, pi
from time import time

from KasnerHeap import KasnerHeap

##
# Constants

TOL = 1.0e-10
SQRT3_2 = 0.8660254037844386 # sqrt(3)/2
SQRT3 = 1.7320508075688772 # sqrt(3)

##
# Point class

class Point(object):
    """
    A simple class to represent the familiar geometrical notion of a
    Point in 2D.
    """

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return 'Point(%f, %f)' % (self.x, self.y)

    def __eq__(self, other):
        return close_at_tolerance(self.x, other.x) and close_at_tolerance(self.y, other.y)

##
# Range class

class Range(object):
    """
    A class to represents an arc of the Kasner ring.
    """

    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2

    def __repr__(self):
        return 'Range(%s, %s)' % (self.p1, self.p2)

##
# Global methods

def close_at_tolerance(f1, f2):
    """
    Implements a floating point comparison algorimth.

    Testing the magnitude of floating point numbers is tricky, I use a
    very simple approach here...

    See:
        Knuth D.E. The art of computer programming (vol II).
        http://www.lahey.com/float.htm
    """

    if fabs(f1 - f2) < TOL: # This is error prone, but in my specific
                            # problem it is okay.
        return True
    else:
        return False

def sgn(x):
    """
    Implements the mathematical sgn*(x) function.

    See:
        http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    if x < 0.0:
        return -1.0
    else:
        return 1.0

def circle_line_intersection(p1, p2):
    """
    Given two points that define a line, return the circle-line
    intersection point(s).  The radius of the circle is assumed to be
    1 unit.

    There are 3 cases that are characterized by the discriminant:
        discriminant < 0 => no intersection
        discriminant = 0 => tangent
        discriminant > 0 => intersection (2 points)

    See:
        http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dr = sqrt( dx**2 + dy**2 )
    D = p1.x*p2.y - p2.x*p1.y
    discriminant = dr**2 - D**2

    # For the first few iterations of the algorithm, some ranges
    # contain points which define lines that are tangent to the Kasner
    # ring.  In these cases, due to floating point arthmetic, the
    # discriminant is not exactly zero, and in fact may be a very
    # small negative number such as -1.0e-16.  If this is the case,
    # the algorithm below will throw a math domain exception.  To
    # avoid this, we force the value of the discriminat to be zero if
    # close_at_tolerance returns True.
    if discriminant < 0:
        if close_at_tolerance(discriminant, 0.0):
            discriminant = 0.0
        else:
            raise ValueError('Negative discriminant')

    xp = ( D*dy + sgn(dy)*dx*sqrt(discriminant) ) / dr**2
    xn = ( D*dy - sgn(dy)*dx*sqrt(discriminant) ) / dr**2

    yp = ( -D*dx + fabs(dy)*sqrt(discriminant) ) / dr**2
    yn = ( -D*dx - fabs(dy)*sqrt(discriminant) ) / dr**2

    return discriminant, Point(xp, yp), Point(xn, yn)

def point_distance(p1, p2):
    """
    Given two points, return the length of the path connecting them.
    """

    return sqrt( (p2.x - p1.x)**2 + (p2.y - p1.y)**2 )

def rotate_point(p, th):
    """
    Given a point and an angle, return the point after it has been
    rotated th radians counter clockwise about the origin.
    """

    return Point( (p.x*cos(th) - p.y*sin(th)), (p.x*sin(th) + p.y*cos(th)) )

def kasner_point_intersection(kasner_p, triangle_vertex_p):
    """
    Given two points that define a line, return the circle-line
    intersection point.  The first argument to the kasner_intersection
    function is assumed to be a point which satisfies the equation x^2
    + y^2 = 1.  The second argument to the kasner_point_intersection
    function is assumed to be one of the three special triangle vertex
    points.

    The return value from the kasner_intersection function depends on
    the characteristics of the discriminant.  There are 2 cases:

        discriminant = 0 => tangent => return either of the circle-line
                                       intersection points
        discriminant > 0 => intersection => return the point that is different
                                            from the kasner_p input point, since
                                            the circle-line intersection will
                                            return 2 points, one of which we already
                                            know.
    """

    discriminant, p1, p2 = circle_line_intersection(kasner_p, triangle_vertex_p)

    if close_at_tolerance(discriminant, 0.0):
        return p1
    else:
        if p1 == kasner_p:
            return p2
        else:
            return p1

def kasner_range_intersection(rng, triangle_vertex):
    """
    Applies the kasner_point_intersection function to each point contained
    in the Kasner Range input, rng.
    """

    # Define the location of the map's triangle vertices
    triangle_vertex_a = Point(2.0, 0.0)
    triangle_vertex_b = Point(-1.0, SQRT3)
    triangle_vertex_c = Point(-1.0, -SQRT3)

    if triangle_vertex == 'a':
        return Range(kasner_point_intersection(rng.p1, triangle_vertex_a),
                     kasner_point_intersection(rng.p2, triangle_vertex_a))
    if triangle_vertex == 'b':
        return Range(kasner_point_intersection(rng.p1, triangle_vertex_b),
                     kasner_point_intersection(rng.p2, triangle_vertex_b))
    if triangle_vertex == 'c':
        return Range(kasner_point_intersection(rng.p1, triangle_vertex_c),
                     kasner_point_intersection(rng.p2, triangle_vertex_c))

def branch_kasner_range(d):
    """
    This function returns a tuple of dicts that represent the
    verticies from which the input range could have come from.

    It performs the branching logic for the back-tracking portion of the
    algorithm.  The input dictionary, d, contains a letter, {a|b|c},
    as its key and a Range object as the associated value.  The letter
    represents the triangle vertex which the Range lies closest to.
    In the context of the back-tracking algorithm, this range could
    have come from either of remaining two triangle verticies.
    """

    for key in d.keys():
        if key == 'a':
            r1 = kasner_range_intersection(d[key], 'b')
            r2 = kasner_range_intersection(d[key], 'c')
            return {'b': r1}, {'c': r2}
        if key == 'b':
            r1 = kasner_range_intersection(d[key], 'a')
            r2 = kasner_range_intersection(d[key], 'c')
            return {'a': r1}, {'c': r2}
        if key == 'c':
            r1 = kasner_range_intersection(d[key], 'a')
            r2 = kasner_range_intersection(d[key], 'b')
            return {'a': r1}, {'b': r2}

def is_path_periodic(letter_trail, range_trail):
    """
    Determines if a given path is periodic or not.  A path of length
    N, represented by a string 'x_1, x_2, x_3, ..., x_n' is periodic
    if:

        1. x_1 == x_n
        2. Range(x_n) contained in Range(x_1)

    Where Range(x_i) means the the i^{th} range object in the range
    trail.
    """

    if letter_trail[0] == letter_trail[len(letter_trail)-1]:
        start_range = range_trail[0]
        end_range = range_trail[len(range_trail)-1]
        if start_range.p1.x < end_range.p1.x \
                and start_range.p1.y > end_range.p1.y \
                and start_range.p2.x < end_range.p1.x \
                and start_range.p2.y > end_range.p1.y \
                and start_range.p1.x > end_range.p2.x \
                and start_range.p1.y < end_range.p2.y \
                and start_range.p2.x > end_range.p2.x \
                and start_range.p2.y < end_range.p2.y:
            return True
        else:
            return False
    else:
        return False

def refine_path(letter_trail, range_trail):
    """
    Given a periodic path represented by a letter_trail and
    range_trail, repeatedly 'walk' the path by applying the
    kasner_range_intersection function to the range_trail in a
    circular manner while the distance separating the two range points
    is greater than the specified tolerance.
    """

    letter_trail.reverse()
    letter_trail = letter_trail[1:]
    range_trail = range_trail[0:len(range_trail)-1]
    trail_len = len(letter_trail)

    # Loop over the range_trail until the distance between points is
    # less than TOL
    cntr = 0
    while point_distance(range_trail[0].p1, range_trail[0].p2) > TOL:
        range_trail[(cntr+1) % trail_len] = \
            kasner_range_intersection(range_trail[cntr % trail_len],
                                      letter_trail[cntr % trail_len])
        cntr += 1

    # Construct a list of the path's coordinate points
    path = []
    for rng in range_trail:
        path.append(rng.p1)

    # Construct a string to identify the path by
    letter_trail.reverse()
    trail_string = ''.join(letter_trail)

    return trail_string, path

def find_periodic_paths(heap, depth):
    """
    Given a populated heap which represents the total possible space
    of periodic paths to a specified depth, follow each of the
    children back to the root (starting range) and decide if the
    range_trail is periodic by applying is_path_periodic.  If it is,
    add it to an array, paths, which contains a number of dicts which
    represent the periodic paths of the map.
    """

    paths = []
    for i in range(4, depth+2):
        paths_at_depth_n = {}
        children = heap.get_child_index(i)
        for child in children:
            trail = heap.follow(child)
            letter_trail, range_trail = [], []
            for index in trail:
                for k,v in heap[index].items():
                    letter_trail.append(k)
                    range_trail.append(v)
            if is_path_periodic(letter_trail, range_trail):
                trail_string, path = refine_path(letter_trail, range_trail)
                paths_at_depth_n[trail_string] = path
        paths.append(paths_at_depth_n)
    return paths

def circular_min(x):
    """
    Given a trail_string x, that represents a periodic path, this
    function will return the starting index that allows one to order
    the trail_string in the lexigraphically least sense.  For example:

    let x = 'abcba' then circular_min(x) = 4.  If we re-order the word
    starting at position 4 (modulo len(x)) we get: 'aabcb' which is
    the lexigraphically least ordering of 'abcba'.

    Said another way, circular_min(x) returns the index k such that
    x[k..k-1] is the least conjugate of x.

    This algorithm is from Lothaire's Applied Combinatorics on Words,
    pg. 14
    """

    (i,j,k) = (0,1,0)
    m = len(x)
    b = [0] * (2*m+1)
    b[0] = -1
    while k+j < 2*m:
        if j-i == m:
            break
        b[j] = i
        while i >= 0 and x[(k+j) % m] != x[(k+i) % m]:
            if x[(k+j) % m] < x[(k+i) % m]:
                (k, j) = (k+j-i, i)
            i = b[i]
        (i, j) = (i+1, j+1)
    return k

def lexigraphically_order_word(word):
    """
    Given a word, return the word in lexigraphically least order.

    See circular_min for an example.
    """

    word_len = len(word)
    least_index = circular_min(word)
    least_word = []
    for i in range(word_len):
        least_word.append(word[(i+least_index) % word_len])
    return ''.join(least_word)

def remove_duplicates(paths):
    """
    When a periodic path has more than one point in the initial
    searching range, the algorithm will find this point and count it
    as a periodic path.  Since this really is not a unique path we
    want to remove it.  This is done by ordering the path strings
    lexigraphically, and then removing any string that is duplicated
    by popping it out of the dictionary.  Notice that the dict is
    modified in place.
    """

    seen = set()
    for path in paths.keys():
        if lexigraphically_order_word(path) in seen:
            paths.pop(path)
            continue
        seen.add(lexigraphically_order_word(path))

def apply_map_symmetries(paths):
    """
    A significant optimization present in this algorithm is to only
    search a portion of the entire Kasner ring for periodic paths.
    This reduces the number of computations by a factor of 6.  It also
    means that only a subset of the total periodic paths are
    discovered.  Luckily, we can exploit the symmetries of the map to
    find the remaining periodic paths in a computationally efficient
    manner.  This is done by applying the appropriate rotational
    transformation to the paths that are discovered by the
    find_periodic_paths function.

    The strategy is to first reflect every point in the initial
    starting range through a line joining the points (2, 0) and (-1,
    0), or in other words: reflect every point through the triangle
    vertex A.  Then the new 'wedge' is rotated through an angle of
    2*pi/3 radians, and finally, -2*pi/3 radians.  One final
    consideration is the effect these rotational transformations have
    on the strings which represent the periodic paths.  This is
    summarized below.

        reflect in vertex A   => (AA)(BC)(CB)
        rotate by 2*pi/3      => (AB)(BC)(CA)
        rotate by -2*pi/3     => (AC)(BA)(CB)

        Read (AA)(BC)(CB) as: "A goes to A, B goes to C, C goes to B"
    """

    # Reflect in vertex 'A'
    for path, points in paths.items():
        paths[reflect_path_string(path, 'A')] = reflect_path_points(points, 'A')
    remove_duplicates(paths)

    # Rotate through 2*pi/3 radians
    for path, points in paths.items():
        paths[rotate_path_string(path, '2PI_3')] = rotate_path_points(points, '2PI_3')
    remove_duplicates(paths)

    # Rotate through -2*pi/3 radians
    for path, points in paths.items():
        paths[rotate_path_string(path, '-2PI_3')] = rotate_path_points(points, '-2PI_3')
    remove_duplicates(paths)

def rotate_path_string(path, angle):
    """
    Implement the string operations summarized in the
    apply_map_symmetries function.
    """

    rotated_path = []
    if angle == '2PI_3':
        for letter in path:
            if letter == 'a':
                rotated_path.append('b')
            if letter == 'b':
                rotated_path.append('c')
            if letter == 'c':
                rotated_path.append('a')
    elif angle == '-2PI_3':
        for letter in path:
            if letter == 'a':
                rotated_path.append('c')
            if letter == 'b':
                rotated_path.append('a')
            if letter == 'c':
                rotated_path.append('b')
    else:
        raise ValueError('Method only defined for angles of +/- 2*pi/3')

    return ''.join(rotated_path)

def rotate_path_points(points, angle):
    """
    Implement the point operations summarized in the
    apply_map_symmetries function.
    """

    rotated_points = []
    if angle == '2PI_3':
        for p in points:
            rotated_points.append(rotate_point(p, 2*pi/3))
    elif angle == '-2PI_3':
        for p in points:
            rotated_points.append(rotate_point(p, -2*pi/3))
    else:
        raise ValueError('Method only defined for angles of +/- 2*pi/3')

    return rotated_points

def reflect_path_points(points, vertex):
    """
    Implement the point operations summarized in the
    apply_map_symmetries function.
    """

    reflected_points = []
    if vertex == 'A':
        for p in points:
            reflected_points.append(Point(p.x, -p.y))
    else:
        raise ValueError('Method only defined for vertex A')

    return reflected_points

def reflect_path_string(path, vertex):
    """
    Implement the string operations summarized in the
    apply_map_symmetries function.
    """

    reflected_path = []
    if vertex == 'A':
        for letter in path:
            if letter == 'a':
                reflected_path.append('a')
            if letter == 'b':
                reflected_path.append('c')
            if letter == 'c':
                reflected_path.append('b')
    else:
        raise ValueError('Method only defined for vertex A')

    return ''.join(reflected_path)


##
# Program entry point

if __name__ == '__main__':

    # Start the clock...
    start_time = time()

    # Find periodic paths up to length N
    N = 10

    # Initial range
    heap = KasnerHeap()
    heap.add({'a': Range(Point(1.0, 0.0), Point(0.5, SQRT3_2))})

    # Populate the heap
    for i in range(1, N+1):
        children = heap.get_child_index(i)
        for child in children:
            d1, d2 = branch_kasner_range(heap[child])
            heap.add(d1)
            heap.add(d2)

    print "populated heap in ... %f seconds" % (time() - start_time)

    # Reset the clock...
    start_time = time()

    # Find all periodic paths up to length N
    all_paths = find_periodic_paths(heap, N)

    print "found all periodic paths in initial range in ... %f seconds" % (time() - start_time)

    # Remove all duplicate paths
    for paths in all_paths:
        remove_duplicates(paths)

    # Apply the symmetries of the map to find the remaining periodic paths
    for paths in all_paths:
        apply_map_symmetries(paths)

    # Print some statistics
    end_time = time()
    print "Finished in %f seconds" % (end_time - start_time)
    print "Period     Total"
    for i, paths in enumerate(all_paths):
        path_len = len(paths)
        print "%3d %11d" % ((i+3), path_len)

    # Print the first 3 periodic paths to stdout
    for i in range(3):
        for k,v in all_paths[i].items():
            print k,v


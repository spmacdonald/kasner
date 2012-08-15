from math import pi, acos, cos


def generate_sequences(n):
    sequence = [i % 2 for i in range(n)]

    def next_sequence(i):
        sequence[i] += 1
        if sequence[i] > 2:
            sequence[i] = 0
            next_sequence(i - 1)
        if sequence[i - 1] == sequence[i]:
            next_sequence(i)

    for _ in range(2 ** (n - 1)):
        yield tuple(sequence)
        next_sequence(n - 1)


def generate_periodic_sequences(n):

    def is_periodic(sequence):
        try:
            sequence.index(0)
            sequence.index(1)
            sequence.index(2)
        except ValueError:
            return False

        for i in range(len(sequence) - 1):
            if sequence[i] == sequence[i + 1]:
                return False

        return True

    seen_sequences = set()

    for s in generate_sequences(n):
        rotations = [s[i:] + s[:i] for i in range(len(s))]
        least_rotation = sorted(rotations)[0]
        if is_periodic(least_rotation):
            seen_sequences.add(least_rotation)

    for s in sorted(seen_sequences):
        yield s


def refine_path(path):

    path_range = [-pi / 3, pi / 3]

    i = 1
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
            return -acos((5 * cos(th + 2 * pi / 3) - 4) / (4 * cos(th + 2 * pi / 3) - 5)) - 2 * pi / 3
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

    for n in range(3, 38):
        print n, len(list(generate_periodic_sequences(n)))

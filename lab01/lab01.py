import unittest
import sys
from contextlib import contextmanager
from io import StringIO

#################################################################################
# TESTING OUTPUTS
#################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


#################################################################################
# EXERCISE 1
#################################################################################

# implement this function
def is_perfect(n):
    # keeps sum of factors
    sum_of_i = 0
    # iterates through values from 1 to n to see if they are factors.
    for i in range(1, n):
        # checks if i is a factor of n.
        if n % i == 0:
            # if so i is added to sum of factors.
            sum_of_i += i
    # if sum of factors is equal to n, n is perfect, else imperfect.
    if sum_of_i == n:
        return True
    else:
        return False


# (3 points)
def test1():
    tc = unittest.TestCase()
    for n in (6, 28, 496):
        tc.assertTrue(is_perfect(n), "{} should be perfect".format(n))
    for n in (1, 2, 3, 4, 5, 10, 20):
        tc.assertFalse(is_perfect(n), "{} should not be perfect".format(n))
    for n in range(30, 450):
        tc.assertFalse(is_perfect(n), "{} should not be perfect".format(n))


#################################################################################
# EXERCISE 2
#################################################################################

# implement this function
def multiples_of_3_and_5(n):
    # keeps sum of multiples
    sum_of_i = 0
    # iterates through values from 1 to n to see if they are multiples of 3 or 5.
    for i in range(1, n):
        # checks if i is a multiple of 3 or 5.
        if i % 3 == 0 or i % 5 == 0:
            # if so i is added to sum of factors.
            sum_of_i += i
    # sum_of_i is returned..
    return sum_of_i


# (3 points)
def test2():
    tc = unittest.TestCase()
    tc.assertEqual(multiples_of_3_and_5(10), 23)
    tc.assertEqual(multiples_of_3_and_5(500), 57918)
    tc.assertEqual(multiples_of_3_and_5(1000), 233168)


#################################################################################
# EXERCISE 3
#################################################################################
def integer_right_triangles(p):
    triangles = [
        (a, b, c)
        for a in range(1, p)
        for b in range(a, p)
        for c in range(b, p)
        if a ** 2 + b ** 2 == c ** 2 and a + b + c == p
    ]
    return len(triangles)


def test3():
    tc = unittest.TestCase()
    tc.assertEqual(integer_right_triangles(60), 2)
    tc.assertEqual(integer_right_triangles(100), 0)
    tc.assertEqual(integer_right_triangles(180), 3)


#################################################################################
# EXERCISE 4
#################################################################################

# implement this function
def gen_pattern(chars):
    # length of string
    n = len(chars)

    # empty string that will hold pattern
    pattern = ""
    # variable used to splice chars in second half of the pattern
    splicer = 0

    # loops through each row in the diamond pattern
    for row in range(2 * n - 1):
        # row pattern is a loop-level string that concatenates pattern.
        row_pattern = ""
        # if row is equal to n, which means the first row of the second hald of the diamond.
        if row == n:
            # splicer is 2 less than row
            splicer = row - 2
            # add to string from the last character to -splicer -1
            row_pattern += chars[-1 : -splicer - 2 : -1]
            # if this is not 0, or not the last row.
            if splicer != 0:
                # the characters after -splice-1 are concantentaed into row pattern.
                row_pattern += chars[-splicer::]
        # if row is greater than n, indicating rows after rows == n.
        elif row > n:
            # slicer is decreased by one
            splicer -= 1
            # add to string from the last character to -splicer -1
            row_pattern += chars[-1 : -splicer - 2 : -1]
            # if this is not 0, or not the last row.
            if splicer != 0:
                # the characters after -splice-1 are concantentaed into row pattern.
                row_pattern += chars[-splicer::]
        # if rows are in first half of diamond
        else:
            ##add to row_pattern from the last character to -splicer -1
            row_pattern += chars[-1 : -row - 2 : -1]
            # if this is not 0, the first row.
            if row != 0:
                # the characters after -row-1 are concantentaed into row pattern.
                row_pattern += chars[-row::]
        # "." are joined to row_pattern
        row_pattern = ".".join(row_pattern)
        # the row pattern in centered with dots
        row_pattern = row_pattern.center(1 + (n - 1) * 4, ".")
        # row_pattern is concatenated into pattern.
        pattern += row_pattern
        # new line character added to pattern.
        pattern += "\n"
    # pattern is printed.
    print(pattern)


def test4():
    tc = unittest.TestCase()
    with captured_output() as (out, err):
        gen_pattern("@")
        tc.assertEqual(out.getvalue().strip(), "@")
    with captured_output() as (out, err):
        gen_pattern("@%")
        tc.assertEqual(
            out.getvalue().strip(),
            """
..%..
%.@.%
..%..
""".strip(),
        )
    with captured_output() as (out, err):
        gen_pattern("ABC")
        tc.assertEqual(
            out.getvalue().strip(),
            """
....C....
..C.B.C..
C.B.A.B.C
..C.B.C..
....C....
""".strip(),
        )
    with captured_output() as (out, err):
        gen_pattern("#####")
        tc.assertEqual(
            out.getvalue().strip(),
            """
........#........
......#.#.#......
....#.#.#.#.#....
..#.#.#.#.#.#.#..
#.#.#.#.#.#.#.#.#
..#.#.#.#.#.#.#..
....#.#.#.#.#....
......#.#.#......
........#........
""".strip(),
        )
    with captured_output() as (out, err):
        gen_pattern("abcdefghijklmnop")
        tc.assertEqual(
            out.getvalue().strip(),
            """
..............................p..............................
............................p.o.p............................
..........................p.o.n.o.p..........................
........................p.o.n.m.n.o.p........................
......................p.o.n.m.l.m.n.o.p......................
....................p.o.n.m.l.k.l.m.n.o.p....................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
....................p.o.n.m.l.k.l.m.n.o.p....................
......................p.o.n.m.l.m.n.o.p......................
........................p.o.n.m.n.o.p........................
..........................p.o.n.o.p..........................
............................p.o.p............................
..............................p..............................
""".strip(),
        )


#################################################################################
# RUN ALL TESTS
#################################################################################
def main():
    test1()
    test2()
    test3()
    test4()


if __name__ == "__main__":
    main()

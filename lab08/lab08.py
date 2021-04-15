from unittest import TestCase
import random
import functools

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################


class Heap:
    def __init__(self, key=lambda x: x):
        self.data = []
        self.key = key

    @staticmethod
    def _parent(idx):
        return (idx - 1) // 2

    @staticmethod
    def _left(idx):
        return idx * 2 + 1

    @staticmethod
    def _right(idx):
        return idx * 2 + 2

    # check if element there in list
    def pos_exists(self, n):
        return n < len(self)

    # switch node conducts switch if there needs to be a switch conducted between parent and child
    def switch_node(self, parent, child):
        parentval = self.data[parent]
        childval = self.data[child]
        self.data[parent] = childval
        self.data[child] = parentval

    # tricklc_down used to move down element to correct position.
    def trickle_down(self, n):
        # get indices of left and right child
        lc = Heap._left(n)
        rc = Heap._right(n)

        # current value
        curval = self.key(self.data[n])

        # if the left child exists, so full binary tree.
        if self.pos_exists(lc):
            # if the right child element exists
            if self.pos_exists(rc):
                # get right child and left child values
                lcval = self.key(self.data[lc])
                rcval = self.key(self.data[rc])

                # if left child or right child is greater than curval.
                if lcval > curval or rcval > curval:
                    # if left child is greater than right child, ensures that greatest val becomes parent
                    if lcval > rcval:
                        # print("switch with left")
                        # switch parent(curval) and left child
                        self.switch_node(n, lc)

                        # curvall is new left-child, see if this left child has children and the positions are appropriate
                        self.trickle_down(lc)
                    else:
                        # if right child is greater than left child, right child switch with parent curval is performed
                        self.switch_node(n, rc)

                        # curvall is new right-child, see if this left child has children and the positions are appropriate
                        self.trickle_down(rc)
            # if right child doesnt exist, but heap is full because left child exists.
            else:
                # left-child's val is get
                lcval = self.key(self.data[lc])
                # if left and only child is greater than curval
                if lcval > curval:
                    # if left and only child is greater than left child, right child switch with parent curval is performed
                    self.switch_node(n, lc)

                    # curvall is new left-child, see if this left child has children and the positions are appropriate
                    self.trickle_down(lc)

        # if right child position exists, fixes illegal structure.
        elif self.pos_exists(rc):
            # right child value is gotten
            rcval = self.data[rc]
            # if right child is greater than curval
            if rcval > curval:
                # switch
                self.switch_node(n, rc)

                # if curval in new position has children and it fits correct position.
                self.trickle_down(rc)

    # for the purpose of moving up value at append.
    def trickle_up(self, n):
        # if index is greater than 0, because then only you can trickle_up
        if n > 0:
            # parent index of element
            p = Heap._parent(n)

            # get parent val
            pval = self.key(self.data[p])

            # get curval
            curval = self.key(self.data[n])

            # if curent is greater than parent.
            if pval < curval:
                # switch val.
                self.switch_node(p, n)

                # check if curval(new parent of node), has another parent and if that parent is greater.
                self.trickle_up(p)

    def heapify(self, idx=0):
        # BEGIN SOLUTION
        # if idx = 0, then trickle_down
        # checks if len is greater than 0 because you only trickle down when you pop, because you add the last element to the first
        # if you deleted last and only element, no point in trickle_down, which looks at the index at top usually.
        if idx == 0 and len(self) != 0:
            self.trickle_down(idx)
        else:
            self.trickle_up(idx)
            # END SOLUTION

    def add(self, x):
        # BEGIN SOLUTION
        self.data.append(x)
        self.heapify(len(self) - 1)
        # END SOLUTION

    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data) - 1]
        del self.data[len(self.data) - 1]
        self.heapify()
        return ret

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################

# (6 point)
def test_key_heap_1():
    from unittest import TestCase
    import random

    tc = TestCase()
    h = Heap()

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])


# (6 point)
def test_key_heap_2():
    tc = TestCase()
    h = Heap(lambda x: -x)

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])


# (6 points)
def test_key_heap_3():
    tc = TestCase()
    h = Heap(lambda s: len(s))

    h.add("hello")
    h.add("hi")
    h.add("abracadabra")
    h.add("supercalifragilisticexpialidocious")
    h.add("0")

    tc.assertEqual(
        h.data,
        ["supercalifragilisticexpialidocious", "abracadabra", "hello", "hi", "0"],
    )


# (6 points)
def test_key_heap_4():
    tc = TestCase()
    h = Heap()

    random.seed(0)
    lst = list(range(-1000, 1000))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in range(999, -1000, -1):
        tc.assertEqual(x, h.pop())


# (6 points)
def test_key_heap_5():
    tc = TestCase()
    h = Heap(key=lambda x: abs(x))

    random.seed(0)
    lst = list(range(-1000, 1000, 3))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x: abs(x))):
        tc.assertEqual(x, h.pop())


################################################################################
# 2. MEDIAN
################################################################################
def running_medians(iterable):
    # BEGIN SOLUTION
    # maximum values
    max_heap = Heap(key=lambda x: -x)

    # smaller values:
    min_heap = Heap()

    # makes the iterable a list
    vals = list(iterable)

    # current median of running median
    median_lst = [vals[0]]

    # add to top of min values:
    min_heap.add(vals[0])

    # running median so has to be as values are examined in iterable.
    # therefore first value is always median because no other value is seen yet from the iterable.
    # Have to iterate through each one which is the forloop
    for val in vals[1:]:
        # if value is greater than median, add to max_heap
        if val > min_heap.peek():
            max_heap.add(val)
        # if value is less than median.
        else:
            min_heap.add(val)
        # if length of min is greater than 1 than max.
        if len(min_heap) > len(max_heap) + 1:
            max_heap.add(min_heap.pop())

        # if length of max is greater than 1 than min.
        elif len(max_heap) > len(min_heap) + 1:
            min_heap.add(max_heap.pop())

        # if length of both are equal indicating even number of list.
        if len(max_heap) == len(min_heap):
            median_lst.append((max_heap.peek() + min_heap.peek())/2)
        # if len of max_heap greater, clearly its peak has median because cross each out, 1 extra left.
        elif len(max_heap) > len(min_heap):
            median_lst.append(max_heap.peek())
        # if len of min_heap greater, clearly its peak has median because cross each out, 1 extra left.
        else:
            median_lst.append(min_heap.peek())
    # running median_lst is returned.
    return median_lst
    ################################################################################
    # TESTS
    ################################################################################


def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i % 2 == 0:
            medians.append(values[i // 2])
        else:
            medians.append((values[i // 2] + values[i // 2 + 1]) / 2)
    return medians


# (13 points)
def test_median_1():
    tc = TestCase()
    tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))


# (13 points)
def test_median_2():
    tc = TestCase()
    vals = [random.randrange(10000) for _ in range(1000)]
    tc.assertEqual(running_medians_naive(vals), running_medians(vals))


# MUST COMPLETE IN UNDER 10 seconds!
# (14 points)
def test_median_3():
    tc = TestCase()
    vals = [random.randrange(100000) for _ in range(100001)]
    m_mid = sorted(vals[:50001])[50001 // 2]
    m_final = sorted(vals)[len(vals) // 2]
    running = running_medians(vals)
    tc.assertEqual(m_mid, running[50000])
    tc.assertEqual(m_final, running[-1])


################################################################################
# 3. TOP-K
################################################################################
def topk(items, k, keyf):
    # BEGIN SOLUTION
    # heap stored students:
    # keeps minimum student at top
    # keyf gives the score, while x is plugged in.
    top_students = Heap(key=lambda x: -keyf(x))

    # adds the first k students to heap
    for i in range(k):
        top_students.add(items[i])
    for item in items[k:]:
        # if current item is greater than minimum in heap
        if keyf(item) > keyf(top_students.peek()):
            # minimum is popped.
            # because popping and adding, the number stays the same.
            top_students.pop()
            top_students.add(item)
    # return top_students in reverse, with highest first.
    return top_students.data[::-1]
    # END SOLUTION


################################################################################
# TESTS
################################################################################
def get_age(s):
    return s[1]


def naive_topk(l, k, keyf):
    def revkey(x): return keyf(x) * -1
    return sorted(l, key=revkey)[0:k]


# (30 points)
def test_topk_students():
    tc = TestCase()
    students = [("Peter", 33), ("Bob", 23), ("Alice", 21), ("Gertrud", 53)]

    tc.assertEqual(naive_topk(students, 2, get_age),
                   topk(students, 2, get_age))

    tc.assertEqual(naive_topk(students, 1, get_age),
                   topk(students, 1, get_age))

    tc.assertEqual(naive_topk(students, 3, get_age),
                   topk(students, 3, get_age))


################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)


def say_success():
    print("SUCCESS")


################################################################################
# MAIN
################################################################################
def main():
    for t in [
        test_key_heap_1,
        test_key_heap_2,
        test_key_heap_3,
        test_key_heap_4,
        test_key_heap_5,
        test_median_1,
        test_median_2,
        test_median_3,
        test_topk_students,
    ]:
        say_test(t)
        t()
        say_success()


if __name__ == "__main__":
    main()

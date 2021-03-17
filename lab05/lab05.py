from unittest import TestCase
import random

################################################################################
# Linked list class you should implement
class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next = next

    def __init__(self):
        self.head = LinkedList.Node(None)  # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head  # set up "circular" topology
        self.cursor = self.head
        self.length = 0

    ### prepend and append, below, from class discussion

    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1

    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1

    ### subscript-based access ###

    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx

    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        # solve get_item in n/2
        assert isinstance(idx, int)
        ### BEGIN SOLUTION
        # normalize_idx
        nidx = self._normalize_idx(idx)

        # if index is greater than length, raise error
        if self.length == 0 or nidx >= self.length:
            raise IndexError

        # mid index of double-linked list
        mid = self.length // 2
        # if index is greater than or equal to mid, use next and loop through second half of list with prior.
        # when you use prior you start with the end list, by referring to self.head.next.prior.
        if nidx >= mid:
            n = self.head.next.prior
            # for elements from the end to the indexed element.
            for i in range(self.length, nidx, -1):
                # n is set to the previous element, until reaches indexed element
                n = n.prior
            # indexed element is returned.
            return n.val
        # if index is less than mid, refer to next element to head(head is not really an element).
        else:
            # 1st element
            n = self.head.next
            for i in range(nidx):
                n = n.next
            return n.val
        ### END SOLUTION

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert isinstance(idx, int)
        ### BEGIN SOLUTION
        nidx = self._normalize_idx(idx)

        # if index is greater than length, raise error
        if self.length == 0 or nidx >= self.length:
            raise IndexError

        # mid index of double-linked list
        mid = self.length // 2
        # if index is greater than or equal to mid, use next and loop through second half of list with prior.
        # when you use prior you start with the end list, by referring to self.head.next.prior.
        if nidx >= mid:
            n = self.head.next.prior
            # for elements from the end to the indexed element.
            for i in range(self.length, nidx, -1):
                # n is set to the previous element, until reaches indexed element
                n = n.prior
            # indexed element is found.
        # if index is less than mid, refer to next element to head(head is not really an element).
        else:
            # 1st element
            n = self.head.next
            for i in range(0, nidx):
                n = n.next

        # element's value is set.
        n.val = value
        ### END SOLUTION

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert isinstance(idx, int)
        ### BEGIN SOLUTION
        nidx = self._normalize_idx(idx)

        # if index is greater than length, raise error
        if self.length == 0 or nidx >= self.length:
            raise IndexError

        # mid index of double-linked list
        mid = self.length // 2
        # if index is greater than or equal to mid, use next and loop through second half of list with prior.
        # when you use prior you start with the end list, by referring to self.head.next.prior.
        if nidx >= mid:
            n = self.head.next.prior
            # for elements from the end to the indexed element.
            for i in range(self.length, nidx, -1):
                # n is set to the previous element, until reaches indexed element
                n = n.prior
            # indexed element is found.
        # if index is less than mid, refer to next element to head(head is not really an element).
        else:
            # 1st element
            n = self.head.next
            for i in range(0, nidx):
                n = n.next

        # previous to element of index.
        prev_n = n.prior

        # previous to element of index, it's next is set to the next of the indexed element
        # this is making it so that the previous element has no connection to the indexed element.
        prev_n.next = n.next

        # the element after the indexed element is set to have a prior to the element before the indexed element
        n.next.prior = prev_n

        # cuts off links of indexed elements, so cannot be accessed again.

        # because element is deleted, then length of the list is reduced.
        self.length += -1
        ### END SOLUTION

    ### cursor-based access ###

    def cursor_get(self):
        """retrieves the value at the current cursor position"""
        assert self.cursor is not self.head
        ### BEGIN SOLUTION
        return self.cursor.val
        ### END SOLUTION

    def cursor_set(self, idx):
        """sets the cursor to the node at the provided index"""
        ### BEGIN SOLUTION
        nidx = self._normalize_idx(idx)

        # if index is greater than length, raise error
        if nidx >= self.length or self.length == 0:
            raise IndexError

        # mid index of double-linked list
        mid = self.length // 2
        # if index is greater than or equal to mid, use next and loop through second half of list with prior.
        # when you use prior you start with the end list, by referring to self.head.next.prior.
        if nidx >= mid:
            n = self.head.next.prior
            # for elements from the end to the indexed element.
            for i in range(self.length, nidx, -1):
                # n is set to the previous element, until reaches indexed element
                n = n.prior
            # indexed element is found.
        # if index is less than mid, refer to next element to head(head is not really an element).
        else:
            # 1st element
            n = self.head.next
            for i in range(0, nidx):
                n = n.next
        # sets cursor to node at index.
        self.cursor = n
        ### END SOLUTION

    def cursor_move(self, offset):
        """moves the cursor forward or backward by the provided offset
        (a positive or negative integer); note that it is possible to advance
        the cursor by further than the length of the list, in which case the
        cursor will just "wrap around" the list, skipping over the sentinel
        node as needed"""
        assert len(self) > 0
        ### BEGIN SOLUTION

        # cursor
        n = self.cursor
        # if offset is greater than 0, move forward
        if offset > 0:
            for i in range(offset):
                if n.next is self.head:
                    n = n.next.next
                else:
                    n = n.next
        # if have to move backward
        else:
            for i in range(-1 * offset):
                if n.prior is self.head:
                    n = n.prior.prior
                else:
                    n = n.prior
        self.cursor = n

        ### END SOLUTION

    def cursor_insert(self, value):
        """inserts a new value after the cursor and sets the cursor to the
        new node"""
        ### BEGIN SOLUTION
        # new node is created.
        node = LinkedList.Node(value, self.cursor, self.cursor.next)
        self.cursor.next.prior = self.cursor.next = node
        self.length += 1
        self.cursor = self.cursor.next
        ### END SOLUTION

    def cursor_delete(self):
        """deletes the node the cursor refers to and sets the cursor to the
        following node"""
        assert self.cursor is not self.head and len(self) > 0
        ### BEGIN SOLUTION
        # sets the prior to cursor's next to the element after the element being deleted.
        self.cursor.prior.next = self.cursor.next
        # sets the cursor's next's prior the prior of cursor.
        self.cursor.next.prior = self.cursor.prior

        # moves the cursor to the next element
        self.cursor = self.cursor.next

        # a node was deleted so length decreases.
        self.length += -1
        ### END SOLUTION

    ### stringification ###

    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        ### BEGIN SOLUTION
        return "[" + ", ".join(str(x) for x in self) + "]"
        ### END SOLUTION

    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        ### BEGIN SOLUTION
        return str(self)
        ### END SOLUTION

    ### single-element manipulation ###

    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        ### BEGIN SOLUTION
        nidx = self._normalize_idx(idx)

        # if index is greater than length, raise error
        if nidx > self.length:
            raise IndexError

        if nidx == self.length:
            self.append(value)

        elif nidx == 0:
            self.prepend(value)
        else:
            # mid index of double-linked list
            mid = self.length // 2
            # if index is greater than or equal to mid, use next and loop through second half of list with prior.
            # when you use prior you start with the end list, by referring to self.head.next.prior.
            if nidx >= mid:
                n = self.head.next.prior
                # for elements from the end to the indexed element.
                for i in range(self.length, nidx, -1):
                    # n is set to the previous element, until reaches indexed element
                    n = n.prior
                # indexed element is found.
                # if index is less than mid, refer to next element to head(head is not really an element).
            else:
                # 1st element
                n = self.head.next
                for i in range(0, nidx):
                    n = n.next
            # n is the current element at idx.
            # so create a new element
            node = LinkedList.Node(value, prior=n.prior, next=n)

            # set n's previous element's next to node, so before n.
            n.prior.next = node

            # set before n, node
            n.prior = node

            # length increases by 1
            self.length += 1
            ### END SOLUTION

    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        ### BEGIN SOLUTION
        last_elem = self[idx]
        del self[idx]
        return last_elem

        ### END SOLUTION

    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        ### BEGIN SOLUTION
        if value not in self:
            raise ValueError
        else:
            for i in range(self.length):
                if self[i] == value:
                    del self[i]
                    break
        ### END SOLUTION

    ### predicates (T/F queries) ###

    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        ### BEGIN SOLUTION
        # if self and other aren't the same lengths, they can't be equal to each other.
        if self.length != other.length:
            return False
        else:
            # if they are a linked list and are they same list, theay are checked to have the same values.
            for i in range(self.length):
                # can use this because get item is implemented in this class so can access index.
                if self[i] != other[i]:
                    return False
            return True
        ### END SOLUTION

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        ### BEGIN SOLUTION
        # for each node in linkedlist
        for i in range(self.length):
            # if the node's value equals the value, then it is found in the list, so True is returned.
            if self[i] == value:
                return True
        # else False is returned.
        return False
        ### END SOLUTION

    ### queries ###

    def __len__(self):
        """Implements `len(self)`"""
        return self.length

    def min(self):
        """Returns the minimum value in this list."""
        ### BEGIN SOLUTION
        min = self.head.next.val
        for i in range(self.length):
            if self[i] < min:
                min = self[i]
        return min
        ### END SOLUTION

    def max(self):
        """Returns the maximum value in this list."""
        ### BEGIN SOLUTION
        max = self.head.next.val
        for i in range(self.length):
            if self[i] > max:
                max = self[i]
        return max
        ### END SOLUTION

    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        ### BEGIN SOLUTION
        i = self._normalize_idx(i)
        if j is None:
            for idx in range(i, self.length):
                if self[idx] == value:
                    return idx
            raise ValueError
        else:
            j = self._normalize_idx(j)
            for idx in range(i, j):
                if self[idx] == value:
                    return idx
            raise ValueError
        ### END SOLUTION

    def count(self, value):
        """Returns the number of times value appears in this list."""
        ### BEGIN SOLUTION
        count = 0
        for i in range(self.length):
            if self[i] == value:
                count += 1
        return count
        ### END SOLUTION

    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those
        of other."""
        assert isinstance(other, LinkedList)
        ### BEGIN SOLUTION
        # don't need do delete because head from other won't carry over because extend uses built in iter,
        # which only yields a value of each element.
        self.extend(other)
        return self
        ### END SOLUTION

    def clear(self):
        """Removes all elements from this list."""
        ### BEGIN SOLUTION
        # while there are nodes other than head, delete the last element.
        while self.length > 0:
            del self[self.length - 1]
        ### END SOLUTION

    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        ### BEGIN SOLUTION
        # just return
        new_list = LinkedList()
        for val in self:
            new_list.append(val)
        return new_list
        ### END SOLUTION

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        ### BEGIN SOLUTION
        for value in other:
            self.append(value)
        ### END SOLUTION

    ### iteration ###
    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        ### BEGIN SOLUTION
        n = self.head.next
        while n is not self.head:
            yield n.val
            n = n.next
        ### END SOLUTION

    ### reverse ###
    def reverse(self):
        """Return a copy of the list with all elements in reverse order.
        E.g., for [1,2,3] you shoudl return [3,2,1].
        """
        ### BEGIN SOLUTION
        # new list
        rev_lst = LinkedList()
        # for val in self, prepend for reverse.
        for val in self:
            rev_lst.prepend(val)
        # return list
        return rev_lst
        ### END SOLUTION


################################################################################
# TEST CASES
################################################################################

################################################################################
def say_test(mess):
    print(80 * "*" + "\n" + mess)


def say_success():
    print("SUCCESS")


################################################################################
# (11 points) test subscript-based access
def test_subscript_access():
    say_test("test_subscript_access")
    tc = TestCase()
    data = [1, 2, 3, 4]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    with tc.assertRaises(IndexError):
        x = lst[100]

    with tc.assertRaises(IndexError):
        lst[100] = 0

    with tc.assertRaises(IndexError):
        del lst[100]

    lst[1] = data[1] = 20
    del data[0]
    del lst[0]

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    data = [random.randint(1, 100) for _ in range(100)]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    for i in range(len(data)):
        lst[i] = data[i] = random.randint(101, 200)
    for i in range(50):
        to_del = random.randrange(len(data))
        del lst[to_del]
        del data[to_del]

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    for i in range(0, -len(data), -1):
        tc.assertEqual(lst[i], data[i])


################################################################################
### (12 points) test cursor-based access
def test_custor_based_access():
    say_test("test_custor_based_access")
    tc = TestCase()

    ## insert a bunch of values at different cursor positions

    lst1 = []
    lst2 = LinkedList()
    for _ in range(100):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    for _ in range(10):
        pos = random.randrange(len(lst1))
        vals = [random.randrange(1000) for _ in range(10)]
        lst1[pos + 1 : pos + 1] = vals
        lst2.cursor_set(pos)
        for x in vals:
            lst2.cursor_insert(x)

    assert len(lst1) == len(lst2)
    for i in range(len(lst1)):
        assert lst1[i] == lst2[i]

    ## move the cursor around and check that values are correct

    lst1 = []
    lst2 = LinkedList()
    for _ in range(100):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    idx = 0
    lst2.cursor_set(0)
    for _ in range(100):
        offset = random.randrange(-200, 200)
        idx = (idx + offset) % 100
        lst2.cursor_move(offset)
        assert lst1[idx] == lst2.cursor_get()

    ## move the cursor around and delete values at the cursor

    lst1 = []
    lst2 = LinkedList()
    for _ in range(500):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    idx = 0
    lst2.cursor_set(0)
    for _ in range(100):
        offset = random.randrange(-200, 200)
        idx = (idx + offset) % len(lst1)
        lst2.cursor_move(offset)
        del lst1[idx]
        lst2.cursor_delete()

    assert len(lst1) == len(lst2)
    for i in range(len(lst1)):
        assert lst1[i] == lst2[i]


################################################################################
# (11 points) test stringification
def test_stringification():
    say_test("test_stringification")
    tc = TestCase()

    lst = LinkedList()
    tc.assertEqual("[]", str(lst))
    tc.assertEqual("[]", repr(lst))

    lst.append(1)
    tc.assertEqual("[1]", str(lst))
    tc.assertEqual("[1]", repr(lst))

    lst = LinkedList()
    for d in (10, 20, 30, 40, 50):
        lst.append(d)
    tc.assertEqual("[10, 20, 30, 40, 50]", str(lst))
    tc.assertEqual("[10, 20, 30, 40, 50]", repr(lst))


################################################################################
# (11 points) test single-element manipulation
def test_single_element_manipulation():
    say_test("test_single_element_manipulation")
    tc = TestCase()
    lst = LinkedList()
    data = []

    for _ in range(100):
        to_ins = random.randrange(1000)
        ins_idx = random.randrange(len(data) + 1)
        data.insert(ins_idx, to_ins)
        lst.insert(ins_idx, to_ins)

    for i in range(100):
        tc.assertEqual(data[i], lst[i])

    for _ in range(50):
        pop_idx = random.randrange(len(data))
        tc.assertEqual(data.pop(pop_idx), lst.pop(pop_idx))

    for i in range(50):
        tc.assertEqual(data[i], lst[i])

    for _ in range(25):
        to_rem = data[random.randrange(len(data))]
        data.remove(to_rem)
        lst.remove(to_rem)

    for i in range(25):
        tc.assertEqual(data[i], lst[i])

    with tc.assertRaises(ValueError):
        lst.remove(9999)


################################################################################
# (11 points) test predicates
def test_predicates():
    say_test("test_predicates")
    tc = TestCase()
    lst = LinkedList()
    lst2 = LinkedList()

    tc.assertEqual(lst, lst2)

    lst2.append(100)
    tc.assertNotEqual(lst, lst2)

    lst.append(100)
    tc.assertEqual(lst, lst2)

    tc.assertFalse(1 in lst)
    tc.assertFalse(None in lst)

    lst = LinkedList()
    for i in range(100):
        lst.append(i)
    tc.assertFalse(100 in lst)
    tc.assertTrue(50 in lst)


################################################################################
# (11 points) test queries
def test_queries():
    say_test("test_queries")
    tc = TestCase()
    lst = LinkedList()

    tc.assertEqual(0, len(lst))
    tc.assertEqual(0, lst.count(1))
    with tc.assertRaises(ValueError):
        lst.index(1)

    import random

    data = [random.randrange(1000) for _ in range(100)]
    for d in data:
        lst.append(d)

    tc.assertEqual(100, len(lst))
    tc.assertEqual(min(data), lst.min())
    tc.assertEqual(max(data), lst.max())
    for x in data:
        tc.assertEqual(data.index(x), lst.index(x))
        tc.assertEqual(data.count(x), lst.count(x))

    with tc.assertRaises(ValueError):
        lst.index(1000)

    lst = LinkedList()
    for d in (1, 2, 1, 2, 1, 1, 1, 2, 1):
        lst.append(d)
    tc.assertEqual(1, lst.index(2))
    tc.assertEqual(1, lst.index(2, 1))
    tc.assertEqual(3, lst.index(2, 2))
    tc.assertEqual(7, lst.index(2, 4))
    tc.assertEqual(7, lst.index(2, 4, -1))
    with tc.assertRaises(ValueError):
        lst.index(2, 4, -2)


################################################################################
# (11 points) test bulk operations
def test_bulk_operations():
    say_test("test_bulk_operations")
    tc = TestCase()
    lst = LinkedList()
    lst2 = LinkedList()
    lst3 = lst + lst2

    tc.assertIsInstance(lst3, LinkedList)
    tc.assertEqual(0, len(lst3))

    import random

    data = [random.randrange(1000) for _ in range(50)]
    data2 = [random.randrange(1000) for _ in range(50)]
    for d in data:
        lst.append(d)
    for d in data2:
        lst2.append(d)
    lst3 = lst + lst2
    tc.assertEqual(100, len(lst3))
    data3 = data + data2
    for i in range(len(data3)):
        tc.assertEqual(data3[i], lst3[i])

    lst.clear()
    tc.assertEqual(0, len(lst))
    with tc.assertRaises(IndexError):
        lst[0]

    for d in data:
        lst.append(d)
    lst2 = lst.copy()
    tc.assertIsNot(lst, lst2)
    tc.assertIsNot(lst.head.next, lst2.head.next)
    for i in range(len(data)):
        tc.assertEqual(lst[i], lst2[i])
    tc.assertEqual(lst, lst2)

    lst.clear()
    lst.extend(range(10))
    lst.extend(range(10, 0, -1))
    lst.extend(data.copy())
    tc.assertEqual(70, len(lst))

    data = list(range(10)) + list(range(10, 0, -1)) + data
    for i in range(len(data)):
        tc.assertEqual(data[i], lst[i])


################################################################################
# (11 points) test iteration
def test_iteration():
    say_test("test_iteration")
    tc = TestCase()
    lst = LinkedList()

    import random

    data = [random.randrange(1000) for _ in range(100)]
    lst = LinkedList()
    for d in data:
        lst.append(d)
    tc.assertEqual(data, [x for x in lst])

    it1 = iter(lst)
    it2 = iter(lst)
    for x in data:
        tc.assertEqual(next(it1), x)
        tc.assertEqual(next(it2), x)


################################################################################
# (11 points) test reverse
def test_reverse():
    say_test("test_reverse")
    tc = TestCase()
    lst = LinkedList()

    import random

    data = [random.randrange(1000) for _ in range(20)]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    rev = lst.reverse()
    for i in range(0, len(data)):
        tc.assertEqual(lst[i], rev[len(data) - i - 1])


################################################################################
# MAIN
def main():
    test_subscript_access()
    say_success()
    test_custor_based_access()
    say_success()
    test_stringification()
    say_success()
    test_single_element_manipulation()
    say_success()
    test_predicates()
    say_success()
    test_queries()
    say_success()
    test_bulk_operations()
    say_success()
    test_iteration()
    say_success()
    test_reverse()
    say_success()


if __name__ == "__main__":
    main()

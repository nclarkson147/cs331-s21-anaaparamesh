from unittest import TestCase


################################################################################
# STACK IMPLEMENTATION (DO NOT MODIFY THIS CODE)
################################################################################
class Stack:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def __init__(self):
        self.top = None

    def push(self, val):
        self.top = Stack.Node(val, self.top)

    def pop(self):
        assert self.top, "Stack is empty"
        val = self.top.val
        self.top = self.top.next
        return val

    def peek(self):
        return self.top.val if self.top else None

    def empty(self):
        return self.top == None

    def __bool__(self):
        return not self.empty()

    def __repr__(self):
        if not self.top:
            return ""
        return "--> " + ", ".join(str(x) for x in self)

    def __iter__(self):
        n = self.top
        while n:
            yield n.val
            n = n.next


################################################################################
# CHECK DELIMITERS
################################################################################
def check_delimiters(expr):
    """Returns True if and only if `expr` contains only correctly matched delimiters, else returns False."""
    delim_openers = "{([<"
    delim_closers = "})]>"

    ### BEGIN SOLUTION
    # new stack.
    s = Stack()

    # for each delim in the expr.
    for delim in expr:
        # if delim is opening, push delim.
        if delim in delim_openers:
            s.push(delim)
        # if delim is closing.
        elif delim in delim_closers:
            # if stack is not empty, meaning it has opening delims.
            if not s.empty():
                # if delim_index in closers matches the top most in stack. ex. index ">" == "<"
                if delim_closers.index(delim) == delim_openers.index(s.peek()):
                    # then pop.
                    s.pop()
            # if stack is empty, or if first or statement left is closing.
            else:
                # push delim, nothing done to opening because doesn't make sense if opening delim comes after.
                s.push(delim)
    # if stack is empty, no delimeter errors.
    return s.empty()

    ### END SOLUTION


################################################################################
# CHECK DELIMITERS - TEST CASES
################################################################################
# points: 5
def test_check_delimiters_1():
    tc = TestCase()
    tc.assertTrue(check_delimiters("()"))
    tc.assertTrue(check_delimiters("[]"))
    tc.assertTrue(check_delimiters("{}"))
    tc.assertTrue(check_delimiters("<>"))


# points:5
def test_check_delimiters_2():
    tc = TestCase()
    tc.assertTrue(check_delimiters("([])"))
    tc.assertTrue(check_delimiters("[{}]"))
    tc.assertTrue(check_delimiters("{<()>}"))
    tc.assertTrue(check_delimiters("<({[]})>"))


# points: 5
def test_check_delimiters_3():
    tc = TestCase()
    tc.assertTrue(check_delimiters("([] () <> [])"))
    tc.assertTrue(check_delimiters("[{()} [] (<> <>) {}]"))
    tc.assertTrue(check_delimiters("{} <> () []"))
    tc.assertTrue(check_delimiters("<> ([] <()>) <[] [] <> <>>"))


# points: 5
def test_check_delimiters_4():
    tc = TestCase()
    tc.assertFalse(check_delimiters("("))
    tc.assertFalse(check_delimiters("["))
    tc.assertFalse(check_delimiters("{"))
    tc.assertFalse(check_delimiters("<"))
    tc.assertFalse(check_delimiters(")"))
    tc.assertFalse(check_delimiters("]"))
    tc.assertFalse(check_delimiters("}"))
    tc.assertFalse(check_delimiters(">"))


# points: 5
def test_check_delimiters_5():
    tc = TestCase()
    tc.assertFalse(check_delimiters("( ]"))
    tc.assertFalse(check_delimiters("[ )"))
    tc.assertFalse(check_delimiters("{ >"))
    tc.assertFalse(check_delimiters("< )"))


# points: 5
def test_check_delimiters_6():
    tc = TestCase()
    tc.assertFalse(check_delimiters("[ ( ] )"))
    tc.assertFalse(check_delimiters("((((((( ))))))"))
    tc.assertFalse(check_delimiters("< < > > >"))
    tc.assertFalse(check_delimiters("( [] < {} )"))


################################################################################
# INFIX -> POSTFIX CONVERSION
################################################################################


def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    # you may find the following precedence dictionary useful
    # keeps the order of operations.
    prec = {"*": 2, "/": 2, "+": 1, "-": 1}
    # stack holding operations.
    ops = Stack()
    # holds final string.
    postfix = []

    # each element in operation.
    toks = expr.split()
    ### BEGIN SOLUTION

    # for each token
    for tok in toks:
        # if token is a digit append right away cause digits occur before operations.
        if tok.isdigit():
            postfix.append(tok)
        # else.
        else:
            # if ops is empty or if opening parentheses added.
            if ops.empty() or ops.peek() == "(":
                # push the operation.
                ops.push(tok)
            # push openning parantheses.
            elif tok == "(":
                ops.push(tok)
            elif tok == ")":
                # if end paranthesis, add all the operations to append that occur within the parantheses.
                # this deletes the most recent parantheses, keeps the oldest.
                while not (ops.empty() or ops.peek() == "("):
                    postfix.append(ops.pop())
                ops.pop()
            # these next functions make sure order of operations.
            elif prec[tok] > prec[ops.peek()]:
                # if token is multiplication for ex. and peak is add, then multiplication appears first, so top of stack.
                ops.push(tok)
            elif prec[tok] < prec[ops.peek()]:
                # if token is add for ex. and peak is multiplication, then multiplication appears first, so top of stack.
                postfix.append(ops.pop())
                ops.push(tok)
            elif prec[tok] == prec[ops.peek()]:
                # if they are equivalent operations, then what comes first in infix has to be poped first.
                postfix.append(ops.pop())
                ops.push(tok)

    # last expressions or if no having no more numbers left or paranthesis.
    if not ops.empty():
        while not ops.empty():
            if ops.peek() == "(":
                ops.pop()
            else:
                postfix.append(ops.pop())

        ### END SOLUTION
    return " ".join(postfix)


################################################################################
# INFIX -> POSTFIX CONVERSION - TEST CASES
################################################################################

# points: 10
def test_infix_to_postfix_1():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix("1"), "1")
    tc.assertEqual(infix_to_postfix("1 + 2"), "1 2 +")
    tc.assertEqual(infix_to_postfix("( 1 + 2 )"), "1 2 +")
    tc.assertEqual(infix_to_postfix("1 + 2 - 3"), "1 2 + 3 -")
    tc.assertEqual(infix_to_postfix("1 + ( 2 - 3 )"), "1 2 3 - +")


# points: 10
def test_infix_to_postfix_2():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix("1 + 2 * 3"), "1 2 3 * +")
    tc.assertEqual(infix_to_postfix("1 / 2 + 3 * 4"), "1 2 / 3 4 * +")
    tc.assertEqual(infix_to_postfix("1 * 2 * 3 + 4"), "1 2 * 3 * 4 +")
    tc.assertEqual(infix_to_postfix("1 + 2 * 3 * 4"), "1 2 3 * 4 * +")


# points: 10
def test_infix_to_postfix_3():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix("1 * ( 2 + 3 ) * 4"), "1 2 3 + * 4 *")
    tc.assertEqual(infix_to_postfix("1 * ( 2 + 3 * 4 ) + 5"), "1 2 3 4 * + * 5 +")
    tc.assertEqual(
        infix_to_postfix("1 * ( ( 2 + 3 ) * 4 ) * ( 5 - 6 )"), "1 2 3 + 4 * * 5 6 - *"
    )


################################################################################
# QUEUE IMPLEMENTATION
################################################################################
class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    ### BEGIN SOLUTION
    ### END SOLUTION

    def enqueue(self, val):
        ### BEGIN SOLUTION
        # if array's size is not big enough, raise error.
        if self.data.count(None) == 0:
            raise RuntimeError

        # if queue was empty, tail and head increased by one.
        if self.head == -1:
            self.head = 0
        # tail end of the list wraps around.
        self.tail = (self.tail + 1) % len(self.data)

        # self.data.tail the end is set to val.
        self.data[self.tail] = val
        ### END SOLUTION

    def dequeue(self):
        ### BEGIN SOLUTION
        if self.empty():
            raise RuntimeError

        # hold current head for returning.
        val = self.data[self.head]

        # self.head is emptied or set to None.
        self.data[self.head] = None

        # self.head is wrapped around if last element is released
        self.head = (self.head + 1) % len(self.data)

        # if head and tail are the same index, then last element, so dequeing empties queue
        if self.empty():
            self.head = -1
            self.tail = -1

        # val is returned, like pop.
        return val
        ### END SOLUTION

    def resize(self, newsize):
        assert len(self.data) < newsize
        ### BEGIN SOLUTION
        # new array of size newsie
        new_array = [None] * newsize

        # if tail is greater than head, meaning that tail has not been wrapped around yet.
        if self.tail > self.head:
            # new array all the way from head to tail inclusive copied.
            new_array[0 : ((self.tail + 1) - self.head)] = self.data[
                self.head : self.tail + 1
            ]
            # tail is last element before Nones.
            self.tail = self.tail - self.head
            # head is first element.
            self.head = 0
        else:
            # there are no empty space from head to rest of lst if tail is less than head, because tail is wrapped around at this point
            new_array = (
                self.data[self.head :]
                + self.data[: self.tail + 1]
                + [None] * (newsize - len(self.data))
            )
            # head is first element.
            self.head = 0
            # tail is the element before the none
            self.tail = new_array.index(None) - 1
        # self.data is new_array
        self.data = new_array

    def empty(self):
        ### BEGIN SOLUTION
        # if empty all elements will be none.
        return self.data.count(None) == len(self.data)
        ### END SOLUTION

    def __bool__(self):
        return not self.empty()

    def __str__(self):
        if not (self):
            return ""
        return ", ".join(str(x) for x in self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        ### BEGIN SOLUTION
        # for a value in data.
        for x in range(self.head, self.tail + 1):
            yield self.data[x]

        ### END SOLUTION


################################################################################
# QUEUE IMPLEMENTATION - TEST CASES
################################################################################

# points: 13
def test_queue_implementation_1():
    tc = TestCase()

    q = Queue(5)
    tc.assertEqual(q.data, [None] * 5)

    for i in range(5):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(5)

    for i in range(5):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())


# points: 13
def test_queue_implementation_2():
    tc = TestCase()

    q = Queue(10)

    for i in range(6):
        q.enqueue(i)

    tc.assertEqual(q.data.count(None), 4)

    for i in range(5):
        q.dequeue()

    tc.assertFalse(q.empty())
    tc.assertEqual(q.data.count(None), 9)
    tc.assertEqual(q.head, q.tail)
    tc.assertEqual(q.head, 5)

    for i in range(9):

        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    for x, y in zip(q, [5] + list(range(9))):
        tc.assertEqual(x, y)

    tc.assertEqual(q.dequeue(), 5)
    for i in range(9):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())


# points: 14
def test_queue_implementation_3():
    tc = TestCase()

    q = Queue(5)
    for i in range(5):
        q.enqueue(i)
    for i in range(4):
        q.dequeue()
    for i in range(5, 9):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    q.resize(10)

    for x, y in zip(q, range(4, 9)):
        tc.assertEqual(x, y)

    for i in range(9, 14):
        q.enqueue(i)

    for i in range(4, 14):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())
    tc.assertEqual(q.head, -1)


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
        test_check_delimiters_1,
        test_check_delimiters_2,
        test_check_delimiters_3,
        test_check_delimiters_4,
        test_check_delimiters_5,
        test_check_delimiters_6,
        test_infix_to_postfix_1,
        test_infix_to_postfix_2,
        test_infix_to_postfix_3,
        test_queue_implementation_1,
        test_queue_implementation_2,
        test_queue_implementation_3,
    ]:
        say_test(t)
        t()
        say_success()


if __name__ == "__main__":
    main()

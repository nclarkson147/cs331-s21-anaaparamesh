import urllib.request
import unittest
from typing import TypeVar, Callable, List

T = TypeVar("T")
S = TypeVar("S")

#################################################################################
# EXERCISE 1
#################################################################################
def mysort(lst: List[T], compare: Callable[[T, T], int]) -> List[T]:
    """
    This method should sort input list lst of elements of some type T.

    Elements of the list are compared using function compare that takes two
    elements of type T as input and returns -1 if the left is smaller than the
    right element, 1 if the left is larger than the right, and 0 if the two
    elements are equal.
    """
    for i in range(1, len(lst)):  # number of times? n-1
        for j in range(i, 0, -1):  # number 1, 2, 3, 4, ..., n-1
            # compares the element to the element before, if equals to 1, the elements are switched
            if compare(lst[j - 1], lst[j]) == 1:
                lst[j - 1], lst[j] = lst[j], lst[j - 1]
            # else the loop is breaked
            else:
                break
    # lst is returned.
    return lst


def mybinsearch(lst: List[T], elem: S, compare: Callable[[T, S], int]) -> int:
    """
    This method search for elem in lst using binary search.

    The elements of lst are compared using function compare. Returns the
    position of the first (leftmost) match for elem in lst. If elem does not
    exist in lst, then return -1.
    """
    # low
    l = 0
    # high is last index
    h = len(lst) - 1

    # while high is greater than or equal to low
    while h >= l:
        # mid is mid element
        mid = ((h - l) // 2) + l
        # if element and middle element is 0, then mid index is returned.
        if compare(lst[mid], elem) == 0:
            return mid
        # if elem is greater than the middle element, l is 1 greater than mid.
        elif compare(lst[mid], elem) == -1:
            l = mid + 1
        # else high is reduced to less than mid.
        else:
            h = mid - 1
    # if element is not found in list, -1 is returned.
    return -1


class Student:
    """Custom class to test generic sorting and searching."""

    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        return self.name == other.name


# 30 Points (total)
def test1():
    """Tests for generic sorting and binary search."""
    print(80 * "#" + "\nTests for generic sorting and binary search.")
    test1_1()
    test1_2()
    test1_3()
    test1_4()
    test1_5()


# 6 Points
def test1_1():
    """Sort ints."""
    print("\t-sort ints")
    tc = unittest.TestCase()
    ints = [4, 3, 7, 10, 9, 2]
    intcmp = lambda x, y: 0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(sortedints, [2, 3, 4, 7, 9, 10])


# 6 Points
def test1_2():
    """Sort strings based on their last character."""
    print("\t-sort strings on their last character")
    tc = unittest.TestCase()
    strs = ["abcd", "aacz", "zasa"]
    suffixcmp = lambda x, y: 0 if x[-1] == y[-1] else (-1 if x[-1] < y[-1] else 1)
    sortedstrs = mysort(strs, suffixcmp)
    tc.assertEqual(sortedstrs, ["zasa", "abcd", "aacz"])


# 6 Points
def test1_3():
    """Sort students based on their GPA."""
    print("\t-sort students on their GPA.")
    tc = unittest.TestCase()
    students = [
        Student("Josh", 3.0),
        Student("Angela", 2.5),
        Student("Vinesh", 3.8),
        Student("Jia", 3.5),
    ]
    sortedstudents = mysort(
        students, lambda x, y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1)
    )
    expected = [
        Student("Angela", 2.5),
        Student("Josh", 3.0),
        Student("Jia", 3.5),
        Student("Vinesh", 3.8),
    ]
    tc.assertEqual(sortedstudents, expected)


# 6 Points
def test1_4():
    """Binary search for ints."""
    print("\t-binsearch ints")
    tc = unittest.TestCase()
    ints = [4, 3, 7, 10, 9, 2]
    intcmp = lambda x, y: 0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(mybinsearch(sortedints, 3, intcmp), 1)
    tc.assertEqual(mybinsearch(sortedints, 10, intcmp), 5)
    tc.assertEqual(mybinsearch(sortedints, 11, intcmp), -1)


# 6 Points
def test1_5():
    """Binary search for students by gpa."""
    print("\t-binsearch students")
    tc = unittest.TestCase()
    students = [
        Student("Josh", 3.0),
        Student("Angela", 2.5),
        Student("Vinesh", 3.8),
        Student("Jia", 3.5),
    ]
    stcmp = lambda x, y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1)
    stbincmp = lambda x, y: 0 if x.gpa == y else (-1 if x.gpa < y else 1)
    sortedstudents = mysort(students, stcmp)
    tc.assertEqual(mybinsearch(sortedstudents, 3.5, stbincmp), 2)
    tc.assertEqual(mybinsearch(sortedstudents, 3.7, stbincmp), -1)


#################################################################################
# EXERCISE 2
#################################################################################
class PrefixSearcher:
    def __init__(self, document, k):
        """'

        Initializes a prefix searcher using a document and a maximum
        search string length k.
        """
        # data holds list
        self.data = []

        # maximum_length of string in list.
        self.max_length = k

        # document is stored.
        self.document = document

        # for i until the length of the document, the i until max_length is appended as element.
        for i in range(0, len(document)):
            self.data.append(document[i : i + self.max_length])

    def search(self, q):
        """
        Return true if the document contains search string q (of

        length up to n). If q is longer than n, then raise an
        Exception.
        """

        # If q has greater length that max_length.
        if len(q) > self.max_length:
            raise Exception("q is larger than maximum length of substrings")
        else:
            # compare function
            stringcmp = (
                lambda x, y: 0
                if x[: len(q)] == y[: len(q)]
                else (-1 if x[: len(q)] < y[: len(q)] else 1)
            )
            # data is sorted with compare function
            self.data = mysort(self.data, stringcmp)

            # Binary search results are returned.
            return mybinsearch(self.data, q, stringcmp) != -1


# 30 Points
def test2():
    print("#" * 80 + "\nSearch for substrings up to length n")
    test2_1()
    test2_2()


# 15Points
def test2_1():
    print("\t-search in hello world")
    tc = unittest.TestCase()
    p = PrefixSearcher("Hello World!", 1)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("e"))
    tc.assertFalse(p.search("h"))
    tc.assertFalse(p.search("Z"))
    tc.assertFalse(p.search("Y"))
    p = PrefixSearcher("Hello World!", 2)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("ll"))
    tc.assertFalse(p.search("lW"))


# 20 Points
def test2_2():
    print("\t-search in Moby Dick")
    tc = unittest.TestCase()
    md_url = "https://www.gutenberg.org/files/2701/2701-0.txt"
    md_text = urllib.request.urlopen(md_url).read().decode()
    p = PrefixSearcher(md_text[0:1000], 4)
    tc.assertTrue(p.search("Moby"))
    tc.assertTrue(p.search("Dick"))


#################################################################################
# EXERCISE 3
#################################################################################
class SuffixArray:
    def __init__(self, document: str):
        """
        Creates a suffix array for document (a string).
        """
        # suffix_array
        self.suffix_array = []

        # for length of document, index of list to end of document is appended as element to index.
        for i in range(0, len(document)):
            self.suffix_array.append(document[i:])

        # String compare function
        stringcmp = lambda x, y: 0 if x == y else (-1 if x < y else 1)
        self.suffix_array = mysort(self.suffix_array, stringcmp)

    def positions(self, searchstr: str):
        """
        Returns all the positions of searchstr in the documented indexed by the suffix array.
        """
        # String compare function with searchstr.
        stringcmp = (
            lambda x, y: 0
            if x[: len(searchstr)] == y[: len(searchstr)]
            else (-1 if x[: len(searchstr)] < y[: len(searchstr)] else 1)
        )

        # index returned by binary search
        index = mybinsearch(self.suffix_array, searchstr, stringcmp)

        # occurances
        occurances = []

        # if the element is actually in suffix_array:
        if index != -1:
            # checks if there are other occureneces in suffix array.
            while stringcmp(self.suffix_array[index], searchstr) == 0:
                # appends occurences
                occurances.append(index)
                # index is decreased.
                index = index - 1
        # returns occureneces
        return occurances

    def contains(self, searchstr: str):
        """
        Returns true of searchstr is coontained in document.
        """
        # compare string
        stringcmp = (
            lambda x, y: 0
            if x[: len(searchstr)] == y[: len(searchstr)]
            else (-1 if x[: len(searchstr)] < y[: len(searchstr)] else 1)
        )
        # returns if found in binarysearch.
        return mybinsearch(self.suffix_array, searchstr, stringcmp) != -1


# 40 Points
def test3():
    """Test suffix arrays."""
    print(80 * "#" + "\nTest suffix arrays.")
    test3_1()
    test3_2()


# 20 Points
def test3_1():
    print("\t-suffixarray on Hello World!")
    tc = unittest.TestCase()
    s = SuffixArray("Hello World!")
    tc.assertTrue(s.contains("l"))
    tc.assertTrue(s.contains("e"))
    tc.assertFalse(s.contains("h"))
    tc.assertFalse(s.contains("Z"))
    tc.assertFalse(s.contains("Y"))
    tc.assertTrue(s.contains("ello Wo"))


# 20 Points
def test3_2():
    print("\t-suffixarray on Moby Dick!")
    tc = unittest.TestCase()
    md_url = "https://www.gutenberg.org/files/2701/2701-0.txt"
    md_text = urllib.request.urlopen(md_url).read().decode()
    s = SuffixArray(md_text[0:1000])
    tc.assertTrue(s.contains("Moby Dick"))
    tc.assertTrue(s.contains("Herman Melville"))
    tc.assertEqual(s.positions("Moby Dick"), [427])


#################################################################################
# TEST CASES
#################################################################################
def main():
    test1()
    test2()
    test3()


if __name__ == "__main__":
    main()

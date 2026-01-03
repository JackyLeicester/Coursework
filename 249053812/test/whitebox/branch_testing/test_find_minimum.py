import unittest
from find_minimum import MINIMUMVALUE


class MyTestCase(unittest.TestCase):
    def testEmpty(self):
        testcase1 = []
        self.assertEqual(MINIMUMVALUE().find_min(testcase1), 0)

    def testOneElement(self):
        testcase2 = [1]
        self.assertEqual(MINIMUMVALUE().find_min(testcase2), 1)

    def testTwoElements(self):
        testcase3 = [2, 1]
        self.assertEqual(MINIMUMVALUE().find_min(testcase3), 1)

    def testUnorderedShortArray(self):
        testcase4 = [9, 3, 4]
        self.assertEqual(MINIMUMVALUE().find_min(testcase4), 3)

    def testOrderedShortArray(self):
        testcase5 = [3, 4, 9]
        self.assertEqual(MINIMUMVALUE().find_min(testcase5), 3)

    def testUnorderedLongArray(self):
        testcase6 = [5, 1, 3, 4, 6]
        self.assertEqual(MINIMUMVALUE().find_min(testcase6), 1)

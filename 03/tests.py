import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def compare_lists(self, lhs, rhs):
        self.assertEqual(len(lhs), len(rhs))
        for left, right in zip(lhs, rhs):
            self.assertEqual(left, right)

    def test_sub(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1, 3, 5])

        self.compare_lists(list_1 - list_2, [-2, 3, 0, -1])
        self.compare_lists(list_2 - list_1, [2, -3, 0, 1])

        self.compare_lists(CustomList([1, 2, 3, 4]), list_1)
        self.compare_lists(CustomList([3, -1, 3, 5]), list_2)

        list_1 = CustomList([10] * 10)
        list_2 = CustomList([10] * 5)

        self.compare_lists(list_1 - list_2, [0] * 5 + [10] * 5)
        self.compare_lists(list_2 - list_1, [0] * 5 + [-10] * 5)

        self.compare_lists(CustomList([10] * 10), list_1)
        self.compare_lists(CustomList([10] * 5), list_2)

    def test_sub_with_list(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1, 3, 5])

        test_result = [1, 2, 3, 4] - list_2
        self.compare_lists(test_result, [-2, 3, 0, -1])
        self.assertEqual(type(test_result), CustomList)

        test_result = [3, -1, 3, 5] - list_1
        self.compare_lists(test_result, [2, -3, 0, 1])
        self.assertEqual(type(test_result), CustomList)

        self.compare_lists(list_1 - [10] * 10, [-9, -8, -7, -6] + [-10] * 6)
        self.compare_lists([10] * 10 - list_1, [9, 8, 7, 6] + [10] * 6)

        self.compare_lists(CustomList([1, 2, 3, 4]), list_1)
        self.compare_lists(CustomList([3, -1, 3, 5]), list_2)

    def test_sub_empty(self):
        list_1 = CustomList([1] * 10)
        list_2 = CustomList([])

        self.compare_lists(CustomList([]) - CustomList([]), [])
        self.assertEqual(type(CustomList([]) - CustomList([])), CustomList)

        self.compare_lists(list_1 - list_2, [1] * 10)
        self.compare_lists(list_2 - list_1, [-1] * 10)

        self.compare_lists(list_1 - [], [1] * 10)
        self.compare_lists([] - list_1, [-1] * 10)

        self.assertEqual(type(list_1 - []), CustomList)
        self.assertEqual(type([] - list_1), CustomList)

        self.compare_lists(list_2 - [], [])
        self.compare_lists([] - list_2, [])

        self.assertEqual(type(list_2 - []), CustomList)
        self.assertEqual(type([] - list_2), CustomList)

        self.compare_lists(list_1, CustomList([1] * 10))
        self.compare_lists(list_2, CustomList([]))

    def test_add(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1, 3, 5])

        self.compare_lists(list_1 + list_2, [4, 1, 6, 9])
        self.compare_lists(list_2 + list_1, [4, 1, 6, 9])

        self.compare_lists(CustomList([1, 2, 3, 4]), list_1)
        self.compare_lists(CustomList([3, -1, 3, 5]), list_2)

        list_1 = CustomList([10] * 10)
        list_2 = CustomList([10] * 5)

        self.compare_lists(list_1 + list_2, [20] * 5 + [10] * 5)
        self.compare_lists(list_2 + list_1, [20] * 5 + [10] * 5)

        self.compare_lists(CustomList([10] * 10), list_1)
        self.compare_lists(CustomList([10] * 5), list_2)

    def test_add_with_list(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1, 3, 5])

        test_result = [1, 2, 3, 4] + list_2
        self.compare_lists(test_result, [4, 1, 6, 9])
        self.assertEqual(type(test_result), CustomList)

        test_result = [3, -1, 3, 5] + list_1
        self.compare_lists(test_result, [4, 1, 6, 9])
        self.assertEqual(type(test_result), CustomList)

        self.compare_lists(list_1 + [10] * 10, [11, 12, 13, 14] + [10] * 6)
        self.compare_lists([10] * 10 + list_1, [11, 12, 13, 14] + [10] * 6)

        self.compare_lists(CustomList([1, 2, 3, 4]), list_1)
        self.compare_lists(CustomList([3, -1, 3, 5]), list_2)

    def test_add_empty(self):
        list_1 = CustomList([1] * 10)
        list_2 = CustomList([])

        self.compare_lists(CustomList([]) + CustomList([]), [])
        self.assertEqual(type(CustomList([]) + CustomList([])), CustomList)

        self.compare_lists(list_1 + list_2, [1] * 10)
        self.compare_lists(list_2 + list_1, [1] * 10)

        self.compare_lists(list_1 + [], [1] * 10)
        self.compare_lists([] + list_1, [1] * 10)

        self.assertEqual(type(list_1 + []), CustomList)
        self.assertEqual(type([] + list_1), CustomList)

        self.compare_lists(list_2 + [], [])
        self.compare_lists([] + list_2, [])

        self.assertEqual(type(list_2 + []), CustomList)
        self.assertEqual(type([] + list_2), CustomList)

        self.compare_lists(list_1, CustomList([1] * 10))
        self.compare_lists(list_2, CustomList([]))

    def test_lt(self):
        self.assertTrue(CustomList([1, 2]) < CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, 3]) < CustomList([1, 2]))

    def test_le(self):
        self.assertTrue(CustomList([1, 2]) <= CustomList([2, 1]))
        self.assertFalse(CustomList([1, 2, 3]) <= CustomList([1, 2]))

    def test_eq(self):
        self.assertTrue(CustomList([1, 2]) == CustomList([6, -3]))
        self.assertFalse(CustomList([1, 2, 3]) == CustomList([1, 2]))

    def test_ne(self):
        self.assertFalse(CustomList([-1, 4]) != CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2, 3]) != CustomList([1, 2]))

    def test_gt(self):
        self.assertFalse(CustomList([1, 2]) > CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2, 3]) > CustomList([1, 2]))

    def test_ge(self):
        self.assertTrue(CustomList([5, -2]) >= CustomList([1, 2]))
        self.assertFalse(CustomList([1, 2, 3]) >= CustomList([1, 2, 5]))

    def test_str(self):
        test_list = CustomList([1, 2, 3])

        self.assertEqual(str(test_list), "[1, 2, 3], 6")

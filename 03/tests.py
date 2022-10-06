import unittest

from custom_list import CustomList


class TestPraseJSON(unittest.TestCase):

    def test_sub(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1])

        self.assertListEqual(list_1 - list_2, [-2, 3, 3, 4])
        self.assertListEqual(list_2 - list_1, [2, -3, -3, -4])

        test_result = [1, 2, 3, 4] - list_2
        self.assertListEqual(test_result, [-2, 3, 3, 4])
        self.assertEqual(type(test_result), CustomList)

        test_result = [3, -1] - list_1
        self.assertListEqual(test_result, [2, -3, -3, -4])
        self.assertEqual(type(test_result), CustomList)

    def test_add(self):
        list_1 = CustomList([1, 2, 3, 4])
        list_2 = CustomList([3, -1])

        self.assertListEqual(list_1 + list_2, [4, 1, 3, 4])
        self.assertListEqual(list_2 + list_1, [4, 1, 3, 4])

        test_result = [1, 2, 3, 4] + list_2
        self.assertListEqual(test_result, [4, 1, 3, 4])
        self.assertEqual(type(test_result), CustomList)

        test_result = [3, -1] + list_1
        self.assertListEqual(test_result, [4, 1, 3, 4])
        self.assertEqual(type(test_result), CustomList)

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

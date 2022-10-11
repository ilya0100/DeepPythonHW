import unittest

from descriptors import Data
from custom_meta import CustomClass, CustomMeta


class TestClass(metaclass=CustomMeta):
    c_attr = "something"

    def __init__(self):
        self.i_attr = 123

    def test_method(self):
        return True

    def __fake_magic__(self):
        return True


class TestCustomMeta(unittest.TestCase):

    def test_custom_meta_new(self):
        test_class = TestClass()

        self.assertEqual(TestClass.custom_c_attr, "something")
        self.assertTrue(TestClass.custom_test_method(test_class))
        self.assertTrue(TestClass.__fake_magic__(test_class))

        with self.assertRaises(AttributeError):
            TestClass.c_attr
        with self.assertRaises(AttributeError):
            TestClass.test_method(test_class)

    def test_custom_meta_setattr(self):
        test_class = TestClass()

        self.assertEqual(test_class.custom_i_attr, 123)
        with self.assertRaises(AttributeError):
            test_class.i_attr

        test_class.new_attr = 32
        test_class.i_attr = 45

        self.assertEqual(test_class.custom_new_attr, 32)
        self.assertEqual(test_class.custom_i_attr, 45)

        with self.assertRaises(AttributeError):
            test_class.new_attr
        with self.assertRaises(AttributeError):
            test_class.i_attr

    def test_custom_class(self):
        inst = CustomClass()

        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError):
            inst.dynamic
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            inst.yyy
        with self.assertRaises(AttributeError):
            CustomClass.x


class TestDescriptors(unittest.TestCase):

    def test_integer_get(self):
        data = Data(num=123)
        self.assertEqual(data.num, 123)

    def test_integer_set(self):
        data = Data()

        data.num = 123
        self.assertEqual(data.num, 123)

        with self.assertRaises(ValueError):
            data.num = "string"

    def test_string_get(self):
        data = Data(name="string")
        self.assertEqual(data.name, "string")

    def test_string_set(self):
        data = Data()

        data.name = "string"
        self.assertEqual(data.name, "string")

        with self.assertRaises(ValueError):
            data.name = 123

    def test_positive_integer_get(self):
        data = Data(price=123)
        self.assertEqual(data.price, 123)

    def test_positive_integer_set(self):
        data = Data()

        data.price = 123
        self.assertEqual(data.price, 123)

        with self.assertRaises(ValueError):
            data.price = "string"
        with self.assertRaises(ValueError):
            data.price = -100

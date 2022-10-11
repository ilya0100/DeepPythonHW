from dataclasses import dataclass


class Integer:
    def __init__(self):
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if isinstance(value, int):
            return setattr(obj, self._name, value)
        raise ValueError("value must be integer")


class String:
    def __init__(self):
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if isinstance(value, str):
            return setattr(obj, self._name, value)
        raise ValueError("value must be string")


class PositiveInteger:
    def __init__(self):
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if isinstance(value, int) and value >= 0:
            return setattr(obj, self._name, value)
        raise ValueError("value must be integer and positive")


@dataclass
class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num=0, name="", price=0):
        self.num = num
        self.name = name
        self.price = price

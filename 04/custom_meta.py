class CustomMeta(type):
    def __new__(cls, name, bases, classdict, **kwargs):
        keys = list(classdict)
        for i, key in enumerate(keys):
            if not key.startswith("__") and not key.endswith("__"):
                keys[i] = f"custom_{keys[i]}"

        classdict = dict(zip(keys, classdict.values()))
        classdict["__setattr__"] = cls.__setattr__
        return super().__new__(cls, name, bases, classdict, **kwargs)

    def __setattr__(cls, name, value):
        cls.__dict__[f"custom_{name}"] = value


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

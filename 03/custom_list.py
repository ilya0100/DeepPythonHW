class CustomList(list):

    def __add__(self, other):
        result = CustomList()
        for i in range(min(len(self), len(other))):
            result.append(self[i] + other[i])

        if len(result) < len(self):
            for elem in self[len(result):]:
                result.append(elem)

        if len(result) < len(other):
            for elem in other[len(result):]:
                result.append(elem)
        return result

    def __sub__(self, other):
        result = CustomList()
        for i in range(min(len(self), len(other))):
            result.append(self[i] - other[i])

        if len(result) < len(self):
            for elem in self[len(result):]:
                result.append(elem)

        if len(result) < len(other):
            for elem in other[len(result):]:
                result.append(-elem)
        return result

    def __radd__(self, other):
        result = CustomList()
        for i in range(min(len(self), len(other))):
            result.append(other[i] + self[i])

        if len(result) < len(self):
            for elem in self[len(result):]:
                result.append(elem)

        if len(result) < len(other):
            for elem in other[len(result):]:
                result.append(elem)
        return result

    def __rsub__(self, other):
        result = CustomList()
        for i in range(min(len(self), len(other))):
            result.append(other[i] - self[i])

        if len(result) < len(self):
            for elem in self[len(result):]:
                result.append(-elem)

        if len(result) < len(other):
            for elem in other[len(result):]:
                result.append(elem)
        return result

    def __lt__(self, other) -> bool:
        return sum(self) < sum(other)

    def __le__(self, other) -> bool:
        return sum(self) <= sum(other)

    def __eq__(self, other) -> bool:
        return sum(self) == sum(other)

    def __ne__(self, other) -> bool:
        return sum(self) != sum(other)

    def __gt__(self, other) -> bool:
        return sum(self) > sum(other)

    def __ge__(self, other) -> bool:
        return sum(self) >= sum(other)

    def __str__(self) -> str:
        return f"{super().__str__()}, {sum(self)}"

class LRUCache:
    def __init__(self, limit=42):
        self._value_storage = {}
        self._limit = limit
        self._size = 0

    def get(self, key):
        value = self._value_storage.get(key)
        if value:
            del self._value_storage[key]
            self._value_storage[key] = value
        return value

    def set(self, key, value):
        if key in self._value_storage:
            del self._value_storage[key]
            self._size -= 1

        self._insert_item(key, value)
        self._pop_items()
        return None

    def change_limit(self, limit):
        self._limit = limit
        self._pop_items()

    def _pop_items(self):
        while self._size > self._limit:
            key = list(self._value_storage.keys())[0]
            del self._value_storage[key]
            self._size -= 1

    def _insert_item(self, key, value):
        self._value_storage[key] = value
        self._size += 1

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

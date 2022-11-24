import logging

from argparse import ArgumentParser
from sys import stdout


formatter = logging.Formatter("%(asctime)s\t%(message)s")

file_handler = logging.FileHandler("lru_cache.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger = logging.getLogger("cache_log")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


class LRUCache:
    def __init__(self, limit=42):
        logger.info(f"Cache initializing with limit = {limit}")

        self._value_storage = {}
        self._limit = limit
        self._size = 0

    def get(self, key):
        logger.info(f"Get value with key: {key}")

        value = self._value_storage.get(key)
        if value:
            logger.info(f"Update cache storage for key: {key}")

            del self._value_storage[key]
            self._value_storage[key] = value
        else:
            logger.debug(f"Key: {key} not exist")
        return value

    def set(self, key, value):
        logger.info(f"Set value: {value} with key: {key}")

        if key in self._value_storage:
            logger.info(f"Update cache storage for existing key: {key}")

            del self._value_storage[key]
            self._size -= 1

        self._insert_item(key, value)
        self._pop_items()

        logger.info(f"Cache size = {self._size}")

    def change_limit(self, limit):
        logger.info(f"Change cache limit, new limit = {limit}")

        self._limit = limit
        self._pop_items()

    def _pop_items(self):
        logger.debug(
            f"Del extra items, current size = {self._size}, limit = {self._limit}"
        )
        while self._size > self._limit:
            key = list(self._value_storage.keys())[0]

            logger.debug(f"Del item with key: {key}")

            del self._value_storage[key]
            self._size -= 1

        logger.debug(f"Size after deleting extra items: {self._size}")

    def _insert_item(self, key, value):
        logger.debug(f"Insert item: '{key}': {value}")

        self._value_storage[key] = value
        self._size += 1

        logger.debug(f"Size after inserting item: {self._size}")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


def main():
    cache = LRUCache(3)
    cache.set("key_1", "value_1")
    cache.set("key_2", "value_2")
    cache.get("key_1")
    cache.set("key_3", "value_3")
    cache.set("key_4", "value_4")
    cache.get("invalid_key")
    cache.set("key_3", "value")
    cache.change_limit(1)
    cache.set("key", "value")
    cache.get("key")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-s", action="store_true", help="Enable logging into stdout"
    )
    args = parser.parse_args()

    if args.s:
        debug_formatter = logging.Formatter(
            "%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s"
        )

        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(debug_formatter)

        logger.addHandler(stdout_handler)
        logger.setLevel(logging.DEBUG)

    main()

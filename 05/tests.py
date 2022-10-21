import io
import unittest

from lru_cache import LRUCache
from filter_file import filter_file


class TestFilterFile(unittest.TestCase):
    def test_file_open(self):
        word_list = ["city", "TrAvEl", "COUNTRY", "Conference"]
        gen = filter_file("test_data/test_file.txt", word_list)

        lines = []
        for line in gen:
            lines.append(line)

        out_lines = []
        with open("test_data/test_out.txt", encoding="utf-8") as file:
            for line in file:
                out_lines.append(line)

        self.assertEqual(lines, out_lines)

    def test_file_fileobj(self):
        # pylint: disable=line-too-long
        texts = [
            "Coach final discussion garden reveal spend.\n",
            "Scientist impact yourself sign.\n",
            "Store man no gas spring animal serve difference. With expert law specific ability build opportunity.\n",  # noqa
            "Table walk sound leave office myself decision detail.\n",
            "Much pass glass page read bad shake. Tv wall history identify officer little.\n",  # noqa
            "Cost board significant. Performance whatever top himself resource term.\n",  # noqa
            "а Роза упала на лапу Азора",
        ]
        # pylint: enable=line-too-long

        file_obj = io.StringIO("".join(texts))
        word_list = ["impact", "myself", "BOARD", "роз"]

        gen = filter_file(file_obj, word_list)

        lines = []
        for line in gen:
            lines.append(line)

        self.assertEqual(lines, [texts[1], texts[3], texts[5]])


class TestLRUCahce(unittest.TestCase):
        # pylint: disable=protected-access
    def test_set(self):
        cache = LRUCache(3)

        for i in range(3):
            cache.set(f"k{i}", f"v{i}")

        self.assertEqual(
            cache._value_storage, {"k0": "v0", "k1": "v1", "k2": "v2"}
        )

        cache.set("k3", "v3")
        self.assertEqual(
            cache._value_storage, {"k1": "v1", "k2": "v2", "k3": "v3"}
        )

        cache["k4"] = "v4"
        self.assertEqual(
            cache._value_storage, {"k2": "v2", "k3": "v3", "k4": "v4"}
        )

    def test_get(self):
        cache = LRUCache(3)

        for i in range(3):
            cache.set(f"k{i}", f"v{i}")

        self.assertEqual(cache.get("k0"), "v0")

        cache.set("k3", "v3")
        self.assertEqual(
            cache._value_storage, {"k0": "v0", "k2": "v2", "k3": "v3"}
        )

        self.assertEqual(cache["k2"], "v2")

    def test_change_limit(self):
        cache = LRUCache(10)

        for i in range(10):
            cache.set(f"k{i}", f"v{i}")

        cache.change_limit(3)
        self.assertEqual(
            cache._value_storage, {"k7": "v7", "k8": "v8", "k9": "v9"}
        )

        cache.change_limit(4)
        cache["k0"] = "v0"
        self.assertEqual(
            cache._value_storage,
            {"k7": "v7", "k8": "v8", "k9": "v9", "k0": "v0"},
        )

    def test_case(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

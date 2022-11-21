import dataclasses
import json


def parse_json(json_str: str, keyword_callback, required_fields, keywords):
    if keyword_callback is None or required_fields is None or keywords is None:
        return

    json_doc = json.loads(json_str)

    for key in required_fields:
        if key in json_doc:
            for keyword in keywords:
                if keyword in json_doc[key]:
                    keyword_callback(keyword)


@dataclasses.dataclass
class KeyWordList:
    def __init__(self):
        self.list = []

    def __call__(self, keyword):
        self.list.append(keyword)

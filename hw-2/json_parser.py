import json


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    if (required_fields == None or keywords == None):
        return
    
    json_doc = json.loads(json_str)

    for key in json_doc:
        if key in required_fields:
            for keyword in keywords:
                if keyword in json_doc[key]:
                    keyword_callback(keyword)


class KeyWordList:
    
    def __init__(self):
        self.list = []

    def __call__(self, keyword):
        self.list.append(keyword)

import uuid
from datetime import date, datetime
from json import JSONEncoder


class Choices:
    def __init__(self):
        self.__ignore_fields = ("CHOICES", "VALUES")

    @property
    def CHOICES(self) -> tuple:
        choice = []
        for attr in dir(self):
            if not attr.startswith("_") and attr not in self.__ignore_fields:
                choice.append((getattr(self, attr), attr))
        return tuple(choice)

    @property
    def VALUES(self) -> dict:
        value = {}
        for attr in dir(self):
            if not attr.startswith("_") and attr not in self.__ignore_fields:
                key = getattr(self, attr)
                value[key] = " ".join(list(map(lambda x: x.capitalize(), attr.split("_"))))

        return value


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)


def dict_to_json(dict_data):
    import json
    return json.loads(json.dumps(dict_data, cls=CustomJsonEncoder))

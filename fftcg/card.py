import json
import re

import yaml


class Card(yaml.YAMLObject):
    yaml_tag = u'!Card'

    __ELEMENTS_MAP = {
        "火": "Fire",
        "氷": "Ice",
        "風": "Wind",
        "土": "Earth",
        "雷": "Lightning",
        "水": "Water",
        "光": "Light",
        "闇": "Darkness"
    }

    def __init__(self, opus, serial, rarity, elements, name, text):
        self.__opus = opus
        self.__serial = serial
        self.__rarity = rarity
        self.__elements = elements
        self.__name = name
        self.__text = text

    @classmethod
    def from_data(cls, data: dict[str, any], language: str):
        if not data:
            return cls(
                opus="0",
                serial="000",
                rarity="X",
                elements=[],
                name=None,
                text=None,
            )

        else:
            if str(data["Code"])[0].isnumeric():
                # card code starts with a number
                opus, serial, rarity = \
                    re.match(r"([0-9]+)-([0-9]+)([CRHLS])", data["Code"]).groups()

            elif str(data["Code"]).startswith("PR"):
                # card code starts with "PR"
                opus, serial = \
                    re.match(r"(PR)-([0-9]+)", data["Code"]).groups()
                rarity = ""

            elif str(data["Code"]).startswith("B"):
                # card code starts with "B"
                opus, serial = \
                    re.match(r"(B)-([0-9]+)", data["Code"]).groups()
                rarity = ""

            else:
                # card code not recognized
                opus, serial, rarity = \
                    "?", "???", "?"

            return cls(
                opus=opus,
                serial=serial,
                rarity=rarity,
                elements=[Card.__ELEMENTS_MAP[element] for element in data["Element"].split("/")],
                name=data[f"Name_{language}"],
                text=data[f"Text_{language}"],
            )

    def __str__(self) -> str:
        return f"'{self.__name}' ({'/'.join(self.__elements)}, {self.code})"

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)

    # 6-048C
    @property
    def code(self) -> str:
        return f"{self.__opus}-{self.__serial}{self.__rarity}"

    @property
    def opus(self) -> str:
        return self.__opus

    @property
    def serial(self) -> int:
        return int(self.__serial)

    @property
    def rarity(self) -> str:
        return self.__rarity

    @property
    def name(self) -> str:
        return self.__name

    @property
    def text(self) -> str:
        return self.__text

    @property
    def elements(self) -> list[str]:
        return self.__elements

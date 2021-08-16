import json
import re

import yaml

from .code import Code


def encircle_symbol(symbol: str, negative: bool):
    symbol = symbol[0].upper()

    base_symbols: tuple[str, str] = "", ""
    if symbol.isalpha():
        if negative:
            base_symbols = "A", "🅐"
        else:
            base_symbols = "A", "Ⓐ"
    elif symbol == "0":
        if negative:
            base_symbols = "0", "🄌"
        else:
            base_symbols = "0", "⓪"
    elif symbol.isnumeric():
        if negative:
            base_symbols = "1", "➊"
        else:
            base_symbols = "1", "①"

    symbol_num = ord(symbol) - ord(base_symbols[0])
    return chr(ord(base_symbols[1]) + symbol_num)


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

    __ELEMENTS = "".join(__ELEMENTS_MAP.keys())

    def __init__(self, code, elements, name, text):
        self.__code = code
        self.__elements = elements
        self.__name = name
        self.__text = text

    @classmethod
    def from_data(cls, data: dict[str, any], language: str):
        if not data:
            return cls(
                code=Code(""),
                elements=[],
                name=None,
                text=None,
            )

        else:
            def sub_encircle(match: re.Match):
                return encircle_symbol(match.group(1), True)

            def sub_elements(match: re.Match):
                return encircle_symbol(Card.__ELEMENTS_MAP[match.group(1)], True)

            # load text
            text = str(data[f"Text_{language}"])
            # place "S" symbols
            text = text.replace("《S》", encircle_symbol("S", False))
            # place other letter and numerical cost symbols
            text = re.sub(r"《([a-z0-9])》", sub_encircle, text, flags=re.IGNORECASE)
            # place elemental cost symbols
            text = re.sub(rf"《([{Card.__ELEMENTS}])》", sub_elements, text, flags=re.IGNORECASE)
            # place dull symbols
            text = text.replace("《ダル》", "[⤵]")
            # replace formatting hints with brackets
            text = re.sub(r"\[\[[a-z]\]\]([^\[]*?)\s*\[\[/\]\]\s*", r"[\1] ", text, flags=re.IGNORECASE)
            # place EX-BURST markers
            text = re.sub(r"\[\[ex\]\]\s*EX BURST\s*\[\[/\]\]\s*", r"[EX BURST] ", text, flags=re.IGNORECASE)
            # place line breaks
            text = re.sub(r"\s*\[\[br\]\]\s*", "\n\n", text, flags=re.IGNORECASE)

            return cls(
                code=Code(data["Code"]),
                elements=[Card.__ELEMENTS_MAP[element] for element in data["Element"].split("/")],
                name=data[f"Name_{language}"],
                text=text,
            )

    def __str__(self) -> str:
        return f"'{self.__name}' ({'/'.join(self.__elements)}, {self.code})"

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)

    # 6-048C
    @property
    def code(self) -> Code:
        return self.__code

    @property
    def name(self) -> str:
        return self.__name

    @property
    def text(self) -> str:
        return self.__text

    @property
    def elements(self) -> list[str]:
        return self.__elements

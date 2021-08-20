from __future__ import annotations

import re

from .code import Code
from .utils import encircle_symbol


class Card:
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

    def __init__(self, code: Code, elements: list[str], name: str, text: str, face_url: str = "", index: int = 0):
        self.__code = code
        self.__elements = elements
        self.__name = name
        self.__text = text

        self.__face_url = face_url
        self.__index = index

    @classmethod
    def from_square_api_data(cls, data: dict[str, any], language: str) -> Card:
        if not data:
            return cls(
                code=Code(""),
                elements=[],
                name="",
                text="",
            )

        else:
            def sub_encircle(match: re.Match):
                return encircle_symbol(match.group(1), False)

            def sub_elements(match: re.Match):
                return encircle_symbol(Card.__ELEMENTS_MAP[match.group(1)], False)

            # load text
            text = str(data[f"Text_{language}"])
            # place "S" symbols
            text = text.replace("《S》", encircle_symbol("S", False))
            # place other letter and numerical cost symbols
            text = re.sub(r"《([a-z0-9])》", sub_encircle, text, flags=re.IGNORECASE)
            # place elemental cost symbols
            text = re.sub(rf"《([{''.join(Card.__ELEMENTS_MAP.keys())}])》", sub_elements, text, flags=re.IGNORECASE)
            # place dull symbols
            text = text.replace("《ダル》", "[⤵]")
            # replace formatting hints with brackets
            text = re.sub(r"\[\[[a-z]]]([^\[]*?)\s*\[\[/]]\s*", r"[\1] ", text, flags=re.IGNORECASE)
            # place EX-BURST markers
            text = re.sub(r"\[\[ex]]\s*EX BURST\s*\[\[/]]\s*", r"[EX BURST] ", text, flags=re.IGNORECASE)
            # place line breaks
            text = re.sub(r"\s*\[\[br]]\s*", "\n\n", text, flags=re.IGNORECASE)

            return cls(
                code=Code(data["Code"]),
                elements=[
                    Card.__ELEMENTS_MAP[element]
                    for element in data["Element"].split("/")
                ],
                name=data[f"Name_{language}"],
                text=text,
            )

    def __str__(self) -> str:
        return f"'{self.__name}' ({'/'.join(self.__elements)}, {self.code})"

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

    @property
    def face_url(self) -> str:
        return self.__face_url

    @face_url.setter
    def face_url(self, face_url: str) -> None:
        self.__face_url = face_url

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, index: int) -> None:
        self.__index = index

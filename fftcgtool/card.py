from __future__ import annotations

import re
from dataclasses import dataclass

from .code import Code
from .language import Language, API_LANGS
from .utils import encircle_symbol


@dataclass(frozen=True)
class CardContent:
    name: str
    text: str
    face: str


class Card:
    __ELEMENTS_JAP = [
        "火", "氷", "風", "土", "雷", "水", "光", "闇"
    ]

    __ELEMENTS_ENG = [
        "Fire", "Ice", "Wind", "Earth", "Lightning", "Water", "Light", "Darkness"
    ]

    __ELEMENTS_MAP = {
        elem_j: elem_e
        for elem_j, elem_e in zip(__ELEMENTS_JAP, __ELEMENTS_ENG)
    }

    def __init__(self, code: Code, elements: list[str], content: dict[Language, CardContent], index: int = 0):
        self.__code: Code = code
        self.__elements: list[str] = elements
        self.__content: dict[Language, CardContent] = content
        self.__index = index

    @classmethod
    def from_square_api_data(cls, data: dict[str, any]) -> Card:
        if not data:
            return cls(
                code=Code(""),
                elements=[],
                content={},
            )

        else:
            def sub_encircle(match: re.Match) -> str:
                return encircle_symbol(match.group(1), False)

            def sub_elements(match: re.Match) -> str:
                return encircle_symbol(Card.__ELEMENTS_MAP[match.group(1)], False)

            def load_name(language: Language) -> str:
                return data[f"Name{language.key_suffix}"]

            def load_text(language: Language) -> str:
                # load text
                text = str(data[f"Text{language.key_suffix}"])
                # place "S" symbols
                text = text.replace("《S》", encircle_symbol("S", False))
                # place elemental cost symbols
                text = re.sub(rf"《([{''.join(Card.__ELEMENTS_JAP)}])》", sub_elements, text, flags=re.UNICODE)
                # place dull symbols
                text = text.replace("《ダル》", "[⤵]")
                # relocate misplaced line break markers
                text = re.sub(r"(\[\[[a-z]+]][^\[]*?)(\[\[br]])([^\[]*?\[\[/]])", r"\2\1\3", text,
                              flags=re.IGNORECASE | re.UNICODE)
                # # relocate misplaced spaces
                # text = re.sub(r"(\[\[[a-z]+]][^\[]*?)\s+(\[\[/]])", r"\1\2 ", text, flags=re.IGNORECASE | re.UNICODE)
                # text = re.sub(r"(\[\[[a-z]+]])\s+([^\[]*?\[\[/]])", r" \1\2", text, flags=re.IGNORECASE | re.UNICODE)
                # place EX-BURST markers
                text = re.sub(r"\[\[ex]]\s*EX BURST\s*\[\[/]]\s*", r"[EX BURST] ", text,
                              flags=re.IGNORECASE | re.UNICODE)
                text = re.sub(r"([^\[]|^)(EX BURST)\s*([^]]|$)", r"\1[\2] \3", text, flags=re.UNICODE)
                # replace Damage hints with brackets and en-dash
                text = re.sub(r"\[\[i]](Schaden|Damage|Daños|Dégâts|Danni)\s*([0-9]+)\s*--\s*\[\[/]]\s*", r"[\1 \2] – ",
                              text, flags=re.IGNORECASE | re.UNICODE)
                # place other letter and numerical cost symbols
                text = re.sub(r"《([a-z0-9])》", sub_encircle, text, flags=re.IGNORECASE | re.UNICODE)
                # remove empty formatting hints
                text = re.sub(r"\[\[[a-z]]]\s*\[\[/]]\s*", r" ", text, flags=re.IGNORECASE | re.UNICODE)
                # replace formatting hints with brackets
                text = re.sub(r"\[\[[a-z]]]([^\[]*?)\s*\[\[/]]\s*", r"[\1] ", text, flags=re.IGNORECASE | re.UNICODE)
                # relocate misplaced spaces
                text = re.sub(r"(\[[^]]*?)\s+(])\s*", r"\1\2 ", text, flags=re.IGNORECASE | re.UNICODE)
                text = re.sub(r"\s*(\[)\s+([^]]*?])", r" \1\2", text, flags=re.IGNORECASE | re.UNICODE)
                # place line breaks
                return re.sub(r"\s*\[\[br]]\s*", "\n\n", text, flags=re.IGNORECASE | re.UNICODE)

            content = {
                language: CardContent(load_name(language), load_text(language), "")
                for language in API_LANGS
            }

            return cls(
                code=Code(data["Code"]),
                elements=[
                    Card.__ELEMENTS_MAP[element]
                    for element in data["Element"].split("/")
                ],
                content=content,
            )

    def __repr__(self) -> str:
        return f"Card(code={self.code!r}, content={self.__content!r})"

    def __str__(self) -> str:
        if self.__content:
            return f"'{self[''].name}' ({'/'.join(self.__elements)}, {self.code})"

    def __getitem__(self, item: Language | str) -> CardContent:
        if isinstance(item, Language):
            return self.__content[item]
        else:
            return self.__content[Language(item)]

    def __setitem__(self, key: Language | str, value: CardContent) -> None:
        if isinstance(key, Language):
            self.__content[key] = value
        else:
            self.__content[Language(key)] = value

    # 6-048C
    @property
    def code(self) -> Code:
        return self.__code

    @property
    def elements(self) -> list[str]:
        return self.__elements

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, index: int) -> None:
        self.__index = index

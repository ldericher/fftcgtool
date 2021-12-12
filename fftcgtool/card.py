from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .code import Code
from .language import Language, API_LANGS
from .utils import encircle_symbol


@dataclass(frozen=True)
class CardContent:
    name: str
    text: str
    face: str


_ELEMENTS_JAP = [
    "火", "氷", "風", "土", "雷", "水", "光", "闇",
]

_ELEMENTS_ENG = [
    "Fire", "Ice", "Wind", "Earth", "Lightning", "Water", "Light", "Darkness",
]

_ELEMENTS_MAP = {
    elem_j: elem_e
    for elem_j, elem_e in zip(_ELEMENTS_JAP, _ELEMENTS_ENG)
}


def _sub_encircle(match: re.Match) -> str:
    return encircle_symbol(match.group(1), False)


def _sub_elements(match: re.Match) -> str:
    return encircle_symbol(_ELEMENTS_MAP[match.group(1)], False)


def _load_name(language: Language, data: dict[str, Any]) -> str:
    return data[f"Name{language.key_suffix}"]


def _load_text(language: Language, data: dict) -> str:
    # load text
    text = str(data[f"Text{language.key_suffix}"])
    # place "S" symbols
    text = text.replace("《S》", encircle_symbol("S", False))
    # place elemental cost symbols
    text = re.sub(rf"《([{''.join(_ELEMENTS_JAP)}])》", _sub_elements, text, flags=re.UNICODE)
    # place crystal symbols
    text = text.replace("《C》", "⟠")
    # place dull symbols
    text = text.replace("《ダル》", "[⤵]")
    # relocate misplaced line break markers
    text = re.sub(r"(\[\[[a-z]+]][^\[]*?)(\[\[br]])([^\[]*?\[\[/]])", r"\2\1\3", text,
                  flags=re.IGNORECASE | re.UNICODE)
    # place EX-BURST markers
    text = re.sub(r"\[\[ex]]\s*EX BURST\s*\[\[/]]\s*", r"[EX BURST] ", text,
                  flags=re.IGNORECASE | re.UNICODE)
    # also place unmarked EX-BURST markers
    text = re.sub(r"([^\[]|^)(EX BURST)\s*([^]]|$)", r"\1[\2] \3", text, flags=re.UNICODE)
    # replace Damage hints with brackets and en-dash
    text = re.sub(r"\[\[i]](Schaden|Damage|Daños|Dégâts|Danni)\s*([0-9]+)\s*--\s*\[\[/]]\s*", r"[\1 \2] – ",
                  text, flags=re.IGNORECASE | re.UNICODE)
    # place other letter and numerical cost symbols
    text = re.sub(r"《([a-z0-9])》", _sub_encircle, text, flags=re.IGNORECASE | re.UNICODE)
    # remove empty formatting hints
    text = re.sub(r"\[\[[a-z]]]\s*\[\[/]]\s*", r" ", text, flags=re.IGNORECASE | re.UNICODE)
    # replace formatting hints with brackets
    text = re.sub(r"\[\[[a-z]]]([^\[]*?)\s*\[\[/]]\s*", r"[\1] ", text, flags=re.IGNORECASE | re.UNICODE)
    # relocate misplaced spaces at start of bracketed string
    text = re.sub(r"\s*(\[)\s+([^]]*?])", r" \1\2", text, flags=re.IGNORECASE | re.UNICODE)
    # relocate misplaced spaces at end of bracketed string
    text = re.sub(r"(\[[^]]*?)\s+(])\s*", r"\1\2 ", text, flags=re.IGNORECASE | re.UNICODE)
    # place line breaks
    return re.sub(r"\s*\[\[br]]\s*", "\n\n", text, flags=re.IGNORECASE | re.UNICODE)


class Card:
    def __init__(self, code: Code, elements: list[str], content: dict[Language, CardContent], index: int = 0):
        self.__code: Code = code
        self.__elements: list[str] = elements
        self.__content: dict[Language, CardContent] = content
        self.__index = index

    @classmethod
    def from_square_api_data(cls, data: dict[str, Any]) -> Card:
        if not data:
            return cls(
                code=Code(""),
                elements=[],
                content={},
            )

        else:
            code = Code(data["Code"])

            if code.opus == "C":
                elements = ["Crystal"]
                content = {
                    language: CardContent(
                        name="⟠",
                        text="",
                        face="",
                    )
                    for language in API_LANGS
                }

            else:
                elements = [
                    _ELEMENTS_MAP[element]
                    for element in data["Element"].split("/")
                ]
                content = {
                    language: CardContent(
                        name=_load_name(language, data),
                        text=_load_text(language, data),
                        face="",
                    )
                    for language in API_LANGS
                }

            return cls(
                code=code,
                elements=elements,
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

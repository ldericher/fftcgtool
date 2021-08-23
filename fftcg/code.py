from __future__ import annotations

import re


class Code:
    __RE_NUM = re.compile(r"([0-9]+)-([0-9]+)([CRHLS]?)")
    __RE_PROMO = re.compile(r"(PR)-([0-9]+)")
    __RE_BOSS = re.compile(r"(B)-([0-9]+)")

    def __init__(self, code: str):
        if code[0].isnumeric():
            # card code starts with a number
            self.__opus, self.__serial, self.__rarity = \
                Code.__RE_NUM.match(code).groups()

        elif code.startswith("PR"):
            # card code starts with "PR"
            self.__opus, self.__serial = \
                Code.__RE_PROMO.match(code).groups()
            self.__rarity = ""

        elif code.startswith("B"):
            # card code starts with "B"
            self.__opus, self.__serial = \
                Code.__RE_BOSS.match(code).groups()
            self.__rarity = ""

        else:
            # card code not recognized
            self.__opus, self.__serial, self.__rarity = \
                "?", "???", "?"

    def __str__(self) -> str:
        return f"{self.__opus}-{self.__serial}{self.__rarity}"

    def __repr__(self) -> str:
        return f"Code({str(self)!r})"

    def __hash__(self) -> hash:
        return hash(self.short)

    def __eq__(self, other: Code):
        return self.short == other.short

    @property
    def short(self) -> str:
        return f"{self.__opus}-{self.__serial}"

    @property
    def opus(self) -> str:
        return self.__opus

    @property
    def serial(self) -> int:
        return int(self.__serial)

    @property
    def rarity(self) -> str:
        return self.__rarity

from __future__ import annotations

import re
from dataclasses import dataclass, InitVar, field


@dataclass(frozen=True)
class Code:
    opus: str = field(init=False)
    serial: int = field(init=False)
    rarity: str = field(init=False, compare=False)
    code_init: InitVar[str] = field(default="")

    __RE = re.compile(r"([1-9][0-9]*|PR|B)-([0-9]+)([CRHLS]?)", flags=re.UNICODE)

    def __post_init__(self, code_init: str):
        match = Code.__RE.match(code_init)

        if match is not None:
            groups = match.groups()
            opus, serial, rarity = \
                groups[0], int(groups[1]), groups[2]

        else:
            # card code not recognized
            opus, serial, rarity = \
                "?", 0, "?"

        object.__setattr__(self, "opus", opus)
        object.__setattr__(self, "serial", serial)
        object.__setattr__(self, "rarity", rarity)

    def __str__(self) -> str:
        return self.long

    @property
    def short(self) -> str:
        return f"{self.opus}-{self.serial:03}"

    @property
    def long(self) -> str:
        return f"{self.short}{self.rarity}"

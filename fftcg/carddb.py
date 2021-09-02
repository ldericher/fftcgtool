from __future__ import annotations

import bz2
import pickle

from .card import Card
from .cards import Cards
from .code import Code
from .utils import CARDDB_FILE_NAME


class CardDB:
    __instance: CardDB = None
    __content: dict[Code, Card]

    def __new__(cls) -> CardDB:
        if CardDB.__instance is None:
            CardDB.__instance = object.__new__(cls)
            CardDB.__instance.__content = {}

        return CardDB.__instance

    def __contains__(self, item: Code) -> bool:
        return item in self.__content

    def __getitem__(self, code: Code) -> Card:
        return self.__content[code]

    def update(self, cards: Cards):
        for card in cards:
            self.__content[card.code] = card

        # pickle db file
        with bz2.BZ2File(CARDDB_FILE_NAME, "w") as file:
            pickle.dump(self.__content, file)

    def load(self) -> None:
        # unpickle db file
        self.__content.clear()
        try:
            with bz2.BZ2File(CARDDB_FILE_NAME, "r") as file:
                self.__content |= pickle.load(file)
        except FileNotFoundError:
            pass

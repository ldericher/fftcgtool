from __future__ import annotations

import yaml

from fftcg import Card
from fftcg.code import Code
from fftcg.utils import BOOK_YML_NAME


class CardDB:
    __instance: CardDB = None

    @classmethod
    def get(cls) -> CardDB:
        if not CardDB.__instance:
            CardDB.__instance = CardDB()

        return CardDB.__instance

    def __init__(self):
        self.__content: dict[Code, Card] = {}

    def __getitem__(self, code: Code) -> Card:
        return self.__content[code]

    def load(self):
        # load book.yml file
        book: dict
        try:
            with open(BOOK_YML_NAME, "r") as file:
                book = yaml.load(file, Loader=yaml.Loader)
        except FileNotFoundError:
            book = {}

        # "invert" book into card database:
        # every card is indexable by its code
        self.__content.clear()

        for file_name, cards in book.items():
            self.__content |= {
                card.code: card
                for card in cards
            }

        # write carddb.yml file
        with open("carddb.yml", "w") as file:
            yaml.dump(self.__content, file, Dumper=yaml.Dumper)

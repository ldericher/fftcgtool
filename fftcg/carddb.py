from __future__ import annotations

import pickle

from fftcg import Card
from fftcg.code import Code
from fftcg.utils import BOOK_PICKLE_NAME


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
            with open(BOOK_PICKLE_NAME, "rb") as file:
                book = pickle.load(file)
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

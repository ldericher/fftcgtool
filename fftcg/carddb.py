from __future__ import annotations

import yaml

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
        self.__content: dict[Code, dict[str, any]] = {}

    def __getitem__(self, code: Code) -> dict[str, any]:
        return self.__content[str(code)]

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

        for file_name, content in book.items():
            self.__content |= {
                str(card.code): {
                    "card": card,
                    "file": file_name,
                    "index": i,
                } for i, card in enumerate(content["cards"])
            }

        # write carddb.yml file
        with open("carddb.yml", "w") as file:
            yaml.dump(self.__content, file, Dumper=yaml.Dumper)

    # def make_deck(self, filters):
    #     # filter codes by card criteria
    #     codes = [
    #         content["card"].code
    #         for content in self.__content.values()
    #         if all([f(content["card"]) for f in filters])
    #     ]
    #
    #     from .ttsdeck import TTSDeck
    #     return TTSDeck(codes)

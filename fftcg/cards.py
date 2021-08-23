import re

from .card import Card


class Cards(list[Card]):
    def __init__(self, name, cards: list[Card] = None):
        if cards is None:
            cards = []

        super().__init__(cards)
        self.__name = name

    def __str__(self) -> str:
        return f"[{', '.join(str(card) for card in self)}]"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def file_name(self) -> str:
        val = self.name.lower().replace(" ", "_")
        return re.sub(r"[^\w]", "", val, flags=re.UNICODE)

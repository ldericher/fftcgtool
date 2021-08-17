import logging

import roman

from .cards import Cards
from .ttsdeck import TTSDeck


class Opus(Cards):
    def __init__(self, opus_id: str):
        super().__init__()

        logger = logging.getLogger(__name__)

        if opus_id.isnumeric():
            self.__name = f"Opus {roman.toRoman(int(opus_id)).upper()}"
            self.__number = opus_id
            self.__filename = f"opus_{opus_id}"
            params = {"set": [self.__name]}

        elif opus_id == "chaos":
            self.__name = "Boss Deck Chaos"
            self.__number = "B"
            self.__filename = "boss_deck_chaos"
            params = {"set": [self.__name]}

        elif opus_id == "promo":
            self.__name = "Promo"
            self.__number = "PR"
            self.__filename = "promo"
            params = {"rarity": ["pr"]}

        else:
            self.__name = "?"
            self.__number = "?"
            self.__filename = "?"
            params = {"set": "?"}

        self._load(params)

        # remove reprints
        for card in self:
            if not card.code.opus == self.__number:
                self.remove(card)

        # sort cards by opus, then serial
        self.sort(key=lambda x: x.code.serial)
        self.sort(key=lambda x: x.code.opus)

        for card in self:
            logger.info(f"imported card {card}")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def number(self) -> str:
        return self.__number

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def elemental_decks(self) -> list[TTSDeck]:
        if self.name in ["Promo", "Boss Deck Chaos"]:
            return [TTSDeck([
                card.code
                for card in self
            ])]

        else:
            def element_filter(element: str):
                return lambda card: card.elements == [element]

            # simple cases: create lambdas for base elemental decks
            base_elements = ["Fire", "Ice", "Wind", "Earth", "Lightning", "Water"]
            filters = [element_filter(elem) for elem in base_elements]

            filters += [
                # light/darkness elemental deck
                lambda card: card.elements == ["Light"] or card.elements == ["Darkness"],
                # multi element deck
                lambda card: len(card.elements) > 1,
            ]

            return [TTSDeck([
                card.code
                for card in self
                if f(card)
            ]) for f in filters]

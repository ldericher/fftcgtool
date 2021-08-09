import logging

import roman

from .cards import Cards


class Opus(Cards):
    def __init__(self, opus_id: str):
        logger = logging.getLogger(__name__)

        if opus_id.isnumeric():
            roman_opus_id = roman.toRoman(int(opus_id))
            params = {"set": [f"Opus {roman_opus_id.upper()}"]}
            self.__number = opus_id
            self.__name = f"opus_{opus_id}"

        elif opus_id == "chaos":
            params = {"set": ["Boss Deck Chaos"]}
            self.__number = "B"
            self.__name = "boss_deck_chaos"

        elif opus_id == "promo":
            params = {"rarity": ["pr"]}
            self.__number = "PR"
            self.__name = "promo"

        else:
            params = {"set": ["?"]}
            self.__number = "?"
            self.__name = "?"

        super().__init__(params)

        # remove reprints
        for card in self:
            if not card.code.startswith(self.__number + "-"):
                self.remove(card)

        # sort cards by opus, then serial
        self.sort(key=lambda x: x.serial)
        self.sort(key=lambda x: x.opus)

        for card in self:
            logger.info(f"imported card {card}")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def number(self) -> str:
        return self.__number

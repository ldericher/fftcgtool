import logging

import roman

from .cards import Cards


class Opus(Cards):
    def __init__(self, opus_id: str):
        logger = logging.getLogger(__name__)

        if opus_id.isnumeric():
            roman_opus_id = roman.toRoman(int(opus_id))
            params_add = {"set": [f"Opus {roman_opus_id.upper()}"]}
            self.__number = opus_id
            self.__name = f"opus_{opus_id}"

        elif opus_id == "chaos":
            params_add = {"set": ["Boss Deck Chaos"]}
            self.__number = "B"
            self.__name = "boss_deck_chaos"

        elif opus_id == "promo":
            params_add = {"rarity": ["pr"]}
            self.__number = "PR"
            self.__name = "promo"

        else:
            params_add = {"set": ["?"]}
            self.__number = "?"
            self.__name = "?"

        params = {
            "text": "",
            # "element": ["darkness"],
            **params_add
        }

        Cards.__init__(self, params)

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

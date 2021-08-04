import logging

import roman

from .cards import Cards


class Opus(Cards):
    def __init__(self, number):
        logger = logging.getLogger(__name__)

        if isinstance(number, str) and number.isnumeric():
            set_name = f"Opus {roman.toRoman(int(number))}"
            number = str(number)

        elif number == "Boss Deck Chaos":
            set_name = number
            number = "B"

        else:
            set_name = "?"
            number = "?"

        params = {
            "text": "",
            # "element": ["fire"],
            "set": [set_name],
        }

        Cards.__init__(self, params)

        # filter out reprints
        reprints = [card for card in self if not card.code.startswith(number)]
        for reprint in reprints:
            self.remove(reprint)

        # sort every element alphabetically
        self.sort(key=lambda x: x.code)
        self.sort(key=lambda x: x.name)
        self.sort(key=lambda x: "Multi" if len(x.elements) > 1 else x.elements[0])

        for card in self:
            logger.info(f"imported card {card}")

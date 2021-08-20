import logging

import requests
import roman

from . import Card
from .cards import Cards
from .ttsdeck import TTSDeck


class Opus(Cards):
    __SQUARE_API_URL = "https://fftcg.square-enix-games.com/de/get-cards"

    def __init__(self, opus_id: str):
        logger = logging.getLogger(__name__)

        params: dict[str, any]
        if opus_id.isnumeric():
            name = f"Opus {opus_id}"
            self.__number = opus_id
            params = {"set": [f"Opus {roman.toRoman(int(opus_id)).upper()}"]}

        elif opus_id == "chaos":
            name = "Boss Deck Chaos"
            self.__number = "B"
            params = {"set": [name]}

        elif opus_id == "promo":
            name = "Promo"
            self.__number = "PR"
            params = {"rarity": ["pr"]}

        else:
            name = "?"
            self.__number = "?"
            self.__filename = "?"
            params = {"set": "?"}

        # required params:
        #  text
        # supported params:
        #  [str] text, language, code, multicard="○"|"", ex_burst="○"|"", special="《S》"|""
        #  [array] type, element, cost, rarity, power, category_1, set
        #  [int] exactmatch=0|1

        if "text" not in params:
            params["text"] = ""

        # get cards from square api
        req = requests.post(Opus.__SQUARE_API_URL, json=params)
        super().__init__(name, [
            Card.from_square_api_data(card_data, "EN")
            for card_data in req.json()["cards"]
        ])

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
    def number(self) -> str:
        return self.__number

    @property
    def elemental_decks(self) -> list[TTSDeck]:
        if self.name in ["Promo", "Boss Deck Chaos"]:
            return [TTSDeck(
                [
                    card.code
                    for card in self
                ],
                f"{self.name}",
                f"All {self.name} Cards in elemental, then alphabetical order"
            )]

        else:
            def element_filter(element: str):
                return lambda card: card.elements == [element]

            # simple cases: create lambdas for base elemental decks
            base_elements = ["Fire", "Ice", "Wind", "Earth", "Lightning", "Water"]
            filters = {
                elem: element_filter(elem)
                for elem in base_elements
            }

            filters |= {
                # light/darkness elemental deck
                "Light-Darkness": lambda card: card.elements == ["Light"] or card.elements == ["Darkness"],
                # multi element deck
                "Multi": lambda card: len(card.elements) > 1,
            }

            return [TTSDeck(
                [
                    card.code
                    for card in self
                    if f(card)
                ],
                f"{self.name} {elem}",
                f"All {self.name} Cards with {elem} element in alphabetical order"
            ) for elem, f in filters.items()]

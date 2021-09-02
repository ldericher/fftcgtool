import logging
from dataclasses import replace

import requests
import roman

from .card import Card
from .carddb import CardDB
from .cards import Cards
from .language import Language, API_LANGS
from .ttsdeck import TTSDeck


class Opus(Cards):
    __SQUARE_API_URL = "https://fftcg.square-enix-games.com/en/get-cards"

    def __init__(self, opus_id: str, language: Language):
        logger = logging.getLogger(__name__)
        self.__language = language

        params: dict[str, any]
        if opus_id.isnumeric():
            name = f"Opus {opus_id} ({self.__language.short})"
            self.__number = opus_id
            params = {"set": [f"Opus {roman.toRoman(int(opus_id)).upper()}"]}

        elif opus_id == "chaos":
            name = f"Boss Deck Chaos ({self.__language.short})"
            self.__number = "B"
            params = {"set": ["Boss Deck Chaos"]}

        elif opus_id == "promo":
            name = f"Promo ({self.__language.short})"
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
        carddb = CardDB()
        cards = [
            Card.from_square_api_data(card_data)
            for card_data in req.json()["cards"]
        ]

        # remove reprints
        super().__init__(name, [
            card
            for card in cards
            if card.code.opus == self.__number
        ])

        # sort cards by opus, then serial
        self.sort(key=lambda x: x.code.serial)
        self.sort(key=lambda x: x.code.opus)

        for card in self:
            if card.code in carddb:
                for lang in API_LANGS:
                    card[lang] = replace(card[lang], face=carddb[card.code][lang].face)

            logger.debug(f"imported card {card}")

    @property
    def number(self) -> str:
        return self.__number

    @property
    def elemental_decks(self) -> list[TTSDeck]:
        if self.number in ["PR", "B"]:
            return [TTSDeck(
                [
                    card.code
                    for card in self
                ],
                f"{self.name}",
                f"All {self.name} Cards"
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

            # sort cards by element, then alphabetically
            cards = list(self)
            cards.sort(key=lambda x: x[self.__language].name)
            cards.sort(key=lambda x: "Multi" if len(x.elements) > 1 else x.elements[0])

            return [TTSDeck(
                [
                    card.code
                    for card in cards
                    if f(card)
                ],
                f"{self.name} {elem}",
                f"All {self.name} Cards with {elem} element in alphabetical order"
            ) for elem, f in filters.items()]

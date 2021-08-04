import requests

from .card import Card


class Cards(list):
    __API_URL = "https://fftcg.square-enix-games.com/de/get-cards"

    def __init__(self, params):
        list.__init__(self)

        if isinstance(params, dict):
            # required params:
            #  text
            # supported params:
            #  [str] text, language, code, multicard="○"|"", ex_burst="○"|"", special="《S》"|""
            #  [array] type, element, cost, rarity, power, category_1, set
            #  [int] exactmatch=0|1

            req = requests.post(Cards.__API_URL, json=params)
            self.extend([Card(card_data) for card_data in req.json()["cards"]])

        elif isinstance(params, list):
            self.extend(params)

    def __str__(self):
        return "\n".join(str(card) for card in self)

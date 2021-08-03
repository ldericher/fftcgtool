import requests

from .card import Card

APIURL = "https://fftcg.square-enix-games.com/de/get-cards"


class Cards:
    def __init__(self, params):
        # supported params:
        #  [str] text (required)
        #  [array] type, element, cost, rarity, power, category_1, set
        #  [str] language, code, multicard="○"|"", ex_burst="○"|"", special="《S》"|""
        #  [int] exactmatch=0|1

        req = requests.post(APIURL, json=params)
        self.__content = [Card(card_data) for card_data in req.json()["cards"]]

    def __str__(self):
        return "\n".join(str(card) for card in self.__content)

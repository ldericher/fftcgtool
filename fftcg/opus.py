import requests

from .card import Card

APIURL = "https://fftcg.square-enix-games.com/de/get-cards"


class Opus:
    def __init__(self, params):
        # self.__cards = [Card(card_data) for card_data in data]
        req = requests.post(APIURL, json=params)
        self.__cards = [Card(card_data) for card_data in req.json()["cards"]]

    def __str__(self):
        return "\n".join(str(card) for card in self.__cards)

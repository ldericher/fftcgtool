import requests

from .card import Card


class Cards(list[Card]):
    __API_URL = "https://fftcg.square-enix-games.com/de/get-cards"

    def __init__(self, params: dict[str, any]):
        list.__init__(self)

        # required params:
        #  text
        # supported params:
        #  [str] text, language, code, multicard="○"|"", ex_burst="○"|"", special="《S》"|""
        #  [array] type, element, cost, rarity, power, category_1, set
        #  [int] exactmatch=0|1

        if "text" not in params:
            params["text"] = ""

        req = requests.post(Cards.__API_URL, json=params)
        self.extend([Card(card_data) for card_data in req.json()["cards"]])

    def __str__(self) -> str:
        return "\n".join(str(card) for card in self)

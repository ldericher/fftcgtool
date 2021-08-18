import requests

from .card import Card


class Cards(list[Card]):
    __API_URL = "https://fftcg.square-enix-games.com/de/get-cards"

    def __init__(self, name):
        super().__init__()

        self.__name = name

    def __str__(self) -> str:
        return f"[{', '.join(str(card) for card in self)}]"

    def _load(self, params: dict[str, any]) -> None:
        # required params:
        #  text
        # supported params:
        #  [str] text, language, code, multicard="○"|"", ex_burst="○"|"", special="《S》"|""
        #  [array] type, element, cost, rarity, power, category_1, set
        #  [int] exactmatch=0|1

        if "text" not in params:
            params["text"] = ""

        req = requests.post(Cards.__API_URL, json=params)
        self.clear()
        self.extend([Card.from_data(card_data, "EN") for card_data in req.json()["cards"]])

    @property
    def name(self) -> str:
        return self.__name

    @property
    def file_name(self) -> str:
        return self.name.lower().replace(" ", "_")

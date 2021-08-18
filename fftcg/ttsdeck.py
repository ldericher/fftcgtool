import json

from .carddb import CardDB
from .cards import Cards
from .code import Code
from .utils import CARD_BACK_URL


class TTSDeck(Cards):
    def __init__(self, codes: list[Code], name: str, description: str):
        super().__init__(name)
        self.__description = description

        # get cards from carddb
        carddb = CardDB.get()
        self.extend([carddb[code] for code in codes])

        # unique face urls used
        unique_face_urls = set([
            card.face_url
            for card in self
        ])

        # lookup for indices of urls
        self.__url_indices = {
            url: i + 1
            for i, url in enumerate(unique_face_urls)
        }

    @property
    def tts_object(self) -> dict[str, any]:
        # build the "CustomDeck" dictionary
        custom_deck = {
            str(i): {
                "NumWidth": "10",
                "NumHeight": "7",
                "FaceURL": url,
                "BackURL": CARD_BACK_URL,
            } for url, i in self.__url_indices.items()
        }

        # values both in main deck and each contained card
        common_dict = {
            "Transform": {
                "scaleX": 2.17822933,
                "scaleY": 1.0,
                "scaleZ": 2.17822933
            },
            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
        }

        # cards contained in deck
        contained_objects = [
            {
                "Nickname": card.name,
                "Description": card.text,
                "CardID": 100 * self.__url_indices[card.face_url] + card.index,

                "Name": "Card",
                "Hands": True,
                "SidewaysCard": False,
            } | common_dict for card in self
        ]

        # extract the card ids
        deck_ids = [
            contained_object["CardID"]
            for contained_object in contained_objects
        ]

        # create the deck dictionary
        return {"ObjectStates": [
            {
                "Nickname": self.name,
                "Description": self.__description,
                "DeckIDs": deck_ids,
                "CustomDeck": custom_deck,
                "ContainedObjects": contained_objects,

                "Name": "Deck",
                "Hands": False,
                "SidewaysCard": False,
            } | common_dict
        ]}

    def save(self) -> None:
        # only save if the deck contains cards
        if self:
            with open(f"{self.file_name}.json", "w") as file:
                json.dump(self.tts_object, file, indent=2)

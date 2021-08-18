import json

from .carddb import CardDB
from .code import Code
from .utils import CARD_BACK_URL


class TTSDeck(list[dict[str, any]]):
    def __init__(self, codes: list[Code], name: str, description: str):
        carddb = CardDB.get()
        super().__init__([carddb[code] for code in codes])

        self.__name = name
        self.__description = description

    def __str__(self) -> str:
        face_urls = list(set([entry["file"] for entry in self]))

        custom_deck = {
            str(i + 1): {
                "NumWidth": "10",
                "NumHeight": "7",
                "FaceURL": url,
                "BackURL": CARD_BACK_URL,
            } for i, url in enumerate(face_urls)
        }

        custom_deck_inv = {
            url: i + 1
            for i, url in enumerate(face_urls)
        }

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

        contained_objects = [
            {
                "Name": "Card",
                "Nickname": entry["card"].name,
                "Description": entry["card"].text,

                "CardID": 100 * custom_deck_inv[entry["file"]] + entry["index"],

                "Hands": True,
                "SidewaysCard": False,
            } | common_dict for entry in self
        ]

        deck_ids = [
            contained_object["CardID"]
            for contained_object in contained_objects
        ]

        jsondict = {"ObjectStates": [
            {
                "Name": "Deck",
                "Nickname": self.__name,
                "Description": self.__description,

                "Hands": False,
                "SidewaysCard": False,

                "DeckIDs": deck_ids,
                "CustomDeck": custom_deck,
                "ContainedObjects": contained_objects,
            } | common_dict
        ]}

        return json.dumps(jsondict, indent=2)

    def save(self, file_name: str) -> None:
        pass

from __future__ import annotations

import json
import logging
import os

from .carddb import CardDB
from .cards import Cards
from .code import Code
from .language import Language
from .utils import CARD_BACK_URL, DECKS_DIR_NAME


class TTSDeck(Cards):
    def __init__(self, codes: list[Code], name: str, description: str, face_down: bool):
        logger = logging.getLogger(__name__)
        super().__init__(name)
        self.__description = description
        self.__face_down = face_down

        # get cards from carddb
        carddb = CardDB()

        # non-imported cards
        codes_invalid = frozenset([
            code
            for code in codes
            if code not in carddb
        ])

        # show errors and remove non-imported cards
        for code in codes_invalid:
            logger.error(f"Code '{code}' not in CardDB, ignoring!")
            while code in codes:
                codes.remove(code)

        # put existing cards into deck
        self.extend([
            carddb[code]
            for code in codes
        ])

    @property
    def file_name(self) -> str:
        return f"{super().file_name}.json"

    def get_tts_object(self, language: Language) -> dict[str, any]:
        carddb = CardDB()

        # unique face urls used
        unique_faces = set([
            card[language].face
            for card in self
        ])

        # lookup for indices of urls
        face_indices = {
            url: i + 1
            for i, url in enumerate(unique_faces)
        }

        # build the "CustomDeck" dictionary
        custom_deck = {
            str(i): {
                "NumWidth": "10",
                "NumHeight": "7",
                "FaceURL": carddb.get_face_url(face),
                "BackURL": CARD_BACK_URL,
            } for face, i in face_indices.items()
        }

        # values both in main deck and each contained card
        common_dict = {
            "Transform": {
                "scaleX": 2.17822933,
                "scaleY": 1.0,
                "scaleZ": 2.17822933,
                "rotY": 180.0,
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
                "Nickname": card[language].name,
                "Description": card[language].text,
                "CardID": 100 * face_indices[card[language].face] + card.index,

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
        deck_dict = {"ObjectStates": [
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

        if self.__face_down:
            # flip the deck
            deck_dict["ObjectStates"][0]["Transform"]["rotZ"] = 180.0

        return deck_dict

    def get_json(self, language: Language) -> str:
        return json.dumps(self.get_tts_object(language), indent=2)

    def save(self, language: Language) -> None:
        # only save if the deck contains cards
        if self:
            if not os.path.exists(DECKS_DIR_NAME):
                os.mkdir(DECKS_DIR_NAME)

            with open(os.path.join(DECKS_DIR_NAME, self.file_name), "w") as file:
                file.write(self.get_json(language))

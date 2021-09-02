from __future__ import annotations

import bz2
import pickle

from .card import Card
from .cards import Cards
from .code import Code
from .language import API_LANGS
from .utils import CARDDB_FILE_NAME


class CardDB:
    __instance: CardDB = None
    __cards: dict[Code, Card]
    __face_to_url: dict[str, str]

    def __new__(cls) -> CardDB:
        if CardDB.__instance is None:
            CardDB.__instance = object.__new__(cls)
            CardDB.__instance.__cards = {}
            CardDB.__instance.__face_to_url = {}

        return CardDB.__instance

    def __contains__(self, item: Code) -> bool:
        return item in self.__cards

    def __getitem__(self, code: Code) -> Card:
        return self.__cards[code]

    def __pickle(self):
        # pickle db file
        with bz2.BZ2File(CARDDB_FILE_NAME, "w") as file:
            pickle.dump(self.__cards, file)
            pickle.dump(self.__face_to_url, file)

    def update(self, cards: Cards):
        for card in cards:
            self.__cards[card.code] = card

        self.__pickle()

    def get_face_url(self, face: str) -> str:
        if face in self.__face_to_url:
            return self.__face_to_url[face]
        else:
            return face

    def upload_prompt(self) -> None:
        faces = list(set([
            card[lang].face
            for card in self.__cards.values()
            for lang in API_LANGS
            if card[lang].face
        ]))
        faces.sort()

        for face in faces:
            if face not in self.__face_to_url:
                face_url = input(f"Upload '{face}' and paste URL: ")
                if face_url:
                    self.__face_to_url[face] = face_url

        self.__pickle()

    def __unpickle(self):
        # unpickle db file
        self.__cards.clear()
        self.__face_to_url.clear()
        try:
            with bz2.BZ2File(CARDDB_FILE_NAME, "r") as file:
                self.__cards |= pickle.load(file)
                self.__face_to_url |= pickle.load(file)
        except FileNotFoundError:
            pass

    def load(self) -> None:
        self.__unpickle()

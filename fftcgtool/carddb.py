from __future__ import annotations

import io
import json
import pickle
import zipfile
from os import PathLike
from typing import IO

import requests

from .card import Card
from .cards import Cards
from .code import Code
from .language import API_LANGS


class CardDB:
    _instance: CardDB = None
    _cards: dict[Code, Card]
    _face_to_url: dict[str, str]

    _DB_FILE_NAME = "cards.pickle"
    _MAPPING_FILE_NAME = "face_to_url.json"

    def __new__(cls, *more) -> CardDB:
        if CardDB._instance is None:
            CardDB._instance = object.__new__(CardDB)

        return CardDB._instance

    def __init__(self, db_url: str = None):
        if db_url is not None:
            try:
                with open(db_url, "rb") as db_file:
                    self._load(db_file)

            except FileNotFoundError:
                res = requests.get(db_url, stream=True)
                if not res.ok:
                    raise ValueError("Invalid URL given to CardDB!")

                self._load(io.BytesIO(res.content))

    def _load(self, db: str | PathLike[str] | IO[bytes]):
        try:
            # unpickle db file
            with zipfile.ZipFile(db, "r") as zip_file:
                # cards db
                with zip_file.open(CardDB._DB_FILE_NAME, "r") as file:
                    self._cards = pickle.load(file)

                # face_to_url mapping
                with zip_file.open(CardDB._MAPPING_FILE_NAME, "r") as file:
                    self._face_to_url = json.load(file)

        except FileNotFoundError:
            self._cards = {}
            self._face_to_url = {}

    def __contains__(self, item: Code) -> bool:
        return item in self._cards

    def __getitem__(self, code: Code) -> Card:
        return self._cards[code]

    def get_face_url(self, face: str) -> str:
        try:
            return self._face_to_url[face]
        except KeyError:
            return face

    def save(self) -> None:
        return

    def update(self, cards: Cards) -> None:
        return

    def upload_prompt(self) -> None:
        return


class RWCardDB(CardDB):
    __db_path: PathLike[str]

    def __new__(cls, *more) -> RWCardDB:
        if CardDB._instance is None:
            CardDB._instance = object.__new__(RWCardDB)

        return CardDB._instance

    def __init__(self, db_path: str | PathLike[str] = None):
        super().__init__(None)

        if db_path is not None:
            self.__db_path = db_path
            self._load(self.__db_path)

    def save(self) -> None:
        with zipfile.ZipFile(self.__db_path, "w", compression=zipfile.ZIP_LZMA) as zip_file:
            # cards db
            with zip_file.open(CardDB._DB_FILE_NAME, "w") as file:
                pickle.dump(self._cards, file)

            # face_to_url mapping
            with zip_file.open(CardDB._MAPPING_FILE_NAME, "w") as file:
                file.write(json.dumps(self._face_to_url, indent=2).encode("utf-8"))

    def update(self, cards: Cards) -> None:
        for card in cards:
            self._cards[card.code] = card

    def upload_prompt(self) -> None:
        faces = list(set([
            card[lang].face
            for card in self._cards.values()
            for lang in API_LANGS
            if card[lang].face
        ]))
        faces.sort()

        for face in faces:
            if face not in self._face_to_url:
                face_url = input(f"Upload '{face}' and paste URL: ")
                if face_url:
                    self._face_to_url[face] = face_url

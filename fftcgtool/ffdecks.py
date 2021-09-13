from __future__ import annotations

import logging
import re
from typing import Iterable, Iterator, Optional

import requests

from .code import Code
from .ttsdeck import TTSDeck


class FFDecks(list[TTSDeck]):
    __FFDECKS_API_URL = "https://ffdecks.com/api/deck"
    __RE_FFDECKS_ID = re.compile(r"((https?://)?ffdecks\.com(/+api)?/+deck/+)?([0-9]+).*", flags=re.UNICODE)

    @classmethod
    def sanitized_ids(cls, deck_ids: Iterable) -> Iterator[Optional[str]]:
        matches = (
            cls.__RE_FFDECKS_ID.match(str(deck_id))
            for deck_id in deck_ids
        )

        return (
            match.groups()[3]
            if match is not None
            else None
            for match in matches
        )

    def __init__(self, deck_ids: Iterable):
        super().__init__()
        logger = logging.getLogger(__name__)

        def by_type(data: dict[str, str | int]) -> int:
            key_prios = {
                "Forward": 1,
                "Summon": 2,
                "Monster": 3,
                "Backup": 5,
            }

            try:
                return key_prios[data["type"]]
            except KeyError:
                return 4

        def by_cost(data: dict[str, str | int]) -> int:
            return data["cost"]

        for deck_id in self.sanitized_ids(deck_ids):
            if deck_id is None:
                logger.error("Malformed Deck ID for FFDecks API!")

            else:
                # api request
                res = requests.get(FFDecks.__FFDECKS_API_URL, params={"deck_id": deck_id})

                if not res.ok:
                    logger.error(f"Invalid Deck ID '{deck_id}' for FFDecks API!")

                else:
                    # general metadata
                    name = f"{res.json()['name']}"
                    description = deck_id

                    logger.info(f"Importing Deck {name!r}")

                    # pre-extract the used data
                    deck_cards = [{
                        "code": card["card"]["serial_number"],
                        "type": card["card"]["type"],
                        "cost": int(card["card"]["cost"]),
                        "count": int(card["quantity"]),
                    } for card in res.json()["cards"]]

                    # sort cards by type, then by cost
                    deck_cards.sort(key=by_cost)
                    deck_cards.sort(key=by_type)

                    # ffdecks quirk: some full-art promos in database
                    replace_full_arts = {
                        # line format:
                        # full-art-id: normal id,
                        "PR-051": "11-083",
                        "PR-055": "11-062",
                    }

                    # replace with normal-art cards
                    for card in deck_cards:
                        try:
                            card["code"] = replace_full_arts[card["code"]]
                        except KeyError:
                            pass

                    codes = [
                        # create list of code objects
                        Code(card["code"])
                        # for each card
                        for card in deck_cards
                        # repeat to meet count
                        for _ in range(card["count"])
                    ]

                    # create deck object
                    self.append(TTSDeck(codes, name, description, True))

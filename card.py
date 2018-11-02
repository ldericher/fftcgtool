import requests

from PIL import Image
from io import BytesIO

# Card front by Square API
FACEURL = "https://fftcg.square-enix-games.com/theme/tcg/images/cards/full/{}_eg.jpg"

# Card back image by Aurik
BACKURL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"

class Card:
    def __init__(self, data):
        # check if this is a card back
        if data == 0:
            self._serial = "0-000"
            self._name = "[cardback]"
            self._rarity = "X"
            self._element = "None"

            self._description = "None"
            self._iurl = BACKURL

        # else import from data
        else:
            self._serial = data["serial_number"]
            self._name = data["name"]
            self._rarity = data["rarity"][0]
            self._element = data["element"]

            self._description = "\n\n".join(data["abilities"])
            self._iurl = FACEURL.format(self.get_id()) # official url
            #self._iurl = data["image"] # ffdecks url

    # 'Shinra' (Wind, 6-048C)
    def __str__(self):
        return "'{}' ({}, {})".format(self._name, self._element, self.get_id())

    # 6-048C
    def get_id(self):
        rarity = self._rarity if self._rarity in ["C", "R", "H", "L", "S"] else ""
        return "{}{}".format(self._serial, rarity)

    # return in dictionary format
    def get_dict(self):
        return {
            "Nickname": self._name,
            "Description": self._description,

            "Name": "Card",
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
            "SidewaysCard": False,
            "Hands": True
        }

    # download and resize card image
    def get_image(self, resolution):
        response = requests.get(self._iurl)
        im = Image.open(BytesIO(response.content))
        im = im.convert("RGB")
        im = im.resize(resolution, Image.BICUBIC)
        return im

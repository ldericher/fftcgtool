import requests

from PIL import Image
from io import BytesIO
import json

# Base-URL of ffdecks card pages
FFDECKURL = "https://ffdecks.com/api/cards?alternates=1&serial_number={}"
# Card back image by Aurik
BACKURL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"
# Card front by Square API
FACEURL = "https://fftcg.square-enix-games.com/theme/tcg/images/cards/full/{}_eg.jpg"

class Card:
    # 'Shinra' (Wind, 6-048C)
    def __str__(self):
        return "'{}' ({}, {})".format(self._name, self._element, self.get_id())

    # 6-048
    def get_id(self):
        return "{}-{:03}".format(self._opus, self._cardid)

    # find card
    def load(self, opus, cardid):
        self._opus = opus
        self._cardid = cardid

        # check if this is a card back
        if opus == 0:
            self._rarity = ""
            self._name = "[cardback]"
            self._element = "None"
            self._iurl = BACKURL
            return True

        try:
            # fetch card page from ffdecks API
            result = requests.get( FFDECKURL.format(self.get_id()) )
            res_obj = json.loads( result.content.decode("utf-8") )

            cname = res_obj["name"].strip()

            # success?
            if cname:
                self._name = cname
                self._iurl = res_obj["image"]
                self._element = res_obj["element"]
                self._description = "\n\n".join(res_obj["abilities"])
                return True

        except:
            # Something went wrong
            return False

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

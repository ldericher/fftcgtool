import requests

from PIL import Image
from io import BytesIO
from lxml import etree

# Base-URL of fftcgmognet card pages
TCGMOGURL = "http://www.fftcgmognet.com/card/"
# Card back image by Aurik
BACKURL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"

# Possible rarity suffixes
RARITIES = ["C", "R", "H", "L", "S"]

# If fftcgmognet alters designs, these *might* get old
XP_IMAGEURL = 'string(//div[@class="col-xs-12 col-sm-5 text-center mog-cardpage-image"]//img/@src)'
XP_CARDNAME = 'string(//div[@class="col-xs-12 col-sm-7 box mog-cardpage-props"]/div[@class="row"][1]/div[2])'
XP_ELEMENT  = 'string(//div[@class="col-xs-12 col-sm-7 box mog-cardpage-props"]/div[@class="row"][3]/div[2])'
XP_DESCRIPT = 'string(//div[@class="col-xs-12 col-sm-7 box mog-cardpage-props"]/div[@class="row"][7]/div[2])'


class Card:
    # 'Shinra' (Wind, 6-048C)
    def __str__(self):
        return "'{}' ({}, {})".format(self._name, self._element, self.get_id())

    # 6-048C
    def get_id(self):
        return "{}-{:03}{}".format(self._opus, self._cardid, self._rarity)

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

        # rarity was not given (but needed for mognet URL!)
        for rarity in RARITIES:
            # assume some rarity
            self._rarity = rarity

            # try to fetch card name
            html = requests.get(TCGMOGURL + self.get_id())
            doc = etree.HTML(html.content)
            cname = doc.xpath(XP_CARDNAME).strip()

            # succeed or retry with next rarity tier
            if cname:
                self._name = cname
                self._iurl = doc.xpath(XP_IMAGEURL).strip()
                self._element = doc.xpath(XP_ELEMENT).strip()
                self._description = doc.xpath(XP_DESCRIPT).strip()
                return True

        # No fitting rarity found,
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

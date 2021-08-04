import re


class Card:
    __ELEMENTS_MAP = {
        '火': "Fire",
        '氷': "Ice",
        '風': "Wind",
        '土': "Earth",
        '雷': "Lightning",
        '水': "Water",
        '光': "Light",
        '闇': "Darkness"
    }

    def __init__(self, data: dict, language: str = "EN"):
        if not data:
            self.__opus = "0"
            self.__serial = "000"
            self.__rarity = "X"
            self.__elements = None
            self.__text = None

        else:
            if str(data["Code"])[0].isnumeric():
                # card code starts with a number
                self.__opus, self.__serial, self.__rarity = \
                    re.match(r'([0-9]+)-([0-9]+)([CRHLS])', data["Code"]).groups()

            elif str(data["Code"]).startswith("PR"):
                # card code starts with "PR"
                self.__opus, self.__serial = \
                    re.match(r'(PR)-([0-9]+)', data["Code"]).groups()
                self.__rarity = ""

            elif str(data["Code"]).startswith("B"):
                # card code starts with "B"
                self.__opus, self.__serial = \
                    re.match(r'(B)-([0-9]+)', data["Code"]).groups()
                self.__rarity = ""

            else:
                # card code not recognized
                self.__opus, self.__serial, self.__rarity = \
                    "?", "???", "?"

            self.__elements = [Card.__ELEMENTS_MAP[element] for element in data["Element"].split("/")]
            self.__name = data[f"Name_{language}"]
            self.__text = data[f"Text_{language}"]

    def __str__(self):
        return f"'{self.__name}' ({'/'.join(self.__elements)}, {self.code})"

    # 6-048C
    @property
    def code(self):
        return f"{self.__opus}-{self.__serial}{self.__rarity}"

    @property
    def opus(self):
        return self.__opus

    @property
    def serial(self):
        return int(self.__serial)

    @property
    def rarity(self):
        return self.__rarity

    @property
    def name(self):
        return self.__name

    @property
    def text(self):
        return self.__text

    @property
    def elements(self):
        return self.__elements

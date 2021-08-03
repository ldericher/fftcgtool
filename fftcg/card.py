import re


class Card:
    def __init__(self, data):
        if not data:
            self.__opus = "0"
            self.__serial = "000"
            self.__rarity = "X"
            self.__element = None
            self.__description = None

        else:
            if str(data["Code"])[0].isnumeric():
                self.__opus, self.__serial, self.__rarity = \
                    re.match(r'([0-9]+)-([0-9]+)([CRHLS])', data["Code"]).groups()

            elif str(data["Code"]).startswith("PR"):
                self.__opus, self.__serial = \
                    re.match(r'(PR)-([0-9]+)', data["Code"]).groups()
                self.__rarity = ""

            elif str(data["Code"]).startswith("B"):
                self.__opus, self.__serial = \
                    re.match(r'(B)-([0-9]+)', data["Code"]).groups()
                self.__rarity = ""

            else:
                self.__opus, self.__serial, self.__rarity = \
                    "?", "???", "?"

            self.__name = data["Name_EN"]
            self.__element = data["Element"].split("/")
            self.__description = data["Text_EN"]

    def __str__(self):
        return f"'{self.__name}' ({self.__element}, {self.get_id()})"

    # 6-048C
    def get_id(self):
        return f"{self.__opus}-{self.__serial}{self.__rarity}"

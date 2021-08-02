import re


class Card:
    def __init__(self, data):
        code_match = re.match(r'([0-9]+)-([0-9]+)([CRHLSB])', data["Code"])
        if code_match:
            self.__opus, self.__serial, self.__rarity = code_match.groups()

        else:
            code_match = re.match(r'PR-([0-9]+)', data["Code"])
            if code_match:
                self.__opus = "PR"
                self.__serial = code_match.group(1)
                self.__rarity = "P"

            else:
                code_match = re.match(r'B-([0-9]+)', data["Code"])
                if code_match:
                    self.__opus = "B"
                    self.__serial = code_match.group(1)
                    self.__rarity = "B"

        self.__name = data["Name_EN"]
        self.__element = data["Element"]

    def __str__(self):
        return f"'{self.__name}' ({self.__element}, {self.get_id()})"

    # 6-048C
    def get_id(self):
        return f"{self.__opus}-{self.__serial}{self.__rarity}"

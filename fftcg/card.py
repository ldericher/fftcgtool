import re


class Card:
    def __init__(self, data):
        code_match = re.match(r'([0-9]+)-([0-9]+)([CRHLSB])', data["Code"])
        if code_match:
            self._opus, self._serial, self._rarity = code_match.groups()

        else:
            self._opus = "PR"
            self._serial = re.match(r'PR-([0-9]+)', data["Code"]).group(1)
            self._rarity = "P"

        self._name = data["Name_EN"]
        self._element = data["Element"]

    def __str__(self):
        return f"'{self._name}' ({self._element}, {self.get_id()})"

    # 6-048C
    def get_id(self):
        return f"{self._opus}-{self._serial}{self._rarity}"

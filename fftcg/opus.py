from roman import toRoman

from .cards import Cards


class Opus(Cards):
    def __init__(self, number):
        if isinstance(number, int):
            number = f"Opus {toRoman(number)}"

        params = {
            "text": "",
            "element": ["fire"],
            "set": [number],
        }

        Cards.__init__(self, params)

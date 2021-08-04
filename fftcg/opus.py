import roman

from .cards import Cards


class Opus(Cards):
    def __init__(self, number):
        if isinstance(number, int):
            number = f"Opus {roman.toRoman(number)}"

        params = {
            "text": "",
            "element": ["fire"],
            "set": [number],
        }

        Cards.__init__(self, params)

        # sort every element alphabetically
        self.sort(key=lambda x: x.get_code())
        self.sort(key=lambda x: x.get_name())
        self.sort(key=lambda x: "Multi" if len(x.get_elements()) > 1 else x.get_elements()[0])

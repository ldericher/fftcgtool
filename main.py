import requests

from fftcg.opus import Opus


def print_hi(name):
    # supported params:
    #  [str] language, text,
    #  [array] type, element, cost, rarity, power, category_1, set
    #  [str] multicard="○"|"", ex_burst="○"|"", code, special="《S》"|""
    #  [int] exactmatch=0|1
    params = {
        "language": "de",
        "text": "",
        "element": ["fire"],
        # "set": ["Opus XIV"],
    }

    opus_json = requests.post(url="https://fftcg.square-enix-games.com/de/get-cards", json=params).json()

    opus = Opus(opus_json["cards"])
    print(opus)


if __name__ == '__main__':
    print_hi('PyCharm')

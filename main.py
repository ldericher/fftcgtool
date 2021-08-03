#!/usr/bin/env python3

from fftcg.opus import Opus


def print_hi(name):
    # supported params:
    #  [str] language, text,
    #  [array] type, element, cost, rarity, power, category_1, set
    #  [str] multicard="○"|"", ex_burst="○"|"", code, special="《S》"|""
    #  [int] exactmatch=0|1
    params = {
        "text": "",
        "element": ["fire"],
        "set": ["Opus XIV"],
    }

    opus = Opus(params)
    print(opus)


if __name__ == '__main__':
    print_hi('PyCharm')

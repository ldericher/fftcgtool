from .card import Card


class Opus:
    def __init__(self, data):
        self.__cards = [Card(card_data) for card_data in data]

    def __str__(self):
        return "\n".join(str(card) for card in self.__cards)

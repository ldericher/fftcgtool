import queue

from .imageloader import ImageLoader


class Book:
    def __init__(self, cards):
        self.__cards = cards

    def __get_pages(self, grid):
        # cards per sheet
        r, c = grid
        capacity = r*c - 1
        # flat copy
        cards = self.__cards

        # while there are cards
        while cards:
            # get a chunk
            yield cards[:capacity]
            # remove that chunk
            cards = cards[capacity:]

    def populate(self, grid, resolution, threadnum=16):
        card_queue = queue.Queue()
        for i, card in enumerate(self.__cards):
            card_queue.put((i, card))

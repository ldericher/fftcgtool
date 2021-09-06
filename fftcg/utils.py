import itertools
from typing import Iterator, Generator, Iterable

from PIL import Image

from .grid import Grid

# constants
GRID = Grid((10, 7))  # default in TTsim: 10 columns, 7 rows
RESOLUTION = Grid((429, 600))  # default in TTsim: 480x670 pixels per card
DECKS_DIR_NAME = "decks"  # name of decks directory
IMAGES_DIR_NAME = "images"  # name of images directory
# card back URL (image by Aurik)
CARD_BACK_URL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"


# functions
def encircle_symbol(symbol: str, negative: bool) -> str:
    symbol = symbol[0].upper()

    base_symbols: tuple[str, str] = "", ""
    if symbol.isalpha():
        if negative:
            base_symbols = "A", "🅐"
        else:
            base_symbols = "A", "Ⓐ"
    elif symbol == "0":
        if negative:
            base_symbols = "0", "🄌"
        else:
            base_symbols = "0", "⓪"
    elif symbol.isnumeric():
        if negative:
            base_symbols = "1", "➊"
        else:
            base_symbols = "1", "①"

    symbol_num = ord(symbol) - ord(base_symbols[0])
    return chr(ord(base_symbols[1]) + symbol_num)


def chunks(chunk_size: int, whole: Iterable) -> Generator[Iterator, None, None]:
    it = iter(whole)
    # get chunk
    while chunk := itertools.islice(it, chunk_size):
        # stop if no first element was found
        try:
            first_el = next(chunk)
        except StopIteration:
            return
        # reattach first element
        yield itertools.chain((first_el,), chunk)


def grid_paste(page: Image.Image, index: int, card: Image.Image) -> None:
    w, h = card.size
    position = (index % GRID.x) * w, (index // GRID.x) * h
    page.paste(card, position)

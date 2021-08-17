from .grid import Grid

# constants
GRID = Grid((10, 7))  # default in TTsim: 10 columns, 7 rows
RESOLUTION = Grid((429, 600))  # default in TTsim: 480x670 pixels per card
BOOK_YML_NAME = "book.yml"


# functions
def encircle_symbol(symbol: str, negative: bool):
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

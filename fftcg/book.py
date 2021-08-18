import logging

import yaml
from PIL import Image

from .cards import Cards
from .imageloader import ImageLoader
from .utils import GRID, RESOLUTION, BOOK_YML_NAME, CARD_BACK_URL


class Book:
    def __init__(self, cards: Cards, language: str, num_threads: int):
        logger = logging.getLogger(__name__)

        # sort cards by element, then alphabetically
        cards.sort(key=lambda x: x.name)
        cards.sort(key=lambda x: "Multi" if len(x.elements) > 1 else x.elements[0])

        # all card face URLs
        urls = [f"https://fftcg.cdn.sewest.net/images/cards/full/{card.code}_{language}.jpg" for card in cards]
        # card back URL
        urls.append(CARD_BACK_URL)

        # multi-threaded download
        images = ImageLoader.load(urls, language, num_threads)
        # card back Image
        back_image = images.pop(-1)

        self.__pages = []
        for page_images, page_cards in zip(GRID.chunks(images), GRID.chunks(cards)):
            # create book page Image
            page_image = Image.new("RGB", GRID * RESOLUTION)
            logger.info(f"New image: {page_image.size[0]}x{page_image.size[1]}")

            # paste card faces onto page
            for i, image in enumerate(page_images):
                GRID.paste(page_image, i, image)

            # paste card back in last position
            GRID.paste(page_image, GRID.capacity, back_image)

            # save page
            self.__pages.append({
                "image": page_image,
                "cards": page_cards,
            })

    def save(self, file_name: str) -> None:
        book: dict[str, dict[str, any]]

        # load book.yml file
        try:
            with open(BOOK_YML_NAME, "r") as file:
                book = yaml.load(file, Loader=yaml.Loader)
        except FileNotFoundError:
            book = {}

        # save book
        for i, page in enumerate(self.__pages):
            fn = f"{file_name}_{i}.jpg"
            # save page image
            page["image"].save(fn)
            # add contents of that image
            book[fn] = {"cards": page["cards"]}

        # update book.yml file
        with open(BOOK_YML_NAME, "w") as file:
            yaml.dump(book, file, Dumper=yaml.Dumper)

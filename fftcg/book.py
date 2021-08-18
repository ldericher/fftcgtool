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
        self.__file_name = cards.file_name

        # all card face URLs
        urls = [f"https://fftcg.cdn.sewest.net/images/cards/full/{card.code}_{language}.jpg" for card in cards]
        # card back URL
        urls.append(CARD_BACK_URL)

        # multi-threaded download
        images = ImageLoader.load(urls, language, num_threads)
        # card back Image
        back_image = images.pop(-1)

        self.__pages = []

        page_images: list[Image.Image]
        page_cards: Cards
        for page_images, page_cards in zip(GRID.chunks(images), GRID.chunks(cards)):
            # create book page Image
            page_image = Image.new("RGB", GRID * RESOLUTION)
            logger.info(f"New image: {page_image.size[0]}x{page_image.size[1]}")

            # paste card faces onto page
            for i, image in enumerate(page_images):
                GRID.paste(page_image, i, image)

            # paste card back in last position
            GRID.paste(page_image, GRID.capacity, back_image)

            # set card indices
            for i, card in enumerate(page_cards):
                card.index = i

            # save page
            self.__pages.append({
                "image": page_image,
                "cards": page_cards,
            })

    def save(self) -> None:
        # save images
        for i, page in enumerate(self.__pages):
            fn = f"{self.__file_name}_{i}.jpg"
            # save page image
            page["image"].save(fn)

        book: dict[str, Cards]
        try:
            with open(BOOK_YML_NAME, "r") as file:
                book = yaml.load(file, Loader=yaml.Loader)
        except FileNotFoundError:
            book = {}

        # save book
        for i, page in enumerate(self.__pages):
            fn = f"{self.__file_name}_{i}.jpg"
            # ask for upload
            face_url = input(f"Upload '{fn}' and paste URL: ")
            for card in page["cards"]:
                card.face_url = face_url
            # add contents of that image
            book[fn] = page["cards"]

        # update book.yml file
        with open(BOOK_YML_NAME, "w") as file:
            yaml.dump(book, file, Dumper=yaml.Dumper)

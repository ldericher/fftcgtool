import logging
import os
from dataclasses import replace

from PIL import Image

from .cards import Cards
from .imageloader import ImageLoader
from .language import Language
from .utils import GRID, RESOLUTION, CARD_BACK_URL, IMAGES_DIR_NAME, chunks, grid_paste


class Book:
    def __init__(self, cards: Cards, language: Language, num_threads: int):
        logger = logging.getLogger(__name__)

        # all card face URLs
        urls = [
            ("https://fftcg.cdn.sewest.net/images/cards/full/{}_{}.jpg", card.code.long, language.image_suffix)
            for card in cards
        ]
        # card back URL
        urls.append((CARD_BACK_URL, "", ""))

        # multi-threaded download
        images = ImageLoader.load(urls, num_threads)
        # card back Image
        back_image = images.pop(-1)

        self.__pages = []

        for page_num, (page_images, page_cards) in enumerate(zip(
                chunks(GRID.capacity, images), chunks(GRID.capacity, cards)
        )):
            file_name = f"{cards.file_name}_{page_num}.jpg"

            # create book page Image
            page_image = Image.new("RGB", GRID * RESOLUTION)
            logger.info(f"New image: {page_image.size[0]}x{page_image.size[1]}")

            # paste card faces onto page
            for i, image in enumerate(page_images):
                grid_paste(page_image, i, image)

            # paste card back in last position
            grid_paste(page_image, GRID.capacity, back_image)

            # set card indices
            for i, card in enumerate(page_cards):
                card.index = i
                card[language] = replace(card[language], face=file_name)

            # save page
            self.__pages.append({
                "file_name": file_name,
                "image": page_image,
                "cards": page_cards,
            })

    def save(self) -> None:
        if not os.path.exists(IMAGES_DIR_NAME):
            os.mkdir(IMAGES_DIR_NAME)

        # save images
        for page in self.__pages:
            page["file_name"] = os.path.join(IMAGES_DIR_NAME, page["file_name"])
            page["image"].save(page["file_name"])

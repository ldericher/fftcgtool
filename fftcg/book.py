import logging

from PIL import Image

from .imageloader import ImageLoader


def chunks(whole: list, chunk_size):
    # while there are elements
    while whole:
        # get a chunk
        yield whole[:chunk_size]
        # remove that chunk
        whole = whole[chunk_size:]


class Book:
    def __init__(self, cards, grid, resolution, language, num_threads):
        logger = logging.getLogger(__name__)

        images = ImageLoader.load(cards, resolution, language, num_threads)
        images = [images[card] for card in cards]

        # shorthands
        # rows and columns per sheet
        r, c = grid
        # width, height per card
        w, h = resolution

        self.__pages = []
        for images in chunks(images, r * c - 1):
            page = Image.new("RGB", (c * w, r * h))
            logger.info(f"New image: {page.size[0]}x{page.size[1]}")

            for i, image in enumerate(images):
                x, y = (i % c) * w, (i // c) * h
                page.paste(image, (x, y, x + w, y + h))

            self.__pages.append(page)

    def save(self, filename):
        for i, page in enumerate(self.__pages):
            page.save(filename.format(i))

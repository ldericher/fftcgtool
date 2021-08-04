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
    # Card faces by Square API
    __FACE_URL = "https://fftcg.cdn.sewest.net/images/cards/full/{}_{}.jpg"

    # Card back image by Aurik
    __BACK_URL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"

    def __init__(self, cards, grid, resolution, language, num_threads):
        logger = logging.getLogger(__name__)

        # sort cards by element, then alphabetically
        cards.sort(key=lambda x: x.name)
        cards.sort(key=lambda x: "Multi" if len(x.elements) > 1 else x.elements[0])

        # all card face URLs
        urls = [Book.__FACE_URL.format(card.code, language) for card in cards]
        # card back URL
        urls.append(Book.__BACK_URL)

        # multithreaded download
        images = ImageLoader.load(urls, resolution, language, num_threads)
        # card back Image
        back_image = images.pop(-1)

        # shorthands
        # rows and columns per sheet
        r, c = grid
        # capacity of grid (reserve last space for card back)
        grid_capacity = r * c - 1
        # width, height per card
        w, h = resolution

        def paste_image(page, index, image):
            x, y = (index % c) * w, (index // c) * h
            page.paste(image, (x, y))

        self.__pages = []
        for images in chunks(images, grid_capacity):
            # create book page Image
            page = Image.new("RGB", (c * w, r * h))
            logger.info(f"New image: {page.size[0]}x{page.size[1]}")

            # paste card faces onto page
            for i, image in enumerate(images):
                paste_image(page, i, image)

            # paste card back in last position
            paste_image(page, c * r - 1, back_image)

            self.__pages.append(page)

    def save(self, filename):
        for i, page in enumerate(self.__pages):
            page.save(filename.format(i))

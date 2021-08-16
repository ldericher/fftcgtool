import logging

import yaml
from PIL import Image

from .cards import Cards
from .grid import Grid
from .imageloader import ImageLoader


class Book:
    def __init__(self, cards: Cards, grid: tuple[int, int], resolution: tuple[int, int], language: str,
                 num_threads: int):
        logger = logging.getLogger(__name__)

        # transform grid into Grid
        grid = Grid(grid)

        # sort cards by element, then alphabetically
        cards.sort(key=lambda x: x.name)
        cards.sort(key=lambda x: "Multi" if len(x.elements) > 1 else x.elements[0])

        # all card face URLs
        urls = [f"https://fftcg.cdn.sewest.net/images/cards/full/{card.code}_{language}.jpg" for card in cards]
        # card back URL (image by Aurik)
        urls.append(
            "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"
        )

        # multi-threaded download
        images = ImageLoader.load(urls, resolution, language, num_threads)
        # card back Image
        back_image = images.pop(-1)

        self.__pages = []
        for page_images, page_cards in zip(grid.chunks(images), grid.chunks(cards)):
            # create book page Image
            page_image = Image.new("RGB", grid * resolution)
            logger.info(f"New image: {page_image.size[0]}x{page_image.size[1]}")

            # paste card faces onto page
            for i, image in enumerate(page_images):
                grid.paste(page_image, i, image)

            # paste card back in last position
            grid.paste(page_image, grid.capacity, back_image)

            # save page
            self.__pages.append({
                "image": page_image,
                "cards": page_cards,
            })

    def __getitem__(self, index: int) -> Image.Image:
        return self.__pages[index]["image"]

    def save(self, file_name: str, book_yml_name: str) -> None:
        book: dict[str, dict[str, any]]

        # load book.yml file
        try:
            with open(book_yml_name, "r") as file:
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
        with open(book_yml_name, "w") as file:
            yaml.dump(book, file, Dumper=yaml.Dumper)

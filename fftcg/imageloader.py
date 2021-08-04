import io
import logging
import queue
import threading

import requests
from PIL import Image


class ImageLoader(threading.Thread):
    # Card faces by Square API
    __FACE_URL = "https://fftcg.cdn.sewest.net/images/cards/full/{}_{}.jpg"

    # Card back image by Aurik
    __BACK_URL = "http://cloud-3.steamusercontent.com/ugc/948455238665576576/85063172B8C340602E8D6C783A457122F53F7843/"

    def __init__(self, card_queue, resolution, language):
        threading.Thread.__init__(self)

        self.__queue = card_queue
        self.__resolution = resolution
        self.__language = language
        self.__images = {}

    def run(self) -> None:
        logger = logging.getLogger(__name__)

        while not self.__queue.empty():
            # take next card
            card = self.__queue.get()

            # fetch card image (retry on fail)
            while True:
                logger.info(f"get image for card {card}")
                try:
                    res = requests.get(ImageLoader.__FACE_URL.format(card.code, self.__language))
                    image = Image.open(io.BytesIO(res.content))

                    # unify images
                    image.convert("RGB")
                    image = image.resize(self.__resolution, Image.BICUBIC)
                    break
                except:
                    pass

            # put image in correct position
            self.__images[card] = image

            # image is processed
            self.__queue.task_done()

    @classmethod
    def load(cls, cards, resolution, language, num_threads):
        card_queue = queue.Queue()
        for card in cards:
            card_queue.put(card)

        loaders = []
        for _ in range(num_threads):
            loader = cls(card_queue, resolution, language)
            loaders.append(loader)
            loader.start()

        card_queue.join()

        images = {}
        for loader in loaders:
            images = {**images, **loader.images}

        # sort images to match the initial "cards" list
        images = [images[card] for card in cards]

        return images

    @property
    def images(self):
        return self.__images

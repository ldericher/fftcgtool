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
            i, card = self.__queue.get()

            # fetch card image (retry on fail)
            while True:
                logger.info("get image for card {}".format(card))
                try:
                    res = requests.get(ImageLoader.__FACE_URL.format(card.get_code(), self.__language))
                    image = Image.open(io.BytesIO(res.content))
                    image.convert("RGB")
                    image = image.resize(self.__resolution, Image.BICUBIC)
                    break
                except:
                    pass

            # put image in correct position
            self.__images[i] = image

            # image is processed
            self.__queue.task_done()

    @classmethod
    def spawn(cls, cards, resolution, language="eg", num_threads=16):
        card_queue = queue.Queue()
        for i, card in enumerate(cards):
            card_queue.put((i, card))

        for _ in range(num_threads):
            cls(card_queue, resolution, language).start()

        return card_queue

    def get_images(self):
        return self.__images

import io
import logging
import queue
import threading

import requests
from PIL import Image


class ImageLoader(threading.Thread):
    def __init__(self, url_queue, resolution, language):
        threading.Thread.__init__(self)

        self.__queue = url_queue
        self.__resolution = resolution
        self.__language = language
        self.__images = {}

    def run(self) -> None:
        logger = logging.getLogger(__name__)

        while not self.__queue.empty():
            # take next url
            url = self.__queue.get()

            # fetch image (retry on fail)
            while True:
                logger.info(f"downloading image {url}")
                try:
                    res = requests.get(url)
                    image = Image.open(io.BytesIO(res.content))

                    # unify images
                    image.convert("RGB")
                    image = image.resize(self.__resolution, Image.BICUBIC)
                    break
                except:
                    pass

            # put image in correct position
            self.__images[url] = image

            # image is processed
            self.__queue.task_done()

    @classmethod
    def load(cls, urls, resolution, language, num_threads):
        url_queue = queue.Queue()
        for url in urls:
            url_queue.put(url)

        loaders = []
        for _ in range(num_threads):
            loader = cls(url_queue, resolution, language)
            loaders.append(loader)
            loader.start()

        url_queue.join()

        # stitch all "images" dicts together
        images = {}
        for loader in loaders:
            images = {**images, **loader.images}

        # sort images to match the initial "cards" list
        images = [images[url] for url in urls]

        return images

    @property
    def images(self):
        return self.__images

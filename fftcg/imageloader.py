import io
import logging
import multiprocessing

import requests
from PIL import Image

from fftcg.utils import RESOLUTION


class ImageLoader:
    @classmethod
    def _load(cls, url: str) -> Image.Image:
        logger = logging.getLogger(__name__)

        # fetch image (retry on fail)
        while True:
            logger.info(f"downloading image {url}")
            try:
                res = requests.get(url)
                image = Image.open(io.BytesIO(res.content))

                # unify images
                image.convert(mode="RGB")
                return image.resize(RESOLUTION, Image.BICUBIC)

            except requests.exceptions.RequestException:
                pass

    @classmethod
    def load(cls, urls: list[str], num_threads: int) -> list[Image.Image]:
        with multiprocessing.Pool(num_threads) as p:
            return p.map(ImageLoader._load, urls)

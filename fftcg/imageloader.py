import logging
import multiprocessing

import requests
from PIL import Image

from .language import Language
from .utils import RESOLUTION

# constants
FALLBACK_LANGUAGE = Language("en")


class ImageLoader:
    @classmethod
    def _load_inner(cls, url_parts: tuple[str, str, str]) -> Image.Image:
        logger = logging.getLogger(__name__)
        base_url, code, lang_suffix = url_parts

        # put together image url
        url = base_url.format(code, lang_suffix)
        logger.info(f"trying image {url}")

        # fetch image (retry on fail)
        while True:
            try:
                res = requests.get(url, stream=True)
                break

            except requests.RequestException:
                pass

        # if rejected, substitute the english version
        if not res.ok:
            logger.warning(f"falling back to english version of {url}")
            return cls._load_inner((base_url, code, FALLBACK_LANGUAGE.image_suffix))

        # unify images
        image = Image.open(res.raw)
        image.convert(mode="RGB")
        return image.resize(RESOLUTION, Image.BICUBIC)

    @classmethod
    def load(cls, urls_parts: list[tuple[str, str, str]], num_threads: int) -> list[Image.Image]:
        with multiprocessing.Pool(num_threads) as p:
            return p.map(cls._load_inner, urls_parts)

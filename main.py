#!/usr/bin/env python3

from fftcg.opus import Opus
from fftcg.imageloader import ImageLoader


def main():
    opus = Opus(14)
    print(opus)

    queue = ImageLoader.spawn(opus, (429, 600))
    queue.join()


if __name__ == '__main__':
    main()

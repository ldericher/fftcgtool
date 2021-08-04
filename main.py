#!/usr/bin/env python3
import argparse
import logging
import os

from fftcg.opus import Opus
from fftcg.book import Book


def main():
    # Setup CLI
    parser = argparse.ArgumentParser(
        description='Imports FFTCG cards for TT-Sim.')

    parser.add_argument(
        'opusid',
        default="2",
        metavar="OpusID",
        nargs="?",
        help='the Opus to import')

    parser.add_argument(
        '-n', '--num_threads',
        type=int,
        default=20,
        metavar="COUNT",
        help='maximum number of concurrent requests')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(threadName)s %(message)s')

    opus = Opus(args.opusid)

    # output directory
    if not os.path.exists("out"):
        os.mkdir("out")
    os.chdir("out")

    book = Book(opus, (7, 10), (429, 600), "eg", 16)
    book.save(f"opus_{args.opusid}_{{}}.jpg")


if __name__ == '__main__':
    main()

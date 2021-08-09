#!/usr/bin/env python3
import argparse
import logging
import os

import fftcg

# constants
GRID = 10, 7  # default in TTsim: 10 columns, 7 rows
RESOLUTION = 429, 600  # default in TTsim: 480x670 pixels per card


def main() -> None:
    # set up CLI
    parser = argparse.ArgumentParser(
        description="Imports FFTCG cards for TT-Sim.",
    )

    parser.add_argument(
        "opus_id",
        default="promo",
        metavar="Opus_ID",
        nargs="?",
        help="the Opus to import",
    )

    parser.add_argument(
        "-n", "--num_threads",
        type=int,
        default=20,
        metavar="COUNT",
        help="maximum number of concurrent requests",
    )

    args = parser.parse_args()

    # set up logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(threadName)s %(message)s")

    # output directory
    if not os.path.exists("out"):
        os.mkdir("out")
    os.chdir("out")

    # main program
    opus = fftcg.Opus(args.opus_id)
    book = fftcg.Book(opus, GRID, RESOLUTION, "eg", args.num_threads)
    book.save(opus.filename)

    # bye
    logging.info("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
    logging.info("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

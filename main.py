#!/usr/bin/env python3
import argparse
import logging
import os

import fftcg

# constants
GRID = 10, 7  # default in TTsim: 10 columns, 7 rows
RESOLUTION = 429, 600  # default in TTsim: 480x670 pixels per card
BOOK_YML_NAME = "book.yml"


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
    book.save(opus.filename, BOOK_YML_NAME)

    # create elemental decks for opus
    carddb = fftcg.CardDB(BOOK_YML_NAME)

    def opus_filter(card: fftcg.Card):
        return card.code.opus == opus.number

    filters: list
    if opus.number == "PR":
        filters = [[opus_filter]]

    else:
        def element_filter(element: str):
            return lambda card: card.elements == [element]

        # simple cases: create lambdas for base elemental decks
        base_elements = ["Fire", "Ice", "Wind", "Earth", "Lightning", "Water"]
        element_filters = [element_filter(elem) for elem in base_elements]

        element_filters += [
            # light/darkness elemental deck
            lambda card: card.elements == ["Light"] or card.elements == ["Darkness"],
            # multi element deck
            lambda card: len(card.elements) > 1,
        ]

        # add in the opus_filter for all elemental decks
        filters = list(zip([opus_filter] * len(element_filters), element_filters))

    # make the decks
    for f in filters:
        print(carddb.make_deck(f))

    # bye
    logging.info("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
    logging.info("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

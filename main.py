#!/usr/bin/env python3
import argparse
import logging
import os

import fftcg

# constants
OUT_DIR_NAME = "out"  # name of output directory


def opus_decks(args: argparse.Namespace) -> list[fftcg.TTSDeck]:
    # import an opus
    opus = fftcg.Opus(args.opus_id)
    book = fftcg.Book(opus, "eg", args.num_requests)
    book.save()

    # load the current carddb
    carddb = fftcg.CardDB.get()
    carddb.load()
    carddb.update(opus)

    # create elemental decks for opus
    return opus.elemental_decks


def ffdecks_deck(args: argparse.Namespace) -> list[fftcg.TTSDeck]:
    # load the current carddb
    carddb = fftcg.CardDB.get()
    carddb.load()

    # import a deck
    return [fftcg.TTSDeck.from_ffdecks_deck(args.deck_id)]


def main() -> None:
    # set up CLI

    # main parser
    parser = argparse.ArgumentParser(
        prog="fftcgtool",
        description="Imports FFTCG cards for TT-Sim.",
    )

    subparsers = parser.add_subparsers(
        description="Import either an Opus to extend the mod, or import a deck to play right away.",
        dest="subcommand",
        help="valid subcommands",
        required=True,
    )

    # "opus" subcommand
    opus_parser = subparsers.add_parser(
        "opus",
        description="Imports an Opus from the square API and creates its elemental decks as JSON files.",
    )

    opus_parser.set_defaults(
        func=opus_decks
    )

    opus_parser.add_argument(
        "opus_id",
        type=str,
        metavar="Opus_ID",
        help="the Opus to import",
    )

    opus_parser.add_argument(
        "-n", "--num_requests",
        type=int,
        default=20,
        metavar="COUNT",
        help="maximum number of concurrent requests",
    )

    # "deck" subcommand
    deck_parser = subparsers.add_parser(
        "deck",
        description="Imports a Deck from the ffdecks.com API and creates it as a JSON file.",
    )

    deck_parser.set_defaults(
        func=ffdecks_deck
    )

    deck_parser.add_argument(
        "deck_id",
        type=str,
        metavar="Deck_ID",
        help="the Deck to import",
    )

    # set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(processName)s %(message)s",
    )

    # output directory
    if not os.path.exists(OUT_DIR_NAME):
        os.mkdir(OUT_DIR_NAME)

    os.chdir(OUT_DIR_NAME)

    # call function based on args
    args = parser.parse_args()
    for deck in args.func(args):
        deck.save()

    # bye
    logging.info("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
    logging.info("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

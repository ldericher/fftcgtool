#!/usr/bin/env python3
import argparse
import logging
import os

import fftcg

# constants
OUT_DIR_NAME = "out"  # name of output directory


def opus_decks(args: argparse.Namespace) -> list[fftcg.TTSDeck]:
    decks: list[fftcg.TTSDeck] = []

    for opus_id in args.opus_ids:
        # import an opus
        opus = fftcg.Opus(opus_id, args.language)
        book = fftcg.Book(opus, args.language, args.num_requests)
        book.save()

        # load the current carddb
        carddb = fftcg.CardDB.get()
        carddb.load()
        carddb.update(opus)

        decks.extend(opus.elemental_decks)

    # create elemental decks for opus
    return decks


def ffdecks_decks(args: argparse.Namespace) -> list[fftcg.TTSDeck]:
    # load the current carddb
    carddb = fftcg.CardDB.get()
    carddb.load()

    decks: list[fftcg.TTSDeck] = []
    for deck_id in args.deck_ids:
        decks.append(fftcg.TTSDeck.from_ffdecks_deck(deck_id))

    # import a deck
    return decks


def main() -> None:
    # set up CLI

    # main parser
    parser = argparse.ArgumentParser(
        prog="fftcgtool",
        description="Imports FFTCG cards for TT-Sim.",
    )

    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="count",
    )

    parser.add_argument(
        "-l", "--language",
        type=fftcg.Language,
        default="en",
        metavar="LANGUAGE",
        help="lang",
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
        "opus_ids",
        type=str,
        nargs="+",
        metavar="Opus_ID",
        help="the Opuses to import",
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
        func=ffdecks_decks
    )

    deck_parser.add_argument(
        "deck_ids",
        type=str,
        nargs="+",
        metavar="Deck_ID",
        help="the Decks to import",
    )

    # parse arguments
    args = parser.parse_args()

    # set up logging
    if args.verbose is None:
        args.verbose = logging.WARN
    elif args.verbose == 1:
        args.verbose = logging.INFO
    else:
        args.verbose = logging.DEBUG

    logging.basicConfig(
        level=args.verbose,
        format="%(levelname)s: %(processName)s %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.debug(f"{args = }")

    # output directory
    if not os.path.exists(OUT_DIR_NAME):
        os.mkdir(OUT_DIR_NAME)

    os.chdir(OUT_DIR_NAME)

    # call function based on args
    for deck in args.func(args):
        deck.save()

    # bye
    print("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
    print("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

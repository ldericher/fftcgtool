#!/usr/bin/env python3
import logging
import os
import sys
import zipfile

import click

import fftcg

# constants
OUT_DIR_NAME = "out"  # name of output directory


class LanguageParamType(click.ParamType):
    name = "lang"

    def convert(self, value, param, ctx) -> fftcg.Language:
        if isinstance(value, fftcg.Language):
            return value
        elif isinstance(value, str):
            return fftcg.Language(value)
        else:
            return fftcg.Language("")


LANGUAGE = LanguageParamType()


@click.group()
@click.option(
    "-v", "--verbose",
    help="increase output verbosity",
    count=True,
)
@click.option(
    "-l", "--language",
    type=LANGUAGE,
    default="en",
    help="language for imported objects",
)
@click.option(
    "-s", "--stdout",
    is_flag=True,
    help="print the deck files in a zip archive to stdout, skip creating JSONs on disk",
)
@click.pass_context
def main(ctx, verbose, language, stdout) -> None:
    """Imports FFTCG cards for TT-Sim."""

    ctx.ensure_object(dict)
    ctx.obj['LANG'] = language

    # set up logging
    if verbose == 0:
        verbose = logging.WARN
    elif verbose == 1:
        verbose = logging.INFO
    else:
        verbose = logging.DEBUG

    logging.basicConfig(
        level=verbose,
        format="%(levelname)s: %(processName)s %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info("fftcgtool started.")
    logger.debug(f"args: {verbose = }, {language = }, {stdout = }")

    # output directory
    if not os.path.exists(OUT_DIR_NAME):
        os.mkdir(OUT_DIR_NAME)

    os.chdir(OUT_DIR_NAME)

    # load the current carddb
    carddb = fftcg.CardDB()
    carddb.load()


@main.command()
@click.option(
    "-n", "--num_requests",
    type=int,
    default=20,
    help="maximum number of concurrent requests",
)
@click.argument(
    "opus_ids",
    nargs=-1,
    type=str,
    metavar="[OPUS_ID] ...",
)
@click.pass_context
def opuses(ctx, opus_ids, num_requests) -> list[fftcg.TTSDeck]:
    """
    Imports Opuses from the square API and creates its elemental decks as JSON files.

    OPUS_ID: each of the Opuses to import
    """

    ctx.ensure_object(dict)
    language = ctx.obj['LANG'] or fftcg.Language("")

    carddb = fftcg.CardDB()
    decks: list[fftcg.TTSDeck] = []
    for opus_id in opus_ids:
        # import an opus
        opus = fftcg.Opus(opus_id, language)
        book = fftcg.Book(opus, language, num_requests)
        book.save()

        carddb.update(opus)
        decks.extend(opus.elemental_decks)

    carddb.upload_prompt()

    # create elemental decks for opus
    return decks


@main.command()
@click.argument(
    "deck_ids",
    nargs=-1,
    type=str,
    metavar="[DECK_ID] ...",
)
def ffdecks(deck_ids) -> list[fftcg.TTSDeck]:
    """
    Imports Decks from the ffdecks.com API and creates it as a JSON file.

    DECK_ID: each of the Decks to import
    """

    print(f"{deck_ids = }")
    decks: list[fftcg.TTSDeck] = []
    for deck_id in deck_ids:
        # import a deck
        decks.append(fftcg.TTSDeck.from_ffdecks_deck(deck_id))

    return decks


@main.result_callback()
def process_decks(decks: list[fftcg.TTSDeck], verbose, language, stdout):
    # arg needed because it's in this group
    int(verbose)

    # decide what to do with the decks
    if stdout:
        # print out a zip file
        with open(sys.stdout.fileno(), "wb", closefd=False, buffering=0) as raw_stdout:
            with zipfile.ZipFile(raw_stdout, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                # put the decks into that zip file
                for deck in decks:
                    zip_file.writestr(deck.file_name, deck.get_json(language))

    else:
        # save the decks to disk
        for deck in decks:
            deck.save(language)

        # bye
        print("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
        print("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

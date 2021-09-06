#!/usr/bin/env python3
import logging
import os
import sys
import zipfile

import click

import fftcg


class LanguageParamType(click.ParamType):
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
    metavar="LANG",
)
@click.option(
    "-z", "--zip",
    type=click.File("wb"),
    help="wrap deck files into a zip archive, skip creating individual JSONs",
    metavar="FILE",
)
@click.option(
    "-o", "--output",
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        file_okay=False,
    ),
    help="use specified output directory instead of ./out",
    default="out",
    metavar="DIR",
)
@click.option(
    "-u", "--db-url",
    type=str,
    help="load immutable CardDB from URL instead of local, overrides -f",
    metavar="URL",
)
@click.option(
    "-f", "--db-file",
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        file_okay=True,
    ),
    default="carddb.zip",
    help="use specified CardDB file instead of ./out/carddb.zip",
    metavar="FILE",
)
@click.pass_context
def main(ctx, **kwargs) -> None:
    """Imports FFTCG cards for TT-Sim."""

    ctx.ensure_object(dict)
    ctx.obj["language"] = kwargs["language"]

    # set up logging
    if kwargs["verbose"] == 0:
        verbose = logging.WARN
    elif kwargs["verbose"] == 1:
        verbose = logging.INFO
    else:
        verbose = logging.DEBUG

    logging.basicConfig(
        level=verbose,
        format="%(levelname)s: %(processName)s %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info("fftcgtool started.")
    logger.debug(f"{kwargs = }")

    # output directory
    if not os.path.exists(kwargs["output"]):
        os.mkdir(kwargs["output"])

    os.chdir(kwargs["output"])

    # load the current carddb
    if kwargs["db_url"] is not None:
        try:
            fftcg.CardDB(kwargs["db_url"])

        except (ValueError, KeyError, zipfile.BadZipFile) as cause:
            logger.critical(f"Couldn't initialize CardDB: {cause}")
            sys.exit(1)

    else:
        fftcg.RWCardDB(kwargs["db_file"])


@main.command()
@click.option(
    "-n", "--num-requests",
    type=int,
    default=20,
    help="maximum number of concurrent requests",
)
@click.argument(
    "opus-ids",
    nargs=-1,
    type=str,
    metavar="[OPUS-ID] ...",
)
@click.pass_context
def opuses(ctx, opus_ids, num_requests) -> list[fftcg.TTSDeck]:
    """
    Imports Opuses from the square API and creates its elemental decks as JSON files.

    OPUS_ID: each of the Opuses to import
    """

    ctx.ensure_object(dict)
    language = ctx.obj["language"] or fftcg.Language("")

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
    carddb.save()

    # create elemental decks for opus
    return decks


@main.command()
@click.argument(
    "deck-ids",
    nargs=-1,
    type=str,
    metavar="[DECK-ID] ...",
)
def ffdecks(deck_ids) -> list[fftcg.TTSDeck]:
    """
    Imports Decks from the ffdecks.com API and creates it as a JSON file.

    DECK_ID: each of the Decks to import
    """

    decks: list[fftcg.TTSDeck] = []
    for deck_id in deck_ids:
        # import a deck
        decks.append(fftcg.TTSDeck.from_ffdecks_deck(deck_id))

    return decks


@main.result_callback()
def finalize(decks: list[fftcg.TTSDeck], **kwargs):
    # decide what to do with the decks
    if kwargs["zip"] is not None:
        if decks:
            # create zip file
            with zipfile.ZipFile(kwargs["zip"], "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                # put the decks into that zip file
                for deck in decks:
                    zip_file.writestr(deck.file_name, deck.get_json(kwargs["language"]))

    else:
        # save the decks to disk
        for deck in decks:
            deck.save(kwargs["language"])

        # bye
        print("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
        print("Thanks for using fftcgtool!")


if __name__ == "__main__":
    main()

#!/usr/bin/python3

import argparse
import json
import logging
import os
import requests

from opus import Opus

# constants
GRID = 7, 10    # default in TTsim: 7 rows, 10 columns
RESO = 429, 600 # default in TTsim: 480x670 pixels per card
FURL = "https://ffdecks.com/api/cards/basic" # FFDecks API URL

def main():
    # Setup CLI
    parser = argparse.ArgumentParser(
        description='Imports FFTCG cards for TT-Sim.')

    parser.add_argument(
        'opusid',
        default="7",
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
    logger = logging.getLogger(__name__)

    # Fetch and parse card database from ffdecks API
    ffdecks_raw = requests.get(FURL)
    ffdecks = json.loads(ffdecks_raw.content.decode("utf-8"))

    # Load an Opus
    opus_data = (card_data for card_data in ffdecks["cards"] if card_data["serial_number"].startswith(args.opusid))
    myOpus = Opus(opus_data)

    # output directory
    if not os.path.exists("out"):
        os.mkdir("out")
    os.chdir("out")

    # compose custom deck images
    faceurls = []
    for i, image in enumerate(myOpus.get_images(GRID, RESO, args.num_threads)):
        filename = "opus_{}_{}.jpg".format(args.opusid, i)
        image.save(filename)
        # ask for upload
        iurl = input("Upload '{}' and paste URL: ".format(filename))
        if not iurl:
            # add local file (maybe upload to steam cloud in cloud manager)
            logging.warn("Using local file for '{}'.".format(filename))
            iurl = "file://" + os.path.abspath(filename)
        faceurls.append(iurl)

    # Build json for element decks
    elementaldecks = [
        ["Fire"],
        ["Water"],
        ["Lightning"],
        ["Ice"],
        ["Wind"],
        ["Earth"],
        ["Light", "Dark"]
    ]
    for i, elements in enumerate(elementaldecks):
        json_filename = "opus_{}_{}.json".format(args.opusid, "_".join(elements))
        with open(json_filename, "w") as json_file:
            cardfilter = lambda card: card._element in elements
            json_data = myOpus.get_json(args.opusid, "/".join(elements), GRID, cardfilter, faceurls)
            json_file.write(json_data)

    # Bye
    logging.info("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
    logging.info("Thanks for using fftcgtool!")


if __name__ == "__main__":
   main()

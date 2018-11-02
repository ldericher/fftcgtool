#!/usr/bin/env python3

# base config
opusid = 6

# constants
grid = 7, 10    # default in TTsim: 7 rows, 10 columns
reso = 480, 670 # default in TTsim: 480x670 pixels per card

# set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(threadName)s %(message)s')
logger = logging.getLogger(__name__)

# output directory
import os
if not os.path.exists("out"):
    os.mkdir("out")
os.chdir("out")

# load an Opus
from opus import Opus
myOpus = Opus()
myOpus.load(opusid, 2, 2)

# compose custom deck images
faceurls = []
for i, image in enumerate(myOpus.get_images(grid, reso)):
    filename = "opus_%d_%d.jpg" % (opusid, i)
    image.save(filename)
    # ask for upload
    iurl = input("Upload '%s' and paste URL: " % (filename))
    if not iurl:
        # add local file (maybe upload to steam cloud in cloud manager)
        logging.warn("Using local file for '%s'." % (filename))
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
    json_filename = "opus_%d_%s.json" % (opusid, "_".join(elements))
    with open(json_filename, "w") as json_file:
        cardfilter = lambda card: card._element in elements
        json_data = myOpus.get_json("/".join(elements), grid, cardfilter, faceurls)
        json_file.write(json_data)

logging.info("Done. Put the generated JSON files in your 'Saved Objects' Folder.")
logging.info("Thanks for using fftcgtool!")

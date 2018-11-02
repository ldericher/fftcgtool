import queue
import threading
import logging
import json

from card import Card, BACKURL
from PIL import Image


# multithreaded card image loading
class imageLoader(threading.Thread):
    def __init__(self, queue, composite, composite_lock, grid, resolution):
        threading.Thread.__init__(self)
        self.__queue = queue
        self.__composite = composite
        self.__lock = composite_lock
        self.__grid = grid
        self.__resolution = resolution

    def run(self):
        logger = logging.getLogger(__name__)
        # shorthands
        r, c = self.__grid       # rows and columns per sheet
        w, h = self.__resolution # width, height per card

        while not self.__queue.empty():
            # take next card
            i, card = self.__queue.get()

            # fetch card image (retry on fail)
            while True:
                logger.info("get image for card {}".format(card))
                im = card.get_image(self.__resolution)
                if im:
                    break

            # paste image in correct position
            self.__lock.acquire()
            x, y = (i % c) * w, (i // c) * h
            logger.info("paste image {} at P{}({}, {})".format(im.mode, i, x, y))
            self.__composite.paste(im, (x, y, x+w, y+h))
            self.__lock.release()

            # image is processed
            self.__queue.task_done()


class Opus:
    def __init__(self, data):
        self._cards = []

        for card_data in data:
            card = Card(card_data)
            self._cards.append(card)

        # sort every element alphabetically
        self._cards.sort(key=lambda x: x._serial)
        self._cards.sort(key=lambda x: x._name)
        self._cards.sort(key=lambda x: x._element)

    def __get_sheets(self, grid):
        # cards per sheet
        count = grid[0]*grid[1] - 1
        # flat copy
        cards = self._cards

        # while there are cards
        while cards:
            # get a chunk
            yield cards[:count]
            # remove that chunk
            cards = cards[count:]

    def get_images(self, grid, resolution, threadnum=16):
        logger = logging.getLogger(__name__)
        # shorthands
        r, c = grid       # rows and columns per sheet
        w, h = resolution # width, height per card

        for sheet in self.__get_sheets(grid):
            # enqueue a sheet of cards
            cardQueue = queue.Queue()
            for i, card in enumerate(sheet):
                cardQueue.put((i, card))

            # add hidden face
            hidden = Card(0)
            cardQueue.put((r * c - 1, hidden))

            # create a new card sheet
            sheet = Image.new("RGB", (c*w, r*h))
            logger.info("New image: {}x{}".format(*sheet.size))

            # beware concurrent paste
            sheet_lock = threading.Lock()

            # start multithreading, wait for finish
            for _ in range(threadnum):
                imageLoader(cardQueue, sheet, sheet_lock, grid, resolution).start()
            cardQueue.join()

            # sheet image is generated, return now
            yield sheet

    def get_json(self, opusid, deckname, grid, cardfilter, faceurls):
        # shorthands
        r, c = grid       # rows and columns per sheet

        jsondict = { "ObjectStates": [ {
            "Name": "Deck",
            "Nickname": "Opus {} {}".format(opusid, deckname),
            "Description": "",

            "Transform": {
                "scaleX": 2.17822933,
                "scaleY": 1.0,
                "scaleZ": 2.17822933
            },

            "Locked": False,
            "Grid": True,
            "Snap": True,
            "Autoraise": True,
            "Sticky": True,
            "Tooltip": True,
            "GridProjection": False,
            "Hands": False,
            "SidewaysCard": False,

            "DeckIDs": [],
            "CustomDeck": {},
            "ContainedObjects": []
        } ] }

        for sheetnum, sheet in enumerate(self.__get_sheets(grid)):
            # get current face
            faceurl = faceurls[sheetnum]
            # first sheet is "CustomDeck 1"
            sheetnum = sheetnum + 1

            # recurring sheet dictionary
            sheetdict = { str(sheetnum): {
                "FaceURL": faceurl,
                "BackURL": BACKURL,
                "NumWidth": c,
                "NumHeight": r
            } }

            for cardnum, card in enumerate(sheet):
                if not cardfilter(card):
                    continue

                # cardid 123 is on "CustomDeck 1", 3rd row, 4th column
                cardid = sheetnum * 100 + (cardnum // c) * 10 + (cardnum % c) * 1
                jsondict["ObjectStates"][0]["DeckIDs"].append(cardid)

                # Add card object to ContainedObjects
                carddict = card.get_dict()
                carddict["CardID"] = cardid
                carddict["CustomDeck"] = sheetdict
                jsondict["ObjectStates"][0]["ContainedObjects"].append(carddict)

                # Add sheet to CustomDecks
                jsondict["ObjectStates"][0]["CustomDeck"].update(sheetdict)

        return json.dumps(jsondict, indent=2)

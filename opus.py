import queue
import threading
import logging
import json

from card import Card
from PIL import Image


# multithreaded card loading
class cardLoader(threading.Thread):
    def __init__(self, opusid, queue, cards):
        threading.Thread.__init__(self)
        self.__opusid = opusid
        self.__queue = queue
        self.__cards = cards

    def run(self):
        logger = logging.getLogger(__name__)
        while not self.__queue.empty():
            # take next card number
            cardid = self.__queue.get()

            # try to load that card
            card = Card()
            if card.load(self.__opusid, cardid):
                # success!
                self.__cards.append(card)
                logger.info("found %s" % (card))
            else:
                # seems like the end of this opus!
                logger.info("exiting")
                break
        if self.__queue.empty():
            logger.warn("empty queue, maxsize might be too small!")


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

            # fetch card image
            logger.info("get image for card %s" % (card))
            im = card.get_image(self.__resolution)

            # paste image in correct position
            self.__lock.acquire()
            x, y = (i % c) * w, (i // c) * h
            logger.info("paste image %s at P%d(%d, %d)" % (im.mode, i, x, y))
            self.__composite.paste(im, (x, y, x+w, y+h))
            self.__lock.release()

            # image is processed
            self.__queue.task_done()


class Opus:
    def load(self, opusid, maxsize=500, threadnum=16):
        self._opusid = opusid
        self._cards = []

        # enqueue all card ids
        idQueue = queue.Queue()
        for cardid in range(1, maxsize + 1):
            idQueue.put(cardid)

        # start multithreading, wait for finish
        threads = [cardLoader(opusid, idQueue, self._cards) for _ in range(threadnum)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # sort every element alphabetically
        self._cards.sort(key=lambda x: x._cardid)
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
            hidden = Card()
            hidden.load(0, 0)
            cardQueue.put((r * c - 1, hidden))

            # create a new card sheet
            sheet = Image.new("RGB", (c*w, r*h))
            logger.info("New image: %dx%d" % sheet.size)

            # beware concurrent writes
            sheet_lock = threading.Lock()

            # start multithreading, wait for finish
            for _ in range(threadnum):
                imageLoader(cardQueue, sheet, sheet_lock, grid, resolution).start()
            cardQueue.join()

            # sheet image is generated, return now
            yield sheet

    def get_json(self, deckname, grid, cardfilter, faceurls):
        # shorthands
        r, c = grid       # rows and columns per sheet

        # get BackURL
        back = Card()
        back.load(0, 0)
        backurl = back._iurl

        jsondict = { "ObjectStates": [ {
            "Name": "Deck",
            "Nickname": "Opus %d %s" % (self._opusid, deckname),
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
                "BackURL": backurl,
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

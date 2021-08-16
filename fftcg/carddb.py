import yaml

_DictOfDicts = dict[str, dict[str, any]]


class CardDB(_DictOfDicts):
    def __init__(self, book_yml_name: str):
        book: _DictOfDicts

        # load book.yml file
        try:
            with open(book_yml_name, "r") as file:
                book = yaml.load(file, Loader=yaml.Loader)
        except FileNotFoundError:
            book = {}

        # "invert" book into card database:
        # every card is indexable by its code
        carddb: _DictOfDicts = {}

        for fn, content in book.items():
            carddb |= {
                str(card.code): {
                    "card": card,
                    "file": fn,
                    "index": i,
                } for i, card in enumerate(content["cards"])
            }

        super().__init__(carddb)

        # write carddb.yml file
        with open("carddb.yml", "w") as file:
            yaml.dump(self, file, Dumper=yaml.Dumper)

    def make_deck(self, filters):
        # filter codes by card criteria
        codes = [
            content["card"].code
            for content in self.values()
            if all([f(content["card"]) for f in filters])
        ]

        from .ttsdeck import TTSDeck
        return TTSDeck(codes, self)

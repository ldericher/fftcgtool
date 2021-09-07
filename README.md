# fftcgtool

Card import tool for [Final Fantasy TCG Complete](https://steamcommunity.com/sharedfiles/filedetails/?id=889160751) mod
for the [Tabletop Simulator](http://berserk-games.com/tabletop-simulator/)

## Usage

```
Usage: fftcgtool.py [OPTIONS] COMMAND [ARGS]...

  Imports FFTCG cards for TT-Sim.

Options:
  -v, --verbose        increase output verbosity  [x>=0]
  -l, --language LANG  language for imported objects
  -z, --zip FILE       wrap deck files into a zip archive, skip creating
                       individual JSONs
  -o, --output DIR     use specified output directory instead of ./out
  -u, --db-url URL     load immutable CardDB from URL instead of local,
                       overrides -f
  -f, --db-file FILE   use specified CardDB file instead of ./out/carddb.zip
  --help               Show this message and exit.

Commands:
  ffdecks  Imports Decks from the ffdecks.com API and creates it as a...
  opuses   Imports Opuses from the square API and creates its elemental...
```

## Examples

### Import Opuses

```sh
fftcgtool opuses 14
```

Import Opus XIV.

Card face images are saved to the `out/images/` subdirectory.

For each of the six base elements, an "elemental deck" is saved to the `out/decks/` subdirectory. An elemental deck
contains all cards of that element. Light and Darkness element cards is contained in a combined elemental deck.
Multi-element cards are contained in another combined elemental deck.

Additionally, the card database zip is saved to the `out/` subdirectory. It contains all card data imported so far.

Finally, you will be asked to upload each card face image and provide a link.

Non-existent subdirectories will be created.

```sh
fftcgtool opuses --help
```

Show more info about the `opuses` subcommand.

```sh
fftcgtool opuses -n 11 chaos 4 8 13
```

Import the "Boss Deck Chaos" and the Opuses IV, VIII and XIII using 11 parallel processes.

For small Opuses like the Boss Cards, only a single deck is saved to the `out/decks/` subdirectory.

### Import decks from ffdecks.com

```sh
fftcgtool ffdecks 6272690272862208
# or
fftcgtool ffdecks 'https://ffdecks.com/deck/6272690272862208'
```

Import the deck [WOL Mono Fire🔥](https://ffdecks.com/deck/6272690272862208) from ffdecks.com.

You will need a card database zip with all needed cards for this to work. Cards not found in the zip will be omitted.

The imported deck will be saved to the `out/decks/` subdirectory. It will be created if it doesn't exist.

```sh
fftcgtool ffdecks --help
```

Show more info about the `ffdecks` subcommand.

## Installation

### Using your system's `python3`

1. Make sure you have at least python version `3.9` with `pip` installed. To test, run `python --version` or similar.
2. Install `fftcgtool`.
    - Either from this repository: Use `pip install "git+https://github.com/ldericher/fftcgtool"`.
    - Or from your local source: Clone this repository and run `pip install /path/to/fftcgtool`.
3. Run `pipenv run ./fftcgtool.py` from project root directory.
4. You can `alias fftcgtool='PIPENV_PIPFILE="'$(pwd)'/Pipfile" pipenv run "'$(pwd)'/fftcgtool.py"'` from project root
   directory to define `fftcgtool` shorthand for your running shell.

### Using a `docker` container

1. Make sure you have a working installation of `docker` software.
2. Update your local image.
    - Either use `docker pull ldericher/fftcgtool`.
    - Or build it yourself: Clone this repository and run `docker build --pull --tag ldericher/fftcgtool .` inside.
3. Run `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool` in any directory.
4. You can `alias fftcgtool='docker run --rm -it -v "$(pwd)/out:/app/out" -u "$(id -u):$(id -g)" ldericher/fftcgtool'`
   to define `fftcgtool` shorthand for your running shell.

Output files will go to subdirectory `./out`. CLI arguments are supported
as `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool -n 2 5` (imports Opus 5 using 2 threads)

## To-Do-List

- `deck` subcommand, which would read a custom deck list in text format

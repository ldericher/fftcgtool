# fftcgtool

Card import tool for [Final Fantasy TCG Complete](https://steamcommunity.com/sharedfiles/filedetails/?id=889160751) mod for the [Tabletop Simulator](http://berserk-games.com/tabletop-simulator/)


## Quick Start

If needed, customize `main.py` variables:

- `opusid`: The Card opus you want to import
- `num_threads`: Lower this for really weak systems
- `opus_size`: 500 here means the script will correctly import anything containing *up to* 500 cards

### using your system's `python3`

1. Make sure `PIL` and `requests` python3 libraries (or equivalent) are installed.
1. Run `main.py` in project root directory.

### using a `docker` container

1. Build the container using `docker build -t ldericher/fftcgtool .` in project root directory.
1. Run `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool` in project root directory.


## Future work

- Add command line interface for `main.py` variables
- Multiple opus import

# fftcgtool

Card import tool for [Final Fantasy TCG Complete](https://steamcommunity.com/sharedfiles/filedetails/?id=889160751) mod for the [Tabletop Simulator](http://berserk-games.com/tabletop-simulator/)


## Usage

    usage: main.py [-h] [-n COUNT] [OpusID]

    Imports FFTCG cards for TT-Sim.

    positional arguments:
      OpusID                the Opus to import

    optional arguments:
      -h, --help            show this help message and exit
      -n COUNT, --num_threads COUNT
                            maximum number of concurrent requests

### Run using your system's `python3`

1. Make sure `PIL` and `requests` python3 libraries (or equivalent) are installed.
1. Run `./main.py` from project root directory.

### Run using a `docker` container

1. Make sure you have a working installation of `docker` software.
1. Update your local image `docker pull ldericher/fftcgtool`.
1. Run `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool` in any directory.

Output files will go to subdirectory `./out`. CLI arguments are supported as `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool -n 2 5` (imports Opus 5 using 2 threads)


## Future work

- Multiple opus import

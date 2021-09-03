# fftcgtool

Card import tool for [Final Fantasy TCG Complete](https://steamcommunity.com/sharedfiles/filedetails/?id=889160751) mod for the [Tabletop Simulator](http://berserk-games.com/tabletop-simulator/)


## Usage

```
usage: fftcgtool [-h] [-v] [-l LANG] [-s] {opuses,ffdecks} ...

Imports FFTCG cards for TT-Sim.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -l LANG, --language LANG
                        language for imported objects
  -s, --stdout          print the deck files in a zip archive to stdout, skip creating JSONs on disk

subcommands:
  Import either an Opus to extend the mod, or import a deck to play right away.

  {opuses,ffdecks}      valid subcommands
```

### Run using your system's `python3`

1. Make sure you have at least python version `3.9` installed. 
   To test, run `python --version` or similar. 
   Also, `pipenv` should be installed for that python version.
   Refer to [pipenv installation guide](https://pipenv.pypa.io/en/latest/install/) if needed.
2. To install `fftcgtool` dependencies, run `pipenv install --deploy` from project root directory.
3. Run `pipenv run ./main.py` from project root directory.
4. You can `alias fftcgtool='PIPENV_PIPFILE="'$(pwd)'/Pipfile" pipenv run "'$(pwd)'/main.py"'` from
   project root directory to define `fftcgtool` shorthand for your running shell.

### Run using a `docker` container

> Caveat: This simplistic container runs `fftcgtool` as root user.
> All generated files will thus be owned by `root:root` by default.

1. Make sure you have a working installation of `docker` software.
2. Update your local image
   - Either use `docker pull ldericher/fftcgtool`
   - Or build it yourself
      1. Clone this repository
      2. Inside this directory, run `docker build --pull --tag ldericher/fftcgtool .`
3. Run `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool` in any directory.
4. You can `alias fftcgtool='docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool'`
   to define `fftcgtool` shorthand for your running shell.

Output files will go to subdirectory `./out`. CLI arguments are supported as `docker run --rm -it -v "$(pwd)/out:/app/out" ldericher/fftcgtool -n 2 5` (imports Opus 5 using 2 threads)


## Future work

- Multiple opus import

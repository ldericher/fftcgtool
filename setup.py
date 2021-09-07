from setuptools import setup

setup(
    name="fftcgtool",
    version="0.2",
    author="LDericher",
    author_email="ldericher@gmx.de",
    setup_requires="setuptools-pipfile",
    use_pipfile=True,
    entry_points={
        "console_scripts": [
            "fftcgtool = fftcgtool.scripts.fftcgtool:main"
        ],
    },
    license="LICENSE",
    description="Card import tool for 'Final Fantasy TCG Complete' mod for the 'Tabletop Simulator' game",
    long_description=open("README.md").read(),
)

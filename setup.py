from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def read_local_file(f_name):
    with open(path.join(here, f_name), encoding="utf-8") as f:
        contents = f.read()
    # If on win, get rid of CR from CRLF
    return contents.replace("\r", "")


long_description = read_local_file("README.md")
requirements = read_local_file("requirements.txt").split("\n")

setup(
    name="discordhealthcheck",
    version="0.0.6",
    description="A small Python 3 library and command line app to automate Docker health checks for discord.py bots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psidex/discordhealthcheck",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="discord discord.py docker healthcheck health check bot",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["discordhealthcheck = discordhealthcheck.__main__:main"]
    },
)

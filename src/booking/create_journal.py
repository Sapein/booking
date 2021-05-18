""" Creates a Journal from user input. """
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple, Union, cast
from enum import Enum


@dataclass
class Journal:
    """ Representation of a Journal.
    This is a very bare-bones representation due to it
    just being what we need."""
    name: str
    abbreviation: str

    def create_journal(self, filename, path):
        """ Write Journal to disk. """
        with open("{}/{}".format(path, filename), 'w') as f:
            f.write("{} - {}\n".format(self.name, self.abbreviation))
            f.write("Page 1\n")


def verified_input(prompt: Any, verifier: Callable[[str], bool]) -> str:
    """ Checks and ensures input is correct, and
    reprompts user if it is incorrect. """
    while not verifier((i := input(prompt))):
        pass
    return i


def default_input(prompt: Any, default: str) -> str:
    """ This gets a user input, and returns the default if
    nothing is input."""
    return (verified_input(prompt, lambda: True) or default)


if __name__ == "__main__":
    name = default_input(("Please enter the name of the Journal"
                          "[Default: General]: "),
                         lambda x: bool(x) or not boo,
                         "General")
    abbr = default_input(("Please enter the abbreviation for the journal"
                          "[Default: {}]: "
                          ).format(name[:3].upper()),
                         lambda x: bool(x),
                         name[:3].upper())
    filename = default_input(("Please input the filename for the journal"
                              "[Default: {}.jnl]: "
                              ).format(name.lower()),
                             lambda x: bool(x),
                             "{}.jnl".format(name.lower()))
    path = default_input("Please input the path for the file to be made at"
                         "[Default: ./]: ",
                         lambda x: bool(x),
                         "./")
    Journal(name=name, abbreviation=abbr).create_journal(filename, path)

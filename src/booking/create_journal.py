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


def default_input(prompt: Any, default: str) -> str:
    """ It's basically input, but with a default option
    if the entered value is blank. """
    return (input(prompt) or default)


if __name__ == "__main__":
    name = default_input(("Please enter the name of the Journal"
                          "[Default: General]: "),
                         "General")
    abbr = default_input(("Please enter the abbreviation for the journal"
                          "[Default: {}]: "
                          ).format(name[:3].upper()),
                         name[:3].upper())
    filename = default_input(("Please input the filename for the journal"
                              "[Default: {}.jnl]: "
                              ).format(name.lower()),
                             "{}.jnl".format(name.lower()))
    path = default_input("Please input the path for the file to be made at"
                         "[Default: ./]: ",
                         "./")
    Journal(name=name, abbreviation=abbr).create_journal(filename, path)

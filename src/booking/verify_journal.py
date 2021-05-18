""" Verifies the Journal's Syntax. """
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple, Union, cast
from enum import Enum


class currency(str, Enum):
    """ Represents currencies. """
    usd = "usd"


class transaction_type(str, Enum):
    """ Represents the types of transactions we can do. """
    debit = "Dr"
    credit = "Cr"
    Debit = "Debit"
    Credit = "Credit"

    @staticmethod
    def _not(value: str) -> "transaction_type":
        """ 'Inverts' to opposing type of transaction. """
        is_debit = value.capitalize() == transaction_type.debit
        is_debit = is_debit or value.capitalize() == transaction_type.Debit

        is_credit = value.capitalize() == transaction_type.credit
        is_credit = is_credit or value.capitalize() == transaction_type.Credit

        if is_debit:
            return transaction_type.credit
        elif is_credit:
            return transaction_type.debit
        else:
            raise TypeError("Type must be of transaction_type!")


@dataclass
class Journal_Entry:
    """ Represents a Journal Entry. """
    refrence: str
    date: str
    account: str
    amount: int
    _type: transaction_type
    curr: currency
    desc: Optional[str] = ""
    post_ref: Optional[int] = None


@dataclass
class Journal:
    """ Represents an entire Journal. """
    page_count: int
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    pages: tuple[tuple[Journal_Entry, ...], ...] = ((),)

def parse_journal(journal: list[str]) -> Journal:
    """ Parses the Journal from a list of strings representing a file
    split by newlines. """
    nameline, pageline, *journal = journal
    page_number: int = int(pageline.lower().split(" ")[1])

    try:
        name, abbr = nameline.split(' - ')
    except ValueError:
        name = " - ".join(nameline.split(" - ")[:-1])
        abbr = nameline.split(" - ")[-1]

    pages: list[tuple[Journal_Entry, ...]] = []
    page: list[Journal_Entry] = []

    for line in journal:
        if line.lower().startswith('page'):
            page_number = int(line.lower().split(" ")[1])
            pages.append(tuple(page))
            page = []
        elif line:
            page.append(parse_entry(line))
    else:
        pages.append(tuple(page))

    if not pages:
        pages = [()]
    return Journal(page_number, name, abbreviation=abbr, pages=tuple(pages))


def parse_entry(line: str) -> Journal_Entry:
    """ Parses a singular Journal Entry """
    journal_reference = line.split(" ")[0]
    date = line.split(" ")[1]
    line = line.split("{} ".format(date))[1]
    account = ""

    for word in (line := line.split(" ")):  # type: ignore
        word_is_type = (word.lower() == "dr" or word.lower() == "cr")
        if word_is_type and line[line.index(word) + 1].isdigit():
            curr = line[line.index(word) + 2]
            pr, desc = parse_entry_optionals(' '.join(line[line.index(curr) + 1:]))  # noqa
            return Journal_Entry(journal_reference, date, account,
                                 int(line[line.index(word) + 1]),
                                 transaction_type(word), currency(curr),
                                 desc=desc, post_ref=pr)
        else:
            account = "{} {}".format(account, word)
    raise SyntaxError("Account name does not end!")


def parse_entry_optionals(line: str) -> tuple[Optional[int], Optional[str]]:
    """ Parses the optional parts of an entry
    (Description and Post Reference). """
    pr: Optional[Union[int, str]] = None
    desc: Optional[str] = None
    if "Pr:" in line:
        pr = int(line.split("Pr: ")[1].split(" ")[0])
    if "Description:" in line:
        desc = line.split("Description: ")[1]
        if pr and "Pr: {}".format(pr) in desc:
            desc = desc.split("Pr: {}".format(pr))[0]
    return cast(Optional[int], pr), desc


def verified_input(prompt: Any, verifier: Callable[[str], bool]) -> str:
    """ Checks and ensures input is 'verified' by a function
    prior to returning. If not, it reprompts the user. """
    while not verifier((i := input(prompt))):
        pass
    return i


def verifiy_default(prompt: Any,
                    verifier: Callable[[str], bool],
                    default: Any) -> str:
    """ verified_input but with a deafult. """
    return (verified_input(prompt, verifier) or default)


def default_input(prompt: Any, default: Any) -> str:
    """ verify_default, but just assumes it is valid. """
    return verifiy_default(prompt, lambda x: True, default)


def read_journal(filename: str, path: str) -> str:
    """ Reads a journal file. """
    with open('{}/{}'.format(path, filename), 'r') as f:
        return f.read()

if __name__ == "__main__":
    path = verified_input("Please enter the Journal Path: ", lambda x: bool(x))
    filename = default_input(("Please enter the filename of the Journal "
                              "(leave blank specified in path): "),
                             path.split('/')[-1])
    if filename == path.split('/')[-1]:
        path = '/'.join(path.split('/')[:-1])

    current = parse_journal(read_journal(filename, path).split('\n'))

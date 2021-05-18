""" Creates a Journal Entry. """
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple, Union, cast
from enum import Enum

class currency(str, Enum):
    usd = "usd"

class transaction_type(str, Enum):
    debit = "Dr"
    credit = "Cr"
    Debit = "Debit"
    Credit = "Credit"

    @staticmethod
    def _not(value: str) -> "transaction_type":
        if value.capitalize() == transaction_type.debit or value.capitalize() == transaction_type.Debit:
            return transaction_type.credit
        elif value.capitalize() == transaction_type.credit or value.capitalize() == transaction_type.Credit:
            return transaction_type.debit
        else:
            raise TypeError("Type must be of transaction_type!")

@dataclass
class Journal_Entry:
    refrence: str
    date: str
    account: str
    amount: int
    _type: transaction_type
    curr: currency
    desc: Optional[str] = ""
    post_ref: Optional[int] = None

    def __str__(self) -> str:
        if self.post_ref and self.desc:
            return "{ref} {date} {acc} {ty} {amnt} {curr} Pr:{pr} Description: {desc}".format(ref=self.refrence.strip(" "),
                                                                                              acc=self.account.strip(" "),
                                                                                              date=self.date.strip(" "),
                                                                                              ty=self._type.strip(" "),
                                                                                              amnt=self.amount,
                                                                                              pr=self.post_ref,
                                                                                              desc=self.desc.strip(" "),
                                                                                              curr=self.curr.strip(" "))
        elif self.post_ref:
            return "{ref} {date} {acc} {ty} {amnt} {curr} Pr:{pr}".format(ref=self.refrence.strip(" "),
                                                                          acc=self.account.strip(" "),
                                                                          date=self.date.strip(" "),
                                                                          ty=self._type.strip(" "),
                                                                          amnt=self.amount,
                                                                          pr=self.post_ref,
                                                                          curr=self.curr.strip(" "))
        elif self.desc:
            return "{ref} {date} {acc} {ty} {amnt} {curr} Description:{desc}".format(ref=self.refrence.strip(" "),
                                                                                     acc=self.account.strip(" "),
                                                                                     date=self.date.strip(" "),
                                                                                     ty=self._type.strip(" "),
                                                                                     amnt=self.amount,
                                                                                     desc=self.desc.strip(" "),
                                                                                     curr=self.curr.strip(" "))
        else:
            return "{ref} {date} {acc} {ty} {amnt} {curr}".format(ref=self.refrence.strip(" "),
                                                                  acc=self.account.strip(" "),
                                                                  date=self.date.strip(" "),
                                                                  ty=self._type.strip(" "),
                                                                  amnt=self.amount,
                                                                  curr=self.curr.strip(" "))



@dataclass
class Journal:
    page_count: int
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    pages: tuple[tuple[Journal_Entry, ...]] = ((),)

    def create_journal(self, filename, path):
        with open("{}/{}".format(path, filename), 'w') as f:
            f.write("{} - {}\n".format(self.name, self.abbreviation))
            for page in self.pages:
                f.write("Page {}\n".format(self.pages.index(page) + 1))
                for trans in page:
                    f.write("{}\n".format(str(trans)))


def parse_journal(journal: list[str]) -> Journal:
    nameline, pageline, *journal = journal
    page_number: int = int(pageline.lower().split(" ")[1])

    try:
        name, abbr = nameline.split(' - ')
    except ValueError:
        name = " - ".join(nameline.split(" - ")[:-1])
        abbr = nameline.split(" - ")[-1]

    pages: list[tuple[Journal_Entry, ...]] = []
    page: list[Journal_Entry]= []

    for line in journal:
        if line.lower().startswith('page'):
            page_number = int(line.lower().split(" ")[1])
            pages.append(tuple(page))
            page = []
        elif line:
            page.append(parse_entry(line))
    else:
        pages.append(tuple(page))

    if not pages: pages = [()]
    return Journal(page_number, name, abbreviation=abbr, pages=cast(Tuple[Tuple[Journal_Entry, ...]], tuple(pages)))

def parse_entry(line: str) -> Journal_Entry:
    journal_reference = line.split(" ")[0]
    date = line.split(" ")[1]
    line = line.split("{} ".format(date))[1]
    account = ""
    amount = 0
    _type = ""
    curr = ""
    pr = None
    desc = None
    pos = 0

    for word in (line := line.split(" ")): # type: ignore
        if (word.lower() == 'dr' or word.lower() == 'cr') and line[line.index(word) + 1].isdigit():
            _type = word
            amount = int(line[line.index(word) + 1])
            curr = line[line.index(word) + 2]
            pr, desc = parse_entry_optionals(' '.join(line[line.index(curr) + 1:]))
            break
        else:
            account = "{} {}".format(account, word)


    return Journal_Entry(journal_reference, date, account, amount, transaction_type.abbr(_type), currency.abbr(curr), desc=desc, post_ref=pr)

def parse_entry_optionals(line: str) -> tuple[Optional[int], Optional[str]]:
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
    while not verifier((i := input(prompt))):
        pass
    return i

def read_journal(filename: str, path: str) -> str:
    with open('{}/{}'.format(path, filename), 'r') as f:
        return f.read()

if __name__ == "__main__":
    path: str  = verified_input("Please enter the Journal Path: ", lambda x: bool(x))
    filename: str = verified_input("Pleae enter the Filename of the Journal (leave blank if in path): ", lambda x: True)
    if not filename: (filename := path.split('/')[-1], path := '/'.join(path.split('/')[:-1]))

    current: Journal = parse_journal(read_journal(filename, path).split('\n'))

    date: str = verified_input("Please enter the Date of the transaction (dd.mm.yyyy): ", lambda x: bool(x))
    account1: str = verified_input("Please enter the name of an Account: ", lambda x: bool(x))
    account2: str = verified_input("Please enter the name of a different Account: ", lambda x: True if account1.lower() != x.lower() else False)
    entry_type: transaction_type = transaction_type(verified_input("Is this a debit or credit for Account 1?: ",
                                                                   lambda x: True if x.capitalize() in list(transaction_type) else False))
    amount: int = int(verified_input("Please enter the amount: ", str.isdigit))
    curr: currency = currency(verified_input("Please enter the currency (abbreviation): ", lambda x: True if x.lower() in list(currency) else False))
    post_ref: str = verified_input("Please enter the Post Reference (Leave blank if unposted): ", lambda x: True if str.isdigit(x) or not x else False)
    description: str = input("Please enter a description for this transaction (Optional): ")

    e1 = Journal_Entry("{}-{}-{}".format(current.abbreviation,
                                         current.page_count,
                                         len(current.pages[-1]) + 1),
                                         date, account1, amount, entry_type, curr, description, cast(Optional[int], post_ref))
    e2 = Journal_Entry("{}-{}-{}".format(current.abbreviation,
                                         current.page_count,
                                         len(current.pages[-1]) + 1),
                                         date, account2, amount, transaction_type._not(entry_type), curr, description, cast(Optional[int], post_ref))

    new_books = current.pages[:-1]  + (current.pages[-1] + (e1, e2),)
    Journal(current.page_count, name=current.name, abbreviation=current.abbreviation, pages=new_books).create_journal(filename, path)

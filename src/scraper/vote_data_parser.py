import csv
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

data_path = "../../long_term_bill_records"


@dataclass
class Bill:
    title: str
    desc: str
    house: str
    votes: Dict[str, int]


@dataclass
class BillText:
    title: str
    desc: str


# ARGS: bill_name - filename of a bill, without the extension
# RETURN: Bill object containing title, description, house and voting records of members for bill
def get_bill(bill_name: str) -> Bill:
    votes = dict()
    house = ""
    votes_path = ""
    if os.path.exists(f"***REMOVED***data_path***REMOVED***/house_vote/***REMOVED***bill_name***REMOVED***.csv"):
        house = "HOUSE"
        votes_path = f"***REMOVED***data_path***REMOVED***/house_vote/***REMOVED***bill_name***REMOVED***.csv"
    elif os.path.exists(f"***REMOVED***data_path***REMOVED***/senate_vote/***REMOVED***bill_name***REMOVED***.csv"):
        house = "SENATE"
        votes_path = f"***REMOVED***data_path***REMOVED***/senate_vote/***REMOVED***bill_name***REMOVED***.csv"
    else:
        print("Error: could not find file...")
    with open(votes_path) as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            name, vote = row
            vote = int(vote)
            votes[name] = vote

    title_file = open(f"***REMOVED***data_path***REMOVED***/full_text/***REMOVED***bill_name***REMOVED***.txt", "r")
    title = title_file.readline()

    desc_file = open(f"***REMOVED***data_path***REMOVED***/summary/***REMOVED***bill_name***REMOVED***.txt", "r")
    desc = desc_file.readline()

    return Bill(title, desc, house, votes)


# ARGS: bill_name - filename of a bill, without the extension
# RETURN: BillText object containing title and description of bill
def get_bill_text(bill_name: str) -> Optional[BillText]:
    title_file = open(f"***REMOVED***data_path***REMOVED***/full_text/***REMOVED***bill_name***REMOVED***.txt", "r")
    title = title_file.readline()

    # Some problems with dataset, so check that the summary exists
    try:
        desc_file = open(f"***REMOVED***data_path***REMOVED***/summary/***REMOVED***bill_name***REMOVED***.txt", "r")
    except FileNotFoundError:
        return None
    desc = desc_file.readline()

    return BillText(title, desc)


# RETURN: List of objects with title and descriptions of each bill that has been voted on.
def get_all_bill_text() -> List[BillText]:
    res = []
    for f in os.listdir(f"***REMOVED***data_path***REMOVED***/house_vote"):
        res.append(get_bill_text(os.path.splitext(f)[0]))
    for f in os.listdir(f"***REMOVED***data_path***REMOVED***/senate_vote"):
        res.append(get_bill_text(os.path.splitext(f)[0]))
    return res


if __name__ == "__main__":
    b = get_bill("BILLS-112s307rfh")
    l = get_all_bill_text()
    print(b)

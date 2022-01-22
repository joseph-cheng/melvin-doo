import csv
import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class Bill:
    house: str
    title: str
    desc: str
    votes: Dict[str, int]


def get_bill(bill_name: str):
    votes = dict()
    house = ""
    data_path = "../../long_term_bill_records"
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

    return Bill(house, title, desc, votes)


if __name__ == "__main__":

    b = get_bill("BILLS-112s307rfh")
    print(b)

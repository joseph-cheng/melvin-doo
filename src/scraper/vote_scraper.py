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
    if os.path.exists(f"{data_path}/house_vote/{bill_name}.csv"):
        house = "HOUSE"
        votes_path = f"{data_path}/house_vote/{bill_name}.csv"
    elif os.path.exists(f"{data_path}/senate_vote/{bill_name}.csv"):
        house = "SENATE"
        votes_path = f"{data_path}/senate_vote/{bill_name}.csv"
    else:
        print("Error: could not find file...")
    with open(votes_path) as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            name, vote = row
            vote = int(vote)
            votes[name] = vote

    title_file = open(f"{data_path}/full_text/{bill_name}.txt", "r")
    title = title_file.readline()

    desc_file = open(f"{data_path}/summary/{bill_name}.txt", "r")
    desc = desc_file.readline()

    return Bill(house, title, desc, votes)


if __name__ == "__main__":

    b = get_bill("BILLS-112s307rfh")
    print(b)

import csv
import os
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
import datetime

data_path = "../../scraper/long_term_bill_records"


@dataclass
class Bill:
    title: str
    desc: str
    house: str
    votes: Dict[str, int]
    date: str


@dataclass
class BillText:
    title: str
    desc: str


# ARGS: name - Name of congressman to be searched
# RETURNS: Full name of congressman
def convert_name(name: str) -> Optional[str]:
    url = f"https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22{name}%22%7D"
    r = requests.get(url)

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find("span", {"class": "result-heading"}).a.text
    except Exception:
        print("error parsing name")
        return None


def convert_all_names(votes: Dict[str, int]):
    n = len(votes)
    name_table = []
    for i, (name, _) in enumerate(votes.items()):
        new_name = convert_name(name)
        name_table.append(f"{name},{new_name}\n")
        if i % 10 == 0:
            print(f"{(i * 100)/n}%")
    f = open("converted_names.csv", "w")
    f.writelines(name_table)
    f.close()


# ARGS: bill_name - filename of a bill, without the extension
# RETURN: Bill object containing title, description, house and voting records of members for bill
def get_bill(bill_name: str, name_cache) -> Bill:
    votes = dict()
    house = ""
    votes_path = ""
    if os.path.exists(f"{data_path}/house_vote/{bill_name}.csv"):
        house = "HOUSE"
        votes_path = f"{data_path}/house_vote/{bill_name}.csv"
    elif os.path.exists(f"{data_path}/senate_vote/{bill_name}.csv"):
        house = "SENATE"
        votes_path = f"{data_path}/senate_vote/{bill_name}.csv"
    else:
        print("Error: could not find file...")
    with open(votes_path, "r+") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            name, vote = row
            vote = int(vote)
            if name not in name_cache:
                return None
            name = name_cache[name]
            votes[name] = vote

    # convert_all_names(votes)

    title_file = open(f"{data_path}/full_text/{bill_name}.txt", "r")
    title = title_file.readline()
    title_file.close()

    desc_file = open(f"{data_path}/summary/{bill_name}.txt", "r")
    desc = desc_file.readline()
    print(desc)
    desc_file.close()

    date = datetime.datetime(1787 + int(bill_name[6:9]) * 2 + 1, 1, 3).strftime("%Y-%m-%d")

    return Bill(title[:65535], desc, house, votes, date)


# ARGS: bill_name - filename of a bill, without the extension
# RETURN: BillText object containing title and description of bill
def get_bill_text(bill_name: str) -> Optional[BillText]:
    title_file = open(f"{data_path}/full_text/{bill_name}.txt", "r")
    title = title_file.readline()

    # Some problems with dataset, so check that the summary exists
    try:
        desc_file = open(f"{data_path}/summary/{bill_name}.txt", "r")
    except FileNotFoundError:
        return None
    desc = desc_file.readline()

    return BillText(title, desc)


# RETURN: List of objects with title and descriptions of each bill that has been voted on.
def get_all_bill_text() -> List[BillText]:
    res = []
    text_list = []
    for f in os.listdir(f"{data_path}/house_vote"):
        t = get_bill_text(os.path.splitext(f)[0])
        if t and hash(t.title) not in text_list:
            res.append(t)
            text_list.append(hash(t.title))
    for f in os.listdir(f"{data_path}/senate_vote"):
        t = get_bill_text(os.path.splitext(f)[0])
        if t and hash(t.title) not in text_list:
            res.append(t)
            text_list.append(hash(t.title))
    return res

def get_all_bills():
    f = open("converted_names.csv")
    name_cache = dict()
    for line in f.readlines():
        vals = line.split(":")
        name_cache[vals[0]] = "".join(vals[1:])[:-1]
    res = []
    text_list = []
    for f in os.listdir(f"{data_path}/house_vote"):
        t = get_bill(os.path.splitext(f)[0], name_cache)
        if t is None:
            continue
        if t and hash(t.title) not in text_list:
            res.append(t)
            text_list.append(hash(t.title))
    for f in os.listdir(f"{data_path}/senate_vote"):
        t = get_bill(os.path.splitext(f)[0], name_cache)
        if t is None:
            continue
        if t and hash(t.title) not in text_list:
            res.append(t)
            text_list.append(hash(t.title))
    return res


if __name__ == "__main__":
    f = open("converted_names.csv")
    name_cache = dict()
    for line in f.readlines():
        vals = line.split(":")
        name_cache[vals[0]] = "".join(vals[1:])[:-1]

    print(get_all_bills())

from datetime import date
from datetime import datetime
import mysql
import requests
from bs4 import BeautifulSoup

class Trade:
    def __init__(self, person, ticker, buy_or_sell, date):
        self.person = person
        self.ticker = ticker
        self.buy_or_sell = buy_or_sell
        self.date = date

    def __repr__(self):
        return f"{self.person} | {self.ticker} | {self.buy_or_sell} | {self.date}"



def process_line(line):
    line = line.replace(", ", "|")
    line = line.strip().split(",")
    person = line[1].replace("|", ", ")
    ticker = line[4]
    buy_or_sell = "buy" if "Buy" in line[6] else "sell"
    trade_date = datetime.strptime(line[5], "%d/%b/%Y").strftime("%Y-%m-%d")
    trade = Trade(person, ticker, buy_or_sell, trade_date)

    return trade

def convert_name(name):
    url = f"https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22{name}%22%7D"
    r = requests.get(url)

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find("span", {"class": "result-heading"}).a.text
    except Exception:
        print(name)
        print("error parsing name")
        return None


def convert_all_names(names):
    n = len(names)
    name_table = []
    for i, name in enumerate(names):
        new_name = convert_name(name)
        if new_name is not None:
            name_table.append(f"{name}:{new_name}\n")
        if i % 10 == 0:
            print(f"{(i * 100)/n}%")
    f = open("converted_joe_names.csv", "w+")
    f.writelines(name_table)
    f.close()

name_translations = {}
with open("converted_joe_names.csv", "r") as f:
    for line in f.readlines():
        line = line.strip().split(':')
        name_translations[line[0]]= line[1]

conn = mysql._open_connection()
names = set() 
with open("../../scraper/trades.csv", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        trade = process_line(line)
        trade_name = trade.person
        trade_name = trade_name.split()
        trade_name[0] = trade_name[0][:-1]
        trade_name = trade_name[1] + " " + trade_name[0]
        if trade_name not in name_translations:
            continue
        trade.person = name_translations[trade_name]

        print(trade.date)

        mysql.process_trade(conn,trade)
mysql._close_connection(conn)




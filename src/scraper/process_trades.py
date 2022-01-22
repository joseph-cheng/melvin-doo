from datetime import date
from datetime import datetime

class Trade:
    def __init__(self, person, ticker, buy_or_sell, date):
        self.person = person
        self.ticker = ticker
        self.buy_or_sell = buy_or_sell
        self.date = date

    def __repr__(self):
        return f"***REMOVED***self.person***REMOVED*** | ***REMOVED***self.ticker***REMOVED*** | ***REMOVED***self.buy_or_sell***REMOVED*** | ***REMOVED***self.date***REMOVED***"



def process_line(line):
    line = line.replace(", ", "|")
    line = line.strip().split(",")
    person = line[1].replace("|", ", ")
    ticker = line[4]
    buy_or_sell = "buy" if "Buy" in line[6] else "sell"
    trade_date = datetime.strptime(line[5], "%d/%b/%Y").strftime("%Y-%m-%d")
    trade = Trade(person, ticker, buy_or_sell, trade_date)

    return trade

with open("trades.csv", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        print(process_line(line))



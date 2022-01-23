from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time
import mysql

import os

if 'HOME' in os.environ.keys():
    if os.environ['HOME'] == '/home/joe':
        import mysql

        import sys
        sys.path.insert(0, "../../../")
elif 'HOMEPATH' in os.environ.keys():
    if os.environ['HOMEPATH'] == '\\Users\\Aga':
        import mysql

        import sys
        sys.path.insert(0, "../../../")
else:
    import src.webapp.backend.mysql
from src.scraper.stock_charts import get_stock_prices


app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)


@app.route('/stocks', methods=['GET'])
def get_stock_data():
    args = request.args
    ticker = request.args.get('ticker')
    start_raw = request.args.get('start')
    end_raw = request.args.get('end')
    start = datetime.datetime.strptime(start_raw.split("T")[0], "%Y-%m-%d")
    end = datetime.datetime.strptime(end_raw.split("T")[0], "%Y-%m-%d")

    return {'data': get_stock_prices(ticker, start, end)}


# Returns list of names (for autocomplete)
@app.route('/members', methods=['GET'])
def get_members_list():
    f = None
    if 'HOME' in os.environ.keys():
        if os.environ["HOME"] == "/home/joe":
            f = open("names.txt", "r")
    elif 'HOMEPATH' in os.environ.keys():
        if os.environ['HOMEPATH'] == '\\Users\\Aga':
            f = open("names.txt", "r")
    else:
        f = open("src/webapp/backend/names.txt", "r")
    names = dict()
    for name in f.readlines():
        name = name[:-1]
        names[name] = None
    return names


@app.route('/get_congressperson_bills', methods=['GET'])
def get_congressperson_data():
    conn = mysql.open_connection()
    congressperson_name = request.args.get('name')
    congressperson_name = "Representative Pelosi, Nancy"
   
    votes_query = f"SELECT DISTINCT persons.name, bills.bill, bills.ID, votes.voted_for, categories.category FROM votes INNER JOIN bills ON bills.ID = votes.bill_ID INNER JOIN billcategories as bc ON bc.bill_ID = votes.bill_ID INNER JOIN categories ON categories.ID = bc.category_ID INNER JOIN persons on persons.ID = votes.person_ID INNER JOIN companycategories as cc on cc.category_ID = bc.category_ID INNER JOIN trades ON trades.company_ID = cc.company_ID WHERE trades.person_ID = votes.person_ID AND persons.name = '{congressperson_name}';"
    votes_result = mysql._execute_sql(conn, votes_query)
    print(votes_result)
    mysql.close_connection(conn)

    votes_array = []
    for row in votes_result:
        votes_array.append({
            "Name": row[0],
            "Bill ID": row[1],
            "Bill": row[2][:128],
            "For/Against": row[3],
            "Category": row[4],
            })


    return {
        'votes': votes_array,
    }


@app.route('/trades', methods=['GET'])
def get_trades():
    args = request.args
    bill_id = request.args.get('bill_id')
    person_name = request.args.get('name')

    conn = mysql.open_connection()

    query = "SELECT company_id, was_buy, date FROM trades"
    query += " INNER JOIN companycategories AS cc ON cc.company_id = trades.company_id"
    query += " INNER JOIN billcategories AS bc ON bc.category_id = cc.category_id"
    query += " INNER JOIN persons AS p ON p.id = trades.person_id"
    query += " WHERE (bc.bill_id = {0} AND p.name = {1});".format(bill_id, person_name)

    results = mysql._get_query(conn, query)

    trades = []

    for res in results:
        trades.append(res)

    mysql.close_connection(conn)

    return trades

@app.route("/trades_old", methods=['GET'])
def get_trades_old():
    billID = request.args.get("billID")
    if request.args.get("billID") == '0':
        return { 'trades': [{"Name": "John", "Ticker": "GOOG", "Buy/Sell": "BUY", "Date": datetime.datetime(2019, 10, 15)},
                {"Name": "Alice", "Ticker": "TSLA", "Buy/Sell": "SELL", "Date": datetime.datetime(2020, 1, 13)}]}
    return { 'trades': [{"Name": "Blah", "Ticker": "APPL", "Buy/Sell": "BUY", "Date": datetime.datetime(2018, 10, 15)},
                {"Name": "Melvin", "Ticker": "NOK", "Buy/Sell": "BUY", "Date": datetime.datetime(2021, 1, 13)}]}

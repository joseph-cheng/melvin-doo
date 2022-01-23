from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time
import mysql

import os

if os.environ['HOME'] == '/home/joe':
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
    if os.environ["HOME"] == "/home/joe":
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
   
    votes_query = f"SELECT persons.name, bills.ID, votes.voted_for, categories.category FROM votes INNER JOIN bills ON bills.ID = votes.bill_ID INNER JOIN billcategories as bc ON bc.bill_ID = votes.bill_ID INNER JOIN categories ON categories.ID = bc.category_ID INNER JOIN persons on persons.ID = votes.person_ID INNER JOIN companycategories as cc on cc.category_ID = bc.category_ID INNER JOIN trades ON trades.company_ID = cc.company_ID WHERE trades.person_ID = votes.person_ID AND persons.name = '{congressperson_name}';"
    votes_result = mysql._execute_sql(conn, votes_query)
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
    person_id = request.args.get('person_id')

    conn = mysql.open_connection()

    query = "SELECT company_id, was_buy, date FROM trades"
    query += " INNER JOIN companycategories AS cc ON cc.company_id = trades.company_id"
    query += " INNER JOIN billcategories AS bc ON bc.category_id = cc.category_id"
    query += " WHERE (bc.bill_id = {0} AND trades.person_id = {1});".format(bill_id, person_id)

    results = mysql._get_query(conn, query)

    trades = []

    for res in results:
        trades.append(res)

    mysql.close_connection(conn)

    return trades
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
   
    votes_query = f"SELECT persons.name, bills.ID, bills.bill, votes.voted_for, categories.category FROM persons INNER JOIN votes ON (persons.ID = votes.person_ID) INNER JOIN bills on (bills.ID = votes.bill_ID) INNER JOIN trades on (persons.ID = trades.person_id) INNER JOIN companycategories ON (companycategories.company_ID = trades.company_ID) INNER JOIN billcategories ON (billcategories.bill_ID = bills.ID) INNER JOIN categories on (categories.ID = billcategories.bill_ID) WHERE persons.name = '{congressperson_name}' AND companycategories.category_ID = billcategories.category_ID;"
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

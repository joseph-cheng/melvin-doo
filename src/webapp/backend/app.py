from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time

import os

if os.environ['HOME'] == '/home/joe':
    import mysql

    import sys
    sys.path.insert(0, "../../../")

    from src.scraper.stock_charts import get_stock_prices
else:
    import src.webapp.backend.mysql
    from src.scraper.stock_charts import get_stock_prices


app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)


@app.route('/stocks/', methods=['GET'])
def get_stock_data():
    args = request.args
    ticker = request.args.get('ticker')
    start_raw = request.args.get('start')
    end_raw = request.args.get('end')
    start = datetime.datetime.strptime(start_raw.split("T")[0], "%Y-%m-%d")
    end = datetime.datetime.strptime(end_raw.split("T")[0], "%Y-%m-%d")

    return ***REMOVED***'data': get_stock_prices(ticker, start, end)***REMOVED***


@app.route('/get_congressperson_data', methods=['GET'])
def get_congressperson_data():
    conn = mysql.open_connection()
    congressperson_name = request.args.get('name')
    query = f"SELECT persons.name, companies.company, trades.was_buy, trades.date FROM persons INNER JOIN trades ON (persons.ID = trades.person_ID) INNER JOIN companies ON (companies.ID = trades.company_ID) WHERE persons.name = '***REMOVED***congressperson_name***REMOVED***';"
    result = mysql._execute_sql(conn, query)
    mysql.close_connection(conn)

    trades_array = []
    for row in result:
        trades_array.append(***REMOVED***
            "Name": row[0],
            "Ticker": row[1],
            "Buy/Sell": row[2],
            "Date": row[3].strftime("%Y-%m-%d")
            ***REMOVED***)

    # TODO: actually get data

    return ***REMOVED***
        'votes': [
            ***REMOVED***
                'test': 5,
                'test2': 6,
            ***REMOVED***,
            ***REMOVED***
                'test': 7,
                'test2': 8,
            ***REMOVED***,

        ],

        'trades': trades_array
    ***REMOVED***

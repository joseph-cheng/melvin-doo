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

    return {'data': get_stock_prices(ticker, start, end)}


@app.route('/get_congressperson_data', methods=['GET'])
def get_congressperson_data():
    conn = mysql._open_connection()
    congressperson_name = request.args.get('name')
    query = f"SELECT persons.name, companies.company, trades.was_buy, trades.date FROM persons INNER JOIN trades ON (persons.ID = trades.person_ID) INNER JOIN companies ON (companies.ID = trades.company_ID) WHERE persons.name = '{congressperson_name}';"
    result = mysql._execute_sql(conn, query)
    mysql._close_connection(conn)

    trades_array = []
    for row in result:
        trades_array.append({
            "Name": row[0],
            "Ticker": row[1],
            "Buy/Sell": row[2],
            "Date": row[3].strftime("%Y-%m-%d")
            })

    # TODO: actually get data

    return {
        'votes': [
            {
                'test': 5,
                'test2': 6,
            },
            {
                'test': 7,
                'test2': 8,
            },

        ],

        'trades': trades_array
    }

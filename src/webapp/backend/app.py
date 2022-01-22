from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time

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
    congressperson_name = request.args.get('name')

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

        'trades': [
            {
                'test': 1,
                'test2': 2,
            },
            {
                'test': 1,
                'test2': 2,
            },

        ]
    }

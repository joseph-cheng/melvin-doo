from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker')
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    # TODO: actually get stock information

    return ***REMOVED***
            'data': [
                100,
                105,
                101,
                115,
                145,
                125,
                95,
                85,
                115,
                105,
                100,
            ]
           ***REMOVED***

@app.route('/get_congressperson_data', methods=['GET'])
def get_congressperson_data():
    congressperson_name = request.args.get('name')

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

            'trades': [
                ***REMOVED***
                    'test': 1,
                    'test2': 2,
                ***REMOVED***,
                ***REMOVED***
                    'test': 1,
                    'test2': 2,
                ***REMOVED***,
                    
                ]
            ***REMOVED***


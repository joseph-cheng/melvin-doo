from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime
import time
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

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


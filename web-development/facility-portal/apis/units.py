import os
from datetime import timedelta
from time import time
import pandas as pd
import json
import urllib3
from urllib.parse import quote 

from flask_login import login_required
from flask_restful import Resource

from sqlalchemy import create_engine

### Load Enviornment Variables

EDW_HOST = os.environ['EDW_HOST']
EDW_PORT = os.environ['EDW_PORT']
EDW_DB = os.environ['EDW_DB']
EDW_USER = os.environ['EDW_USER']
EDW_PWD = os.environ['EDW_PWD']
VERBOSE = os.environ['VERBOSE']
DEBUG = os.environ['DEBUG']


### Load Data From Facility Master EDW (Ataccama) ###
dataset = pd.DataFrame()

age = 0

engine = create_engine(f'teradatasql://{EDW_USER}:{quote(EDW_PWD)}@{EDW_HOST}:{EDW_PORT}/{EDW_DB}')

query = open('apis/units.sql','r').read()

# Create Function to pull data from Ataccama that only allows one refresh per hour

def getData():
    global dataset, engine, query, age
    
    # Current Time Inverval in hours
    t = int(time()/3600) 
    
    # If Current Time Inverval > Last Refresh Time Interval then pull fresh data from Facility Master EDW
    if t > age :
        dataset = pd.read_sql(query,engine)
        if VERBOSE:
            print("Local data refreshed from EDW.")
        age = t
    # else:
    #    if VERBOSE:
    #        print("No data pull.")
    return dataset

# Create API resource returning Facility Master site data

class getUnits(Resource):
    decorators = [login_required] #Prevent rouge use of API
    def get(self):
        return json.loads(getData().to_json(orient='records'))
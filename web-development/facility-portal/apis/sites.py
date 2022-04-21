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

RDM_HOST = os.environ['RDM_HOST']
RDM_PORT = os.environ['RDM_PORT']
RDM_DB = os.environ['RDM_DB']
RDM_USER = os.environ['RDM_USER']
RDM_PWD = os.environ['RDM_PWD']
VERBOSE = os.environ['VERBOSE']
DEBUG = os.environ['DEBUG']


### Load Data From Facility Master RDM (Ataccama) ###
dataset = pd.DataFrame()

age = 0

engine = create_engine(f'mssql+pymssql://{RDM_USER}:{quote(RDM_PWD)}@{RDM_HOST}:{RDM_PORT}/{RDM_DB}')

query = open('apis/sites.sql','r').read()

# Create Function to pull data from Ataccama that only allows one refresh per minute

def getData():
    global dataset, engine, query, age
    
    # Current Time Inverval in minutes
    t = int(time()/60) 
    
    # If Current Time Inverval > Last Refresh Time Interval then pull fresh data from Facility Master RDM
    if t > age :
        dataset = pd.read_sql(query,engine)
        if VERBOSE:
            print("Local data refreshed from RDM.")
        age = t
    # else:
    #    if VERBOSE:
    #        print("No data pull.")
    return dataset

# Create API resource returning Facility Master site data

class getSites(Resource):
    decorators = [login_required] #Prevent rouge use of API
    def get(self):
        return json.loads(getData().to_json(orient='records'))
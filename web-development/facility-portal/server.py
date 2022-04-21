# Core packages
import os
from datetime import timedelta, date
from time import time

# Data packages
import pandas as pd
import json
import uuid

# Database packages
from sqlalchemy import create_engine

# Web service packages
import requests
from flask import Flask, render_template, request, url_for, redirect, session, Markup  # Core Flask server packages
from flask_restful import Resource, Api  # RESTful API packages
from flask_login import LoginManager, login_required, login_user, logout_user, current_user  # Authenticaion packages

# Load modules containing API functions
from apis import sites
from apis import units

# Handle clean exits
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

### Load Enviornment Variables

AUTH_URL = os.environ['AUTH_URL']
AUTH_KEY = os.environ['AUTH_KEY']
AUTH_APP = os.environ['AUTH_APP']
SESSION_TIMEOUT = os.environ['SESSION_TIMEOUT']
LOGIN_MESSAGE = os.environ['LOGIN_MESSAGE']
VERBOSE = os.environ['VERBOSE']
DEBUG = os.environ['DEBUG']

### Initiate and configure Flask object ###

application = Flask(__name__)
application.config.update(DEBUG=DEBUG, SECRET_KEY=str(uuid.uuid4()).replace('-','')) #Use random UUID for security
api = Api(application)

# Timeout feature
@application.before_request
def before_request():
    session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=int(SESSION_TIMEOUT))

### User Authentication ###

# User Class (Required)
class User:
  def __init__(self,user):
    self.user=user
  def is_authenticated(self):
    return True
  def is_active(self):
    return True
  def is_anonymous(self):
    return False
  def get_id(self):
    return self.user

# Login Manager (Required)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view="login"

# User Object Reload Method (Required)
@login_manager.user_loader
def load_user(userid):
  return User(userid)

# Login Function
@application.route("/login",methods=["GET","POST"])
def login():
    # FORM POST - Request authentication from CERBERUS
    if request.method == 'POST':
        next_page = request.form['next']
        username = request.form['username']
        password = request.form['password']
        headers = {
            "x-api-key": AUTH_KEY,
            "Content-Type": "application/json"
        }
        auth_data = {
            "threefour": str(username),
            "password": str(password),
            "application": AUTH_APP
        }
        r = requests.post(AUTH_URL, data=json.dumps(auth_data), headers=headers,  verify=False)
        print('%s - %s' %(r.status_code, username))

        #If CERBERUS returns code 200, the user is authenticated and passed to a new User class
        if r.status_code==200:
            new_user = User(username)
            login_user(user=new_user)
            if VERBOSE:
                print('%s - User: %s - Login Successful' %(str(request.remote_addr), username)) #Change to logging method
            return redirect(next_page or url_for('index'))
        
        #If CERBERUS returns anything else, the access is denied
        else:
            if VERBOSE:
                print('%s - User: %s - Invalid Login' %(str(request.remote_addr), username)) #Change to logging method
            return 'Not Authorized'
        
    else:
        next_page = request.args.get('next')
        return render_template('login.htm', next=next_page, message=Markup(LOGIN_MESSAGE))

# Logout Function
@application.route("/logout")
@login_required
def logout():
    _user = current_user.get_id()
    _addr = str(request.remote_addr)
    if VERBOSE:
        print('%s - User: %s - Logout' %(_addr, _user)) #Change to logging method
    logout_user()
    return '%s - User: %s - Logout' %(_addr, _user)

### General Variables for Jinja
@application.context_processor
def inject_date():
    return {'date': date}


### Create APIs

api.add_resource(sites.getSites, '/api/sites/')
api.add_resource(units.getUnits, '/api/units/')

### Create Routes

@application.route('/')
@login_required
def index():
    site = request.args.get('site', default = '', type = str)
    _user = current_user.get_id()
    if site == 'mapSites':
        return render_template('map-sites.htm', username=_user)
    elif site == 'dataSites':
        return render_template('data-sites.htm', username=_user)
    elif site == 'dataUnits':
        return render_template('data-units.htm', username=_user)
    elif site == 'map': # legacy
        return render_template('map-sites.htm', username=_user)
    elif site == 'list': # legacy
        return render_template('data-sites.htm', username=_user)
    elif site == 'dashboard': # experimental
        return render_template('hexgrid-sites.htm', username=_user)
    else:
        return render_template('map-sites.htm', username=_user)

@application.route('/cov/') #Redirect old links to CoV features
def cov():
    return redirect(url_for('index'))

### Launch Site

if __name__ == '__main__':
    signal(SIGINT, handler)
    application.run(debug=DEBUG, host='0.0.0.0', port=5000)

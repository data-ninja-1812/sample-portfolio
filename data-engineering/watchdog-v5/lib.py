# Contains common custom classes and functions used by watchdog

import base64      #Used for basic encoding passwords for storage
import os          #Required for teradata kerberos initiation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2    #Required for postreSQL (pymssql dependency)
import teradatasql #Required for teradata
#import sqlite3     #Required for local sqlitedb testing #OS_READY


### Credential Class ###

# Used to store and obscured passwords

class Password:
    def __init__(self):
        self.pwd = None

    def store(self,password):
        self.pwd = base64.encodebytes(password.encode('UTF-8'))
        return None

    def reveal(self):
        return base64.decodebytes(self.pwd).decode('UTF-8')     
    
### Database Connector Classes ###

# All connector classes must return a session (as oppossed to an engine)

#---------------------------------------------------------

class TeradataObject:
    def __init__(self, server, port, database):
        self.dbtype = 'teradata'
        self.server = server
        self.port = port
        self.database = database
        self.username = ''
        self.password = Password()
        self.password.store('')
        self.driver = ''
        self.connection_string = None

    #Use teradatasql DBAPI method (Works on Analytics Server, should work in OpenShift)
    def connect(self):
        conn = teradatasql.connect(None, host=self.server, user=self.username, password=self.password.reveal())
        return conn

    #def engine(self):
    #    engine = create_engine('teradata://'+self.username+':'+self.password.reveal()+'@'+self.server+':'+self.port)
    #    return engine
    
    def query(self, database, table, column):
        return "SELECT MAX(%s) AS last_update FROM %s.%s;" %(column, database, table)

#---------------------------------------------------------    

class PostgresqlObject:
    def __init__(self, server, port, database):
        self.dbtype = 'postgresql'
        self.server = server
        self.port = port
        self.database = database
        self.username = ''
        self.password = Password()
        self.password.store('')
        self.driver = None
    
    def get_connection_string(self):
        self.connection_string = "host='"+self.server+"' dbname='"+self.database+"' user='"+self.username+"' password='*****'"
        return self.connection_string
    
    def connect(self):
        conn = psycopg2.connect("host='"+self.server+"' dbname='"+self.database+"' user='"+self.username+"' password='"+self.password.reveal()+"'")
        return conn
    
    def engine(self):
        engine = create_engine('postgresql://'+self.username+':'+self.password.reveal()+'@'+self.server+':'+self.port+'/'+self.database)
        return engine

    def query(self, database, table, column):
        return "SELECT MAX(%s) AS last_update FROM %s;" %(column, table)    

#---------------------------------------------------------    

class SqlserverObject:
    def __init__(self, server, port, database):
        self.dbtype = 'mssql'
        self.server = server
        self.port = port
        self.database = database
        self.username = ''
        self.password = Password()
        self.password.store('')
        self.driver = '' #OS_READY

    def get_connection_string(self):
        self.connection_string = 'mssql+pymssql://'+self.username+':******@'+self.server+':'+self.port+'/'+self.database
        return self.connection_string

    def connect(self):
        engine = create_engine('mssql+pymssql://'+self.username+':'+self.password.reveal()+'@'+self.server+':'+self.port+'/'+self.database)
        Session = sessionmaker(bind=engine)
        session = Session()
        conn = session.connection()
        return conn

    def engine(self):
        engine = create_engine('mssql+pymssql://'+self.username+':'+self.password.reveal()+'@'+self.server+':'+self.port+'/'+self.database)
        return engine

    def query(self, database, table, column):
        return "SELECT MAX(%s) AS last_update FROM [dbo].[%s];" %(column, table)

#---------------------------------------------------------    
# Not needed in OpenShift
#
#class SqliteObject:
#    def __init__(self, server, port, database):
#        self.dbtype = 'sqlite3'
#        self.server = server
#        self.port = port
#        self.database = database
#        self.username = ''
#        self.password = Password()
#        self.password.store('')
#        self.driver = ''
#
#    def connect(self):
#        session = sqlite3.connect(self.server)
#        return session
#    
#---------------------------------------------------------

### Error Handeling Functions ###



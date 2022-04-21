import pandas
import subprocess
from datetime import datetime
from time import sleep
import dbo

config_file = 'config.cfg'
verbose = True

### Create status functions - FUTURE move functions to seperate file ###

def watchdog_output_to_db(data_source_updates):
    #Post message to database
    session = dbo.output_db.engine()
    data = pandas.DataFrame()
    data = data.append(data_source_updates, ignore_index=True)
    data.to_sql(dbo.output_db.table, session, if_exists='append', index=False)
    #session.close()
    
def watchdog_status_message(status):    
    status_ts = pandas.datetime.now()
    
    data_source_updates = pandas.Series(
        {'_server'          : 'WatchdogStatusMessage',
         '_db_type'         : None,
         '_table'           : 'WatchdogStatusMessage',
         '_column'          : None,
         '_last_update'     : None,
         '_status'          : status,
         '_query_timestamp' : status_ts })
    
    if verbose: print('WatchdogStatusMessage: ' + str(status))
    
    watchdog_output_to_db(data_source_updates)
    return None

def watchdog_parse_error(source, error):
    
    status_ts = pandas.datetime.now()
    
    _dbobject = eval('dbo.' + source.dbobject)
    _database = source.database
    _table    = source.table
    _column   = source.column
        
    data_source_updates = pandas.Series(
        {'_server'          : _dbobject.server,
         '_db_type'         : _dbobject.dbtype,
         '_table'           : '%s.%s' %(_database,_table),
         '_column'          : _column,
         '_last_update'     : None,
         '_status'          : 'WatchdogParseError: ' + str(error),
         '_query_timestamp' : pandas.datetime.now() })
    
    if verbose: print('WatchdogParseError: ' + str(error))
    
    watchdog_output_to_db(data_source_updates)
    return None

### Begin primary functionality ###

# Log watchdog start in output db
watchdog_status_message('start')

# Get config file
try:
    source = pandas.read_csv(config_file,sep=',', header=None, quotechar="'")
    source.columns = ['dbobject','database','table','column','timezone','parseint','active']

except Exception as error:
    watchdog_status_message('Error loading initial config file - Terminating watchdog - ' + str(error))
    exit()

# Initiate minute holder

minute_previous = datetime.now().minute

while True:

    # Get current minute
    minute_current = datetime.now().minute
    
    # If current minute != previous minute
    if minute_current != minute_previous:
        
        #Store current minute
        minute_previous = minute_current
        
        if verbose: print(datetime.now())
        
        #Send heartbeat to output table
        watchdog_status_message('heartbeat')
        
        #Check for updated config file
        source_ = source.copy(deep=True)
        
        try:
            source = pandas.read_csv(config_file,sep=',', header=None, quotechar="'")
            source.columns = ['dbobject','database','table','column','timezone','parseint','active']
        
        except Exception as error:
            watchdog_status_message('Error loading config file')
            
        if source.equals(source_) == False:
            watchdog_status_message('Change detected in config file')
        
        # Check the schedule for each table
        for idx in source.index.values:
            
            # Check the minute against the interval setting
            # If minute mod interval = 0, call the parsing function
            if (source.active[idx]) * (minute_current % source.parseint[idx] == 0):
        
                # Call parsing function
                try:

                    _dbobject = source.dbobject[idx]
                    _database = source.database[idx]
                    _table    = source.table[idx]
                    _column   = source.column[idx]
                    _timezone = source.timezone[idx]
                    _parseint = source.parseint[idx]

                    parse_cmd = "python parse.py -o '" + _dbobject + "' -d '" + _database + "' -t '" + _table + "' -c '" + _column + "' -z '" + _timezone + "'"

                    if verbose: print(parse_cmd)
                    
                    subprocess.Popen(parse_cmd, shell=True)
                        
                except Exception as error:
                    if verbose: print(error)
                    watchdog_parse_error(source.loc[idx], error)
                    

    ### Hold for one second
    sleep(1)
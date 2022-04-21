import argparse
import pandas
import dbo       #watchdog database objects

### Parameterize script for use as subprocess ###

parser = argparse.ArgumentParser(description='WatchDog - Core script for getting table update metadata.')

parser.add_argument('-o','--dbobject' , metavar='dbobject' , type=str)
parser.add_argument('-d','--database' , metavar='database' , type=str)
parser.add_argument('-t','--table'    , metavar='table'    , type=str)
parser.add_argument('-c','--column'   , metavar='column'   , type=str)
parser.add_argument('-z','--timezone' , metavar='timezone' , type=str)
parser.add_argument('-v','--verbose'  , action="store_true")

args = parser.parse_args()

system_tz = 'UTC'

### Core : BEGIN ###

_dbobject = eval('dbo.' + args.dbobject)
_database = args.database
_table    = args.table
_column   = args.column
_timezone = args.timezone
#_parseint = None

#if args.verbose : print('%s.%s ... ' %(_database,_table), end='', flush=True)

_dbobject.database = _database

conn = _dbobject.connect()

query = _dbobject.query(_database,_table,_column)

try:
    results = pandas.read_sql(query, conn, coerce_float=False)

    results.columns = ['Last_Update']

    #Process Time Zone Information
    last_update = results.Last_Update.iloc[0]

    if last_update.tzinfo != None:
        last_update = last_update.tz_convert(system_tz)
    else:
        last_update = last_update.tz_localize(_timezone).tz_convert(system_tz)


    #Log results
    data_source_updates = pandas.Series(
        {'_server'          : _dbobject.server,
         '_db_type'         : _dbobject.dbtype,
         '_table'           : '%s.%s' %(_database,_table),
         '_column'          : _column,
         '_last_update'     : last_update.tz_localize(None), # Remove timezone for compatibility
         '_status'          : 'Okay',
         '_query_timestamp' : pandas.datetime.now() })

    #if args.verbose : print('Done.')

#except pandas.io.sql.DatabaseError as err:
except Exception as error:
    data_source_updates = pandas.Series(
        {'_server'          : _dbobject.server,
         '_db_type'         : _dbobject.dbtype,
         '_table'           : '%s.%s' %(_database,_table),
         '_column'          : _column,
         '_last_update'     : None,
         '_status'          : str(error),
         '_query_timestamp' : pandas.datetime.now() })

    if args.verbose : print(error)

#Don't forget to close the connection
conn.close()

### Core : END ###

### Send data to watchdog database in PostgreSQL###

engine = dbo.output_db.engine()
data = pandas.DataFrame()
data = data.append(data_source_updates, ignore_index=True)
data.to_sql(dbo.output_db.table, engine, if_exists='append', index=False)

if args.verbose : print(data_source_updates)
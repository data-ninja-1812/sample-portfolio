Watchdog v5
=============================
(For the most recent version operating on the analytics server see archive/v4)

What's New:
- Refactored to operate in OpenShift (Major Change)
- Database object classes reconfigured to function without drivers in `lib.py`
- The `connect()` method of database objects returns a connection class rather than a session class
- The the database connections in `dbo.py` are now parameterized to use environment variables.

Requirements:
- OpenShift
- Python 3.6 + libraries
- Database credentials and connections

Future Work
- Add statsD feature
- Establish a method for being able to update `config.cfg` through github without having to restart watchdog (maybe move config to a db table instead)
- Determine how long watchdog data should be kept

Future Opportunities:
- Add anomolly detection
- Add self-serve config
- Output to Cassandra
- Output to Kafka

Functionality
-------------
The app monitors each table by running a query at defined intervals:

Example: `query = 'SELECT max(%s) as Last_Update FROM %s' %(table, column)`

For each table a timestamp column should be identified where the last refresh can be inferred.

Example: `DW_Last_Update_Date_Time` or `DW_INSRT_TS`

The results are stored in a designated database configured in `parse.py`

File Structure
--------------
```
app.py              # Script for running in OpenShift
requirements.txt    # Environment configuration for OpenShift
watchdog.py         # Primary python code for running watchdog (Cron-less version)
config.cfg          # Customizable csv configuation file for watchdog parameters
dbo.py              # Customizable file for creating and storing database objects
lib.py              # Contains database object classes and functions used by watchdog
parse.py            # Script for querying tables, used for parallel subprocesses
package_list.txt    # List of python packages and installation methods for manual environment creation

statsd.py           # FUTURE - StatD Module (Prometheus)
```

Watchdog Configuration
----------------------
Tables to be monitored are configured in `config.cfg`, a csv file with the following schema:

`dboject, database, table, column, timezone, interval`

```
dbobject  : str  : Name of the object stored in dbo.py that contains the server connection & credentials
database  : str  : Name of the target database
table     : str  : Name of the target table
column    : str  : Name of the column/field containing the timestamp to infer the table's last update
timezone  : str  : Timezone of the timestamp.  Must use python tz stamps.
interval  : int  : Interval in minutes to check the table.  Must be no more than half of table's expected refresh rate.
active    : bool : Activate (TRUE) or Deactive (FALSE) a table without having to remove it from the config file
```

Watchdog Output
-------------
The results of watchdog are stored in a database for consumption by clients.  The target database/table can be configured in `dbo.py`

Data is written to output table each time a configured input database/table is parsed.

```
_table            : str : Target database.table configured in config.cfg
_last_update      : str : Timestamp in US/Central reflecting the implied last update of target table
_query_timestamp  : str : Timestamp in US/Central when target table was last queried
_column           : str : Name of the column _last_update is derived from in the target table.  Set in config.cfg
_server           : str : Address of the server configured in dbo.py associated with the dbobject in config.cfg
_db_type          : str : Type of database _table is located in.  Based on association to dbobject in config.cfg
_status           : str : Status information emitted by watchdog for debugging and error checking
```

Database Server Configuration
-----------------------------

Server addresses and credentials are stored as objects.  These objects classes are defined in `lib.py`.  The objects are stored in `dbo.py`.  These classes also define the query that will be run in the database to pull the timestamp needed for watchdog.

Database object classes are generally defined as:

```
class DatabaseObject:
    def __init__(self, server, port, database):
        self.dbtype = ''
        self.server = server
        self.port = port
        self.database = database
        self.username = ''
        self.password = Password()
        self.password.store('')
        self.driver = ''

    def get_connection_string(self):
        self.connection_string = "host='"+self.server+"' dbname='"+self.database+"' user='"+self.username+"' password='*****'"
        return self.connection_string
    
    def connect(self):
        conn = dblibrary.connect("host='"+self.server+"' dbname='"+self.database+"' user='"+self.username+"' password='"+self.password.reveal()+"'")
        return conn
    
    def engine(self):
        engine = create_engine('sql://'+self.username+':'+self.password.reveal()+'@'+self.server+':'+self.port+'/'+self.database)
        return engine

    def query(self, database, table, column):
        return "SELECT MAX(%s) AS last_update FROM %s;" %(column, table)    
```

Adding new servers require modifing the `dbo.py` file directly.
Adding new connection types require modifying the `lib.py` directly.

Current databases supported include:
- Teradata
- MS SQL Server
- PostgreSQL
- (sqlite is not supported in OpenShift)



More Notes
-----------------

backend
- use classes to create common schema for database connections (lib.py)
- use dbo file to store database objects and credentials for db connections (dbo.py)
- use config file to define tables to monitor (config.py)
- run queries in parallel using subprocesses running mulitple instances of parse.py
- store results for analysis in postgreSQL (or local mySQL database file)

frontend
- configurable "product profiles" perhaps using table views - COMPLETE IN v3
- Web UI = Tableau w/ filters matching product profiles - TESTED ON CLIFFORD and NATE


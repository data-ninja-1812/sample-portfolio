# Customizable file for storing database credentials

# lib.Dboject(server:str, port:str, database:str) 

import lib
import os #OS_READY

# Output Server -- Server/Database for outputing watchdog results
output_db = lib.PostgresqlObject(os.environ['PG_HOST'], os.environ['PG_PORT'],os.environ['PG_OUTPUT_DB'])   #OS_READY
output_db.username = os.environ['PG_USER']        #OS_READY
#output_db.password.store(os.environ['PG_PWD'])    #OS_READY
output_db.password.pwd = bytes(bytes(os.environ['PG_PWD'],'utf-8').decode('unicode_escape'),'utf-8')
output_db.table = os.environ['PG_OUTPUT_TABLE']   #OS_READY
#output_db.table = 'watchdog_v5_s0_dev' #Use until ready to for prime time
#output_db.table = 'watchdog_v5_s0' #Future table for use with v5 (OpenShift)
#output_db.table = 'watchdog_v3_s0' #Current table in use with v4 & v3


# CSG DS PostgreSQL server
postgresql = lib.PostgresqlObject(os.environ['PG_HOST'], os.environ['PG_PORT'],'')  #OS_READY
postgresql.username = os.environ['PG_USER']                      #OS_READY
#postgresql.password.store(os.environ['PG_PWD'])                 #OS_READY
postgresql.password.pwd = bytes(bytes(os.environ['PG_PWD'],'utf-8').decode('unicode_escape'),'utf-8')

# Opengate SQL Server
opengate = lib.SqlserverObject(os.environ['OPENGATE_HOST'],'1433','')  #OS_READY
opengate.username = os.environ['OPENGATE_USER']           #OS_READY
#opengate.password.store(os.environ['OPENGATE_PWD'])       #OS_READY
opengate.password.pwd = bytes(bytes(os.environ['OPENGATE_PWD'],'utf-8').decode('unicode_escape'),'utf-8')

# BMAC SQL Server
bmac = lib.SqlserverObject(os.environ['BMAC_HOST'],'1433','')  #OS_READY
bmac.username = os.environ['BMAC_USER']                    #OS_READY
#bmac.password.store(os.environ['BMAC_PWD'])                #OS_READY
bmac.password.pwd = bytes(bytes(os.environ['BMAC_PWD'],'utf-8').decode('unicode_escape'),'utf-8')

# Teradata Server
edwprod = lib.TeradataObject(os.environ['TD_HOST'],'1025','')  #OS_READY 
edwprod.username = os.environ['TD_USER']                      #OS_READY
#edwprod.password.store(os.environ['TD_PWD'])                  #OS_READY
edwprod.password.pwd = bytes(bytes(os.environ['TD_PWD'],'utf-8').decode('unicode_escape'),'utf-8')
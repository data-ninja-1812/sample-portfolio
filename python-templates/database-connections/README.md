# Database Connections with Python

There are perhaps dozens of libraries for connecting to databases available and perhaps innumerable methods.  At HCA, we have found that SQLAlchemy provides the most versatile set of connectors while maintaining consistent coding patterns.  The SQLAlchemy library utilizes the concept of dialects in an Object Relational Mapper to provide a standard set of functions and methods mapped to multiple database query languages.

SQLAlchemy Official Site - https://www.sqlalchemy.org/

See `database-connections.ipynb` for reusable blocks of code to connect to various HCA databases.

## SQLAlchemy Packages

These should be installed into your virtual environment with `pip install`

`sqlalchemy` - Core SQLAlchemy Library

`teradatasqlalchemy` - Teradata SQL dialect for sqlalchemy - https://pypi.org/project/teradatasqlalchemy/

`pymssql` - Tools & connectors for MS SQL databases and SQL dialect for sqlalchemy - https://www.pymssql.org/

`psycopg2==2.7.1` - Tools & connectors for PostgreSQL databases and SQL dialect for sqlalchemy (v2.7.1 is proven to work on DS tech stack.) - https://pypi.org/project/psycopg2/

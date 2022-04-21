# How to create a python virtual environments

Where not denoted, Linux and Windows commands are the same.

### References & Python Docs

Python Official Reference - https://docs.python.org/3/library/venv.html

Python Official Guide - https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment

Python Official Tutorial - https://docs.python.org/3/tutorial/venv.html

Python Hygiene by CSG Data Science - https://pages.githubdev.medcity.net/CDM-DataScience/wiki/programming/python_hygiene.html

### A Note on Conda

`conda` virtual environments that come in the Anaconda distribution of Python and Jupyter Labs is a useful tool.  However, Conda is not native to python itself and its implementation creates challenges hard to overcome in a production environment.  Use Conda if you must for learning or local development, but it’s best to use the native `venv` module python which is required for production grade code.

## Prepare for virtual environments (first time setup)

Open a new terminal window and follow the below commands.

Make sure you are in your home directory.  You may use an alternative directory as long as it is centrally located for use in your projects.

Linux - `$ cd ~`

Windows - `> cd %HOMEPATH%`

If you do not already have this directory in your home folder, go ahead and create it.   This will hold all of your virtual environments.  Alternatively you can store virtual environments in your project folders, just be sure not to upload them to github.

`$ mkdir .venvs`

## Create the virtual environment

Move into your `.venvs` folder.

`$ cd .venvs`                       

Create a new environment called "myenv" in the current working directory.  You can name this anything.

`$ python -m venv "myenv"`          

You many run into a permission issue regarding pip.  Use `$ python -m venv --without-pip "myenv"` if you run into this issue.          

Conrgatulations! You now have a completely fresh and empty python environment.  To utilize it, and work within it, you must first activate it


## Activate the virtual environment

Return to your home directory (or project directory)

Linux - `$ cd ~`

Windows - `> cd %HOMEPATH%`

Now we activate the virtual environment called "myenv"

Linux - `$ source .venvs/myenv/bin/activate`

Windows - `> .venvs/myenv/Scripts/activate`

## Setup the virtual environment

We need to install some packages, but first, upgrade the install utility `pip` to the latest version

`$ pip install --upgrade pip`

Now you can add any packages you want.  Core packages recommended include...

`$ pip install numpy pandas requests`

## Deactivate the virtual environment

To exit the virutal environment use the command

`$ deactivate`

# Jupyter Notebooks

## Add virtual environment to jupyter notebook

Make sure you are actively working in your virtual environment.

Install ipython kernel in current env for compatibility with jupyter labs

`$ pip install ipykernel `          

Installs kernel to local user for jupyter labs

`$ python -m ipykernel install --user --name=myenv --display-name="My Environment"`

# Python Libraries

## Common Packages

`pandas` - Library providing high-performance, easy-to-use data structures and data analysis

`numpy` - Extended math and numerical operator library

`requests` - Library for accessing URL based connections and APIs


## Database Connectors

`sqlalchemy` - Library for connecting to multiple SQL dialects

`teradatasqlalchemy` - Teradata SQL dialect for sqlalchemy

`pymssql` - Tools & connectors for MS SQL databases and SQL dialect for sqlalchemy

`psycopg2==2.7.1` - Tools & connectors for PostgreSQL databases and SQL dialect for sqlalchemy (v2.7.1 is proven to work on DS tech stack.)

Facility Master Portal
---

This is a web portal designed to provide read-only access and interactivity with the Facility Master data in Ataccama RDM.

More information about Facility Master can be found at https://alation.medcity.net/article/117/edg-facility-master

No PHI or Patient Data is handeled in this application.


Design & Architecture
---

This project is created with Python and the Flask libraries.  The Flask application manages the routes, renders and serves the webpages, and hosts the internal API.  JavaScript is used for the frontend delivery of content.  Data is requested in the app from the primary source of Facility Master data (Ataccama RDM).  Cerberus is utilized for Authentication.

Python Frameworks & Packages
- Flask - Provides HTTP server functionality
- sqlalchemy -  Provides database connectivity

Javascript Frameworks & Packages
- leaflet.js - Map rendering
- tabulator.js - Interactive table

Requirements
---

- Python 3.6
- Python Packages in requirements.txt

Key Files
---

```
requirement.txt - Python packages for PIP install
app.py - Container configuration file
server.py - Flask App
```

Setup
---

This application can be run locally, or as container on any cloud service.

**Envrionment Variables**

The following environment variables must be set:

```
RDM_HOST - Facility Master Database - Host Address
RDM_PORT - Facility Master Database - Host Port
RDM_DB - Facility Master Database - Database Name
RDM_USER - Facility Master Database - Database User
RDM_PWD  - Facility Master Database - Database Password
AUTH_URL - Facility Master Database - Cerberus URL
AUTH_KEY - Facility Master Database - Cerberus API Key
AUTH_APP - Facility Master Database - Cerberus Application Comment - Default = 'facility-master-map-csg-dsp-prod'
SESSION_TIMEOUT - Flask Session Timeout - Default = 60
LOGIN_MESSAGE - Login Page Message - Default = ''
```

**Server Configuration**

Flask is configured for HTTP delivery on `0.0.0.0:8660`.  If run on a local machine or for development purposes, Flask alone will suffice.  `mod_wsgi` must be used for production instances.

**Cloud Configuration**

Routing and networking setup may be required for cloud environments.

Installation
---

**Create and activate Virtual Environment**
```
python3 -m venv myenv           #Create a new environment in the current working directory
source myenv/bin/activate       #Activate env
```

**Clone repo into local directory (or manually copy from github)**
```
git clone https://githubdev.medcity.net/CDM-DataScience/fm-map
cd fm-map
```

**Install python packages**
```
pip install -r requirements.txt
```

**Run application**

Local Instance - `python server.py`

Cloud Instance - `python app.py`


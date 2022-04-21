# slinkydog

Slinkydog is designed to capture and record changes to database tables at intervals of time efficiently.  It reduces information redundancy using a technique widely used in video compression.  More information can be find in the `docs` folder.

As is, slinkydog is configured to operate in teradata.  However, the concept and code can be easily refactored for other databases.

`config.py` - File containing all of the configurable parameters necessary to operate slinkydog

`slinkydog-setup.ipynb`    - Initial setup script

`slinkydog-record.ipynb`   - Core code for recording data from a table or query (This should be converted to *.py in the environment of choice)

`slinkydog-playback.ipynb` - Script for reassembling the original data for a given moment in time (beta - not fully automated)

`slinkydog-record.sh` - Automated bash script useful for cronjobs

`lockout.py` - Library for preventing multiple instances from running at the same time
<br />
<br />
<br />
Original Author:<br /><br />
Matthew K Brown<br />
matthew.brown@hcahealthcare.com<br />
April 12, 2019

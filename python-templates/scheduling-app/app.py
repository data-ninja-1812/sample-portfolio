import subprocess
import sys
from signal import signal, SIGINT
import logging
import schedule
from time import sleep
from datetime import datetime

# Parameters
LOG_FILE = 'app.log'
DATE_FMT = '%Y-%m-%d %H:%M:%S'

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt=DATE_FMT,
                    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]) # Log to file and stdout

logging.info('Initiating scheduling app...')

# Keyboard Interrupt function
def handler(signal_received, frame):
    logging.info('SIGINT or CTRL-C detected.')
    logging.info('Scheduling app exiting')
    exit(0)

# Heartbeat function
def heartBeat():
    logging.info('♥')

# Subprocess function
def myProcess(pyFile):
    
    logging.info('Executing - %s' %(pyFile))
    
    proc = subprocess.Popen(['python',pyFile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # The stdout logging should be moved to within the called pyFile scripts
    # as not to wait for subprocess to finish running
    for line in proc.stdout:
        logging.info(line.decode().rstrip('\n'))
    
    logging.info('Exiting - %s' %(pyFile))

# Scheduling setup function
def schedulePlan():
    schedule.clear()
    schedule.every(10).seconds.do(heartBeat)
    schedule.every(30).seconds.do(myProcess, pyFile='hello.py')
    #schedule.every(1).minutes.do(myProcess, pyFile='hello.py')
    #schedule.every().day.at("03:00").do(myProcess, pyFile='hello.py') #Schedule daily at 10:00PM CT
    
# Main scheduling function
def main():
    
    signal(SIGINT, handler) # Handles CTRL-C Keyboard Interrupt

    schedulePlan()
    
    logging.info('Scheduling app running...')
    
    while True:
        schedule.run_pending()
        sleep(1)

# Launch app
if __name__ == '__main__':
    main()

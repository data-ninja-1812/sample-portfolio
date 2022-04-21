#!/usr/bin/env python3

import subprocess
import os

#dev_mode = os.environ.get('DEV_MODE')
#if dev_mode == 'True' : os.chdir('dev')

## MAIN
def main():
    
    print("watchdog is watching...")
    
    subprocess.run(['python', 'watchdog.py'])
    
    print("watchdog is not watching anymore...")
    
    exit(0) #Exit with an Okay flag

if __name__ == '__main__':
    main()
# File name: format.py
# Description: Basic format for Python scripts
# Author: Louis de Bruijn
# Date: 19-05-2020

import sys
import argparse
import logging
from logging import critical, error, info, warning, debug


import os
import json
from datetime import date, time, datetime
import platform
import subprocess


def parse_arguments():
    """Read arguments from a command line."""
    #parser = argparse.ArgumentParser(description='Arguments get parsed via --commands', prog='PROG', usage='%(prog)s [options]')
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '-verbosity', type=int, default=2, help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug', choices=[0, 1, 2, 3, 4])
    parser.add_argument('-d', '-debug', help='Enable debugging', action='store_true')

    args = parser.parse_args()
    if(args.d):
        logging.basicConfig(format='%(message)s', level=logging.DEBUG, stream=sys.stdout)
    else:
        verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
        logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)
    
    return args
    
    
def main():
    #is the server on?
    _serverStatus = True
    hostname = "192.168.14.160"
    output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', hostname), shell=True)

    if("TTL" not in str(output)):
        _serverStatus = False

    if(_serverStatus):
        print("Server is online")
    else:
        with open('calendar.json', 'r') as f:
            data = json.load(f)

        _currentYear = str(datetime.now().year)
        _currentDate = str(date.today().strftime("%d-%m-%Y"))
        _currentTime = datetime.now().time()
        _currentDay = datetime.now().strftime("%A")
        
        debug(f"Current year: {_currentYear}")
        debug(f"Current date: {_currentDate}")
        
        _normalDay = {
            "on": time(9,00),
            "off": time(23,00)        
        }
        _schoolDay = {
            "on": time(16, 00),
            "off": time(23, 00)
        }

        _startTime = _normalDay

        if(_currentDay == "Saturday" or _currentDay == "Sunday"):
            print(f"Today is a weekend, power on at {_normalDay['on']}, power off at {_normalDay['off']}")
        elif(_currentDate in data[_currentYear]):
            print(f"Today is a {data[_currentYear][_currentDate]}, power on at {_normalDay['on']}, power off at {_normalDay['off']}")
        else:
            print(f"Today is a school day, power on at {_schoolDay['on']}, power off at {_schoolDay['off']}")
            _startTime = _schoolDay

        #print(time(_startTime['on']))

        if(_currentTime > _startTime['on']):
            if(not _serverStatus):
                print("Should be on - WAKE UP!")
        else:
            print("Should be off")


if __name__ == '__main__':
    args = parse_arguments()
    main()

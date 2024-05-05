
#Save an Event Log
import logging
logging.basicConfig(filename='Fire_Monitor.log',level=logging.DEBUG)

#Ready GPIO Ports
import RPi.GPIO as GPIO
import subprocess
import sys
import time
import atexit

def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

GPIO.setmode(GPIO.BCM)
fire_Pin=23
trouble_Pin=24
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #This is GPIO 23, Physical Pin is Pin 16!
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) #This is GPIO 24, Physical Pin is Pin 18!


#Ready Date/Time Info
import time
from time import sleep
def getTime():
    return time.asctime( time.localtime(time.time()))

#IP Address
import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)


#Push Notifications
import subprocess

tbl = 'python3 /home/firecom/trouble.py'
alm = 'python3 /home/firecom/firealarmactive.py'
tblres = 'python3 /home/firecom/tblrestore.py'
fireres = 'python3 /home/firecom/firerestore.py'


import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "pushover api token",
    "user": "pushover user token",
    "message": "System Startup: No Alarms Present",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()



#LCD Display
from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', address=0x027, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()
lcd.write_string('System Startup')
lcd.clear()
time.sleep(5), lcd.write_string('System Normal')


#Variables
def fireAlarmActive():
    lcd.clear()
    lcd.write_string('Fire Alarm')
    p = subprocess.Popen(alm, shell=True)

def fireAlarmRestore():
    lcd.clear()
    lcd.write_string('System Normal')
    p = subprocess.Popen(fireres, shell=True)


def troubleAlert():
    lcd.clear()
    lcd.write_string('System Trouble')
    p = subprocess.Popen(tbl, shell=True)
    
def troubleMonitorRestore():
    lcd.clear()
    lcd.write_string('System Normal')
    p = subprocess.Popen(tblres, shell=True)
    


#Log System Monitor Online
logging.info('Online on %s', getTime())

#Set Default Status to normal
fireStatus = False
troubleStatus = False
networkStatus = True

from functools import wraps
import time

# Global dictionary to track function calls
func_calls = {}

def debounce(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a tuple of arguments for the key
            arg_tuple = tuple(args) + tuple(kwargs.items())
            
            # Check if the function has been called recently with the same arguments
            if arg_tuple in func_calls:
                last_call_time = func_calls[arg_tuple]
                if time.time() - last_call_time < seconds:
                    # Debounce condition met, skip execution
                    return
            
            # Update the tracking dictionary
            func_calls[arg_tuple] = time.time()
            
            # Execute the function
            result = func(*args, **kwargs)
            
            # Return the result
            return result
        return wrapper
    return decorator

timeout = 2 #300ms timeout
@debounce(seconds=timeout)
def my_GPIO_Read(pin):
    res=GPIO.input(pin)
    return res

while True:    
    #Respond to Full Fire Alarm
    if my_GPIO_Read(fire_Pin) == GPIO.LOW and fireStatus == False:
       fireStatus = True
       logging.warning("Fire Alarm Active on %s", getTime())
       fireAlarmActive()
        
    # Fire Alarm Restore    
    elif my_GPIO_Read(fire_Pin) == GPIO.HIGH and fireStatus == True:
       fireStatus = False
       logging.warning("Fire Alarm Restore on %s", getTime())
       fireAlarmRestore()
       
       
       #Respond to Full Fire Alarm
    if my_GPIO_Read(trouble_Pin) == GPIO.LOW and troubleStatus == False:
       troubleStatus = True
       logging.warning("Fire Alarm Active on %s", getTime())
       troubleAlert()
        
    # Fire Alarm Restore    
    elif my_GPIO_Read(trouble_Pin) == GPIO.HIGH and troubleStatus == True:
       troubleStatus = False
       logging.warning("Fire Alarm Restore on %s", getTime())
       troubleMonitorRestore()




   
        
GPIO.cleanup()     #On Exit


import serial
import struct
import json
import threading

from time import sleep


try:
	arduino = serial.Serial('/dev/ttyUSB0', 9600)
except serial.serialutil.SerialException:
	print("arduino failed to connect")


def ConvertSpeedToMessage(speed, forward=True):
    direction = "1"
    if(speed >= 100):
        speed = 99
    if(speed < 0):
        direction = "0" # negative means brake
        speed = speed * -1

    # print(direction + str(speed))

    # stop if speed is 0
    if(speed == 0):
        return "0"

    if(speed < 10):
        return (direction + "0" + str(speed))
    return (direction + str(speed))

def ChangeSpeed(newSpeed):
    print("changing speed")
    arduino.write(ConvertSpeedToMessage(newSpeed).encode())


# settings : [dict]{acceleration, currentSpeed, maxSpeed}
def Accelerate(s):
    while(True):
        while(s['currentSpeed'] != s['maxSpeed']):

            if(s['currentSpeed'] > s['maxSpeed']): #decelerating
                if(s['currentSpeed'] - s['deceleration'] < s['maxSpeed']):
                    s['currentSpeed'] = s['maxSpeed']
                else:
                    s['currentSpeed'] -= s['deceleration']

            else: 
                print("accelerate")
                if(s['currentSpeed'] + s['acceleration'] > s['maxSpeed']):
                    s['currentSpeed'] = s['maxSpeed']
                else:
                    s['currentSpeed'] += s['acceleration']
            ChangeSpeed(s['currentSpeed'])
            
        sleep(0.2)
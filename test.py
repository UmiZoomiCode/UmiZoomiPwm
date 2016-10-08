import serial
import struct
from time import sleep

arduino = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port

while(True):
	num = raw_input("GIve me an int (0 to stop)")
	if(num == "exit"):
		break
	arduino.write(num.encode())
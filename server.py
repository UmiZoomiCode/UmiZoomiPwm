import socketserver
import serial
import struct
import json

from time import sleep
from pprint import pprint

try:
	arduino = serial.Serial('/dev/ttyUSB0', 9600)
except serial.serialutil.SerialException:
	print("arduino failed to connect")


maxSpeed = 1.0
acceleration = 0.3
currentSpeed = 0.0

def newMaxSpeed(newMax):
	if(newMax <= 1.0 and newMax >= 0):
		maxSpeed = newMax
		return True
	return False

def newAcceleration(accel):
	if(accel <= 1.0 and accel >= 0):
		acceleration = accel
		return True
	return False

def sendNewSpeed(newSpeed):
	speed = str(newSpeed).replace('.','')
	print(speed)
	#arduino.write(speed.encode())
	return True

#self.wfile.write(bytearray("Hello World", "utf8"));
class handler(socketserver.StreamRequestHandler):

	def handle(self):
		global currentSpeed
		global maxAcceleration
		global acceleration
		global maxSpeed
		while True:
			self.data = self.rfile.readline().strip()
			if(self.data != None):
				print(self.data)
				message = str(self.data)[1:].replace("\'", "")
				try:
					data = json.loads(message)
					
					if(data['msg'] == "ChangeSpeed"):

						newSpeed = float(data['speed'])
						if(newSpeed > currentSpeed):
							while(currentSpeed < newSpeed):
								if(sendNewSpeed(currentSpeed)):
									self.wfile.write(bytearray("Speed Sent", "utf8"))
								else:
									self.wfile.write(bytearray("Speed failed to send", "utf8"))
								currentSpeed+=acceleration
						else:
							while(currentSpeed > newSpeed):
								if(sendNewSpeed(currentSpeed)):
									self.wfile.write(bytearray("Speed Sent", "utf8"))
								else:
									self.wfile.write(bytearray("Speed failed to send", "utf8"))
								currentSpeed-=acceleration

						self.data = None

					elif(data['msg'] == "Stop"):
						print("stopping motor")
						sendNewSpeed(0)

				except json.decoder.JSONDecodeError:
					print("json failed to load")
					pass

			sleep(0.2)


	def server_bind(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	
	server = socketserver.TCPServer((HOST, PORT), handler)

	try:
		server.serve_forever()
	# except KeyboardInterrupt:
	# 	pass
	except:
		pass
	server.server_close()
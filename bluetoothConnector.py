# connect and get blue tooth stuffs

#!/usr/bin/python
import pygame
import os
import time
import usb

from time import sleep
#from websocket import create_connection

# print("Sending 'Hello, World'...")
# ws.send("Hello, World")
# print("Sent")
# print("Reeiving...")
# result =  ws.recv()
# print("Received '%s'" % result)
# ws.close()

if not pygame.joystick.get_init():
    pygame.joystick.init()

class PS3_Controller:
  
  def __init__(self):
    self.joystick = None
    self.buttons = None
    self.t = 0
    self.time = time.time

  def is_pressed(self, button_name):
    if self.buttons is not None:
      if button_name == 'left_stick':
        self.update_axis()
        if sum(self.left_axis) > 0 or sum(self.left_axis) < 0:
          return True
        else:
          return False
      elif button_name == 'right_stick':
        self.update_axis()
        if sum(self.right_axis) > 0 or sum(self.right_axis) < 0:
          return True
        else:
          return False
      else:
        self.update_buttons()
        if button_name in self.buttons.keys():
          if self.buttons[button_name] == 1:
            return True
          else:
            return False
    else:
      return False

  def update_buttons(self):
    if self.joystick is not None:
      pygame.event.pump()
      try:
        self.buttons = {   
          # 'left': self.joystick.get_button(7), 
          # 'right' : self.joystick.get_button(5),
          # 'up' : self.joystick.get_button(4), 
          # 'down': self.joystick.get_button(6),
          # 'square' : self.joystick.get_button(15),
          # 'x' : self.joystick.get_button(14),
          # 'circle' : self.joystick.get_button(13),
          # 'triangle' : self.joystick.get_button(12),
          # 'l1' : self.joystick.get_button(10),
          # 'l2' : self.joystick.get_button(8),
          # 'select' : self.joystick.get_button(0),
          # 'start' : self.joystick.get_button(3),
          # 'l3' : self.joystick.get_button(1),
          'r1' : self.joystick.get_button(11),
          'r2' : self.joystick.get_button(9),
          'r3' : self.joystick.get_axis(3),
          'l3' : self.joystick.get_axis(2)
        }
      except pygame.error as e:
        self.joystick = None
    else:
      self.buttons = None
    return

  def check_if_connected(self):
    try:
      busses = usb.busses()
      for bus in busses:
          devices = bus.devices
          for dev in devices:
            if dev.idVendor == 1356:
              return True
      return False
    except usb.core.USBError:
      print("USB Disconnected")
      return False
    
  def check_status(self):
    self.update_buttons()
    if self.check_if_connected(): 
      if self.t == 0:
        print("Connected")
        self.t = 1
        pygame.joystick.quit()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        while len(joysticks) <= 0:
          pygame.joystick.quit()
          pygame.joystick.init()
          joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in joysticks:
          if 'playstation' in joystick.get_name().lower():
            print(joystick.get_name())
            self.joystick = joystick
            self.joystick.init()
    
    else:
      print('Disconnected')
      pygame.joystick.quit()
      self.t = 0
      self.joystick = None
      self.buttons = None

pygame.init()

if __name__ == "__main__": 
  controller = PS3_Controller()
  while True:
    controller.check_status()
    if controller.buttons != None:
      newSpeed = float(controller.buttons['r3']) * 100

      if(int(controller.buttons['r3']) <= -1):
        controller.buttons['r3'] = .99

      # if(int(controller.buttons['r1']) == 0):
        # controller.sendMessage("{\"msg\": \"ChangeSpeed\",\"speed\" : "+str(newSpeed * -1)+"}")
    sleep(0.2) 
  

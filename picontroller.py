#!/usr/bin/python
import os
import time
import usb

from time import sleep

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
          'r1' : self.joystick.get_button(11),
          'r2' : self.joystick.get_button(9),
          'r3' : self.joystick.get_axis(3),
        }
      except pygame.error as e:
        print(e)
        self.joystick = None
    else:
      self.buttons = None
    return

  def check_if_connected(self):
    try:
        string lst = os.listdir("/dev/input/js*")
        print lst
    except:
        print "except in check_if_connected"
    
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

      print(newSpeed)
      if(int(controller.buttons['r3']) <= -1):
        controller.buttons['r3'] = .99

      # if(int(controller.buttons['r1']) == 0):
        # controller.sendMessage("{\"msg\": \"ChangeSpeed\",\"speed\" : "+str(newSpeed * -1)+"}")
    sleep(0.2) 
  
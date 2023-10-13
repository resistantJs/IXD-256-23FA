# change RGB LED colors with digital input using state logic
# release and hold the input closed to change between 2 states 

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
rgb_state = 'green'

input_pin = None
input_state = 1

def setup():
  global rgb, input_pin
  M5.begin()
  
  # default built-in RGB setting:
  #rgb = RGB()
  
  # custom RGB setting using pin G35 (M5 AtomS3 built-in LED):
  #rgb = RGB(io=35, n=1, type="SK6812")
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  rgb = RGB(io=2, n=10, type="SK6812")
  
  # initialize pin G41 (M5 AtomS3 built-in button) as input:
  #input_pin = Pin(41)
  
  # initialize pin G39 (M5 PortABC Extension red connector) as input:
  input_pin = Pin(39, mode=Pin.IN, pull=Pin.PULL_UP)


def loop():
  global rgb_state, input_state
  M5.update()
  
  if(rgb_state == 'green'):
    # if input pin changed to 0 go to 'red' state: 
    if (input_pin.value() == 0):
      if (input_state == 1):
        rgb_state = 'red'
        print('change to', rgb_state)
      time.sleep_ms(100)
      input_state = 0
    else:
      input_state = 1
    # fade in all RGB LEDs green:
    for i in range(100):
      rgb.fill_color(get_color(0, i, 0))
      time.sleep_ms(20)
    
  elif(rgb_state == 'red'):
    # if input pin changed to 0 go to 'green' state:
    if (input_pin.value() == 0):
      if (input_state == 1):
        rgb_state = 'green'
        print('change to', rgb_state)
      time.sleep_ms(100)
      input_state = 0
    else:
      input_state = 1
    # turn on 10 RGB LEDs red one by one:
    for i in range(10):
      rgb.set_color(i, get_color(255, 0, 0))
      time.sleep_ms(100)
    # turn off all RGB LEDs (fill with black):
    rgb.fill_color(get_color(0, 0, 0))
    time.sleep_ms(100)

# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

# test get_color function and convert to hexadecimal:
print('green color =', hex(get_color(0, 255, 0)))

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")

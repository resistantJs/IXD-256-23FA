# change RGB LED colors with digital input and time using state logic
# 4 states are implemented as shown:
# 'START'  -> turns on RGB green
# 'OPEN'   -> pulsate RGB blue
# 'CLOSED' -> fade in RGB yellow if digital input is closed
# 'FINISH' -> fade in RGB red 5 seconds after 'CLOSED' state
#             fade out RGB to black after 2 seconds

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
state = 'START'
state_timer = 0

def setup():
  global rgb, input_pin
  M5.begin()
  
  # custom RGB setting using pin G35 (M5 AtomS3 built-in LED):
  rgb = RGB(io=35, n=1, type="SK6812")
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  #rgb = RGB(io=2, n=10, type="SK6812")
  
  # initialize pin G41 (M5 AtomS3 built-in button) as input:
  #input_pin = Pin(41)
  
  # initialize pin G39 (M5 PortABC Extension red connector) as input:
  input_pin = Pin(39, mode=Pin.IN, pull=Pin.PULL_UP)
  
  # turn on RGB green and wait 2 seconds:
  if (state == 'START'):
    print('start with RGB green..')
    rgb.fill_color(get_color(0, 255, 0))
    time.sleep(2)  
    check_input()

def loop():
  global state, state_timer
  M5.update()
      
  if (state == 'OPEN'):
    print('pulsate blue..')
    # fade in RGB blue:
    for i in range(100):
      rgb.fill_color(get_color(0, 0, i))
      time.sleep_ms(20)
    # fade out RGB blue:
    for i in range(100):
      rgb.fill_color(get_color(0, 0, 100-i))
      time.sleep_ms(20)
    check_input()
    
  elif (state == 'CLOSED'):
    # if less than 1 seconds passed since change to 'CLOSED':
    if(time.ticks_ms() < state_timer + 1000):
      print('fade in yellow..')
      for i in range(100):
        rgb.fill_color(get_color(i, i, 0))
        time.sleep_ms(20)
    # if more than 5 seconds passed since change to 'CLOSED':
    elif(time.ticks_ms() > state_timer + 5000):
      state = 'FINISH'
      print('change to', state)
      # save current time in milliseconds:
      state_timer = time.ticks_ms()
      
  elif (state == 'FINISH'):
    print('fade from yellow to red..')
    for i in range(100):
      rgb.fill_color(get_color(100, 100-i, 0))
      time.sleep_ms(20)
      
    # if 2 seconds passed since change to 'FINISH':
    if(time.ticks_ms() > state_timer + 2000):
      print('fade from red to black..') 
      for i in range(100):
        rgb.fill_color(get_color(100-i, 0, 0))
        time.sleep_ms(20)
      time.sleep(1)
      check_input()

# check input pin and change state to 'OPEN' or 'CLOSED'
def check_input():
  global state, state_timer
  if (input_pin.value() == 0):
    if(state != 'CLOSED'):
      print('change to CLOSED')
    state = 'CLOSED'
    # save current time in milliseconds:
    state_timer = time.ticks_ms()
  else:
    if(state != 'OPEN'):
      print('change to OPEN')
    state = 'OPEN'
    
    
# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

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


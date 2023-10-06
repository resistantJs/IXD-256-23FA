# using built-in button to control an LED connected to pin 1 

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

# global pin1 variable:
pin1 = None

def setup():
  global pin1
  # initialize M5 board:
  M5.begin()
  # initialize pin1 as an output pin:
  pin1 = Pin(1, mode=Pin.OUT)

def loop():
  global pin1
  # update M5 board:
  M5.update()
  if BtnA.isPressed():
    # turn pin1 on (high) and sleep for 100 milliseconds:
    pin1.on()
    time.sleep_ms(100)
  else:
    # turn pin1 off (low) and sleep for 100 milliseconds:
    pin1.off()
    time.sleep_ms(100)

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

# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

# switch is connected to the up direction on the d-pad
switch = digitalio.DigitalInOut(board.D1)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
# usb power is connected to the output of the usb 3.3v regulator
usb_power = digitalio.DigitalInOut(board.D0)
usb_power.direction = digitalio.Direction.INPUT
usb_power.pull = digitalio.Pull.DOWN

# true: usb write
# false: circuitpython write
# usb write when usb power connected (=true) AND switch is not pressed (=true)
# circuitpython write when no usb power (=false)
# circuitpython write when switch pressed (=false)
storage.remount("/", usb_power.value and switch.value)

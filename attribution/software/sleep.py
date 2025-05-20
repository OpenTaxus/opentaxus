import alarm
import time

#this class manages the sleep mode.
#the main loop will call update() after no buttons pressed for awhile
#rp2040 sleep info: https://learn.adafruit.com/deep-sleep-with-circuitpython/rp2040-sleep
#light sleep is a quick wakeup, saves ~ 100mW
#deep sleep requires rebooting/reloading, but saves ~200mW

class sleep:
    def __init__(self, display, dpad, leds):
        self.dpad=dpad
        self.display=display
        self.leds=leds

    def update(self,timeout=90):
        #turn off the display - 50mW
        self.display.display.sleep()
        #trigger on 'x' button press
        pin_alarm = self.dpad.getpinalarm()
        #trigger in <timeout> seconds
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + timeout)
        #todo: turn of neopixels and ir
        if self.leds.sleep()=="on":
            #if they want leds on, only do light sleep and save ~100mW
            alarm.light_sleep_until_alarms(pin_alarm)
        else:
            #if leds off go to light sleep ~100mW
            #but trigger on timer to transition to deep sleep
            alarm.light_sleep_until_alarms(time_alarm,pin_alarm)
            if alarm.wake_alarm == time_alarm:
                #if we timed out, go to deep sleep ~7mW
                print("light sleep timeout; deep sleep!")
                alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
            #otherwise, it must've been a button press; wake up
        print("light sleep button; resume!")
        #put dpad back to normal
        self.dpad.clearpinalarm()
        #todo: turn on neopixels and ir
        self.leds.wake()
        #turn display back on
        self.display.display.wake()
        return 0

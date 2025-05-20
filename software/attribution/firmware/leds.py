import board
import neopixel
import digitalio

from adafruit_led_animation.animation.solid import Solid
#from adafruit_led_animation.animation.chase import Chase
#from adafruit_led_animation.animation.comet import Comet
#from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
#from adafruit_led_animation.animation.rainbowcomet import RainbowComet

import adafruit_led_animation.color as color

class led_control:

    neopixel_power=digitalio.DigitalInOut(board.NEOPIXEL_POWER)
    neopixel_power.direction=digitalio.Direction.OUTPUT
    neopixel_power.value=True
    num_pixels = 2
    colors = [color.RED,color.ORANGE,color.YELLOW,color.GREEN,color.BLUE,color.PURPLE,color.WHITE]
    color_name = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "White"]
    color = colors[0]
    brightness_levels = [0.02, 0.15, 0.3, 0.5]
    pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.3)
    led_patterns=[]
    current_pattern=0
    sleep_mode="off"

    def __init__(self):
        self.init_colors()

    #creates all the animations
    def init_colors(self):
        self.led_patterns = [
            Solid(self.pixels,color.BLACK),
#            RainbowComet(self.pixels,0.1,ring=True),
            Rainbow(self.pixels,0.1),
#            Chase(self.pixels,0.1,self.color),
#            Comet(self.pixels,0.1,self.color,tail_length=4,ring=True),
            Solid(self.pixels,self.color),
#            Pulse(self.pixels,0.03,self.color),
        ]

    def sleep(self):
        if self.sleep_mode=="off":
            self.neopixel_power.value=False
        return self.sleep_mode

    def wake(self):
        self.neopixel_power.value=True

    #steps through brightness levels and applies
    def next_brightness(self):
        self.pixels.brightness=self.brightness_levels[(self.brightness_levels.index(self.pixels.brightness) + 1) % len(self.brightness_levels)]
        bright = int(self.pixels.brightness*100)
        return str(bright)+"%"

    #sets the current pattern to be displayed
    def next_pattern(self):
        self.current_pattern=(self.current_pattern+1)%len(self.led_patterns)
        return self.led_patterns[self.current_pattern].__qualname__[0:10]

    #chooses the next color, and then recreates all the animations with that color
    def next_color(self):
        self.color=self.colors[(self.colors.index(self.color) + 1) % len(self.colors)]
        self.init_colors()
        return self.color_name[self.colors.index(self.color)]

    #displays the currently selected animation
    def animate(self):
        self.led_patterns[self.current_pattern].animate()

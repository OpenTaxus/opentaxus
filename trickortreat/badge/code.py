import time
from ssd1306_ui import ssd1306ui
from five_way_pad import FiveWayPad
from disp import disp

from leds import led_control
from home import home
from candy import candies
from friends import friends
from settings import settings
from trade import trade
from sleep import sleep
from game import game_data
import gc

BLACK=0x000000
WHITE=0xFFFFFF



#display, dpad, and leds wrap access to physical I/O
display=ssd1306ui()
dpad=FiveWayPad()
leds=led_control()

#disp is the smart scroll-text display
l_disp = disp(display.homegroup, dpad)

#next, load game data including username
game=game_data()

#create the other view pages, most of which need to access
#a single display group, dpad state, and game data
homepage=home(l_disp, dpad, game)
candies_page=candies(l_disp,dpad,game)
settings_page=settings(display.settingsgroup,dpad,game,leds,l_disp)
friends_page=friends(l_disp,dpad,game)
trade_page=trade(dpad,game,l_disp)
sleep_page=sleep(display,dpad,leds)
gc.collect()

#start out on the home page
page="home"
last_page="home"

# TODO unused
SLEEP_TIMEOUT=90

# ToDo: If not configured, run through configuration steps
while True:
    #update leds and display
    leds.animate()
    gc.collect()
    if page!=0: display.show(page)

    #scan inputs
    dpad.update()

    #sleep if it's been a while - except trade page
    if dpad.duration() > settings_page.timeout and page != "trade":
        page=sleep_page.update()

    #if a button is pressed, handle it
    if not dpad.pressed():
        time.sleep(0.001)
    elif page == "home":
        last_page=page
        page=homepage.update()
    elif page == "settings":
        last_page=page
        page=settings_page.update()
    elif page == "friends":
        last_page=page
        page=friends_page.update()
    elif page == "candies":
        last_page=page
        page=candies_page.update()
    elif page == "trade":
        page=trade_page.update()
    elif page == "sleep":
        page=sleep_page.update()
    else: page=last_page

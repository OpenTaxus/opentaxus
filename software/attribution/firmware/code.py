import time
from ssd1306_ui import ssd1306ui
from five_way_pad import FiveWayPad
from disp import disp

from leds import led_control
from home import home
from clues import clues
from alibis import alibis
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
gc.collect()

l_disp = disp(display.homegroup, dpad)

#instantiate home first, since it manages OOB.
# homepage=home(display.homegroup,dpad)
homepage=home(l_disp, dpad)

#next, load game data since we know we have a username
game=game_data(0)
homepage.game=game
gc.collect()

#finally, create the other view pages, most of which need to access
#a single display group, dpad state, and game data
clues_page=clues(display.cluesgroup,dpad,game)
settings_page=settings(display.settingsgroup,dpad,game,leds)
alibis_page=alibis(l_disp,dpad,game)
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
    elif page == "alibis":
        last_page=page
        page=alibis_page.update()
    elif page == "clues":
        last_page=page
        page=clues_page.update()
    elif page == "trade":
        page=trade_page.update()
    elif page == "sleep":
        page=sleep_page.update()
    else: page=last_page

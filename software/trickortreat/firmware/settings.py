from adafruit_display_text import label
from ssd1306_ui import box
import terminalio
import displayio
import time

BLACK=0x000000
WHITE=0xFFFFFF

#this class manages the settings page. currently it includes LED,
#data wiping, and game advancing options
class settings:
    #todo: use some fancy python data structure to map strings to settings
    #better todo: switch this to gettextselect (after bsidespdx)
    settings=["Sponsors","LED Style","LED Color","LED Brightness","Clear Name","Clear Candies","Clear Contacts","LEDs Off","LED Sleep Mode"]

    def __init__(self, group, dpad, game, leds, l_disp):
        self.group=group
        self.dpad=dpad
        self.game=game
        self.leds=leds
        self.timeout=90
        self.disp = l_disp

        #black text on a white header band, white content on the black box below
        self.header=label.Label(terminalio.FONT,text="Settings", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.contents=label.Label(terminalio.FONT, scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=True
        self.group.append(self.contents)

        #details popup box used by some settings
        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)
        self.group.append(self.details)

        #contains the current selected menu item
        self.x=0

    def update(self):
        #display 3 lines of options. if the first and/or last item is selected,
        #put blank lines in
        new_text= "" if self.x == 0 else self.settings[self.x-1]
        new_text+="\n> "+self.settings[self.x]+"\n"
        new_text+= "" if self.x == len(self.settings)-1 else self.settings[self.x+1]
        self.contents.text=new_text
        self.contents.hidden=False
        self.det.text=self.settings[self.x]

        #u/d to navigate list; l/r to navigate away, x to activate
        if self.dpad.u.fell:
            self.x =(self.x-1)%len(self.settings)
        if self.dpad.d.fell:
            self.x =(self.x+1)%len(self.settings)
        if self.dpad.l.fell:
            return "candies"
        if self.dpad.r.fell:
            return "friends"
        if self.dpad.x.fell:
            if self.details.hidden==True:

                if self.x == 0:
                    print("Looking at sponsors rn")
                    self.det.text="Thank you to our\nPlatinum Sponsors:\n  SecuringHW.com"
                    self.details.hidden=False
                    time.sleep(1.2)
                    self.det.text="Thank you to our\nPlatinum Sponsors:\n       BPM"
                    time.sleep(1.2)
                    self.det.text="Thank you to our\nPlatinum Sponsors:\n     HackerOne"
                    time.sleep(1.2)
                    self.det.text="And a shout\nout to all of\nour voulunteers!"
                    time.sleep(2)
                    self.det.text="It was you that\nmade this all\npossible thank you"
                    time.sleep(2)
                    self.details.hidden=True

                if self.x==1:
                    #advance to next led mode
                    self.settings[self.x]="Style: "+ self.leds.next_pattern()
                elif self.x==2:
                    #advance to next led color
                    self.settings[self.x]="Color: "+ self.leds.next_color()
                elif self.x==3:
                    #advance to next brightness
                    self.settings[self.x]="Brightness: "+ self.leds.next_brightness()
                elif self.x==4:
                    #change name by setting to "" and forcing power cycle
                    #first, pop up confirmation window
                    self.det.text="Wipe your name?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        #block until cancelled(l) or confirmed (r)
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_id()
                            self.det.text="Name Wiped!\n Power cycle\n to continue"
                            while True:
                                pass
                elif self.x==5:
                    #clear candies then resume
                    self.det.text="Wipe ALL candies?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        #block until cancelled(l) or confirmed (r)
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_candies()
                            self.det.text="Candies Wiped!\n'<' to return"
                elif self.x==6:
                    #clear contacts
                    self.det.text="Wipe all Friends?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        #block until cancelled(l) or confirmed (r)
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_friends()
                            self.det.text="Friends Wiped!\n'<' to return"
                elif self.x==7:
                    #leds off
                    self.leds.current_pattern=0
                elif self.x==8:
                    #set sleep behavior of the leds
                    self.det.text="LEDs when idle?\n'<' off  pause '>'\n 'v' don't sleep"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.leds.sleep_mode="off"
                            self.details.hidden=True
                            self.timeout=90
                        if self.dpad.r.fell:
                            self.leds.sleep_mode="on"
                            self.details.hidden=True
                            self.timeout=90
                        if self.dpad.d.fell:
                            self.timeout=1073741823
                            self.details.hidden=True
                        if self.dpad.u.fell:
                            self.details.hidden=True



        return "settings"

import displayio
import board
import busio
import adafruit_displayio_sh1106
from adafruit_ticks import ticks_ms, ticks_add, ticks_less


BLACK=0x000000
WHITE=0xFFFFFF

class sh1106ui:
    WIDTH = 130
    HEIGHT = 64
    BORDER = 10
    ANIMATIONTIME=500
    currentgroup=0

    #initialize display; if already initialized, pass the device. If not, then initialize the default
    def __init__(self,display=None):

        #initialize display
        if display is None:
            displayio.release_displays()
            #i2c = busio.I2C(board.SCL1, board.SDA1)
            i2c=board.I2C()
            display_bus=displayio.I2CDisplay(i2c,device_address=60)
            self.display = adafruit_displayio_sh1106.SH1106(display_bus, width=self.WIDTH, height=self.HEIGHT)
        else:
            self.display=display

        #todo: use a single palette

        # Make maingroup to hold stuff
        self.maingroup = displayio.Group()
        self.maingroup.hidden=False
        self.display.show(self.maingroup)

        # make a background in the back of header
        self.maingroup.append(box(126,15,WHITE,3,0))
        self.maingroup.append(box(126,1,WHITE,3,63))
        
        #make pagegroups that contains a separate group for each page
        self.pagegroup = displayio.Group(x=-260)
        self.maingroup.append(self.pagegroup)

        self.settingsgroup = displayio.Group(x=4)
        self.pagegroup.append(self.settingsgroup)

        self.alibisgroup = displayio.Group(x=134)
        self.pagegroup.append(self.alibisgroup)

        self.homegroup = displayio.Group(x=264)
        self.pagegroup.append(self.homegroup)

        self.cluesgroup = displayio.Group(x=394)
        self.pagegroup.append(self.cluesgroup)

        self.pagegroup.append(box(3,64,WHITE,000,0))
        self.pagegroup.append(box(4,64,WHITE,129,0))
        self.pagegroup.append(box(4,64,WHITE,259,0))
        self.pagegroup.append(box(4,64,WHITE,389,0))
        self.pagegroup.append(box(1,64,WHITE,519,0))

        # make trade group overlay, hidden by default
        self.tradegroup = displayio.Group(x=8,y=0)
        self.tradegroup.hidden=True
        self.maingroup.append(self.tradegroup)

    def show(self,groupname):
        #print(f'{groupname} -- {self.currentgroup}')
        if groupname==self.currentgroup:
            #no change in group, but do we still need to update animation?
            if self.targetx!=self.pagegroup.x:
                #calculate and set x based on starttime
                if ticks_ms()-self.starttime>self.ANIMATIONTIME: self.pagegroup.x=self.targetx
                else: self.pagegroup.x=self.startx+int(((ticks_ms()-self.starttime)/self.ANIMATIONTIME)*(self.targetx-self.startx))
                #print("setting x to ",self.targetx,self.pagegroup.x,self.startx,int((ticks_ms()-self.starttime)/self.ANIMATIONTIME),(self.targetx-self.startx))
        else:
            #prepare for animation
            self.currentgroup=groupname
            self.starttime=ticks_ms()
            self.startx=self.pagegroup.x
            if groupname == "settings": self.targetx=0
            elif groupname == "alibis": self.targetx=-130
            elif groupname == "home": self.targetx=-260
            elif groupname == "clues": self.targetx=-390
            # sleep and trade don't need to move x
            else: self.targetx=self.pagegroup.x

def box(w,h,color,x,y):
    color_bitmap = displayio.Bitmap(w,h, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color
    return displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=x, y=y)

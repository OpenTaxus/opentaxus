import displayio
import terminalio
import adafruit_imageload
from ssd1306_ui import box
from adafruit_display_text import label

BLACK=0x000000
WHITE=0xFFFFFF

#clues manages the clues display in the game
#it needs access to the display group to draw on, dpad for control
#and game data structure
class clues:
    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.game=game
        #set initial position
        self.x=0
        self.y=0

        #Create the title in black text on the existing white header bar
        self.header=label.Label(terminalio.FONT,text="Clues, Game 0", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        #create a layout of all the clues using a sprite table
        clue_sheet, palette = adafruit_imageload.load("assets/clues.bmp",bitmap=displayio.Bitmap, palette=displayio.Palette)
        self.clue_grid = displayio.TileGrid(clue_sheet, pixel_shader=palette,
            width=13, height=3,
            tile_width=12, tile_height=16)
        self.clue_group=displayio.Group(y=15)
        self.clue_group.append(self.clue_grid)
        self.group.append(self.clue_group)

        #create a hidden detail overlay that is shown when the d-pad is pressed
        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.detail_label=label.Label(terminalio.FONT,text="About", color=WHITE, x=4, y=8)
        self.details.append(self.detail_label)
        self.group.append(self.details)

        #lay out all the cards, and set the initial position 
        self.set_cards()
        #highlight the currently selected card
        self.clue_grid[self.x,self.y]+=1


    def set_cards(self):
        #update header based on current game number
        self.header.text="Clues, game # " + str(self.game.game_num)
        #new data structure. todo Need to clarify x,y to type,clue mapping.
        #for row,cluetype in enumerate(self.game.clues):
        for row,cluetype in enumerate(self.game.clues.values()):
        #for cluetype,clues in self.game.clues.items():
            if cluetype["updated"]==True:
                cluetype["updated"]=False
                self.x=0
                self.y=row
                count=0
                #show unknown cards
                for clue in cluetype["unknown"]:
                    self.clue_grid[count,row]=7
                    count+=1
                #show known cards
                #todo: update images
                for clue in cluetype["known"]:
                    self.clue_grid[count,row]=1
                    count+=1
                cluetype["count"]=count
                for i in range(count,13):
                    self.clue_grid[i,row]=0
                #if solved, indicate it
                if len(cluetype["unknown"])==1:
                    self.clue_grid[0,row]=9

    #process inputs and changes to state
    def update(self):
        #show grid
        self.clue_group.hidden=False
        #un-highlight current clue
        self.clue_grid[self.x,self.y]-=1
        #get the right clue for printing...
        cluetype=self.game.clues[list(self.game.clues.keys())[self.y]]
        #this checks for clue updates
        self.set_cards()
        if self.dpad.u.fell:
            #pressing u at the top of the screen goes to trade
            if self.y==0:
                self.clue_grid[self.x,self.y]+=1
                return "trade"
            #otherwise just moves the cursor up
            self.y -=1
            cluetype=self.game.clues[list(self.game.clues.keys())[self.y]]
            self.x=min(self.x,cluetype["count"]-1)
        if self.dpad.d.fell:
            #pressing d at the bottom goes to sleep
            if self.y==2:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "sleep"
            #otherwise just moves the cursor down
            self.y +=1
            cluetype=self.game.clues[list(self.game.clues.keys())[self.y]]
            self.x=min(self.x,cluetype["count"]-1)
        if self.dpad.l.fell:
            #l at the left goes back to home
            if self.x==0:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "home"
            self.x -=1
        if self.dpad.r.fell:
            #r and the right goes around to settings
            if self.x==cluetype["count"]-1:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "settings"
            self.x+=1
        if self.dpad.x.fell:
            #x shows or hides details
            self.details.hidden=not self.details.hidden
        #highlight the current selected clue
        self.clue_grid[self.x,self.y]+=1
        #get the right clue for printing...
        cluetype=self.game.clues[list(self.game.clues.keys())[self.y]]
        all_clues=list(cluetype["unknown"].items())+list(cluetype["known"].items())
        (clue,informant)=all_clues[self.x]
        if self.game.unsolved==0:
                self.detail_label.text=self.game.solution_string
        elif informant=="":
            if len(cluetype["unknown"])==1:
                self.detail_label.text="Attribution!\nIt was\n"+clue
            else:
                self.detail_label.text="Could've been\n"+clue
        elif informant==self.game.myname:
            self.detail_label.text="I know it wasn't\n"+clue
        else:
            self.detail_label.text=informant+"\nknows it wasn't\n"+clue
        return "clues"

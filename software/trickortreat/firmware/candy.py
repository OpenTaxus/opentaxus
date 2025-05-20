import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

#candies manage the candy list. This persists across games. since one candy can give
#you multiple candies, there's a little more work to add that list of candies
class candies:
    def __init__(self, l_disp,  dpad, game):
        #self.group=group
        self.dpad=dpad
        self.game=game
        self.candy_selected=0

        self.disp = l_disp
        self.details = False

    def update(self):
        #there's a better solution than re-doing this every loop... maybe a separate "show()"?
        if len(self.game.candyTally)==0:
            self.disp.setHeader("Candies")  # ToDo: it might be nice to show our own name here
            self.disp.setText("Go collect some candy and make some friends")
        else:
            candyNames=list(self.game.candyTally.keys())
            currentCandyName=candyNames[self.candy_selected]
            #self.group.hidden=False

            if self.details:
                self.disp.setHeader(currentCandyName)
                self.disp.setText("You have "+str(self.game.candyTally[currentCandyName])+" "+currentCandyName)
            else:
                self.disp.setHeader("Candies")  # ToDo: it might be nice to show our own name here
                self.candy_selected = self.disp.setTextGetSelect(candyNames)
                if self.candy_selected >= 0:
                    print("[candies] Selected item {} - {}".format(self.candy_selected, candyNames[self.candy_selected]))
                    self.details = True
                    # skip processing dpad, so we will display the right thing in the next loop
                    return "candies"

        if self.dpad.l.fell:
            #self.group.hidden=True
            self.details = False
            return "home"
        elif self.dpad.r.fell:
            #self.group.hidden=True
            self.details = False
            return "settings"
        elif self.dpad.x.fell:
            self.details = not self.details
        return "candies"

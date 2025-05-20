import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

#alibis manage the alibi list. This persists across games. since one alibi can give
#you multiple clues, there's a little more work to add that list of clues
class alibis:
    def __init__(self, l_disp,  dpad, game):
        #self.group=group
        self.dpad=dpad
        self.game=game

        self.disp = l_disp
        self.details = False

    def update(self):
        #there are 3 lines displayed. The middle line is the 'selected' one
        #and has a > in front
        alibinames=list(self.game.alibis.keys())
        #self.group.hidden=False
        scroll = False


        if self.details:
            # ToDo: Convert this into a pretty pop-up
            self.disp.setHeader(alibinames[self.alibi_selected])
            scroll = self.disp.setText( 
                [alibinames[self.alibi_selected], "said it wasn't:"] + self.game.alibis[alibinames[self.alibi_selected]]
            )
        else:
            self.disp.setHeader("Alibis")  # ToDo: it might be nice to show our own name here
            scroll = self.alibi_selected = self.disp.setTextGetSelect(alibinames)
            if self.alibi_selected >= 0:
                print("[alibis] Selected item {} - {}".format(self.alibi_selected, alibinames[self.alibi_selected]))
                self.details = True
                # skip processing dpad, so we will display the right thing in the next loop
                return "alibis"

        if self.dpad.l.fell:
            #self.group.hidden=True
            self.details = False
            return "settings"
        elif self.dpad.r.fell:
            #self.group.hidden=True
            self.details = False
            return "home"
        elif self.dpad.x.fell:
            self.details = not self.details
        return "alibis"

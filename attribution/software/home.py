# from disp import disp
# import terminalio
# import displayio
# import random
# from ssd1306_ui import box
# from adafruit_display_text.label import Label
import time

# BLACK=0x000000
# WHITE=0xFFFFFF

# this class manages the home display and navigation
# it also presents the new user process when no name is defined
class home:

    def __init__(self, l_disp, dpad):
        # self.group=group
        self.dpad=dpad
        self.game=None
        self.thanks = False # we have 2 main displays, directions and thanks
        self.disp = l_disp

        self.disp.setHeader("OpenTaxus")

        # ToDo: breakout badge setup into it's own thing, should be checked in code.py
        # get the username from file. This duplicates the work done by game.read_name()
        # but i'd rather add file i/o here than add display management there
        try:
            with open("data/myname.txt",'r') as file:
                name=file.readline().rstrip()
        except OSError as e:
            print(e)
            name=""

        #if there's no file or it's blank, give some instructions and ask for a name
        # ToDo: Move to config?
        # ToDo: Break out the instructions message into a config item
        if name=="":
            while True:
                self.dpad.update()
                if self.dpad.x.fell:
                    break
                self.disp.setText([ "The", "Attribution", "Game!"], align="c")
                time.sleep(.01)

            while True:
                self.dpad.update()
                if self.dpad.x.fell:
                    break
                self.disp.setText([
                    "Meet people & trade",
                    "clues to attribute",
                    "the attack",
                    "You don't have",
                    "a handle yet!",
                    "Your handle will",
                    "be shared when you",
                    "trade in the game."
                ])
                time.sleep(.01)

            # nameEntry blocks, not fixing
            name=self.nameEntry()

            while True:
                self.dpad.update()
                if self.dpad.x.fell:
                    break
                self.disp.setText([
                    "Welcome to the game",
                    name,
                    "press '^' & point @",
                    "another to trade",
                    "contact & clues!",
                    "press '<' to get to",
                    "settings and a list",
                    "of alibis",
                    "press '>' to get to",
                    "your clue collection",
                    ""
                    "Collect enough",
                    "clues to figure",
                    "out what happened",
                    "Have fun!"
                ])
                time.sleep(.01)

    # show a string and handle text input
    def nameEntry(self):
        instructions=["Enter your handle","Press to save"]
        player_name = [" "] * 20  # max name length
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'<>.?/|\\{}[] "
        cindex = 0
        nindex = 0
        player_name[nindex] = chars[cindex]
        self.disp.setTextCursor( instructions + ["".join(player_name)], (nindex,2) )

        while True:
            self.dpad.update()
            if self.dpad.u.fell:
                # u increments through the character set for names
                cindex = (cindex + 1) % len(chars)
                player_name[nindex] = chars[cindex]
                self.disp.setTextCursor( instructions + ["".join(player_name)], (nindex,2) )
            elif self.dpad.d.fell:
                # d decrements through the character set for names
                cindex = (cindex - 1) % len(chars)
                player_name[nindex] = chars[cindex]
                self.disp.setTextCursor( instructions + ["".join(player_name)], (nindex,2) )
            elif self.dpad.l.fell:
                # l moves to the previous char
                nindex = nindex - 1 if nindex > 0 else 0
                cindex = chars.find(player_name[nindex])
                self.disp.setTextCursor( instructions + ["".join(player_name)], (nindex,2) )
            elif self.dpad.r.fell:
                # r moves to the next char
                nindex = nindex + 1 if nindex < len(player_name)-1 else len(player_name) - 1
                # move cindex to existing character at slot
                cindex = chars.find(player_name[nindex])
                self.disp.setTextCursor( instructions + ["".join(player_name)], (nindex,2) )
            elif self.dpad.x.fell:
                # x means we're done. Verify and resume.
                self.disp.setText(["Saving your handle:", str.rstrip("".join(player_name))])
                self.disp.setText("Saving handle")
                try:
                    with open("data/myname.txt",'w') as file:
                        file.write("".join(player_name))
                except OSError as e:
                    print(e)
                print("player_name: {}".format("".join(player_name)))
                return str.rstrip("".join(player_name))
            time.sleep(.01)



    def update(self):
        # show contents, process keypresses
        # self.disp.hidden=False
        self.disp.setHeader("OpenTaxus")

        if self.thanks:
            self.disp.setHeader("Sponsors")
            if self.disp.setText([
                "Thank you to our",
                "Sponsors!",
            ]): 
                if self.dpad.u.fell:
                    return "trade"
                elif self.dpad.d.fell:
                    return "sleep"
            if self.dpad.x.fell: self.thanks = not self.thanks
            elif self.dpad.l.fell: 
                return "alibis"
            elif self.dpad.r.fell:
                return "clues"
        else:
            #this is causing oom!
            if self.disp.setText(self.game.solution_string):
                if self.dpad.u.fell:
                    return "trade"
                elif self.dpad.d.fell:
                    return "sleep"
            if self.dpad.l.fell:
                return "alibis"
            elif self.dpad.r.fell:
                return "clues"
            elif self.dpad.x.fell: self.thanks = not self.thanks
        return "home"

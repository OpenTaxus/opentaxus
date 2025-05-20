import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

#friends manage the friend list. This persists across games. since one friend can give
#you multiple candies, there's a little more work to add that list of candies
class friends:
    def __init__(self, l_disp,  dpad, game):
        #self.group=group
        self.dpad=dpad
        self.game=game
        self.friend_selected=0

        self.disp = l_disp
        self.details = False

    def update(self):
        if len(self.game.friends)==0:
            self.disp.setHeader("Friends")
            self.disp.setText("Go make some friends and collect candy!")
        else:
            friendNames=list(self.game.friends.keys())
            currentFriendName=friendNames[self.friend_selected]
            #self.group.hidden=False

            if self.details:
                # ToDo: Convert this into a pretty pop-up
                self.disp.setHeader(currentFriendName)
                self.disp.setText(currentFriendName + " gave you " + self.game.friends[currentFriendName])
            else:
                self.disp.setHeader("Friends")  # ToDo: it might be nice to show our own name here
                self.friend_selected = self.disp.setTextGetSelect(friendNames)
                if self.friend_selected >= 0:
                    print("[friends] Selected item {} - {}".format(self.friend_selected, friendNames[self.friend_selected]))
                    self.details = True
                    # skip processing dpad, so we will display the right thing in the next loop
                    return "friends"

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
        return "friends"

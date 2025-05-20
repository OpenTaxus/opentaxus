from displayio import Group
import terminalio
import gc
from adafruit_display_text.bitmap_label import Label

DEBUG = False

__WHITE      =0xFFFFFF
__BLACK      =0x000000

__DISPLAY_WIDTH    = 128
__DISPLAY_HEIGHT   = 64

__ROWS=3
__COLS=20
__MAX_CHARS_IN_ROW = 20
__FONT_WIDTH = 6
__FONT_HEIGHT = 16

# how far should we move with each scroll
__SCROLL = 2

class disp:
    """
    Class to handle display of content
    """

    def __init__(self,group,dpad):
        self.dpad = dpad
        self.group = group
        self.body_text = ""

        # Create a header and a text block area
        self.head = Label(terminalio.FONT, text="", color=__BLACK, background_color=__WHITE, x=0, y=0)
        self.head.anchor_point = (0,0)
        self.head.anchored_position = (0,0)
        self.group.append(self.head)

        self.body=Group(x=0, y=__FONT_HEIGHT)
        self.group.append(self.body)
        
        self.content=Label(terminalio.FONT, text="", scale=1, color=__WHITE, background_color=__BLACK, x=0, y=0)
        self.content.anchor_point = (0,0)
        self.content.anchored_position = (0,0)
        self.body.append(self.content)

        self.nav_x = Label(terminalio.FONT, text="x", color=__BLACK, background_color=__WHITE,
            y=-2, anchor_point=(1.0,0.5), anchored_position=(__DISPLAY_WIDTH-3, (__DISPLAY_HEIGHT-__FONT_HEIGHT)/2))
        self.nav_x.hidden = True
        self.body.append(self.nav_x)

        self.nav_u=Label(terminalio.FONT, text="^", color=__BLACK, background_color=__WHITE,
            anchor_point=(1.0,0.0), anchored_position=(__DISPLAY_WIDTH-3, -2))
        self.nav_u.hidden=True
        self.body.append(self.nav_u)

        self.nav_d=Label(terminalio.FONT, text="v", color=__BLACK, background_color=__WHITE,
            anchor_point=(1.0,1.0), anchored_position=(__DISPLAY_WIDTH-3, __DISPLAY_HEIGHT-__FONT_HEIGHT))
        self.nav_d.hidden = True
        self.body.append(self.nav_d)

        self.cursor=Label(terminalio.FONT, color=__BLACK, background_color=__WHITE,
            anchor_point=(0.0,0.0), anchored_position=(0,0))
        self.cursor.hidden = True 
        self.body.append(self.cursor)

    def hide_all(self):
        self.cursor.hidden = True 
        self.nav_d.hidden = True 
        self.nav_u.hidden = True 
        self.nav_x.hidden = True

    def wraplines(text):
        res = []
        while len(text) > __MAX_CHARS_IN_ROW:
            for start in range(__MAX_CHARS_IN_ROW,5,-1):
                split = text.find(" ", start)
                if split >= 0 and split < __MAX_CHARS_IN_ROW:
                    res.append(text[0:split])
                    # skips the space
                    text = text[split+1:]
                    break
        # add the last chunk from input
        res.append(text)
        return res

    def setHeader(self,input):
        """
            Sets the header of group being displayed
            input - the label to be used
        """
        if DEBUG: print("[disp.setHeader] self.head.text: {}".format(self.head.text))
        if DEBUG: print("[disp.setHeader] input: {}".format(input))
        if self.head.text != input:
            self.head.text = input

    def setText(self,input, align="l"):
        """
        Displays text provided
        input 
            - An array of lines of text
            - a single line of text
        # ToDo: implement alignment
        align - what alignment should be use
            c - centered
            r - right
            l - left

        behavior:
            Automatically aligns text as requested
            If a single text string is provided, shows that in the middle row
            If an array of text
                Displays from top down
            If an array of more than 3 text rows
                scroll up/down markers are displayed
                    up is displayed if scrolled below input[0] showing
                    down is displayed if scrolled above input[len(input)] showing
                    up & down displayed if input[0] and input[len(input)] are both off screen
                dpad up/down is read to scroll
                any other dpad causes return
        return:
            - True if scrolled up or down ("consuming" a dpad U or D)
            - False if there was no scrolling, or at the top/bottom
        """
        # True if we're in the middle and scrollable
        # False if the caller should handle dpad up/down
        # Return whether caller should handle scrolling up or down
        pass_dpad = False

        # convert input into an array, or save the existing arraay into the right variable
        if type(input) is str:
            # if it's a string, turn it into a nicely wrapped array
            lines = disp.wraplines(input)
        elif type(input) is list:
            lines = input
        # ToDo: Handle bare numbers sent to setText
        else: 
            print("Error with input to setText, not sure how to handle: {}".format(input)) 
            self.content.text = "\n".join(["Problems: please","check serial","console"])
            self.content.color = __BLACK 
            self.content.background_color = __WHITE
            return not pass_dpad

        # this block handles up down dpad presses, and makes sure to tell the calling function it's 
        # been handled
        if self.body_text == input:
            if self.dpad.u.fell:
                # stop at the top of text, no looping
                if self.curTopRow <= 0: pass_dpad = True 
                self.curTopRow = (self.curTopRow - __SCROLL) if self.curTopRow - __SCROLL >= 0 else 0
            elif self.dpad.d.fell:
                # stop at the bottom of text, no looping
                if self.curTopRow + 3 >= len(lines): pass_dpad = True
                if self.curTopRow < len(lines) - __ROWS:
                    self.curTopRow = self.curTopRow + __SCROLL 
                else:
                    self.curTopRow = len(lines) - __ROWS if self.curTopRow - __ROWS >= 0  else 0
            else:
                # if input is the same and we didn't get a dpad, do nothing
                # empty our locals and garbage collect
                lines = []
                gc.collect()
                return pass_dpad
        else:
            # reset for new text to display
            self.curTopRow = 0
            self.body_text = input
        self.hide_all()
        for index in range(len(lines)):
            if len(lines[index]) > __MAX_CHARS_IN_ROW:
                print("[disp.setText] Line too long: {}".format(lines[index]))
        end = self.curTopRow + 3
        if len(lines) <= end:
            end = len(lines)
        # ToDo: Alignment logic goes around this line
        self.content.text = "\n".join(lines[self.curTopRow:end])
        if DEBUG: print("[disp.setText] showing press nav") 
        self.nav_x.hidden = False
        if not self.curTopRow == 0:
            if DEBUG: print("[disp.setText] showing up nav")
            self.nav_u.hidden = False
        if not end >= len(lines):
            if DEBUG: print("[disp.setText] showing down nav")
            self.nav_d.hidden = False
        lines = []
        gc.collect()
        return pass_dpad
        


    def setTextGetSelect(self,input):
        """
            Displays text with a left side selection marker
            Input 
                - an array of options

            behavior:
                dpad is read for up and down scrolling
                is there a non-destructive dpad read, or should this return the dpad position as well?
                    dpad select causes return
                    dpad left/right causes return
                Shows a highlighted selection indicator at the row that will be returned if clicked

            returns
                - the array value of the selected item
                - dpad left/right result
        """
        # Return whether caller should handle scrolling up or down
        scroll = False

        # Sort out any dpad motions
        if self.body_text == input:
            if self.dpad.u.fell:
                # cursorRow up until 0, curTopRow up until 0, no wrap
                if self.cursorRow <= 0:
                    self.curTopRow = self.curTopRow - 1 if self.curTopRow > 0 else 0
                    self.cursorRow = 0
                    scroll = True
                else:
                    self.cursorRow -= 1
            elif self.dpad.d.fell:
                # cursorRow down until 2, curTopRow down until full screen are last lines
                if self.cursorRow >= 2:
                    self.curTopRow = self.curTopRow + 1 if self.curTopRow + 2 > len(input) else len(input) - 3
                    self.cursorRow = 2  # cursorRow should never be above 2, this is a safety only
                    scroll = True
                else:
                    self.cursorRow = self.cursorRow + 1 if self.cursorRow < len(input) - 1 else len(input) - 1
            elif self.dpad.x.fell:
                return self.curTopRow + self.cursorRow
            else:
                # nothing changed, no inputs, give a "nothing selected" answer
                return -1
        else:
            if DEBUG: print("[disp.setTextGetSelect] {}".format(input))
            self.body_text = input 
            self.curTopRow = 0
            self.cursorRow = 0

        # ToDo: put in logic for a fancy line-wrap with prompting here
        lines = input[self.curTopRow:self.curTopRow + 3]
        for idx in range(0,len(lines)):
            if len(lines[idx]) > 18:
                print("[disp.setTextGetSelect] Line too long (18 char limit): {}".format(lines[idx]))
            lines[idx] = lines[idx]
        self.content.text = "\n".join(lines)
        self.content.x = 8

        self.hide_all()
        self.nav_x.hidden = False
        if self.cursorRow > 0 or self.curTopRow > 0:
            self.nav_u.hidden = False
        # if (self.cursorRow < 2 or self.cursorRow < len(input) - 1) and self.curTopRow + 3 <= len(input):
        if self.curTopRow + 3 <= len(input) or (self.curTopRow == 0 and self.cursorRow < len(input) - 1):
            self.nav_d.hidden = False 
        
        self.cursor.text = ">"
        self.cursor.hidden = False
        self.cursor.color = __BLACK 
        self.cursor.background_color = __WHITE
        self.cursor.anchored_position=(0, self.cursorRow * __FONT_HEIGHT)

        lines = []
        gc.collect()
        return -1  # nothing selected, give the "nothing selected" answer

    def setTextCursor(self,input, cursor=(0,0), align="l"):
        """
            Displays text with a cursor marker
            variables:
                input
                    - a single line of text,
                    - an array of text to be displayed
                align
                    - c - centered
                    - l - left
                    - r - right
            
            behavior:
                Cursor location is adjusted for alignment.
                    If you align center and have 3 arrays of text 10 characters log
                    cursor value (1,5) would put the cursor on the 6th letter of the 2nd row
                cursor method to be determined (underline, block inverse, ???)

            return:
                - instant, calling function handles dpad input
        """
        # For clarity...
        X = 0
        Y = 1
        self.hide_all()
        if DEBUG: print("[disp.setTextCursor] cursor: ({})\tinput: {}".format(cursor, input))

        if type(input) is str:
            if len(input) > __MAX_CHARS_IN_ROW:
                # ToDo: line wrap needed here, but also have to figure out how to wrap cursor
                """   ex: disp.setTextCursor("foofoo barbar foo foo fox bar bar bar", cursor=(25,0))
                            we need to put the cursor on 'x' (if I counted right), even after we wrap
                            the phrase
                """
                print("[disp.setTextCursor] Line too long: {}".format(input))
            if cursor[Y] != 0:
                print("[disp.setTextCursor] row out or range, only using col")
            # single strings go on a the middle line, for now
            self.content.text = "\n" + input
        elif type(input) is list:
            if len(input) > __ROWS: 
                # ToDo: Enable scrolling as part of the cursor display (lots of math)
                print("[disp.updateCursorDisplay] Too many rows! {} is my max with a cursor".format(__ROWS))
                return
            if cursor[Y] > __ROWS-1:
                print("[disp.setTextCursor] Cursor below screen")
                return
            for index in range(len(input)):
                if len(input[index]) > __MAX_CHARS_IN_ROW:
                    print("[disp.setTextCursor] Line too long: {}".format(input[index]))
            self.content.text="\n".join(input)
            # put the cursor on top of the right spot with the right content
            self.cursor.hidden = False 
            self.cursor.text = input[cursor[Y]][cursor[X]]
            self.cursor.anchored_position = ( cursor[X] * __FONT_WIDTH , cursor[Y] * __FONT_HEIGHT)
        else: 
            print("Error with input to setTextCursor, not sure how to handle: {}".format(input))
            self.content.text = "\n".join(["Problems: please","check serial","console"])
            self.content.color = __BLACK
            self.content.background_color = __WHITE
        gc.collect()
    
    def setPopup(self,content, visible=True, label=None):
        """
            Displays a popup, with optional label for the pop-up window

            Returns whether it is visible:
                True - Visible
                False - Invisible
        """
        pass

    def setIcons():
        """ See dispText, but an array of icon arrays """
        pass
    
    def setIconsGetSelect():
        """ See dispTextSelect, but an array of icon arrays """
        pass
    
    def setIconCursor():
        """ See dispTextCursor, but an array of icon arrays """
        pass
    
from adafruit_ticks import ticks_ms
from adafruit_display_text import label
from fake_irda import FakeIRDA
from ssd1306_ui import box
import terminalio
from gc import collect
from time import sleep


BLACK=0x000000
WHITE=0xFFFFFF

#this manages the trading of data with others. Unlike the other views,
#this one is blocking during RX (though this could probably be fixed).
#This class manages the crc check to ensure valid data is tx/rx, but
#game.check_candy does the data structure validation and update
class trade:
    collect()
    state="transmitting"
    timeout=0

    def __init__(self, dpad, game, disp):
        # self.group=group
        self.dpad=dpad
        self.ir=FakeIRDA()
        self.game=game
        self.disp=disp

        """
        #draw a box over the screen with black text on top and white below
        self.group.append(box(112,64,WHITE,0,0))
        self.group.append(box(110,47,BLACK,1,16))
        self.header=label.Label(terminalio.FONT,text="trade", color=BLACK, x=4, y=8)
        self.group.append(self.header)
        self.details=label.Label(terminalio.FONT,text="transmitting", color=WHITE, x=12, y=24)
        self.group.append(self.details)
        """

        self.rxname=None
        self.rxcandy=None

    def update(self):
        #show trade page
        self.disp.setHeader(" ^ to retransmit")

        while True:
            #turn on the PHY to enable tx/rx
            self.ir.enablePHY()

            # Transmit state. Transmit the pre-calculated tx value
            if self.state == "transmitting":
                print("transmitting")
                self.disp.setText("transmitting...")
                self.ir.writebytes(self.game.mytxval)
                #tx complete; prepare to rx. Clear buffer and set timeout
                self.ir.uart.reset_input_buffer()
                self.state="receiving"
                self.timeout=ticks_ms()+30000

            # receive state. listen until data received, then check it and proceed
            elif self.state == "receiving":
                if self.ir.ready(100):
                    self.disp.setText("incoming transmission...")
                    #4 bytes are in the queue - enough to get started. Get data
                    rxval=self.ir.readbytes()
                    resultString=self.game.check_candy(rxval)
                    print(resultString)
                    if "Invalid" in resultString:
                        self.state="transmitting"
                        self.disp.setText(resultString + "... retrying now")
                        sleep(.5)
                    else:
                        #self.disp.setText("responding")
                        self.disp.setText(resultString)
                        self.ir.writebytes(self.game.mytxval)
                        #done responding. Go to success state
                        self.state="success"
                        self.disp.setText(resultString)
                #go to timeout if we've been waiting too long
                elif ticks_ms()> self.timeout:
                    print("timeout")
                    self.state="timeout"
                    self.disp.setText(["timeout :(","^ try again","v cancel"])
                #otherwise, show a timeout countdown
                else:
                    #todo: bug here shows really high countdown values. usually after a failed recieve.
                    self.disp.setText("receiving {}".format((self.timeout - ticks_ms()) // 1000))
                    #print("nothing received yet",self.timeout,ticks_ms())

            #success, timeout, and error states don't have any following action - just wait for buttons
            # process keypress
            self.dpad.update()
            # if down is pressed, return to where we came from
            retval=None
            if self.dpad.d.fell:
                retval=0
            elif self.dpad.u.fell:
                self.state="transmitting"
            elif self.state=="success":
                if self.dpad.pressed(): retval=0
            if retval is not None:
                self.ir.disablePHY()
                self.state="transmitting"
                return retval
            # if u is pressed, restart the trade process

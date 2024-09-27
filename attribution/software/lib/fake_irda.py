import board
import busio
import digitalio

#todo - add error checking

class FakeIRDA:
    def __init__(self,uart=busio.UART(board.TX, board.RX, baudrate=19200, receiver_buffer_size=64),sd=board.D8):
        self.uart=uart
        self.iren=digitalio.DigitalInOut(sd)
        self.iren.switch_to_output()
        self.iren.value=1
        self.possiblymisaligned=False

    # reads a byte from uart and returns it
    def readbyte(self):
        #self.enablePHY()
        rxval=self.uart.read(1)
        if rxval is None:
            return None
        return chr(rxval[0])

    # calls readbyte N times, reading 2*N bytes
    def readbytes(self,count=None):
        bytesread=""
        if count == None:
            byte = self.readbyte()
            while byte is not None:
                bytesread+=byte
                #print("read",len(byte),byte,len(bytesread),bytesread,"one more byte?")
                byte = self.readbyte()
                pass
            return bytesread
        for i in range(count):
            bytesread.append(self.readbyte())
        return bytesread

    # takes one byte, expands it to two bytes interleved with '1's and transmits both
    def writebyte(self,txval):
        #self.enablePHY()
        self.uart.write(bytes([txval]))
        #print(bytes([txval]),txval)
        self.uart.reset_input_buffer()

    # calls writebyte N times, writing 2N bytes total
    def writebytes(self,byteswrite):
        for i in byteswrite:
            self.writebyte(i)

    # set ir enable pin to 0 to wake up phy
    def enablePHY(self):
        self.iren.value=1

    #set ir enable pint to 1 to shut down phy and save power
    def disablePHY(self):
        self.iren.value=0

    #return true if uart has enough bytes waiting.
    def ready(self,numbytes=1):
        return self.uart.in_waiting >= (numbytes)


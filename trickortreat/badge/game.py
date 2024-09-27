import circuitpython_csv
import gc
from binascii import crc32,a2b_base64
import json
from adafruit_rsa import PublicKey, verify

# this class contains all the data relevant to the game. It manages
# loading the data from files, updating it, and writing it back.
class game_data:
    myname=None
    mycandy=None
    mysig=None
    mytxval=None

    keyfile="pub.json"
    idfile="id.json"
    candyfile="candies.json"
    friendfile="friends.json"
    
    #initialize all the data. Read all 3 files and load into memory
    def __init__(self):
        self.pubkey=self.read_pubkey()
        self.read_id()
        self.read_friends()
        self.read_candies()

    # pubkey holds the public key arguments for signature checking
    def read_pubkey(self):
        with open(self.keyfile, "r") as f:
            pub_key_obj = json.loads(f.read())
        return PublicKey(*pub_key_obj["public_key_arguments"])
        return PublicKey(*read_json(keyfile)["public_key_arguments"])

    #pretty much the same thing over and over
    def read_json(self,filename):
        try:
            with open(filename, "r") as f:
                print("loaded file",filename)
                return json.loads(f.read())
        except OSError:
            print("error reading",filename)
            return {}
    
    def write_json(self,mydict,file):
        try:
            with open(file, "w") as f:
                f.write(json.dumps(mydict))
        except OSError:
            print("error writing",file)
            return False
        return True

    # clear name and write to file
    def read_id(self):
        myid=self.read_json(self.idfile)
        if "candy" in myid: self.mycandy=myid["candy"]
        if "signature" in myid: self.mysig=myid["signature"]
        if "name" in myid: self.set_name(myid["name"])
        set


    def set_name(self,name):
        self.myname=name  
        #calculate the message we'll send when we trade.
        transmit_data=bytearray(",".join([self.myname,self.mycandy,str(self.mysig)]),'utf8')
        #calculate CRC
        crc = hex(crc32(transmit_data))
        self.mytxval=transmit_data+bytearray(","+crc,'utf8')
        print(f"{self.mytxval}")
        self.write_id()

    def wipe_id(self):
        self.myname=""
        self.write_id()

    def write_id(self):
        return self.write_json({'name': self.myname, 'candy': self.mycandy, 'signature': self.mysig},self.idfile)

    #friends is a dict of people we met and the candies they gave us
    def read_friends(self):
        self.friends=self.read_json(self.friendfile)

    def wipe_friends(self):
        self.friends={}
        self.write_friends()

    def write_friends(self):
        return self.write_json(self.friends,self.friendfile)

    #candies is a dict of candies an their signature
    def read_candies(self):
        self.candies=self.read_json(self.candyfile)
        self.candyTally={}
        for candy in self.candies.keys():
            self.count_candy(candy)

    def count_candy(self,candy):
        candy=candy[0:candy.find(" #")]
        if candy in self.candyTally:
            self.candyTally[candy]+=1
        else:
            self.candyTally[candy]=1

    def wipe_candies(self):
        self.candies={}
        self.candyTally={}
        self.write_candies()

    def write_candies(self):
        return self.write_json(self.candies,self.candyfile)

    #check a candy, and if valid for this game, add it to the structure.
    def check_candy(self,rxval):
        print(rxval)
        if rxval.count(',') != 3:
            return("Invalid RX data")
        friend, candy, signature, chksum = rxval.split(',')
        if bytearray(hex(crc32(bytearray(",".join([friend,candy,signature]),'utf8'))),'utf8') != chksum:
            return("Invalid Checksum")
        try:
            verify(candy.encode(),a2b_base64(signature[1:]),self.pubkey)
        except Exception as e:
            return("Invalid Signature:",e)
        if friend in self.friends:
            return("You already got "+self.friends[friend]+" from "+friend)
        self.friends[friend]=candy
        self.write_friends()
        self.candies[candy]=signature
        self.write_candies()
        self.count_candy(candy)
        return("Recieved "+candy+" from "+friend)



import circuitpython_csv
import gc
#from binascii import crc32
from binascii import crc32,a2b_base64
from json import loads
from adafruit_rsa import PublicKey

# this class contains all the data relevant to the game. It manages
# loading the data from files, updating it, and writing it back.
class game_data:
    # game_num=0  # set in __init__
    myclue=None
    signature=""
    # myname=None # set in __init__ via call to read_myname()
    mytxval=None
    game_file="data/game1.csv"
    alibi_file="data/alibis.csv"

    #initialize all the data. Read all 3 files and load into memory
    def __init__(self,game_num=0):
        self.game_num=game_num
        self.read_name()
        self.read_alibis()
        self.pubkey=self.read_pubkey()
        print(self.pubkey)
        self.game_file="data/game"+str(game_num)+".csv"
        self.read_clues()

    #check a clue, and if valid for this game, add it to the structure.
    def check_clue(self,newclue,alibi):
        #if we haven't met the alibi before, a them to the list, and flush to disk
        if alibi not in self.alibis.keys():
            self.alibis[alibi]=[newclue]
        # if we have, append the clue to the list of clues
        else:
            print(f"Alibi {alibi} already known, appending")
            #check for duplicate clue in this list
            if newclue not in self.alibis[alibi]:
                self.alibis[alibi].append(newclue)
        self.write_alibis()
        #iterate over all clues. If we have the clue, mark it collected, log the alibi,
        #flag it so the display knows to update it, and flush to disk
        match=False
        for typename,cluetype in self.clues.items():
            if newclue in cluetype["known"]:
                print("clue already shared by ",cluetype["known"][newclue]," but thanks anyway "+alibi)
                match=True
                break
            elif len(cluetype["unknown"])>1 and newclue in cluetype["unknown"]:
                print("new clue!",newclue)
                cluetype["known"][newclue]=alibi
                del cluetype["unknown"][newclue]
                self.check_for_solution(typename,cluetype)
                cluetype["updated"]=True
                match=True
                break
        if match : 
            self.write_clues()
            return newclue
        return False

    #load name from file - if it's not there, set to unknown
    #note that we don't do the oob flow here because that needs
    #control of display we don't want in the data storage class.
    def read_name(self):
        try:
            with open("data/myname.txt",'r') as file:
                self.myname=file.readline().rstrip()
                print("hello",self.myname)
        except OSError:
            print("Error reading name from data/myname.txt")
            self.myname="unknown"

    # clear name and write to file
    def wipe_name(self):
        self.myname=""
        self.write_name()

    #open the name file and write out to it
    def write_name(self):
        try:
            with open("data/myname.txt", 'w') as fhandle:
                fhandle.write(self.myname)
        except OSError:
            print("Error writing name file")
            return False
        return True

    def check_for_solution(self,typename,cluetype):
        if len(cluetype["unknown"]) == 1:
            answer=list(cluetype["unknown"].keys())[0]
            self.solution_string=self.solution_string.replace("["+typename+"]",answer)
            print(self.solution_string)
            self.unsolved-=1
            print("#unsolved: ", self.unsolved)
            if self.unsolved==0:
                print("full solution!!")

    #read csv file of clues for this game. Can be called again
    #to change to a different game number
    def read_clues(self):
        try:
            with open(self.game_file, 'r') as file:
                csv=circuitpython_csv.reader(file)
                #dict to hold clue types which hold clues
                self.clues={}
                #first value tells us what type of clue it is
                self.solution_string="#T used #A against #V"
                for row in csv:
                    if row[0] == "*": 
                        #print(row)
                        self.myclue=row[1]
                        #print(self.myclue,row[2],self.signature)
                        #todo: this should be added to game files as row[2]
                        #self.signature=a2b_base64(row[2])
                        self.signature=row[2]
                        #self.signature="none
                    elif row[0] == "#":
                        self.solution_string=row[1]
                        print(self.solution_string)
                    #make sure we have enough data
                    elif len(row) > 3:
                        status="unknown" if row[3]=="" else "known"
                        #if we haven't seen this cluetype before, create the dict
                        if row[0] not in self.clues:
                            self.clues[row[0]]={"known":{},"unknown":{},"updated":True}
                        #and enter the clue into the dict
                        self.clues[row[0]][status][row[1]]=row[3]
            # count of unsolved categories
            self.unsolved=len(self.clues)
            # check for solutions, count unsolved categories
            for typename,cluetype in self.clues.items():
                self.check_for_solution(typename,cluetype)
                cluetype["updated"]=True
            print("#unsolved: ", self.unsolved)
                
            print(self.clues)
            #add our clue to the table
            self.check_clue(self.myclue,self.myname)
            #calculate the message we'll send when we trade.
            transmit_data=bytearray(",".join([self.myname,str(self.game_num),self.myclue,str(self.signature)]),'utf8')
            #calculate CRC
            crc = hex(crc32(transmit_data))#[2:]
            #crc = str(crc32(transmit_data))
            #self.mytxval=transmit_data+crc
            self.mytxval=transmit_data+bytearray(","+crc,'utf8')
            print(f"{self.mytxval}")
        except OSError:
            print("Error reading from file:", self.game_file)

    #essentially 'resets' the current game, wiping all clues then adding yours back
    def wipe_clues(self):
        ## new clue structure
        for cluetype in self.clues.values():
            for clue in cluetype["known"]:
                cluetype["unknown"][clue]=""
            cluetype["known"]={}
            cluetype["updated"]=True
        print(self.clues)
        self.check_clue(self.myclue,self.myname)
        self.write_clues()

    #write clues csv to disk so it persists through power cycles
    def write_clues(self):
        #should be called every time we add a clue?
        try:
            ## new clue structure
            fhandle = open(self.game_file, 'w')
            fhandle.write("#,"+self.solution_string+"\n")
            for cluetype in self.clues.keys():
                for clue in self.clues[cluetype]["known"]:
                    print(cluetype+","+clue+","+self.clues[cluetype]["known"][clue])
                    fhandle.write(cluetype+","+clue+",0,"+self.clues[cluetype]["known"][clue]+"\n")
                for clue in self.clues[cluetype]["unknown"]:
                    print(cluetype+","+clue+",0,")
                    fhandle.write(cluetype+","+clue+",0,"+"\n")
            print("*,"+str(self.myclue))
            #tack on your clue at the end
            fhandle.write("*,"+str(self.myclue)+","+self.signature)
            fhandle.close()
        except OSError:
            print("Error writing clues file:", self.game_file)
            return False
        return True

    def read_alibis(self):
        try:
            self.alibis={}
            with open(self.alibi_file, 'r') as file:
                for row in circuitpython_csv.reader(file):
                    self.alibis[row[0]]=row[1:]
            #print(self.alibis)
        except OSError:
            print("Error reading from file:", self.alibi_file)

    #clear list of alibis except for yourself, and flush to disk
    def wipe_alibis(self):
        self.alibis=[[self.myname]]
        self.write_alibis()

    def write_alibis(self):
        try:
            fhandle = open(self.alibi_file, 'w')
            for alibi_name,alibi in self.alibis.items():
                fhandle.write(alibi_name+","+",".join(alibi))
                print(alibi_name,",".join(alibi))
                fhandle.write("\n")
        except OSError:
            print("Error writing alibi file:", self.alibi_file)
            return False
        return True

    def read_pubkey(self):
        with open("pub.json", "r") as f:
            pub_key_obj = loads(f.read())
        return PublicKey(*pub_key_obj["public_key_arguments"])
    

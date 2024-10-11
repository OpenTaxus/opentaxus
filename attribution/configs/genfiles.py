#!/usr/bin/python3
import random
import os
import sys
import binascii
import adafruit_rsa
import json

# number of variants to generate
num_variants = 50
working_dir = os.path.dirname(os.path.realpath(__file__))
(public_key, private_key) = adafruit_rsa.newkeys(512)
hash_method="SHA-256"

#todo: clean this up, put pub.json into ../software
f=open("pub.json", "w")
public_obj = {"public_key_arguments": [public_key.n, public_key.e]}
f.write(json.dumps(public_obj))
f.close()

f=open("priv.json", "w")
private_obj = {
    "private_key_arguments": [
        private_key.n,
        private_key.e,
        private_key.d,
        private_key.p,
        private_key.q,
    ]
}
f.write(json.dumps(private_obj))
f.close()

# set the random seed so that game files are deterministic
try:
    with open(os.path.join(working_dir, "seed.txt"), 'r') as file:
        file_content = file.read()
        if len(file_content) < 10:
            print("WARNING: seed.txt short")
        random.seed(file_content)
except Exception as e:
    print("Unable to open seed.txt: ", e)
    sys.exit(5)


#build $file_count unique files for separate badges.
#each file will be a CSV of all the T,A, and V for that game
#each file will also have a unique * line with one clue 
def gen_game_files(game_num,clues,solution_string,file_count=None):
    #we'll re-write this for each file, so build a string
    #one line per clue, coded with the clue type
    clue_csv="#,"+solution_string+"\n"
    for typename, cluetype in clues.items():
        for clue in cluetype:
            print(clue)
            clue_csv+=typename+","+clue+",0,,\n"

    #select the winning combo - randomly choose a threat, attack, and victim
    for typename, cluetype in clues.items():
        index=random.randrange(len(cluetype))
        print("index=",index)
        print("removing ",cluetype[index])
        print(cluetype)
        cluetype.remove(cluetype[index])
        print(cluetype)

    #combine what's left so we can give one each
    all_clues=[]
    for typename, cluetype in clues.items():
        all_clues+=cluetype
        print(all_clues)
    
    #if we don't specify how many files, do one of each.
    if file_count is None: file_count=len(all_clues)

    for i in range(file_count):
        #make the dir if not already there
        #create the game file
        filename=os.path.join(working_dir, "data/", str(i), "game"+str(game_num)+".csv")
        print("creating: "+filename)
        os.makedirs(os.path.join(working_dir, "data/",str(i)),exist_ok=True)
        f=open(filename, "w")
        #write the generated CSV, followed by one line with a * containing a single clue
        my_clue=all_clues[i%len(all_clues)]
        my_sig=adafruit_rsa.sign(my_clue.encode(), private_key, hash_method)
        f.write(clue_csv+"*,"+my_clue+","+str(binascii.b2a_base64(my_sig))+"\n")
        f.close()

gen_game_files(0,
        {
            "AI":["Lore","WOPR","Skynet"],
            "tool":["Borg","NORAD","t1000"],
            "fix":["Data","Tic-Tac-Toe","t800"],
            },
        "[AI] tried to take over using [tool] but was thwarted by [fix]",
    num_variants)


gen_game_files(1,
    {
            "year":["2019","1984","1997","2015"],
            "ai":["Pris","WOPR","Skynet","Ultron"],
            "what":["Sebastia","NORAD","everything","Sokivia"],
            },
        "In [year] [ai] conquered [what].",
    num_variants)


gen_game_files(2,
        {
            "Company":["Terrell Corporation","Yoyodyne Propulsion","Weyland-Yutani","PlayTronics","Ellingson Mineral Company",],
            "startup":["Algofy","EyeTech","AiCept","InvoQTy","Uzzy","EgoBots",],
            "tool":["SOAR","DFIR","IR Management","GRC","Supply Chain Security","Cloud IAM",],
            },
"[Company] has just ann`ounced intent to acquire [startup] to build the industry's most advanced AI-powered [tool].",
    num_variants)


gen_game_files(3,
        {
            "organization":["A mysterious group"],
            "event":["disco rave","glamping trip","scuba live-aboard","picnic","festival",],
            "topic":["OWASP Top 10","CISSP domains","NIST CSF Functions","ISO 27035 - Incident Management",],
            "location":["Oakland","San Jose","Farralons","Alameda","Napa",],
            },
        "[organization] is starting a spinoff [event] focused on [topic] that will be based out of [location].",
    num_variants)


gen_game_files(4,
        {
            "swag":["card","frisbee","lightsaber","lipbalm,sticker"],
            "location":["San Francisco","Oakland","Marin","San Mateo","Alameda","Contra Costa"],
            "activity":["swim","drive","ski","snorkel",],
            },
        "Symmetrical [swag] stacking. Just like the [location] mass [activity] of 2020.",
    num_variants)



gen_game_files(5,
        {
            "murderer":["Col. Mustard", "Dr. Scarlett", "Mr. Green", "Ms. White", "Mx. Peacock", "Prof. Plum"],
            "weapon":["Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"],
            "location":["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Study"],
            },
        "It was [murderer] with the [weapon] in the [location]",
    num_variants)

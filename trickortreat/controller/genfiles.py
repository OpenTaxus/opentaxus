#!/usr/bin/python3
import random
import os
import sys
import binascii
import adafruit_rsa
import json
from math import ceil, log10, floor
import pyudev
import time
import subprocess
from threading import Thread
import time
import hashlib


#this should do all the event-specific stuff
# todo: regenerate signatures if a new key was generated
# todo: parameterize the file load/unload/generate

candies=["Sour Patch Kids","Haribo Gummies","Smarties","Reese's Cups","Twix","Snickers"]
badge_count=900  #overestimate this! Actually, maybe it shouldn't be settable? maybe dynamic? hmm.
exchange_ratio=5 #how many unique signatures can be redeemed for real candy
hash_method="SHA-256"
checkdir="./checkdir/" #path to store check files

#if keys are present, load them. if not, generate them
try:
    with open("priv.json", "r") as f:
        private_obj = json.loads(f.read())
        private_key=adafruit_rsa.PrivateKey(*private_obj["private_key_arguments"])
        public_key=adafruit_rsa.PublicKey(private_key.n, private_key.e)
    print("\n1. Prior keys loaded from priv.json.")
except Exception as e:
    if input("\nNo keys found, generate them? 'yes' to continue, anything else to quit\n") != "yes":
        exit(1)
    #remove all other config files, or set flag?
    print("1. Generating new keys...")
    (public_key, private_key) = adafruit_rsa.newkeys(512)
    public_obj = {"public_key_arguments": [public_key.n, public_key.e]}
    private_obj = { "private_key_arguments": [private_key.n, private_key.e,
                    private_key.d, private_key.p, private_key.q]}

    #probably should remove this since it's uncessessary and redundant to priv.json
    with open("pub.json", "w") as f:
        f.write(json.dumps(public_obj))

    with open("../badge/pub.json", "w") as f:
        f.write(json.dumps(public_obj))

    with open("priv.json", "w") as f:
        f.write(json.dumps(private_obj))
    print(private_key)

# check for seed, if not present, set the random seed so that game files are deterministic (not used in trick or treat)
try:
    with open("seed.txt", 'r') as file:
        seed = file.read()
        random.seed(seed)
    print("\n2. Prior seed loaded from seed.txt.")
except Exception as e:
    if input("\nNo random seed found, generate one? 'yes' to continue, anything else to quit\n") != "yes":
        exit(1)
    print("2. Choosing new random seed... ")
    seed = random.randrange(sys.maxsize)
    rng = random.Random(seed)
    f=open("seed.txt", "w")
    f.write(str(seed))
    f.close
    print("seed:", seed)


signatures={}

# if signatures are present, load them. If not, generate them.
try:
    with open("candies.json", 'r') as f:
        signatures = json.loads(f.read())
    print("\n3. Prior candies loaded from candies.json.")
except Exception as e:
    if input("\nNo candy signatures found, generate them? 'yes' to continue, anything else to quit\n") != "yes":
        exit(1)
    print("3. Generating new candy signatures..")
    candyCount=ceil(badge_count/len(candies))
    maxCandy=10**ceil(log10(candyCount))-1
    for i in range(candyCount):
        for candy in candies:
            unique_candy=candy + " #" + str(maxCandy-i)
            signatures[unique_candy]=str(binascii.b2a_base64(adafruit_rsa.sign(unique_candy.encode(), private_key, hash_method)))
    with open("candies.json", "w") as f:
        f.write(json.dumps(signatures))
    #print(signatures)


assignments={}
# if assignments are present, load them. If not, generate them.
try:
    with open("assignments.json", 'r') as f:
        assignments = json.loads(f.read())
    print("\n4. Prior assignments loaded from assignments.json.")
except Exception as e:
    if input("\nNo prior assignments found, start from scratch? 'yes' to continue, anything else to quit\n") != "yes":
        exit(1)
    print("4. New assignments log ready...")

allcandies=list(signatures.keys())

print("\nKeys, candies, and signatures loaded. Entering flashing mode.")
print("if mounting gets messy, run the following line to clear out stale mountpoints in /media/\n")
print("    sudo umount /media/sd*; sudo rm /media/sd*/.created_by_pmount; sudo rmdir /media/sd*")
print("\n\nNow, plug in some badges!!\n")

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')
circuitpy="adafruit-circuitpython-seeeduino_xiao_rp2040-en_US-9.1.4.uf2"
rpi_nuke="flash_nuke.uf2"
cpy_nuke="code.py"
gamefiles="../badge/*"

# write the correct id.json file for this badge serial number to the indicated destination
def registerserial(sn,dest):
    # if a new serial, assign the next candy
    if sn not in assignments:
        #todo: handle overflow here - more than the max # of badges seen!
        candyid=allcandies[len(assignments)]
        print(sn+" now assigned to give out "+candyid)
        assignments[sn]=candyid
    else:
        print(sn+" was already assigned "+assignments[sn])

    # always write out to destination
    with open(dest,"w") as f:
        f.write(json.dumps({'name': '', 'candy': assignments[sn], 'signature': signatures[assignments[sn]]}))

    # update our database
    with open("assignments.json", 'w') as f:
        f.write(json.dumps(assignments))

# node is a badge that was just plugged in. Mount it and return mount point.
def mountnode(node):
    subprocess.run("pmount "+node,shell=True)
    cmd='mount | grep '+node+' | cut -d " " -f 3'
    mountpoint=str(subprocess.check_output(cmd,shell=True),'UTF-8').strip()
    #print(node," was mounted at ",mountpoint)
    return mountpoint

# unmount the badge at this mount point
def umountpoint(mountpoint):
    cmd="sync -d "+mountpoint+" && pumount "+mountpoint
    subprocess.run(cmd,shell=True)
    #print(mountpoint, " unmounted - unplug it")

# copy this file from the badge at this mount point to a unique file locally:
def copyfromdevice(file, mountpoint):
    src=mountpoint+"/"+file
    if not os.path.exists(src): return False
    dest=checkdir+"-".join([time.strftime("%Y%m%d-%H%M%S-"),device.get('ID_SERIAL_SHORT'),file])
    #print("copying from ", src, "to", dest)
    cmd="cp -Lr "+src+" "+dest
    subprocess.run(cmd,shell=True)
    if not os.path.exists(dest): return False
    return dest

# copy this file to the badge at this mount point 
def copytodevice(file, mountpoint):
    #print("copying ", file, " to ", mountpoint)
    cmd="cp -Lr "+file+" "+mountpoint+"/ && sync -d "+mountpoint
    subprocess.run(cmd,shell=True)

# copy game files to a badge with circuitpython loaded
def mkcpy(device):
    start=time.time()
    mountpoint=mountnode(device.device_node)

    if mountpoint == "":
        raise Exception("empty mountpoint, would delete your system!!\n")
    sn=0
    sn=device.get('ID_SERIAL_SHORT')
    print(sn)

    # erase the existing filesystem if any
    # a better way might be to copy over code.py with storage.erase_filesystem()
    cmd="rm -rf "+mountpoint+"/*"
    subprocess.run(cmd,shell=True)

    #copy game code to badge
    copytodevice(gamefiles, mountpoint)

    #write the unique id.json to the device
    registerserial(sn,mountpoint+"/id.json")
    
    #clean up and report
    umountpoint(mountpoint)
    print("CPY #"+sn+" took "+str(time.time()-start)+"s")

# copy circuitpython to a blank rpi badge
def mkrpi(device):
    start=time.time()
    mountpoint=mountnode(device.device_node)
    copytodevice(circuitpy,mountpoint)
    umountpoint(mountpoint)
    print("RPI took "+str(time.time()-start)+"s\n")

# wipe flash on a blank rpi badge (which may still have file fragments in flash)
def nukerpi(device):
    start=time.time()
    mountpoint=mountnode(device.device_node)
    copytodevice(rpi_nuke,mountpoint)
    umountpoint(mountpoint)
    print("Nuking RPI took "+str(time.time()-start)+"s\n")

# reboot badge in rpi uf2 mode for nukerpi
def nukecpy(device):
    start=time.time()
    mountpoint=mountnode(device.device_node)
    copytodevice(cpy_nuke,mountpoint)
    umountpoint(mountpoint)
    print("Nuking CPY took "+str(time.time()-start)+"si\n")

def countCandy(filename, verbose=False):

    if verbose: print("Counting candy in "+filename+":")
    unique_signatures = set()
    candy_counter = dict.fromkeys(candies,0)

    #check file exists and open it
    if (filename is False) or (not os.path.exists(filename)):
        return candy_counter
    
    with open(filename,"r") as f:
        badgeCandyData=json.load(f)

    for badgeCandy, badgeSignature in badgeCandyData.items():
        # if this candy's signature matches our record
        if badgeSignature==signatures.get(badgeCandy):
            # Check if the signature is unique and add it to the set if it is
            if badgeSignature in unique_signatures:
                if verbose: print(f"Duplicate signature found for {badgeCandy} and ignored.\n")
            else:
                unique_signatures.add(badgeSignature)
                # Update the candy count
                # Extract the candy name without the increment (e.g., "Sour Patch Kids" instead of "Sour Patch Kids #1")
                candy_name = badgeCandy.rsplit(' ', 1)[0]
                candy_counter[candy_name] += 1
                if verbose: print(f"{badgeCandy} validated. {candy_name} so far: {candy_counter[candy_name]}")
        elif verbose:
            print(f"{badgeCandy} is a counterfeit!")
            badFriend ="somebody"
            if badgeCandy in badgeFriends.values():
                badFriend =list(badgeFriends.keys())[list(badgeFriends.values()).index(badgeCandy)]
            print(badFriend, "gave you counterfeit", badgeCandy)
    return candy_counter


def checkCandy(device):
    print("\n\nBadge attached. Reading:")
    # previous candy count - before we make a new file!
    sn=0
    sn=device.get('ID_SERIAL_SHORT')
    previousfile="0"
    for filename in os.scandir(checkdir):
        #if the filename matches the serial number, and is greater than the last, it's more recent
        if filename.name.find(sn+"-candies.json")>=0 and filename.name > previousfile:
            #print(filename.name,"is newer than", previousfile)
            previousfile=filename.name
    if previousfile != "0": print("Previous file found: "+previousfile)

    # connect, copy, and unmount badge
    mountpoint=mountnode(device.device_node)
    idFile=copyfromdevice("id.json",mountpoint)
    candiesFile=copyfromdevice("candies.json",mountpoint)
    friendsFile=copyfromdevice("friends.json",mountpoint)
    umountpoint(mountpoint)
    
    # Get userame
    badgeName="Candy Collection Summary"
    if (idFile is not False): 
        with open(idFile,"r") as f:        
            badgeId=json.load(f)
            badgeName=badgeId["name"]+"'s "+badgeName

    #count candies
    newCandyCount=countCandy(candiesFile,verbose=True)
    oldCandyCount=countCandy(checkdir+previousfile,verbose=False)

    print("\n\n|---------------------------------------------------------------------------|")
    print('|{:^75s}|'.format(badgeName))
    print("|---------------------------------------------------------------------------|")
    print("|       Candy       | oldcount | newcount | oldpieces | newpieces |  payout |")
    print("|---------------------------------------------------------------------------|")
    for candy in newCandyCount.keys():
        old=oldCandyCount[candy]
        oldPieces=floor(old/exchange_ratio)
        newPieces=floor(old/exchange_ratio)
        new=newCandyCount[candy]
        print(f"| {candy:18}|{old:9} |{new:9} |{oldPieces:10} |{newPieces:10} |{newPieces-oldPieces:8} |")
    print("|---------------------------------------------------------------------------|")


rpicount=0
cpycount=0
nukemode=False
if len(sys.argv)==2 and sys.argv[1] == "nuke":
    nukemode=True
    print("starting in nuke mode!! next device will get wiped!")

checkmode=False
if len(sys.argv)==2 and sys.argv[1] == "check":
    checkmode=True
    print("starting in checkout mode!")


# listen for device actions
for device in iter(monitor.poll, None):
    if device.action == 'add':
        # a device has been plugged in. Get it's name and do something to it
        label=device.get('ID_FS_LABEL')
        if label=="RPI-RP2":
            if nukemode:
                # the badge booted in uf2 mode and we want to nuke it with a uf2 that will zero all of flash
                print("Nuking flash on RPI at",device.device_node,"\n")
                nukerpi(device)
                nukemode=False
                continue
            # the badge is in uf2 mode, and we're just going to fork a thread to flash it with circuitpython
            rpicount+=1
            print("RPI #",str(rpicount),"\n")
            Thread(target=mkrpi, args=(device,)).start()
        if label=="CIRCUITPY":
            if checkmode:
                checkCandy(device)
                print("\nAll done! Ready for another badge\nMake sure it is powered on before it is plugged in or it will not be recognized")
                continue

            if nukemode:
                # badge running circuitpython and we want to reboot it in uf2 mode to nuke
                print("Nuking flash on CPY at",device.device_node,"\n")
                nukecpy(device)
                #need to nuke RP2 after this
                #nukemode=False
                continue
            # a badge running circutpython is plugged in - fork a thread to copy game files over
            cpycount+=1
            print("CPY #",str(cpycount))
            Thread(target=mkcpy, args=(device,)).start()
        if label=="CLEAR":
            # todo: run this on exit!
            # plugging in a usb drive with the volume label "CLEAR" will pumount all pmounted devices
            cmd="ls -lah /media/"
            subprocess.run(cmd,shell=True)
            print("unmounting\n")
            for filename in os.scandir("/media/"):
                if filename.name.startswith("sd"):
                    #umountpoint(filename.path)
                    print(filename.path)
                    subprocess.run(f"sudo umount {filename.path} || sudo rm {filename.path}/.created_by_pmount || sudo rmdir {filename.path}",shell=True)
            subprocess.run(cmd,shell=True)
            #these require sudo
            #subprocess.run("rm /media/sd?1/.created_by_pmount",shell=True)
            #subprocess.run("rmdir /media/sd*",shell=True)
            print("run the following to clear files: \n\n\nsudo rm /media/sd?1/.created_by_pmount\nrmdir /media/sd*")
        if label=="NUKE":
            # plugging in a usb drive with the volume label "NUKE" will completely zero the flash of the next badge found
            nukemode=True
            print("Nuke mode enabled- next badge will get flash wiped first\n")

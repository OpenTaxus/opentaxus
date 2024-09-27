#!/bin/python3
import os
import pyudev
import time
import subprocess
from threading import Thread
import time
import hashlib
import tempfile

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')
circuitpy="adafruit-circuitpython-seeeduino_xiao_rp2040-en_US-9.0.4.uf2"
software="../software/*"
configs="../configs/data/"
variants=50

# Make sure sudo is configured to not prompt for a password for your user.


def mountnode(node, temp_dir):
    subprocess.run("sudo mount -o rw,users,umask=000 --source "+node + " --target " + temp_dir,shell=True)

def umountpoint(mountpoint):
    cmd="sudo sync -d "+mountpoint+" && sudo umount "+mountpoint
    subprocess.run(cmd,shell=True)
    #print(mountpoint, " unmounted - unplug it")

def copytodevice(file, mountpoint):
    #print("copying ", file, " to ", mountpoint)
    cmd="cp -Lr "+file+" "+mountpoint+"/ && sudo sync -d "+mountpoint
    subprocess.run(cmd,shell=True)

def mkcpy(device):
    start=time.time()
    mountpoint = tempfile.TemporaryDirectory()
    mountnode(device.device_node, mountpoint.name)
    if mountpoint.name == "":
        raise Exception("empty mountpoint, would delete your system!!\n")
    sn=device.get('ID_SERIAL_SHORT')
    hash=hashlib.md5(sn.encode('utf-8'))
    num=int.from_bytes(hash.digest(), 'big', signed=False)
    variant = num % variants
    #config=ord(serial[-1])%50
    cmd="rm -rf "+mountpoint.name+"/*"
    subprocess.run(cmd,shell=True)
    copytodevice(configs+str(variant), mountpoint.name+"data/")
    copytodevice(software, mountpoint.name)
    umountpoint(mountpoint.name)
    print("CPY #"+sn+" config #",variant," took "+str(time.time()-start)+"s\n")

def mkrpi(device):
    start=time.time()
    mountpoint = tempfile.TemporaryDirectory()
    mountnode(device.device_node, mountpoint.name)
    copytodevice(circuitpy,mountpoint.name)
    umountpoint(mountpoint.name)
    print("RPI took "+str(time.time()-start)+"s\n")

def nukerpi(device):
    start=time.time()
    mountpoint = tempfile.TemporaryDirectory()
    mountnode(device.device_node, mountpoint.name)
    copytodevice("flash_nuke.uf2",mountpoint.name)
    umountpoint(mountpoint.name)
    print("Nuking RPI took "+str(time.time()-start)+"s\n")

def nukecpy(device):
    start=time.time()
    mountpoint = tempfile.TemporaryDirectory()
    mountnode(device.device_node, mountpoint.name)
    copytodevice("code.py",mountpoint.name)
    umountpoint(mountpoint.name)
    print("Nuking CPY took "+str(time.time()-start)+"si\n")


rpicount=0
cpycount=0
nukemode=False

for device in iter(monitor.poll, None):
    if device.action == 'add':
        label=device.get('ID_FS_LABEL')
        if label=="RPI-RP2":
            if nukemode: 
                print("Nuking flash on RPI at",device.device_node,"\n")
                nukerpi(device)
                nukemode=False
                continue
            rpicount+=1
            print("RPI #",str(rpicount),"\n")
            Thread(target=mkrpi, args=(device,)).start()
        if label=="CIRCUITPY":
            if nukemode: 
                print("Nuking flash on CPY at",device.device_node,"\n")
                nukecpy(device)
                #need to nuke RP2 after this
                #nukemode=False
                continue
            cpycount+=1
            print("CPY #",str(cpycount),"\n")
            Thread(target=mkcpy, args=(device,)).start()
        if label=="CLEAR":
            cmd="ls -lah /media/"
            subprocess.run(cmd,shell=True)
            print("unmounting\n")
            for filename in os.scandir("/media/"):
                umountpoint(filename.path)
                print(filename)
            subprocess.run(cmd,shell=True)
        if label=="NUKE":
            nukemode=True
            print("Nuke mode enabled- next badge will get flash wiped first\n")


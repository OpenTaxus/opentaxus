#!/bin/bash

#script to check if badge has solved all games
#looks for a badge with game0.csv. when a badge is automounted,
#it checks the hash of all the collected clues so it knows you have them.

mountpoint=/media/`whoami`/CIRCUITPY

while :
do
	echo "plug a badge in"
	while [ ! -f "$mountpoint/data/game0.csv" ]
	do
		sleep 1
	done
	
	hash=`grep ",0,$" $mountpoint/data/game* | sort | cut -d : -f 2 | md5sum | cut -f 1 -d " " `
	name=`cat $mountpoint/data/myname.txt`
	if [[ $hash == "b30985cd9eedc8a2f1d24b769d40b5d2" ]]
	then
		echo $name solved it!
	else
		echo $name "hasn't solved it yet"
	fi
	while [ -f "$mountpoint/data/game0.csv" ]
	do
		sleep 1
	done
done

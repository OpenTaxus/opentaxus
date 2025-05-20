# Trick or Treat Game 

| [Readme](/) | [The Attribution Game](/attribution) | [Trick or Treat Game](/trickortreat) | [Badge Hardware](/hardware) |
| ----------- | ------------------------------------ | ------------------------------------ | --------------------------- |

## Game Overview

In the Trick or Treat game, you get to meet people, trade digital candy, and potentially trade in your digital candy for the real thing.

The OpenTaxus Badge is designed for playing the Attribution Game.
Similar to the board game Clue or some versions of Carmen Sandiego,
you need to figure out who the threat actor, attack tool, and victim
are for each round of the game. You do this by trading cards (or
'clues') as well as your self-entered alibi name with others
at the conference.

## Game Basics

When you first power on your badge, you need to set your handle. This can be any string - your name, email, handle, ICQ number, etc. This will be shared with everyone you interact with. You'll be able to see a list of all the people you interacted with at the conference, too.

You'll be randomly assigned a candy type. You have an unlimited supply of this kind of candy - you can give it freely to everyone you meet and trade with.

When you trade, you'll give the other person your handle and candy type. They'll send the same information back to you. Both of your badges will record this.

On your badge, you can see both your candy inventory, and the list of friends you made along the way.

Once you have collected enough of one type of candy, you can trade it in for the real thing!


## Navigation

There is a 5-way d-pad in the middle of the badge. In general:

- < and > switch between info screens
- ^ and v highlight something
- x (press) to select something

The screens you can navigte between with < and > are:
1. Home Screen where you'll start out:
   - ^ to trade candy
   - x to hear from our sponsors
   - v to turn off your badge
1. Inventory Screen where you can see what candy you have:
   - ^ and v to browse
   - x to see details, and to redeem for the real thing
1. Contacts Screen where you see all your friends:
   - ^ and v to browse
   - x to see what candy they gave you
1. Settings Screen where you can change badge stuff:
   - ^ and v to browse
   - x to change the setting. Some will pop up new screens

## Example Gameplay

1. Set up your badge
   - Start your badge by sliding the power switch to the right. 
   - If you haven't already, enter a handle. Use ^v<> to highlight letters and x to select. 
   - Delete and Done buttons are at the bottom.
   - press x or V to page through a short intro and take you to the home screen.
   - keep pressing x to see details about event sponsors.
1. Trade Candy!
   - Find a person to trade with. 
   - Make smalltalk with them until you have the confidence to ask them for candy.
   - Line your badges up.
   - From the home screen, both of you press '^', one after the other
   - Candy should be traded both ways.
   - If it fails or there's an error, try again
   - Note: Duplicate candies from the same person don't count!
1. See what you've got or configure your badge:
   - Press < or > to navigate to the candy, friend, or setting screen
   - Press ^ or v to scroll through the list of candies/friends/settings
   - Press x to see details
1. Cash out! 
   - Go to the badge prize table
   - Press < or > to navigate to the candy screen
   - Press ^ or v to scroll through the list of candies
   - Press x to see details
   - Line up your badge with the candy validator
   - When told, press ^ to verify your candy earnings
   - Note: There may be a limit to the number of prizes per person
1. HACK!
   - Plug your badge in with a USB cable
   - Your computer should see a read-only USB drive full of python code, and a serial port to connect to the python console
   - Learn about [circuitpython](https://learn.adafruit.com/welcome-to-circuitpython/overview)
   - Read some code to see how it works
   - If you'd like to modify the code on your badge, unplug it and slide the power switch left to the off/usb mode, then plug it back in. The usb drive will now be read/write.

## Repo Contents

* the /trickortreat/ part of the repo is forked from the /attribution/ used for BSidesSF 2024 and developed for BSidesPDX 2024.
* /trickortreat/controller/ contains all the code run on a desktop. This includes generating game files and flashing the badges.
* /trickortreat/badge/ contains the contents of the badge USB storage device, minus the badge-specific parts generated from the controller.

## Event Badge Designer Instructions

To use this game as-is:
1. change necessary strings in controller/strings.py
1. run controller/genfiles.py to generate all the keys and badge-specific files
1. run controller/flash.py to wait for a badge to be attached, then flash it

### Suggested customizations:
	
#### Physical Appearance:
* Add custom artwork such as your logo to the badges KiCad files (found in the [hardware](/hardware) folder). 
* Add in the name of the artist and contributors to the silkscreen.
* Include the repo for your code or events in the silkscreen on the back of the badge.

#### Electronic text:
* With only string changes you can change this from halloween-themed trick-or-treating to any theme and 
* as soon as this is complete, all the easily changed strings will be in /controller/strings.py Right now they're scattered in the code:
  * There are a number of custom strings that can be adjusted within the [genfiles.py](./configs/genfiles.py) file. In particular, you may want to change line 121 to say the name of your event or organization instead of "A mysterious group".
  * The same file also includes other bits of flavor text that could be customized to match your event's theme or location.
  * Changing the menu text of the badge to show your event name instead of "OpenTaxus" can be done on lines 23 and 139 of [home.py](./software/home.py)
  * Sponsor names can be added within [home.py](./software/home.py) around line 144.

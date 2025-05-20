# OpenTaxus 

| [Readme](/) | [The Attribution Game](/attribution) | [Trick or Treat Game](/trickortreat) | [Badge Hardware](/hardware) |
| ----------- | ------------------------------------ | ------------------------------------ | --------------------------- |

Opentaxus is a permissively licensed set of hardware, software, and tooling to help as a starting point for customized conference badges.

## Motivation
Electronic conference badges are a well appreciated feature of an event, but very quickly become large, complicated projects. Typically there's custom hardware, custom embedded software, and sometimes much more. Every one of thos parts has the potential for schedule delays or causing the whole project to fail. Meanwhile, there's almost always a very hard deadline.

OpenTaxus is intended to get you started with a working system, allowing you to customize only as much as you want to or have time to. You are encouranged to use any or all of the parts of OpenTaxus for your own project

## Badge Games

There are currently two games for OpenTaxus. Each is in it's own subdirectory. Right now you'll just pick one (or make a new one) for your conference badge:

### [The Attribution Game](/attribution)

Similar to the board game Clue or some versions of Carmen Sandiego,
you need to figure out who the threat actor, attack tool, and victim
are for each round of the game. You do this by trading cards (or
'clues') as well as your self-entered alibi name with others
at the conference.

The Attribution Game was designed for [LABScon 2023](https://www.labscon.io/) and then revised and improved for [BSidesSF 2024](https://bsidessf.org/)

### [Trick or Treat Game](/trickortreat) 

In this game, you Trick-or-Treat, trading virtual candy with other conference attendees. Once you have collected enough, you can cash out your virtual candy for real candy or prizes.

The Trick or Treat Game was designed for [BSidesPDX 2024](https://bsidespdx.org/)

## Repo Contents

This repository contains the hardware and software for the badge and multiple games. We hope it is useful for those who wish to hack the badges and game, anyone who wants to use the badge to learn some circuitpython, as well as others who might like to reuse some or all of it for other projects.

The badge hardware was designed and produced by @securityfitz, with variants being used for BSidesSF 2024 and Labscon.
The badge software is a fork of the Labscon badge software, further mangled by @rlc4, @lanrat, and @securelyfitz, and then further forked and mangled by *

## Event Badge Designer Instructions

OpenTaxus is intended to be be a drop-in electronic badge that works from the start. While you can use the badge as it's presented here if you plan to use it for an event or organization, you may want to customize the appearance of the badge, and possibly some of the text and programming. 

### Suggested customizations:
	
#### Physical Appearance:
* Add custom artwork such as your logo to the badges KiCad files (found in the [hardware](/hardware) folder). 
* Add in the name of the artist and contributors to the silkscreen.
* Include the repo for your code or events in the silkscreen on the back of the badge.

#### Electronic text:
* The Attribution Game has a number of custom strings that can be adjusted within the [genfiles.py](./attribution/configs/genfiles.py) file. In particular, you may want to change line 121 to say the name of your event or organization instead of "A mysterious group".
* The same file also includes other bits of flavor text that could be customized to match your event's theme or location.
* Changing the menu text of the badge to show your event name instead of "OpenTaxus" can be done on lines 23 and 139 of [home.py](./attribution/software/home.py)
* Sponsor names can be added within [home.py](./attribution/software/home.py) around line 144.

#### Misc:
* You may also want to change the file that you're reading now ([README.md](README.md)) to welcome your attendee's, ctf players, etc.

# The Attribution Game 

| [Readme](/) | [The Attribution Game](/attribution) | [Trick or Treat Game](/trickortreat) | [Badge Hardware](/hardware) |
| ----------- | ------------------------------------ | ------------------------------------ | --------------------------- |

## Badge Game

Similar to the board game Clue or some versions of Carmen Sandiego,
you need to figure out who the threat actor, attack tool, and victim
are for each round of the game. You do this by trading cards (or
'clues') as well as your self-entered alibi name with others
at the conference.

## Attribution Game basics

In order to play in the Attribution Game, you will need to enter a name or handle when you first turn on your badge. This will stay through power cycles. It can be cleared in your settings which will force you to enter a new one.

To trade cards with someone, scroll left or right until you get to the "OpenTaxus" screen.
Once there, press the toggle up, and place your badge edge at the top of the screen against
the same badge edge of the person you are trading with. You should see once your card has
been transmitted and you have received a card from them.

You can check your collected cards by scrolling right from the "OpenTaxus" screen.

When you collect enough cards, the one remaining is the solution that completes the phrase. There are 6 games to play through - try them all!

Please see [Using the Badge](/attribution/GAME.md) for more details about interacting with the badge and [Playing the Game](/attribution/GAME.md) for more details about gameplay.

## Repo Contents

This repository contains the hardware and software for
the badge and game. We hope it is useful for those who wish to hack
the badges and game, anyone who wants to use the badge to learn some
circuitpython, as well as others who might like to reuse some or all
of it for other projects.

The badge hardware was designed and produced by @securityfitz, with variants being used for BSidesSF 2024 and Labscon.
The badge software is a fork of the Labscon badge software, further mangled by @rlc4, @lanrat, and @securelyfitz.

## Event Badge Designer Instructions

OpenTaxus is intended to be be a drop-in electronic badge that works from the start. While you can use the badge as it's presented here if you plan to use it for an event or organization, you may want to customize the appearance of the badge, and possibly some of the text and programming. 

Please see [Developer Instrucitons](/attribution/DEVELOP.md) for more details

### Suggested customizations:
	
#### Physical Appearance:
* Add custom artwork such as your logo to the badges KiCad files (found in the [hardware](/hardware) folder). 
*  Add in the name of the artist and contributors to the silkscreen.
* Include the repo for your code or events in the silkscreen on the back of the badge.

#### Electronic text:
* There are a number of custom strings that can be adjusted within the [genfiles.py](./configs/genfiles.py) file. In particular, you may want to change line 121 to say the name of your event or organization instead of "A mysterious group".
* The same file also includes other bits of flavor text that could be customized to match your event's theme or location.
* Changing the menu text of the badge to show your event name instead of "OpenTaxus" can be done on lines 23 and 139 of [home.py](./software/home.py)
* Sponsor names can be added within [home.py](./software/home.py) around line 144.

#### Misc:
* You may also want to change the file that you're reading now ([README.md](README.md)) to welcome your attendee's, ctf players, etc.

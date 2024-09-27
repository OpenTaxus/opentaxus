# Using the Badge

| [Readme](/) | [The Attribution Game](/attribution) | [Trick or Treat Game](/trickortreat) | [Badge Hardware](/hardware) |
| ----------- | ------------------------------------ | ------------------------------------ | --------------------------- |


## Setup

When you first power on your badge it will give you a brief intro to
the badge and the game, then it will ask you for your contact info.
This could be a handle, email address, or any other string that will
be shared with everyone you interact with. Use the up and down but
tons to choose letters, left and right to move through the string,
and press the button to set your name. (it can be changed later)

## Navigating

- Left and Right switches between:
  - Home page
  - Alibis page, which shows all the people you've traded contact info and clues with
  - Clues page, which shows all the cards you've collected so far
  - Settings, which allow you to change badge features
- Up takes you to trade mode, described below
- Down puts the badge to sleep, which also happens automatically after a few
   seconds
- Pressing the center button usually gives you more details about whatever you're highlighting.

### Trading

Your badge has an infrared transceiver. Press the 'up' button to enter trade mode.
The badge will:

- transmit your clue as well as your contact information
- listen to receive someone elses card and contact info
- verify the cryptographic signature on the clue
- tell you the result of the trade.
  After the trade, you should be able to see the information in your Contacts an
  Cards pages.

### Winning

The real prize isn't attribution but the contacts and friends we made along the way.
If you happen to have collected enough info to attribute the attack, your badge will
tell you. Find a game organizer to validate your win.

### Multiple rounds

The first round of the game will be pretty easy with only a few trades needed to
attribute. Once a game is complete, the game controller will transmit a packet to
advance the game to the next round, which will propagate to everyone when they
trade clues. Each round will have a different set of cards/clues and a different
attack to attribute.

## After the conference

This badge can work as a simple circuitpython learning platform. The best source
of information about circuitpython is available on Adafruit, including a [Welcome
to CircuitPython guide](https://learn.adafruit.com/welcome-to-circuitpython/overview)

The best place to start tinkering is probably with some neat light animations on
the RGB LED on the badge. Adafruit
[has an example](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Welcome_to_CircuitPython/code.py)
on how to use this RGB LEDs.

For working interactively with a python CLI, plug your badge in with a USB cable,
and connect to the serial port that shows up.

For writing your own circuitpython programs, you need to modify the code.py
file you can find on the drive that shows up when you plug in the USB cable.
Every time you save the file, the board will reset and start running your code.

If you've somehow messed up your badge, you can follow the process below to
flash a fresh copy of circuitpython and/or the game code.

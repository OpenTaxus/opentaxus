# Hardware

| [Readme](/) | [The Attribution Game](/attribution) | [Trick or Treat Game](/trickortreat) | [Badge Hardware](/hardware) |
| ----------- | ------------------------------------ | ------------------------------------ | --------------------------- |

`/hardware/` contains the kicad board design files and full details about
design and manufacturing. The hardware on the badge includes:

-  Raspberry Pi 2040, derived from the seeed xiao 2040
-  16MB spi flash for code and files
-  128x64 OLED display with SH1106 or SSD1309 controller over I2C
-  IR LED and Phototransistor used directly on UART.
-  5-way d-pad for input
-  2 neopixel LEDs
-  AA battery plus boost voltage converter
-  USB-C connector plus vreg for usb power
-  power switch to switch between USB and Battery power
-  test points for reset, boot, and swd

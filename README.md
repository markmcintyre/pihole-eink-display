# Simple Pi-hole Stats Display

![Alt text](images/pihole-eink-display.jpg?raw=true "Photo of Pi-hole eInk Display")

This Python script outputs Pi-hole statistics on a 2.7" e-ink display, and updates it periodically.

Note: This is just a statistics display script, not the actual DNS Sinkhole. If you're looking to set up a DNS sinkhole, check out the [Pi-hole project page](https://pi-hole.net), totally unaffiliated with this script.

The display I use is from [WaveShare](https://www.waveshare.com), and this script uses [their library](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT). (Instructions on how to install their library can be found in the previous link.)

## Configuring the script

There are three variables to customize, which are near the top of ``main.py``.

PIHOLE_IP
   : The IP address of your Pi-hole instances. (Use ``localhost`` if it's running on the same Pi as the PiHole).

API_TOKEN
   : The API Token of your Pi-hole instance. This can be found in the settings screen of the Pi-hole admin interface. Click on the API tab and then click the Show API Key button.

DISPLAY_TITLE
   : A title to display at the top of your stats. Customize it to your liking!

REFRESH_MINUTES
   : The number of minutes between refreshes. I use five minutes.

## Fonts

The fonts folder includes the open-source [Roboto](https://github.com/googlefonts/roboto) font family.

Enjoy! 👍
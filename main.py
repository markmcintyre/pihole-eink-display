#!/usr/bin/python3
# -*- coding:utf-8 -*-

import epd2in7
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
import json
import urllib.request
from threading import Timer
import os

# CUSTOM VARIABLES
PIHOLE_IP = 'pihole.local'
DISPLAY_TITLE = 'PiHole Statistics'
REFRESH_MINUTES = 5

# Get our path
dirname = os.path.dirname(__file__)

# Prepare some fonts and images
blackHoleImage = Image.open(os.path.join(dirname, 'images/black-hole.png'))
smallBlackHoleImage = blackHoleImage.resize((32, 27))
titleFont = ImageFont.truetype(os.path.join(dirname, 'fonts/Roboto-Bold.ttf'), 22)
font = ImageFont.truetype(os.path.join(dirname, 'fonts/Roboto-Thin.ttf'), 16)
metricFont = ImageFont.truetype(os.path.join(dirname, 'fonts/Roboto-Regular.ttf'), 32)
descriptionFont = ImageFont.truetype(os.path.join(dirname, 'fonts/Roboto-Thin.ttf'), 14)

def renderData(canvas, data):

    # Elements
    draw = ImageDraw.Draw(canvas)
    today = datetime.date.today()
    width = canvas.width
    height = canvas.height

    # Display our header, with black hole icon and the date
    canvas.paste(smallBlackHoleImage, (8, 16))
    draw.text((50, 7), DISPLAY_TITLE, font = titleFont, fill = 0)
    draw.text((50, 32), '{:%A, %B %-d}'.format(today), font = font, fill = 0)
    draw.line((0, 60, width, 60), fill = 0, width = 3)

    # Display our grid
    draw.line((width / 2, 60, width / 2, height))
    draw.line((0, ((height - 60) / 2) + 60, width, ((height - 60) / 2) + 60))

    # Display the number of ads blocked
    draw.text((5, 63), '{:,}'.format(data['ads_blocked_today']), font = metricFont)
    draw.text((5, 98), 'Ads blocked today', font = descriptionFont)

    # Display number of queries
    draw.text((width / 2 + 10, 63), '{:,}'.format(data['dns_queries_today']), font = metricFont)
    draw.text((width / 2 + 10, 98), 'DNS queries today', font = descriptionFont)

    # Display the percentage of ads
    draw.text((5, ((height - 60) / 2) + 63), '{:.2f}%'.format(data['ads_percentage_today']), font = metricFont)
    draw.text((5, ((height - 60) / 2) + 98), 'Ad percentage', font = descriptionFont)

    # Display devices protected
    draw.text(((width / 2 + 10), ((height - 60) / 2 + 63)), '{0:d}'.format(data['unique_clients']), font = metricFont)
    draw.text(((width / 2 + 10), ((height - 60) / 2 + 98)), 'Devices protected', font = descriptionFont)

try:

    # Update every x minutes
    interval = REFRESH_MINUTES * 60

    # Initialize our ePaper Display
    epd = epd2in7.EPD()
    
    # Prepare our canvas
    width = epd2in7.EPD_HEIGHT
    height = epd2in7.EPD_WIDTH
    
    # Define our main loop function
    def loop():

        # Initialize the ePaper display
        epd.init()
        epd.Clear(0xFF)

        # (Re-)create our canvas
        canvas = Image.new('1', (width, height), 255)

        try:
            # Get our ad blocker data
            response = urllib.request.urlopen(f'http://{PIHOLE_IP}/admin/api.php')
            data = json.loads(response.read().decode())

            # Render the data
            renderData(canvas, data)
            epd.display(epd.getbuffer(canvas))

        except urllib.request.URLError as err:
            print('Could not get API data.')

        # Put our display to sleep
        epd.sleep()

        # Do it again at the next interval
        Timer(interval, loop).start()

    loop()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()


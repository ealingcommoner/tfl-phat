## A script to display live bus arrivals on Pimoroni InkyPhat for raspberry pi. Adapts london-bus-arrivals code from M24murray
##Kudos to gadgetoid and davidxbuck for fixing code #ealingcommoner
#import inky libraries
from inky import InkyPHAT

inky_display = InkyPHAT("black")

inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne

font = ImageFont.truetype(FredokaOne, 15)
##import python libraries for code cloned from github.com/m24murray/london-bus-arrivals
import os, requests
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv('.env')
app_id = os.getenv('api id') #register at Tfl api for these
app_key = os.getenv('api key')
stop_id = os.getenv('STOPID') #use long code eg490006192N

##draw grid for inkyphat display
draw.line((1, 34, 212, 34), 1)       # Vertical line
draw.line((1, 68, 212, 68), 1)      # Horizontal top line
draw.line((1, 102, 212, 102), 1)      # Horizontal middle line

#obtain bus arrival info from tfl api (also from m24murray)
url = 'https://api.tfl.gov.uk/StopPoint/490006192S/arrivals' #replace with chosen stop code
params = {'app_id': app_id, 'app_key': app_key}

r = requests.get(url, params=params)
buses = r.json()

sorted_buses = []
for b in buses:
    sorted_buses.append({'bus': b[u'lineName'], 'destinationName': b[u'destinationName'], 'arrival': datetime.strptime(b[u'timeToLive'], '%Y-%m-%dT%H:%M:%S%fZ')})

sorted_buses = sorted(sorted_buses, key=lambda k: k['arrival'])
##truncate sorted buses to just next three arrivals
sorted_busestrun = sorted_buses[0:3]
#print(sorted_busestrun) #unhash to see full string

#uncomment to output to console, do not use if using crontab without mailer
#for ix, bus in enumerate(sorted_busestrun, 1):

#    time = (bus['arrival'] - datetime.now()).seconds / 60
#   if time < 1:
#       disptime = "Due"
#   elif time < 2:
#       disptime = "1 Min"
#   else:
#       disptime = "{} Mins".format(int(time))
#   dest = bus['destinationName'].split(',')[0]
#   print("{} {}: {}".format(bus['bus'], dest, disptime))

#draws output to phat 
for ix, bus in enumerate(sorted_busestrun, 1):

    time = (bus['arrival'] - datetime.now()).seconds / 60
    if time < 1:
        disptime = "Due"
    elif time < 2:
        disptime = "1 Min"
    else:
        disptime = "{} Mins".format(int(time))
    dest = bus['destinationName'].split(',')[0]

    draw.text((1, ix*34-33), " {}  {}".format(bus['bus'], dest), inky_display.BLACK, font=font)
    draw.text((160, ix*34-33), disptime, inky_display.BLACK, font=font) 

#output image to inkyphat
inky_display.set_image(img)
inky_display.show()


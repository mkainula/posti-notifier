import urllib2
import smtplib
import hashlib
import time
import sys
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser

if len(sys.argv) <= 1:
  print "Usage: python posti_notifier.py <tracking code>"
  sys.exit(0)

parser = SafeConfigParser()
parser.read("config.ini")

# Get tracking code from parameters
trackingCode = sys.argv[1]
timeToSleep = 300

# Open requested url
url = "http://www.posti.fi/itemtracking/posti/search_by_shipment_id?lang=fi&ShipmentId=" + trackingCode
data = urllib2.urlopen(url)
html = data.read()
soup = BeautifulSoup(html)
details_old = soup.find_all("div", {"id": "shipment-event-table-cell"})

# Main loop
while True:
  data = urllib2.urlopen(url)
  html = data.read()
  soup = BeautifulSoup(html)
  details = soup.find_all("div", {"id": "shipment-event-table-cell"})

  if(details != details_old):
    print "Found a change, mailing"

    # Construct the message
    status = ""
    for event in details:
      status = status + "\n" + event.get_text() + "\n --------- \n"

    # Initialize SMTP
    server = smtplib.SMTP(parser.get('email', 'server'))
    username = parser.get('email', 'username')
    password = parser.get('email', 'password')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    recipient = parser.get('email', 'recipient')
    sender = 'posti_notifier@kapsi.fi'
    message = 'From: "posti-notifier" <%s> \nTo: %s\nSubject: New status for package %s\n\n %s' % (sender, recipient, trackingCode, status.encode('utf-8'))

    # Send message
    server.sendmail(sender,recipient,message);

    # Disconnect
    server.quit()
    details_old = details

  # Sleep and fade away
  print "Sleeping for %d seconds" % (timeToSleep)
  time.sleep(timeToSleep)


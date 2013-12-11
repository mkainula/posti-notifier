posti-notifier
==============

A simple python script that periodically checks the Itella / Posti tracking site for changes in the package status. When the script detects a new event, it automatically emails you the list of the latest events.

## Tech stack ##

* Python
* BeautifulSoup

## Running ##

Insert your SMTP settings (tested with Gmail) and recipient to config.ini and then run the script using

    python posti-notifier.py <tracking_code>

## TODO ##

* More configuration options (language, email related configurations)
* Daemonization / launching of a background process

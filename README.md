# Log Parser

This is a parser for log files

## Installation

python3 -m pip install --user -U virtualenv

python3 -m virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

Change settings in .env file

alembic upgrade head

You can also use Dockerfile to create an image


## Usage

Example:

python3 app.py -f access1.log access2.log -o output.json -op most-frequent-ip

-f - The list of input files
-o - The name of output .json file
-op - Operation

The list of available operations:

most-frequent-ip

less-frequent-ip

calc-events

total-amount-ex

## Note

Use https://www.secrepo.com/squid/access.log.gz as input data
You can copy the part of it to the another file and use as the input file

The format of input data:

Field 1: 1157689324.156 [Timestamp in seconds since the epoch]

Field 2: 1372 [Response header size in bytes]

Field 3: 10.105.21.199 [Client IP address]

Field 4: TCP_MISS/200 [HTTP response code]

Field 5: 399 [Response size in bytes]

Field 6: GET [HTTP request method]

Field 7: http://www.google-analytics.com/__utm.gif? [URL]

Field 8: badeyek [Username]

Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address] Field 10: image/gif [Response type]

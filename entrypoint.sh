#!/bin/sh

sleep 2
python app.py -f access.log -o output.json -op most-frequent-ip

exec "$@"
#!/usr/bin/env bash

cd /home/pi/bots/ea_api/
git pull
/home/pi/.virtualenvs/ea/bin/python update-data.py 2852TH-level-stage-i-15_min-mASD /home/pi/bots/ea_api/data/
/home/pi/.virtualenvs/ea/bin/python update-data.py 2859TH-level-downstage-i-15_min-mASD /home/pi/bots/ea_api/data/
/home/pi/.virtualenvs/ea/bin/python update-data.py 2859TH-level-stage-i-15_min-mASD /home/pi/bots/ea_api/data/
/home/pi/.virtualenvs/ea/bin/python update-data.py 278744TP-rainfall-tipping_bucket_raingauge-t-15_min-mm /home/pi/bots/ea_api/data/

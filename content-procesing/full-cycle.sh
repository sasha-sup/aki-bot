#!/bin/bash
cd /opt/akibot/content-procesing
python3 1-logo-on-pic.py
./2-logo-on-video.sh
./3-video-resizer.sh

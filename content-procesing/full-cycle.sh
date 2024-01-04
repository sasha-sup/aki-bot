#!/bin/bash
cd /opt/akibot/content-procesing
chmod +x *.sh
yandex-disk sync
sleep 120
yandex-disk stop
python3 1-logo-on-pic.py
sleep 10
./2-logo-on-video.sh
./3-video-resizer.sh

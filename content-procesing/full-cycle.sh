#!/bin/bash

scripts=(
    "0-sort-content.sh"
    "1-logo-on-pic.py"
    "2-logo-on-video.sh"
    "3-video-resizer.sh"
)


for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "Running: $script"
        bash "$script"
        echo "$script done"
        # TODO: orig files cleaner
    fi
done
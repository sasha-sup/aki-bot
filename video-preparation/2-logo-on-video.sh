#!/bin/bash

LOGO_PATH="/root/Yandex.Disk/content/logo/akibot-logo1.png"
INPUT_DIR="/root/Yandex.Disk/content/unsorted"

for video_file in "$INPUT_DIR"/*; do
    if [ -f "$video_file" ]; then
        file_name=$(basename "$video_file")
        # Check if the file name starts with "w-logo"
        if [[ ! "$file_name" =~ ^w-logo.* ]]; then
            output_video="$INPUT_DIR/w-logo_$file_name"
            ffmpeg -i "$video_file" -i "$LOGO_PATH" -filter_complex "[1:v]scale=iw*0.5:ih*0.5 [logo]; [0:v][logo]overlay=W-w-10:H-h-10[out]" -map "[out]" -map 0:a -c:a copy "$output_video"
            rm $video_file
            sleep 10
        else
            echo "Skipping file: $video_file (already has 'w-logo' prefix)"
        fi
    fi
done

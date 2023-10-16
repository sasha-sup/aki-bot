#!/bin/bash

LOGO_PATH="/root/Yandex.Disk/content/logo/akibot-logo.png"
INPUT_DIR="/root/Yandex.Disk/content/video"


if [ -f "$output_file" ]; then
    echo "Skip: $video_file"
    else
for video_file in "$INPUT_DIR"*; do
    output_video="$INPUT_DIR/w-logo_$(basename "$video_file")"
    ffmpeg -i "$video_file" -i "$LOGO_PATH" -filter_complex "[0:v][1:v]overlay=W-w-10:H-h-10[out]" -map "[out]" -map 0:a -c:a copy "$output_video"
    # TODO: logs
done
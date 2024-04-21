#!/bin/bash

set -o pipefail

LOGO_PATH="/root/Yandex.Disk/content/logo/akibot-logo1.png"
INPUT_DIR="/root/Yandex.Disk/content/unsorted"
OUTPUT_DIR="/root/Yandex.Disk/content/video"
MAX_FILE_SIZE=$((45 * 1024 * 1024)) # in bytes
LOKI_URL="http://145.14.158.1:3100/loki/api/v1/push"

log() {
    local message="$1"
    local timestamp
    timestamp=$(date +"%Y-%m-%dT%H:%M:%S.%3NZ")
    echo "{\"timestamp\":\"$timestamp\", \"message\":\"$message\"}" | curl -XPOST -H "Content-Type: application/json" --data-binary @- "$LOKI_URL"
}

for video_file in "$INPUT_DIR"/*; do
    if [ ! -f "$video_file" ]; then
        continue
    fi
    
    file_name=$(basename "$video_file")
    output_file="$OUTPUT_DIR/resized_w-logo_$file_name"

    if [[ "$file_name" =~ ^w-logo.* ]]; then
        log "Skipping file: $video_file (already has 'w-logo' prefix)"
        continue
    fi

    current_size=$(stat --format=%s "$video_file")
    if [ "$current_size" -le "$MAX_FILE_SIZE" ]; then
        log "Skipped file: $video_file (size already meets the condition)"
        continue
    fi

    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video_file")
    target_bitrate=$(python3 -c "print(int($MAX_FILE_SIZE * 8 / ($duration * 1024)))")

    log "Processing file: $video_file"
    ffmpeg -i "$video_file" -i "$LOGO_PATH" -filter_complex "[1:v]scale=iw*0.5:ih*0.5 [logo]; [0:v][logo]overlay=W-w-10:H-h-10[out]" -map "[out]" -map 0:a -b:v "$target_bitrate"k -preset medium -vf "scale=1280:-1" "$output_file"

    rm "$video_file"
    sleep 10
done

log "Video execution completed"

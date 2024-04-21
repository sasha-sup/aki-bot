#!/bin/bash

set -o pipefail

ENV_PATH="/opt/monitor-me/.env"

if [[ -f $ENV_PATH ]]; then
    source $ENV_PATH
else
    echo "Where is env?"
    exit 1
fi

INPUT_DIR="/root/Yandex.Disk/content/video"
MAX_FILE_SIZE=$((45 * 1024 * 1024)) # in bytes
LOG_FILE="/var/log/aki_bot_video_check.log"

send_telegram_message() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=$message"
}

log_message() {
    local message="$1"
    echo "$message" >> "$LOG_FILE"
}

remove_duplicate_log_entries() {
    awk '!seen[$0]++' "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
}


message="🦊 Aki Bot bad size videos:"

for video_file in "$INPUT_DIR"/*; do
    if [ ! -f "$video_file" ]; then
        continue
    fi
    file_name=$(basename "$video_file")
    current_size=$(stat --format=%s "$video_file")
    file_size_mb=$((current_size / 1024 / 1024)) # in megabytes
    if [ "$current_size" -gt "$MAX_FILE_SIZE" ]; then
        message="$message
📦 $file_size_mb MB 🎞 $file_name:"
        log_message "$message"
    fi
done

send_telegram_message "$message"
remove_duplicate_log_entries

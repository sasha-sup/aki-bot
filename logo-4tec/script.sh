#!/bin/bash

if [ -f /opt/akibot/logo-4tec/.env ]; then
    source /opt/akibot/logo-4tec/.env
fi

log_file="/var/log/akibot/main.log"
message=""

error_lines=$(grep "Error with .*: HTTP Client says - Request Entity Too Large" "$log_file" | awk -F 'Error with |: HTTP Client says - Request Entity Too Large' '{print $2}')

send_telegram_message() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=$message"
}

if [ -n "$error_lines" ]; then
    message+="🎥 Bad video:
$error_lines"
    send_telegram_message "$message"
fi



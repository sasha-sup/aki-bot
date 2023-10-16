#!/bin/bash


INPUT_DIR='/root/Yandex.Disk/content/video'

max_file_size=$((45 * 1024 * 1024)) # in bytes

for video_file in "$INPUT_DIR"/*; do
    output_file="$OUTPUT_DIR/resized_$(basename "$video_file")"
    current_size=$(stat --format=%s "$video_file")
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video_file")
    if [ "$current_size" -le "$max_file_size" ]; then
        echo "Skipped file: $video_file (size already meets the condition)"
        continue
    fi
    target_bitrate=$(python -c "print(int($max_file_size * 8 / ($duration * 1024)))")
    ffmpeg -i "$video_file" -b:v "$target_bitrate"k -preset medium -vf "scale=1280:-1" "$output_file"
    new_size=$(stat --format=%s "$output_file")
    # TODO: logs
done

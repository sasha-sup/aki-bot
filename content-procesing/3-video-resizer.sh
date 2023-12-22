#!/bin/bash

renamer() {
    files=("$OUTPUT_DIR"/*)
    filtered_files=()
    max_number=0

    for file in "${files[@]}"; do
        if [[ -f "$file" && $(basename "$file") =~ ^w-logo_ ]]; then
            filtered_files+=("$file")
            current_number=$(basename "$file" | awk -F'_' '{print $2}' | awk -F'.' '{print $1}')
            if [ "$current_number" -gt "$max_number" ]; then
                max_number="$current_number"
            fi
        fi
    done
}

INPUT_DIR='/root/Yandex.Disk/content/unsorted'
OUTPUT_DIR="/root/Yandex.Disk/content/video"
max_file_size=$((45 * 1024 * 1024)) # in bytes
max_number=$(renamer)
count=$((max_number + 1))

renamer

for video_file in "$INPUT_DIR"/*; do
    output_file="$OUTPUT_DIR/resized_$(basename "$video_file")"
    current_size=$(stat --format=%s "$video_file")
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video_file")
    if [ "$current_size" -le "$max_file_size" ]; then
        echo "Skipped file: $video_file (size already meets the condition)"
        continue
    fi
    target_bitrate=$(python3 -c "print(int($max_file_size * 8 / ($duration * 1024)))")
    ffmpeg -i "$video_file" -b:v "$target_bitrate"k -preset medium -vf "scale=1280:-1" "$output_file"
done

for file in "$INPUT_DIR"/*; do
    if [ -f "$file" ]; then
        extension="${file##*.}"
        new_name="w-logo_$count.$extension"
        mv "$file" "$OUTPUT_DIR/$new_name"
        echo "Renamed $file to $new_name"
        ((count++))
    fi
done

echo "Maximum number: $max_number"

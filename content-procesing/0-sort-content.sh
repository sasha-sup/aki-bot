#!/bin/bash

source_directory="/root/Yandex.Disk/content"
image_directory="/root/Yandex.Disk/content/pic"
video_directory="/root/Yandex.Disk/content/video"

# Remove empty spaces in filename
for file in $source_directory/*; do
    new_name=$(echo "$file" | tr ' ' '_')
    mv "$file" "$new_name"
done


find "$source_directory" -type f -iregex '.*\.\(jpg\|jpeg\|png\|gif\|bmp\|tiff\|ico\)' -exec bash -c '
    source_file="$0"
    target_directory="$1"
    target_file="$target_directory/$(basename "$source_file")"
    if [ ! -f "$target_file" ]; then
        mv "$source_file" "$target_file"
        echo "Moved $source_file"
    else
        echo "Skiped"
    fi
' {} "$image_directory" \;

find "$source_directory" -type f -iregex '.*\.\(mp4\|avi\|mkv\|mov\|flv\|wmv\|m4v\|webm\)' -exec bash -c '
    source_file="$0"
    target_directory="$1"
    target_file="$target_directory/$(basename "$source_file")"
    if [ ! -f "$target_file" ]; then
        mv "$source_file" "$target_file"
        echo "Moved $source_file"
    else
        echo "Skiped"
    fi
' {} "$video_directory" \;
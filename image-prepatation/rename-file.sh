#!/bin/bash

count=1
image_directory="/root/Yandex.Disk/content/pic"

for file in $image_directory/*; do
    if [ -f "$file" ]; then
        extension="${file##*.}"
        new_name="w-logo_$count.$extension"
        mv "$file" "$image_directory/$new_name"
        echo "Renamed $file to $new_name"
        ((count++))
    fi
done

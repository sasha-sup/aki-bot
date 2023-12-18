#!/bin/bash

count=1

for file in ../*; do
    if [ -f "$file" ]; then
        extension="${file##*.}"
        new_name="w-logo_$count.$extension"
        mv "$file" "$new_name"
        echo "Renamed $file to $new_name"
        ((count++))
    fi
done
scripts=(
    "0-sort-content.sh"
    "1-logo-on-pic.py"
    "2-logo-on-video.sh"
    "3-video-resizer.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "Running: $script"
        if [[ "$script" == *".py" ]]; then
            python3 "$script"
        else
            bash "$script"
        fi
        echo "--------------------"
        echo "$script done"
        echo "--------------------"
    fi
done

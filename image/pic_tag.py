import os
import json
import random
from logger import logger
from PIL import Image

with open("./pic-config.json", "r") as f:
    config = json.load(f)


def renamer():
    files = os.listdir(config["BASE_PIC_DIR"])
    filtered_files = [file for file in files if file.startswith("w-logo_")]
    if not filtered_files:
        return 0
    max_number = max([int(file.split("_")[1].split(".")[0]) for file in filtered_files])
    return max_number


def add_logo():
    image_files = [
        f
        for f in os.listdir(config["NEW_PIC_DIR"])
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))
    ]
    for image_file in image_files:
        new_name = int(renamer()) + 1
        try:
            if image_file.startswith("w-logo_"):
                continue
            image_path = os.path.join(config["NEW_PIC_DIR"], image_file)
            output_filename = f"w-logo_{new_name}.jpg"
            output_path = os.path.join(config["BASE_PIC_DIR"], output_filename)
            image = Image.open(image_path).convert("RGBA")
            logo = Image.open(config["LOGO_PATH"]).convert("RGBA")
            logo = logo.resize((100, 100))
            img_width, img_height = image.size
            logo_width, logo_height = logo.size
            x = random.randint(0, img_width - logo_width)
            y = random.randint(0, img_height - logo_height)
            image.paste(logo, (x, y), logo)
            image = image.convert("RGB")
            image.save(output_path, "JPEG")
            os.remove(image_path)
            logger.info(
                f"Image: {image_file}, New name: {output_filename}, Moved to: {output_path}",
                extra={"tags": {"Aki-Bot-Image": "pick-tag"}},
            )
        except Exception as e:
            logger.error(
                f"Error add_logo {image_file}: {e}",
                extra={"tags": {"Aki-Bot-Image": "pick-tag"}},
            )

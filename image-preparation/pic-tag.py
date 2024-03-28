import os
import random
from logger import logger
from PIL import Image

with open("./pic-config.json", "r") as f:
    config = json.load(f)


def renamer():
    files = os.listdir(config["PIC_DIR"])
    filtered_files = [file for file in files if file.startswith("w-logo_")]
    if not filtered_files:
        return 0
    max_number = max([int(file.split("_")[1].split(".")[0]) for file in filtered_files])
    return max_number


def add_logo(directory, logo_path, output_dir):

    image_files = [
        f
        for f in os.listdir(directory)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))
    ]

    for image_file in image_files:
        new_name = int(renamer()) + 1
        try:
            if image_file.startswith("w-logo_"):
                continue
            image_path = os.path.join(directory, image_file)
            output_filename = f"w-logo_{new_name}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            image = Image.open(image_path).convert("RGBA")
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((100, 100))
            img_width, img_height = image.size
            logo_width, logo_height = logo.size
            x = random.randint(0, img_width - logo_width)
            y = random.randint(0, img_height - logo_height)
            image.paste(logo, (x, y), logo)
            image = image.convert("RGB")
            image.save(output_path, "JPEG")
            os.remove(image_path)
            logging.info(
                f"Image: {image_file}, New name: {output_filename}, Moved to: {output_path}"
            )
        except Exception as e:
            logging.error(f"Error add_logo {image_file}: {e}")


add_logo(config["NEW_PIC_DIR"], config["LOGO_PATH"], config["PIC_DIR"])

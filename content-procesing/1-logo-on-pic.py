import os
import random

from PIL import Image

LOGO_PATH="/root/Yandex.Disk/content/logo/akibot-logo1.png"
INPUT_DIR="/root/Yandex.Disk/content/pic"


# TODO: logs

def add_logo(directory, logo_path):
    os.makedirs(directory, exist_ok=True)
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
    for image_file in image_files:
        try:
            if image_file.startswith("w-logo_"):
                continue
            image_path = os.path.join(directory, image_file)
            output_filename = f"w-logo_{image_file}"
            output_path = os.path.join(directory, output_filename)
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
            print(f"Processed image: {image_file}")
            os.remove(image_path)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")



add_logo(INPUT_DIR, LOGO_PATH)

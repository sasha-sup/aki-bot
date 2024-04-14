import os
from PIL import Image
import logging


def rotate(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        image_files = [
            f
            for f in os.listdir(directory)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))
        ]
        for image_file in image_files:
            try:
                image_path = os.path.join(directory, image_file)
                output_filename = f"rotate-{image_file}"
                output_path = os.path.join(directory, output_filename)
                image = Image.open(image_path)
                angle = 180
                rotated_image = image.rotate(angle, expand=True)
                rotated_image.save(output_path, "JPEG")
                logger.info(
                    f"Processed image: {image_file}",
                    extra={"tags": {"Aki-Bot-Image": "Pick-Rotate"}},
                )
                os.remove(image_path)
            except Exception as e:
                logger.error(
                    f"Error image rotate {image_file}: {e}",
                    extra={"tags": {"Aki-Bot-Image": "Pick-Rotate"}},
                )
    except Exception as e:
        logger.error(
            f"Error in image rotate --> creating directory or listing image files: {e}",
            extra={"tags": {"Aki-Bot-Image": "Pick-Rotate"}},
        )


with open("./pic-config.json", "r") as f:
    config = json.load(f)

rotate(config["PIC_DIR"])

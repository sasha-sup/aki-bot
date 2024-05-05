import os
import json
from PIL import Image
from logger import logger


# https://core.telegram.org/bots/api#sendphoto


with open("./pic-config.json", "r") as f:
    config = json.load(f)


def check_images():
    filenames = os.listdir(config["BASE_PIC_DIR"])
    all_good = True
    for filename in filenames:
        input_path = os.path.join(config["BASE_PIC_DIR"], filename)
        output_path = os.path.join(config["BASE_PIC_DIR"], filename)

        if os.path.isfile(input_path) and any(
            input_path.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]
        ):

            with Image.open(input_path) as img:
                width, height = img.size

                if os.path.getsize(input_path) / (1024 * 1024) > config["max_size"]:
                    logger.error(
                        f"Size of {input_path} > {config['max_size']} MB",
                        extra={"tags": {"Aki-Bot-Image": "Get-Size"}},
                    )
                    all_good = False

                if (
                    width / height > config["max_ratio"]
                    or height / width > config["max_ratio"]
                ):
                    logger.error(
                        f"Aspect ratio of {input_path} exceeds {config['max_ratio']}",
                        extra={"tags": {"Aki-Bot-Image": "Max-Ratio"}},
                    )
                    all_good = False

                if width + height > config["max_dimensions"]:
                    logger.error(
                        f"Dimensions of {input_path} exceed {config['max_dimensions']}",
                        extra={"tags": {"Aki-Bot-Image": "Max-Dimensions"}},
                    )
                    all_good = False

    if all_good:
        logger.info(
            f"All images ready to use",
            extra={"tags": {"Aki-Bot-Image": "All-good"}},
        )


def count_objects_in_directory():
    filenames = os.listdir(config["BASE_PIC_DIR"])
    return len(filenames)
    return None

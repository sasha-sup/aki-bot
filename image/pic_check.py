import os
import json
from PIL import Image
from logger import logger


# https://core.telegram.org/bots/api#sendphoto


with open("./pic-config.json", "r") as f:
    config = json.load(f)


def resize_and_compress_images():
    try:
        filenames = os.listdir(config["PIC_DIR"])
        for filename in filenames:
            input_path = os.path.join(config["PIC_DIR"], filename)
            output_path = os.path.join(config["PIC_DIR"], filename)

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
                        raise Exception(
                            f"Size of {input_path} > {config['max_size']} MB",
                            extra={"tags": {"Aki-Bot-Image": "Get-Size"}},
                        )

                    if (
                        width / height > config["max_ratio"]
                        or height / width > config["max_ratio"]
                    ):
                        logger.error(
                            f"Aspect ratio of {input_path} exceeds {config['max_ratio']}",
                            extra={"tags": {"Aki-Bot-Image": "Max-Ratio"}},
                        )
                        raise Exception(
                            f"Aspect ratio of {input_path} exceeds {config['max_ratio']}",
                            extra={"tags": {"Aki-Bot-Image": "Max-Ratio"}},
                        )

                    if width + height > config["max_dimensions"]:
                        logger.error(
                            f"Dimensions of {input_path} exceed {config['max_dimensions']}",
                            extra={"tags": {"Aki-Bot-Image": "Max-Dimensions"}},
                        )
                        raise Exception(
                            f"Dimensions of {input_path} exceed {config['max_dimensions']}",
                            extra={"tags": {"Aki-Bot-Image": "Max-Dimensions"}},
                        )

                    new_width = int(width * (config["width_percent"] / 100))
                    new_height = int(height * (config["height_percent"] / 100))
                    resized_img = img.resize((new_width, new_height))
                    resized_img.save(output_path)

    except Exception as e:
        logger.error(
            f"Ну тут явно дерьом какое-то с пик-чеком: {e}",
            extra={"tags": {"Aki-Bot-Image": "PIZDEC"}},
        )



def count_objects_in_directory():
    try:
        filenames = os.listdir(config["PIC_DIR"])
        return len(filenames)
    except Exception as e:
        logger.error(
            f"Error counting objects in directory {directory}: {e}",
            extra={"tags": {"Aki-Bot-Image": "Count-Objects"}},
        )
        return None


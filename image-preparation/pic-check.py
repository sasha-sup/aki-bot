import os
import json
from multiprocessing import Pool
from PIL import Image
from logger import logger


def process_image(filename):
    try:
        input_path = os.path.join(config["PIC_DIR"], filename)
        output_path = os.path.join(config["PIC_DIR"], filename)

        if os.path.isfile(input_path) and any(
            input_path.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]
        ):
            with Image.open(input_path) as img:
                width, height = img.size

                if os.path.getsize(input_path) / (1024 * 1024) > config["max_size"]:
                    logger.error(f"Size of {input_path} > {config['max_size']} MB")
                    raise Exception(f"Size of {input_path} > {config['max_size']} MB")

                if (
                    width / height > config["max_ratio"]
                    or height / width > config["max_ratio"]
                ):
                    logger.error(
                        f"Aspect ratio of {input_path} exceeds {config['max_ratio']}"
                    )
                    raise Exception(
                        f"Aspect ratio of {input_path} exceeds {config['max_ratio']}"
                    )

                if width + height > config["max_dimensions"]:
                    logger.error(
                        f"Dimensions of {input_path} exceed {config['max_dimensions']}"
                    )
                    raise Exception(
                        f"Dimensions of {input_path} exceed {config['max_dimensions']}"
                    )

                    new_width = int(width * (config["width_percent"] / 100))
                    new_height = int(height * (config["height_percent"] / 100))
                    resized_img = img.resize((new_width, new_height))
                    resized_img.save(output_path)

            logger.info(f"Image {filename} processed successfully.")

    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")


def resize_and_compress_images():
    try:
        filenames = os.listdir(config["PIC_DIR"])
        with Pool() as pool:
            pool.map(process_image, filenames)

    except Exception as e:
        logger.error(f"Error in resize_and_compress_images: {e}")


if __name__ == "__main__":
    with open("./pic-config.json", "r") as f:
        config = json.load(f)

    resize_and_compress_images()

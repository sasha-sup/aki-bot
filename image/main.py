from logger import logger
import json
from pic_check import resize_and_compress_images
from pic_tag import add_logo
import sys


def main():
    try:
        with open("./pic-config.json", "r") as f:
            config = json.load(f)
        resize_and_compress_images()
        add_logo(config["NEW_PIC_DIR"], config["LOGO_PATH"], config["PIC_DIR"])
    except Exception as e:
        logger.error(
            f"Error in main function: {e}",
            extra={"tags": {"Aki-Bot-Image": "Main-Error"}},
        )
    finally:
        sys.exit()


if __name__ == "__main__":
    main()

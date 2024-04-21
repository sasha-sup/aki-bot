from logger import logger
import json
from pic_check import resize_and_compress_images
from pic_tag import add_logo


def log_step(step_name):
    logger.info(
        f"Starting {step_name} job",
        extra={"tags": {"Aki-Bot-Image": "Pick-Check"}},
    )

def main():
    try:
        with open("./pic-config.json", "r") as f:
            config = json.load(f)

        log_step("resize and compress")
        resize_and_compress_images()
        log_step("resize and compress")

        log_step("add logo")
        add_logo(config["NEW_PIC_DIR"], config["LOGO_PATH"], config["PIC_DIR"])
        log_step("add logo")

    except Exception as e:
        logger.error(
            f"Error in main function: {e}",
            extra={"tags": {"Aki-Bot-Image": "Resizer"}},
        )

if __name__ == "__main__":
    main()

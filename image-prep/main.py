from logger import logger
from pic_check import resize_and_compress_images
from pic_tag import add_logo


def main():
    try:
        resize_and_compress_images()
        logger.info(
            "Resize and compress job complete",
            extra={"tags": {"Aki-Bot-Image-Prep": "Pick-Check"}},
        )
        add_logo()
        logger.info(
            "Add logo job complete",
            extra={"tags": {"Aki-Bot-Image-Prep": "Pick-Check"}},
        )

    except Exception as e:
        logger.error(
            f"Error in main function: {e}",
            extra={"tags": {"Aki-Bot-Image-Prep": "Resizer"}},
        )


if __name__ == "__main__":
    main()

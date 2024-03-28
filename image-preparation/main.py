from logger import logger
from pic_check import resize_and_compress_images
from pic_rotate import rotate
from pic_tag import add_logo


def main():
    try:
        resize_and_compress_images()
        # rotate()
        add_logo()
    except Exception as e:
        logger.error(f"Error in main function: {e}")


if __name__ == "__main__":
    main()

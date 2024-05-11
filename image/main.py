from logger import logger
import json
from pic_check import check_images
from pic_tag import add_logo
import sys


def main():
    check_images()
    # TODO: resize pic if check_image find bad images
    add_logo()


if __name__ == "__main__":
    main()

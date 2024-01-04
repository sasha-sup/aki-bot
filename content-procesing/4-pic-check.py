from PIL import Image
import os

PIC_DIR = "/root/Yandex.Disk/content/pic"


def resize_and_compress_images(PIC_DIR, max_size=10, max_dimensions=10000, max_ratio=20, width_percent=40, height_percent=40):
    try:
        for filename in os.listdir(PIC_DIR):
            input_path = os.path.join(PIC_DIR, filename)
            output_path = os.path.join(PIC_DIR, filename)
            if os.path.isfile(input_path) and any(input_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                resize_and_compress_image(input_path, output_path, max_size, max_dimensions, max_ratio, width_percent, height_percent)
    except Exception as e:
        print(f"Error with: {e}")

def resize_and_compress_image(input_path, output_path, max_size=10, max_dimensions=10000, max_ratio=20, width_percent=40, height_percent=40):
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            if os.path.getsize(input_path) / (1024 * 1024) > max_size:
                raise Exception(f"Size of {input_path} > 10 MB")

            if width + height > max_dimensions:
                raise Exception(f"Sum of width and height of {input_path} exceeds 10000 pixels")

            if width / height > max_ratio or height / width > max_ratio:
                raise Exception(f"Aspect ratio of {input_path} exceeds 20")

            if width + height > max_dimensions:
                new_width = int(width * (width_percent / 100))
                new_height = int(height * (height_percent / 100))
                resized_img = img.resize((new_width, new_height))
                resized_img.save(output_path)

    except Exception as e:
        print(f"Error with {input_path}: {e}")

resize_and_compress_images(PIC_DIR)

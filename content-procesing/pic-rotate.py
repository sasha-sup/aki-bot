import os
import random

from PIL import Image
import PIL

INPUT_DIR=""

def rotate(directory):
    os.makedirs(directory, exist_ok=True)
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
    for image_file in image_files:
        try:
            image_path = os.path.join(directory, image_file)
            output_filename = f"rotate-{image_file}"
            output_path = os.path.join(directory, output_filename)
            image = Image.open(image_path)
            angle = 180
            rotated_image = image.rotate(angle, expand=True)
            rotated_image.save(output_path, "JPEG")
            print(f"Processed image: {image_file}")
            #os.remove(image_path)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

rotate(INPUT_DIR)

from PIL import Image
import os
import logging as log

INPUT_FOLDER = "selfies"
OUTPUT_FOLDER = "cropped_selfies"

"""
Crop the selfies to squares, centered.

Requirements : place the selfies in the folder IMG_FOLDER
Make the directory OUTPUT_FOLDER
"""

def crop_selfies():
    images = os.listdir(INPUT_FOLDER)
    for image_name in images:
        image_path = os.path.join(INPUT_FOLDER, image_name)
        cropped_image_path = os.path.join(OUTPUT_FOLDER, image_name)
        im = Image.open(image_path)
        log.debug("Processing file :" + image_name)
        width, height = im.size
        if(width == height):
            im.save(cropped_image_path)
            log.debug("image processed")
            continue
        log.debug("needs cropping")
        new_width = min(width, height)
        new_height = new_width
        left = (width - new_width)/2
        top = (height - new_height)/2
        right = (width + new_width)/2
        bottom = (height + new_height)/2
        cropped = im.crop((left, top, right, bottom))
        cropped.save(cropped_image_path)
        log.debug("image processed")
    log.info("Selfies cropped")

crop_selfies()

from PIL import Image
import os
import logging as log

INPUT_FOLDER = "selfies"
OUTPUT_FOLDER = "cropped_selfies"
SIZE = 512, 512

"""
Crop the selfies to squares (if needed) and resize them.

Requirements : place the selfies in the folder IMG_FOLDER
Make directory : OUTPUT_FOLDER
"""

def crop_selfies():
    images = os.listdir(INPUT_FOLDER)
    for image_name in images:
        try:
            image_path = os.path.join(INPUT_FOLDER, image_name)
            cropped_image_path = os.path.join(OUTPUT_FOLDER, image_name)
            im = Image.open(image_path)
            log.debug("Processing file :" + image_name)
            width, height = im.size
            if(width != height): # Make it square
                new_width = min(width, height)
                new_height = new_width
                left = (width - new_width)/2
                top = (height - new_height)/2
                right = (width + new_width)/2
                bottom = (height + new_height)/2
                im = im.crop((left, top, right, bottom))
            im.thumbnail(SIZE, Image.Resampling.LANCZOS) # Downscale
            im.save(cropped_image_path)
            log.debug("image processed")
        except IOError:
            log.error("cannot create thumbnail for '%s'" % infile)
    log.info("Selfies cropped")

crop_selfies()

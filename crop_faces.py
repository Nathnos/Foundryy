from PIL import Image
import os
import logging as log
from math import ceil
log.basicConfig()
log.getLogger().setLevel(log.DEBUG)
#import face_recognition

INPUT_FOLDER = "selfies"
OUTPUT_FOLDER = "cropped_selfies"

"""
Crop the selfies to squares. Keep as much of the image as possible.
Doens’t crop to a specific size.

Requirements : place the selfies in the folder IMG_FOLDER
make the directory OUTPUT_FOLDER
"""

def crop_selfies():
    images = os.listdir(INPUT_FOLDER    )
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
        #image = face_recognition.load_image_file(image_path)
        #face_locations = face_recognition.face_locations(image)
        face_locations = [["file_name", 0, 0, 500, 500]] # TODO : implem
        if(len(face_locations) != 1):
            # If 2+ faces are detected, or no face at all, ignore the selfie
            log.debug(str(len(face_locations)) + " faces found, image ignored")
            continue
        log.debug("face found")
        portrait_format = True # Need to remove pixels at top or bottom
        if(width > height):
            portrait_format = False # Need to remove pixels at left or right
        top, right, bottom, left = get_crop_coordonates(face_locations[0],
                                                        portrait_format,
                                                        im.size)
        cropped = im.crop((left, top, right, bottom))
        cropped.save(cropped_image_path)
        log.debug("image processed")
    log.info("Selfies cropped")

def calculate_coordonate(top, bottom, height, pixels_to_remove):
    """
    calculate coordonate that will change : top and bottom if portrait_format,
    left and right otherwise.

    NB : I named my variables (top, bottom, height). These are only correct
    names for portrait_format. But the function is still valid if we input
    (left, right, width). In this case, the output is (left, right)
    """
    top_margin, bottom_margin = top, height-bottom
    half_pix_to_remove = ceil(pixels_to_remove/2)
    if(half_pix_to_remove <= top_margin and half_pix_to_remove <= bottom_margin):
        # We balance removal between top and bottom
        top = half_pix_to_remove
        bottom = height - half_pix_to_remove
    else:
        if(half_pix_to_remove > top_margin): # If top blocks
            top = top # Remove as much as we can from top
            bottom = height - (pixels_to_remove - top)
        else: # If bottom blocks
            bottom = bottom # Remove as much as we can from bottom
            top = pixels_to_remove - (height - bottom)
    return top, bottom

def get_crop_coordonates(face_locations, portrait_format, im_size):
    """
    return coordonates for cropping
    """
    # Try to crop as much on each side
    # If not possible, crop more on top OR left
    width, height = im_size
    pixels_to_remove = abs(height-width)
    _, top, right, bottom, left = face_locations
    if(portrait_format):
        log.debug("needs cropping on height : " + str(pixels_to_remove) + " pixels")
        left, right = 0, width
        top, bottom = calculate_coordonate(top, bottom, height,
                                           pixels_to_remove)
    else: #landscape format
        log.debug("needs cropping on width")
        top, bottom = 0, height
        left, right = calculate_coordonate(left, right, width, pixels_to_remove)
    log.debug("cropping top/right/bottom/left : " + str(top) + " " +
              str(right) + " " + str(bottom) + " " + str(left))
    log.debug("original top/right/bottom/left : 0 " + str(width) + " " +
              str(height) + " 0" )
    return top, right, bottom, left

crop_selfies()

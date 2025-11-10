import sys
import os
from PIL import Image, ImageOps

try:
    for arg in sys.argv[1:]:
        arg = os.path.splitext(arg)
        if ["jpg", "jpeg", "png"]:
            pass
        else:
            sys.exit("Supported image formats: jpg, jpeg, png")
except FileNotFoundError:
     sys.exit("Your file doesn't exist")


with Image.open("shirt.png") as shirt:
    with Image.open(sys.argv[1]) as input:
            size = shirt.size
            cropped = ImageOps.fit(input, size)
            cropped.paste(shirt, shirt)
            cropped.save(sys.argv[2])
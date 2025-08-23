import numpy as np
from PIL import Image
import matplotlib as plt

image = Image.open("uiui.jpg")
image.show("uiui")

print(image.size)

width, height = image.size

print(width)
print(height)

print(image.filename)
print(image.format)
print(image.format_description)
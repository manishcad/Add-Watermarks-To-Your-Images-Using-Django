import uuid
from django.shortcuts import render, redirect
from .models import Watermark
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.contrib import messages

image_extension = ['jpg', 'png', 'jpeg', "JPG", "PNG", "JPEG"]


def create_watermark(request, file_input, text):

    string = str(file_input).split(".")
    print(string[-1])
    if string[-1] in image_extension:
        # Open the image
        im = Image.open(file_input)

        # Create an ImageDraw object
        draw = ImageDraw.Draw(im)

        # Choose a font and a font size
        font = ImageFont.truetype("arial.ttf", 40)

        # Choose the position for the text
        x, y = 10, 10
        text = f"©{text}"
        # Add the text watermark
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        file_name = f"{uuid.uuid4()}.png"
        # Save the image with the watermark
        im.save(f"static/output/{file_name}")
        return f"http://127.0.0.1:8000/static/output/{file_name}"
    else:
        messages.warning(request, "Please Select an Image")
        return "Home"

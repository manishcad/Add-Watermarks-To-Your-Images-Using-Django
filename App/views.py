import uuid
from django.shortcuts import render, redirect
from .models import Watermark
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.contrib import messages

# Create your views here.


image_extension = ['jpg', 'png', 'jpeg', "JPG", "PNG", "JPEG"]


def copywrite_apply(request, file_input, text):

    string = str(file_input).split(".")
    if string[-1] in image_extension:
        # Open the image
        im = Image.open(file_input)
        draw = ImageDraw.Draw(im)
        width, height = im.size
        font = ImageFont.truetype("arial.ttf", 36)
        text_width, text_height = draw.textsize(text, font)
        margin = 10
        x = width-text_width-margin
        y = height-text_height-margin
        draw.text((x, y), text, font=font)

        file_name = f"{uuid.uuid4()}.png"
        # Save the image with the watermark
        im.save(f"static/output/{file_name}")

        return f"http://127.0.0.1:8000/static/output/{file_name}"
    else:
        messages.warning(request, "Please Select an Image")
        return "Home"


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


def home(request):
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("file")
        new_str = str(image).split(".")
        if new_str[-1] not in image_extension:
            messages.warning(request, "Please Select an Image")
            return redirect("Home")
        else:
            watermark_image = Watermark(text=text, image=image)
            watermark_image.save()

            output_path = copywrite_apply(request,
                                          f"media/{watermark_image.image}", text)

            output_path = str(output_path)[36::]

            if output_path == "":

                return redirect("Home")
            return redirect("Download", pk=output_path)
    return render(request, 'index.html')


def download(request, pk):
    context = {"pk": pk}
    return render(request, 'download.html', context)

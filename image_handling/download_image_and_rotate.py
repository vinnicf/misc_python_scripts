import requests
from PIL import Image
from io import BytesIO
import os
import pyperclip

def download_and_rotate_and_resize_image():

    image_url = pyperclip.paste()
    # Extract the name of the last folder in the image URL path
    image_folder_name = image_url.strip('/').split('/')[-2]
    suffix = image_url.strip('/').split('/')[-3][-2:]
    # The path where the image will be saved
    save_path = os.path.join(os.getcwd(), f"{image_folder_name}{suffix}.jpg")

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Open the image from the binary response content
        image = Image.open(BytesIO(response.content))

        # Rotate the image 90 degrees
        rotated_image = image.rotate(-90, expand=True)

        # If the original width (new height) is greater than 1500px, resize the image
        if rotated_image.height > 1500:
            # Calculate the new width to maintain aspect ratio
            new_height = 1500
            new_width = int((new_height / rotated_image.height) * rotated_image.width)
            # Resize the image
            rotated_image = rotated_image.resize((new_width, new_height), Image.ANTIALIAS)

        # Save the rotated and resized image to the same folder as the script with the new name
        rotated_image.save(save_path)
        print(f"Image saved as {save_path}")
    else:
        print("Failed to download the image.")


download_and_rotate_and_resize_image()

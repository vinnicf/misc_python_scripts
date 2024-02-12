from PIL import Image
import os

def remove_white_background(image_path, output_path, tolerance=220):

    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure image is in RGBA format to handle alpha channel

    datas = img.getdata()
    newData = []

    for item in datas:
        # Check if the pixel is close to white based on the tolerance
        if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
            # Replace it with a transparent pixel
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")

def process_directory(directory_path, output_directory):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.png')
            remove_white_background(image_path, output_path)

# Example usage
directory_path = 'C:\\WEBDEV\\melhorprop\\products'
output_directory = 'C:\\WEBDEV\\melhorprop\\products\\transparent'
process_directory(directory_path, output_directory)

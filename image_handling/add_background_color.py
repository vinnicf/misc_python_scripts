from PIL import Image
import os

def add_background_to_png(input_folder, output_folder, background_color):
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            original_image_path = os.path.join(input_folder, filename)
            with Image.open(original_image_path) as img:
                # Resize original image while maintaining aspect ratio
                target_size = (900, 500) # Considering padding
                img.thumbnail(target_size)

                # Create new image with desired background color and size
                new_image = Image.new("RGBA", (1000, 600), background_color)

                # Calculate positioning for the original image
                x = (new_image.width - img.width) // 2
                y = (new_image.height - img.height) // 2

                # Paste the original image onto the new image
                new_image.paste(img, (x, y), img)

                # Convert RGBA to RGB if saving as JPEG or other formats not supporting transparency
                if new_image.mode == 'RGBA':
                    new_image = new_image.convert('RGB')

               # Save the modified image in WebP format
                output_image_filename = os.path.splitext(filename)[0] + '.webp'
                output_image_path = os.path.join(output_folder, output_image_filename)
                new_image.save(output_image_path, format='WEBP')

# Usage example
input_folder = 'C:\\WEBDEV\\melhorprop\\products\\transparent'
output_folder = 'C:\\WEBDEV\\melhorprop\\products\\output'
background_color = (246, 246, 246)
add_background_to_png(input_folder, output_folder, background_color)

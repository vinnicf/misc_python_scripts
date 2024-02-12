# from selenium import webdriver
import csv, re, bs4, time, requests, os, io
from random import randrange
from requests.exceptions import InvalidURL
import pyperclip, json
from PIL import Image
import sys
import re

api_url = 'https://domain.com/api/profissional-check/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

url = pyperclip.paste()

r = requests.get(url, headers=headers)

soup = bs4.BeautifulSoup(r.content,'html.parser')

descricao = soup.select('#listify_widget_panel_listing_content-2')
cidade = soup.select('.content-single-job_listing-title-category')
imagens = soup.select('.watermarked img')
nome = soup.select('h1')
telefone = soup.select('.job_listing-phone')
bairro = soup.select('.job_listing-location')
link_maps = soup.select('.js-toggle-directions')
bairrotrim = bairro[0].getText().split(',')[0]

#Cleans the name
clean_name = nome[0].getText().strip()
clean_name = clean_name.replace('–', '-').replace('—', '-')
clean_name = clean_name.split(' - ')[0].strip()

clean_phone = telefone[0].getText().strip()

data = {
    "phone_number": clean_phone,  # Extracted phone number
    "nome": clean_name.strip(),  # Extracted name
    "cidade": cidade[0].getText().strip()  # Extracted city name
}

apiresponse = requests.post(api_url, json=data)

if apiresponse.status_code == 200:
    print("Phone number exists in the database. Skipping CSV writing and image downloading.")
    # Exit the script after printing the message
    sys.exit()
else:
    print("Phone number does not exist in the database. Proceeding with CSV writing and image downloading.")
    print("API Response:", apiresponse.text)


if descricao:
    paragraphs = descricao[0].find_all('p')
    filtered_paragraphs = []
    for paragraph in paragraphs:
        # Check if 'conteúdo exclusivo' is in paragraph (case insensitive)
        if not re.search(r'conteúdo exclusivo', paragraph.get_text(), re.IGNORECASE):
            filtered_paragraphs.append(paragraph.prettify())
    desc = ''.join(filtered_paragraphs)
else:
    desc = ""

print(nome[0].getText())
print(telefone[0].getText())
print(bairrotrim)
print(cidade[0].getText())



city_name = cidade[0].getText().strip()
print(f"City name from site: '{city_name}'")  # Surround with quotes to visualize any extra characters
print(clean_name)

# Load phone numbers from a file
with open('phone_numbers.txt', 'r') as file:
    phone_numbers_to_exclude = set(file.read().splitlines())

extracted_phone = telefone[0].getText().strip()
if extracted_phone in phone_numbers_to_exclude:
    print(f"Skipping extraction for {extracted_phone}")
    sys.exit()
    # Add code to skip or exit the script here

outputfile = open('professionals.csv', 'a', newline='')
outputwriter = csv.writer(outputfile)
outputwriter.writerow([clean_name.strip(), telefone[0].getText().strip(), cidade[0].getText().strip(), bairrotrim.strip(), link_maps[0]['href'], desc])
outputfile.close()


# Extract text from the nome[0]
if clean_name:
    nome_simple = clean_name.replace(" ", "_").lower()
else:
    nome_text = "acompanhante"

# Image counter
count = 1
max_images = 20

imagenslista = []
for img in imagens:
        if count >= max_images:
            break  # Stop processing after 10 images


        imgurl = img.get('src') or img.get('data-src')

        if not imgurl or imgurl.startswith("data"):
            print("Both data-src and src are missing for this image. Skipping...")
            continue

        # Use nome_text and count to form new image name
        imgnewname = f"{nome_simple}_{count}.jpg"

        # Sanitize the filename
        imgnewname = imgnewname.replace("/", "_").replace(":", "_").replace("\\", "_") # Add any other problematic characters as needed


        request_img = requests.get(imgurl)
        request_img.raise_for_status()

        # Ensure 'imagens' directory exists
        if not os.path.exists('imagens'):
            os.makedirs('imagens')

        imagefile = open(os.path.join('imagens',imgnewname),'wb')

        for chunk in request_img.iter_content(100000):
             imagefile.write(chunk)

        imagefile.close()

        # Open the image file with Pillow
        img = Image.open(os.path.join('imagens', imgnewname))

        # Flip the image horizontally
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

        # Save the flipped image
        flipped_img.save(os.path.join('imagens', imgnewname))


        # Increment image counter
        count += 1


        print('done for ' + imgurl)
        print(imagenslista)


listing_cover_div = soup.select_one('.listing-cover')
if listing_cover_div:
    style = listing_cover_div.get('style', '')
    bg_image_url = re.search(r'url\((.*?)\)', style)
    if bg_image_url:
        bg_image_url = bg_image_url.group(1)
        print("Background Image URL:", bg_image_url)

        # Form new image name
        bg_img_name = f"{nome_simple}_feat.jpg"
        bg_img_name = bg_img_name.replace("/", "_").replace(":", "_").replace("\\", "_")

        # Download the background image
        bg_response = requests.get(bg_image_url)
        bg_response.raise_for_status()

        # Ensure 'imagens' directory exists
        if not os.path.exists('imagens'):
            os.makedirs('imagens')

        # Open the image and flip it horizontally
        with Image.open(io.BytesIO(bg_response.content)) as img:
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

            # Save the flipped image
            flipped_img.save(os.path.join('imagens', bg_img_name))

        print(f"Background image saved as {bg_img_name}")
    else:
        print("Background image URL not found.")
else:
    print("Listing cover div not found.")

#the part where I save the images

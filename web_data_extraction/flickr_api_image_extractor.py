import requests
import sys
from PIL import Image
from io import BytesIO
import re

def download_and_flip_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Open the image and flip it
        image = Image.open(BytesIO(response.content))

        # Save the flipped image
        image.save(filename)

# Flickr API endpoint

def download_images_for_keyword(keyword):
    api_endpoint = "https://www.flickr.com/services/rest/"
    api_key = "API_KEY"
    api_secret = "API_SECRETE"

    params = {
        "method": "flickr.photos.search",
        "api_key": api_key,
        "text": keyword,
        "format": "json",
        "extras": "url_l,owner_name",
        "nojsoncallback": 1,
        "sort": "relevance",
        "per_page": 3
    }

    response = requests.get(api_endpoint, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            for j, photo in enumerate(data['photos']['photo'], start=1):
                photo_url = photo.get("url_l")
                photographer = photo.get("ownername")
                if photo_url:
                    clean_keyword = re.sub(r'\W+', '_', keyword)  # Replace non-alphanumeric characters with underscore
                    clean_photographer = re.sub(r'\W+', '_', photographer)
                    filename = f"{clean_keyword}_{j}_{clean_photographer}.jpg"
                    download_and_flip_image(photo_url, filename)
                    print(f"Downloaded and flipped image for keyword: {keyword} as {filename}. Author: {photographer}")
                else:
                    print(f"No large image found for keyword: {keyword}")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response content:", response.text)
    else:
        print("Failed to get a successful response:", response.status_code)
        print("Response content:", response.text)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        images = download_images_for_keyword(keyword)
        print(images)
    else:
        print("Please provide a keyword as an argument.")

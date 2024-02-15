import requests
from bs4 import BeautifulSoup
import pyperclip
import re
import csv


# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
}
LABELS = ["Weight", "Clamping Force", "Ease Of Use", "Call/Music Control", "Volume Control", "Microphone Control", "Battery Type", "Continuous Battery Life", "Charge Time"]

AUDIO = ["Bass Accuracy","Mid Accuracy","Treble Accuracy"]



def fetch_html(url):
    """Fetch the HTML content for a given URL."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve data for {url}. Status code: {response.status_code}")
        return None


def extract_product_name(soup):
    """Extract the product name from the page title."""
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        # Title format is '[PRODUCT NAME] Review - SITE.com'
        return title_tag.string.split(' Review -')[0]
    return "Unknown Product"

def label_filter(label):
    """Custom filter function to match labels considering nested elements."""
    def filter_func(tag):
        if tag.name != 'span':
            return False
        text = ''.join(tag.find_all(text=True, recursive=False)).strip()
        return re.compile(r'\s*' + re.escape(label) + r'\s*', re.IGNORECASE).search(text)
    return filter_func


def find_values(soup, labels, audio_labels):
    """Find values for predefined labels, handling both next and previous siblings."""
    results = {}
    # Handle standard labels with next sibling
    for label in labels:
        label_span = soup.find(label_filter(label))
        if label_span:
            next_span = label_span.find_next_sibling('span')
            if next_span:
                results[label] = next_span.text.strip()
            else:
                results[label] = "Value not found"
        else:
            results[label] = "Label not found"

    # Handle audio labels with previous sibling
    for label in audio_labels:
        label_span = soup.find(label_filter(label))
        if label_span:
            prev_span = label_span.find_previous_sibling('span')
            if prev_span:
                results[label] = prev_span.text.strip()
            else:
                results[label] = "Value not found"
        else:
            results[label] = "Label not found"

    return results

def read_urls_from_file(filename):
    """Read URLs from a file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def save_to_csv(data, filename):
    """Save extracted data to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name'] + LABELS + AUDIO)
        for row in data:
            writer.writerow(row)

def main():
    urls = read_urls_from_file('urls.txt')
    all_data = []
    for url in urls:
        soup = fetch_html(url)
        if soup:
            product_name = extract_product_name(soup)
            values = find_values(soup, LABELS, AUDIO)
            row = [product_name] + [values[label] for label in LABELS + AUDIO]
            all_data.append(row)
    save_to_csv(all_data, 'extracted_data.csv')

if __name__ == "__main__":
    main()

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

# Input PDF file
input_path = 'sinani.pdf'

# Set up a text stream for the extracted text
output_stream = io.StringIO()

# Specify the pages you want to extract: skip first 2 and extract the next 10
with open(input_path, 'rb') as input_file:
    extract_text_to_fp(input_file, output_stream, laparams=LAParams(), pagenos=set(range(2, 12)))

# Get the extracted text
extracted_text = output_stream.getvalue()

# Save the extracted text to a file
with open('somepages.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)

output_stream.close()

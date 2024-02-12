import os
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import io

# Directory containing the PDF files
directory_path = 'C:\\WEBDEV\\sinapi\\docs\\cadernos'

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        # Construct full file path
        input_path = os.path.join(directory_path, filename)

        # Set up a text stream for the extracted text
        output_stream = io.StringIO()

        # Extract text from the PDF
        with open(input_path, 'rb') as input_file:
            extract_text_to_fp(input_file, output_stream, laparams=LAParams())

        # Get the extracted text
        extracted_text = output_stream.getvalue()

        # Construct the output path for the text file
        output_path = os.path.join(directory_path, filename.replace('.pdf', '.txt'))

        # Save the extracted text to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        output_stream.close()

print("Extraction completed!")

import json
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def extract_text_from_box(input_path, bbox):
    text_content = {}

    with open(input_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        page_counter = 0

        for page in PDFPage.create_pages(doc):
            page_counter += 1

            if page_counter < 3:
                continue

            interpreter.process_page(page)
            layout = device.get_result()

            current_id = ""
            current_main_text = ""
            current_line = ""

            for obj in layout:
                if isinstance(obj, LTTextBoxHorizontal):
                    # Extract ID:
                    if obj.bbox[0] >= bbox['id'][0] and obj.bbox[1] >= bbox['id'][1] and obj.bbox[2] <= bbox['id'][2] and obj.bbox[3] <= bbox['id'][3]:
                        current_id = obj.get_text().strip()

                    # Extract and reformat main text:
                    if obj.bbox[0] >= bbox['main_text'][0] and obj.bbox[1] >= bbox['main_text'][1] and obj.bbox[2] <= bbox['main_text'][2] and obj.bbox[3] <= bbox['main_text'][3]:
                        lines = obj.get_text().split("\n")
                        for line in lines:
                            if line.endswith('.'):
                                current_line += line
                                current_main_text += current_line + "\n"
                                current_line = ""
                            else:
                                current_line += line + ""

            if current_id:
                text_content[current_id] = current_main_text.strip()

    return text_content

# Define bounding box coordinates
bbox_coordinates = {
    'main_text': (150, 0, 550, 500),
    'id': (168, 710, 228, 734)
}

# PDF file path
pdf_path = 'rest.pdf'

# Extract text
extracted_text = extract_text_from_box(pdf_path, bbox_coordinates)

# Save to JSON file
with open("extracted_data.json", "w") as json_file:
    json.dump(extracted_text, json_file, indent=4)

# Pretty print the extracted text
print("Extraction complete. Data saved to 'extracted_data.json'")
print("Pretty-printing extracted data:")
for id_key, text_value in extracted_text.items():
    print(f"\nID: {id_key}")
    print("=" * 40)
    print(f"Text:\n{text_value}")
    print("=" * 40)

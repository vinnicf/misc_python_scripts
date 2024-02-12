import os
import re
import json

def extract_data_from_section(section, text):
    items = []
    for part in text.split('\n\n'):
        # Skip if this is the footer pattern
        if re.match(r'\d+\n\nSINAPI - Caderno Técnico do Serviço - Concretagem para Estruturas de Concreto Armado', part):
            continue
        if part.strip():  # Skip empty or whitespace lines
             # Normalize line breaks: only break lines after a period or semicolon at the end of a line
            normalized_part = part.replace('\n', ' ').replace('; ', ';\n')
            # Special case for colon and period only at the end of a line
            normalized_part = re.sub(r':\s*$', ':\n', normalized_part)
            normalized_part = re.sub(r'\.\s*$', '.\n', normalized_part)
            # Ensure no colons or periods in the middle of lines are followed by a newline
            normalized_part = re.sub(r':\s+', ': ', normalized_part)
            normalized_part = re.sub(r'\.\s+', '. ', normalized_part)
            
            items.append(normalized_part.strip())
    return ' '.join(items)

def extract_multiple_data(document_text):
    data_dicts = []

    # Splits at each 'Código SIPCI', but keeps the delimiter as part of the split
    parts = re.split(r"(Código SIPCI\s+\d+)", document_text)

    # Pair up the parts so that each 'Código SIPCI' is together with its following content
    for i in range(1, len(parts), 2):
        section_dict = {}
        section_text = parts[i] + parts[i+1]

        # Extract SIPCI Code
        sipci_code_match = re.search(r"Código SIPCI\s+(\d+)", section_text)
        if sipci_code_match:
            section_dict["codigo"] = sipci_code_match.group(1)

        # Loop through and extract items 2-7
        for section, key in zip(
            ["2. ITENS E SUAS CARACTERÍSTICAS", "3. EQUIPAMENTO", "4. CRITÉRIOS PARA QUANTIFICAÇÃO DOS SERVIÇOS",
             "5. CRITÉRIOS DE AFERIÇÃO", "6. EXECUÇÃO", "7. INFORMAÇÕES COMPLEMENTARES"],
            ["itens", "equipamento", "quantificacao", "afericao", "execucao", "complementares"]
        ):
            pattern = re.compile(rf"{re.escape(section)}(.*?)(?=\n\n|$)", re.DOTALL)
            match = pattern.search(section_text)
            if match:
                content = match.group(1).strip()
                content = extract_data_from_section(section, content)
                section_dict[key] = content

        data_dicts.append(section_dict)

    return data_dicts

directory = 'C:\\WEBDEV\\sinapi\\docs\\cadernos'
json_data = {}

# Loop through the .txt files in the specified directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            file_data = extract_multiple_data(text)
            json_data[filename] = file_data

with open('extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

# Use the json.dumps() method for pretty printing
def pretty_print_json(data):
    for filename, file_data_list in data.items():
        print(f"File: {filename}\n{'=' * (len(filename) + 6)}")
        for i, file_data in enumerate(file_data_list):
            print(f"Entry {i+1}")
            print('-' * 8)
            for key, value in file_data.items():
                print(f"{key.upper()}:\n{'-' * (len(key) + 1)}\n{value}\n")
        print("\n")


pretty_print_json(json_data)

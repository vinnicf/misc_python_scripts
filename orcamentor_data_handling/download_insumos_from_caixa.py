import requests
import zipfile
import os
import json
import pandas as pd
import time

def download_zip_file(url, destination):
    print(f"Downloading ZIP file from {url}...")
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
    print(f"Downloaded ZIP file to {destination}")

def extract_xls_from_zip(zip_path, extract_path, xls_name, xls_fallback_name):
    print(f"Attempting to extract {xls_name} or {xls_fallback_name} from ZIP...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            zip_ref.extract(xls_name, path=extract_path)
            print(f"Extracted {xls_name} to {extract_path}")
            return xls_name
        except KeyError:
            zip_ref.extract(xls_fallback_name, path=extract_path)
            print(f"Extracted {xls_fallback_name} to {extract_path}")
            return xls_fallback_name

def read_xls_and_update_json(xls_path, json_path, state, type_):
    # Reading the XLS file into a DataFrame
    df = pd.read_excel(xls_path, skiprows=7)  # Skip the first 7 rows
    df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: str(x).replace('.', '').replace(',', '.')).astype(float) # transform the price column

    codigos = df.iloc[:, 0].tolist()  # First column for 'codigo'
    prices = df.iloc[:, 4].tolist()  # Fifth column for 'price'

    # Load existing JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Update JSON data
    state_type_key = f"{state}_{type_}"
    for codigo, price in zip(codigos, prices):
        codigo_str = str(codigo)
        if codigo_str not in data:
            data[codigo_str] = {}
        data[codigo_str][state_type_key] = price

    # Save updated JSON data
    with open(json_path, 'w') as f:
        json.dump(data, f)

     # Create the extraction path if it doesn't exist
if not os.path.exists("extracted"):
    os.makedirs("extracted")

# Initialize JSON file if it doesn't exist
json_path = "data202311.json"
if not os.path.exists(json_path):
    print(f"Initializing empty JSON file {json_path}...")
    with open(json_path, 'w') as f:
        json.dump({}, f)
    print(f"Initialized empty JSON file {json_path}")

# Base URL for the ZIP files
base_url = "https://www.caixa.gov.br/Downloads/sinapi-a-partir-jul-2009-{state}/SINAPI_ref_Insumos_Composicoes_{state}_202311_{desonerado}.zip"
states = [
    'AC', 'AL', 'AP', 'AM',
    'BA', 'CE', 'DF', 'ES',
    'GO', 'MA', 'MT', 'MS',
    'MG', 'PA', 'PB', 'PR',
    'PE', 'PI', 'RJ', 'RN',
    'RO', 'RR', 'SC', 'SE',
    'TO', 'RS', 'SP'
]
types = ["Desonerado", "NaoDesonerado"]
zip_path = "temp.zip"
extract_path = "extracted"



# Loop through all state and type combinations to download, extract, and update JSON
# Loop through all state and type combinations to download, extract, and update JSON
for state in states:
    upper_state = state.upper()  # State codes are always in uppercase in the file names
    for type_ in types:
        specific_zip_path = f"temp_{upper_state}_{type_}.zip"  # Unique zip file for each state and type
        url = base_url.format(state=state, desonerado=type_)
        print(f"Downloading ZIP file from {url}...")
        download_zip_file(url, specific_zip_path)

        # Try both .xlsx and .xls extensions
        xls_name = f"SINAPI_Preco_Ref_Insumos_{upper_state}_202311_{type_}.xlsx"
        xls_fallback_name = f"SINAPI_Preco_Ref_Insumos_{upper_state}_202311_{type_}.xls"
        print(f"Attempting to extract {xls_name} or {xls_fallback_name} from ZIP...")

        extract_xls_from_zip(specific_zip_path, extract_path, xls_name, xls_fallback_name)
        xls_path = f"{extract_path}/{xls_name}"

        print("Reading XLS file {}...".format(xls_path))
        read_xls_and_update_json(xls_path, json_path, upper_state, type_)
        print("Updated JSON file {}".format(json_path))

        time.sleep(60)

print("All done!")

import os
import json
import django
from django.db import transaction

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Insumo  # Importing the Insumo model

# Load JSON data
with open('output.json', 'r') as f:
    data = json.load(f)

# Atomic database transaction
with transaction.atomic():
    for codigo, detaileddescription in data.items():
        codigo = str(codigo).strip()  # Converting to str and removing leading/trailing whitespace

        # Check if Insumo with this 'codigo' exists
        try:
            insumo_instance = Insumo.objects.get(codigo=codigo)
        except Insumo.DoesNotExist:
            print(f"No Insumo with codigo {codigo} found.")
            continue

        # Update the 'detaileddescription'
        insumo_instance.detaileddescription = detaileddescription
        insumo_instance.save()
        print(f"Insumo with codigo {codigo} updated.")

print("Insumo descriptions have been updated.")

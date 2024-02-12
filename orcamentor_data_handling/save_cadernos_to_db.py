import os
import json
import django
from django.db import transaction

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinapi.settings')
django.setup()

from compositions.models import Composition  # Importing the Insumo model

# Load JSON data
with open('cadernos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Atomic database transaction
with transaction.atomic():
    for filename, compositions in data.items():
        for composition in compositions:
            codigo = str(composition["codigo"]).strip()  # Converting to str and removing leading/trailing whitespace

            # Check if Composition with this 'codigo' exists
            try:
                composition_instance = Composition.objects.get(codigo=codigo)
            except Composition.DoesNotExist:
                print(f"No Composition with codigo {codigo} found.")
                continue

            # Update the caderno tecnico fields
            composition_instance.ct_itens = composition["itens"]
            composition_instance.ct_equipamento = composition["equipamento"]
            composition_instance.ct_quantificacao = composition["quantificacao"]
            composition_instance.ct_afericao = composition["afericao"]
            composition_instance.ct_execucao = composition["execucao"]
            composition_instance.ct_complementares = composition["complementares"]

            composition_instance.save()
            print(f"Composition with codigo {codigo} updated.")

print("Composition caderno tecnico fields have been updated.")

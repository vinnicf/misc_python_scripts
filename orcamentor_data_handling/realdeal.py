import json
import ast


def load_txt_list(file_name):
    with open(file_name, "r") as f:
        data = f.read().strip()
        return ast.literal_eval(data)


# 1. Load registered compositions and insumos from .txt files
print("Loading registered compositions and insumos...")
registered_compositions = set(map(str, load_txt_list("compositions.txt")))
registered_insumos = set(map(str, load_txt_list("insumos.txt")))


# 2. Load the compositions data from the JSON file
print("Loading compositions from JSON file...")
with open("transformed_data.json", "r") as f:
    compositions = json.load(f)

# 3. Check each parent composition and their children
print("Checking each composition and their children...")
compositions_to_register = []

for comp in compositions:
    all_children_registered = True


    if comp["codigo"] == 96547:  # Specific debug for this composition
        print("Debugging composition 96547...")
        if str(comp["codigo"]) in registered_compositions:
            print("Composition 96547 is already registered!")

        for child in comp["children"]:
            if child["type"] == "COMPOSICAO" and str(child["codigo"]) not in registered_compositions:
                print(f"Child composition {child['codigo']} of 96547 not found in registered_compositions.")
            elif child["type"] == "INSUMO" and str(child["codigo"]) not in registered_insumos:
                print(f"Insumo {child['codigo']} of 96547 not found in registered_insumos.")



    # Check if the parent composition is already registered
    if str(comp["codigo"]) in registered_compositions:
        print(f"  Parent comp already reg: {comp['codigo']}")
        continue  # Skip this parent composition and move to the next one



    for child in comp["children"]:
        if child["type"] == "COMPOSICAO":
            print(f"  Checking child comp: {child['codigo']}")
            if str(child["codigo"]) not in registered_compositions:
                all_children_registered = False
                print(f"    Composicao Not registered: {child['codigo']}")
                break

        elif child["type"] == "INSUMO":
            print(f"  Checking child insumo: {child['codigo']}")
            if str(child["codigo"]) not in registered_insumos:
                all_children_registered = False
                print(f"    Insumo Not registered: {child['codigo']}")
                break


    if all_children_registered:
        print("  All children are registered.")
        compositions_to_register.append(comp)



# 4. Save the compositions that passed the check to a new JSON file
print("\nSaving compositions that passed the check...")
with open("compositions_to_register.json", "w") as f:
    json.dump(compositions_to_register, f, indent=4)

print(f"Saved {len(compositions_to_register)} compositions to 'compositions_to_register.json'")

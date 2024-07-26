import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    owner = controller = add_core = None
    
    # Wyszukaj interesujące linie i zidentyfikuj litery oraz cyfry
    for line in lines:
        if line.startswith("owner = "):
            owner = line.strip().split(' = ')[1]
        elif line.startswith("controller = "):
            controller = line.strip().split(' = ')[1]
        elif line.startswith("add_core = "):
            add_core = line.strip().split(' = ')[1]

    if owner and controller and add_core:
        # Wyszukaj literę i zamień cyfry na 00
        letter = owner[0]
        new_tag = f"{letter}00"

        # Dodaj nową sekcję na końcu pliku
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write("\n1444.11.13 = {\n")
            file.write(f"remove_core = {owner}\n")
            file.write(f"add_core = {new_tag}\n")
            file.write(f"owner = {new_tag}\n")
            file.write(f"controller = {new_tag}\n")
            file.write("}\n")

def process_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            process_file(filepath)

# Użycie skryptu
directory_path = 'C:/Users/oskar/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/Gmina Universalis/history/provinces'
process_directory(directory_path)

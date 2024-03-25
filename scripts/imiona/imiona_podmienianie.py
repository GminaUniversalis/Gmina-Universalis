import os
import re

# Ścieżki
base_script_path = r"C:\Users\oskar\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\Gmina Universalis\scripts\imiona"
base_countries_config_path = r"C:\Users\oskar\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\Gmina Universalis\common\countries"
gmina_countries_file = os.path.join(base_script_path, "00_gmina_countries.txt")

# Wczytaj plik z mapowaniem gmin
gmina_map = {}
with open(gmina_countries_file, 'r', encoding='utf-8') as file:
    for line in file:
        if match := re.match(r"([A-Z])00 = \"countries/(.*?)\.txt\"", line):
            letter, wojewodztwo = match.groups()
            gmina_map[letter] = wojewodztwo

# Funkcja do aktualizacji plików konfiguracyjnych krajów
def update_country_configs(letter, wojewodztwo):
    config_path = os.path.join(base_countries_config_path, f"{wojewodztwo}.txt")
    script_path = os.path.join(base_script_path, f"{wojewodztwo}.py")

    # Sprawdź, czy istnieje odpowiedni plik skryptu
    if not os.path.exists(script_path):
        print(f"Brak pliku skryptu dla: {wojewodztwo}")
        return

    # Wczytaj zawartość skryptu
    with open(script_path, 'r', encoding='utf-8') as script_file:
        script_content = script_file.read()

    # Aktualizuj plik konfiguracyjny
    if os.path.exists(config_path):
        with open(config_path, 'r+', encoding='utf-8') as config_file:
            content = config_file.read()

            # Znajdź i zastąp sekcje monarch_names i leader_names
            content = re.sub(r"(monarch_names = {)[^}]*}", r"\1\n" + script_content + "\n}", content)
            content = re.sub(r"(leader_names = {)[^}]*}", r"\1\n" + script_content + "\n}", content)

            # Zapisz zmodyfikowaną zawartość
            config_file.seek(0)
            config_file.write(content)
            config_file.truncate()
    else:
        print(f"Brak pliku konfiguracyjnego dla: {wojewodztwo}")

# Iteruj przez mapowanie gmin i aktualizuj pliki
for letter, wojewodztwo in gmina_map.items():
    update_country_configs(letter, wojewodztwo)

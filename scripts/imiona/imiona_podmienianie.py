import os
import re

# Ścieżki
base_script_path = r"C:\Users\oskar\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\Gmina Universalis\scripts\imiona"
base_countries_config_path = r"C:\Users\oskar\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\Gmina Universalis\common\countries"
gmina_countries_file = os.path.join(base_script_path, "00_gmina_countries.txt")

# Wczytaj plik z mapowaniem gmin
print("Wczytywanie mapowania gmin...")
gmina_map = {}
with open(gmina_countries_file, 'r', encoding='utf-8') as file:
    for line in file:
        match = re.match(r"([A-Z])\d\d = \"countries/(.*?)\.txt\"", line)
        if match:
            letter, path = match.groups()
            wojewodztwo_name = path.split('/')[-1].replace('.txt', '')
            gmina_map[wojewodztwo_name] = letter
            print(f"Dodano mapowanie: {letter} -> {wojewodztwo_name}")

# Pobierz listę wszystkich plików ze skryptami
script_files = [file.split('.')[0] for file in os.listdir(base_script_path) if file.endswith('.py')]
print("Lista plików ze skryptami:", script_files)

def get_script_content(wojewodztwo):
    script_path = os.path.join(base_script_path, f"{wojewodztwo}.py")
    if not os.path.exists(script_path):
        print(f"Brak pliku skryptu dla: {wojewodztwo}")
        return None

    with open(script_path, 'r', encoding='utf-8') as script_file:
        return script_file.read()

def update_country_configs(letter, wojewodztwo):
    script_content = get_script_content(wojewodztwo)
    if script_content is None:
        return

    updated = False  # Flaga wskazująca, czy plik został zaktualizowany

    for root, dirs, files in os.walk(base_countries_config_path):
        for file_name in files:
            # Sprawdź, czy nazwa pliku zawiera nazwę województwa
            if wojewodztwo in file_name:
                config_path = os.path.join(root, file_name)
                print(f"Aktualizacja pliku: {config_path}")
                with open(config_path, 'r+', encoding='utf-8') as config_file:
                    content = config_file.read()

                    # Zaktualizuj lub dodaj monarch_names
                    if "monarch_names = {" in content:
                        content = re.sub(r"monarch_names = \{[^\}]*\}", f"monarch_names = {{\n{script_content}\n}}", content, flags=re.DOTALL)
                    else:
                        content += f"\nmonarch_names = {{\n{script_content}\n}}\n"

                    # Zaktualizuj lub dodaj leader_names
                    if "leader_names = {" in content:
                        content = re.sub(r"leader_names = \{[^\}]*\}", f"leader_names = {{\n{script_content}\n}}", content, flags=re.DOTALL)
                    else:
                        content += f"\nleader_names = {{\n{script_content}\n}}\n"

                    config_file.seek(0)
                    config_file.write(content)
                    config_file.truncate()

                    updated = True  # Plik został zaktualizowany

    if not updated:
        print(f"Nie zmieniono pliku dla: {wojewodztwo}")

# Dodatkowa funkcja do śledzenia niezmodyfikowanych plików
def track_unmodified_files(script_files, gmina_map):
    for wojewodztwo, letter in gmina_map.items():
        if wojewodztwo in script_files:
            update_country_configs(letter, wojewodztwo)
            script_files.remove(wojewodztwo)  # Usuń przetworzony plik ze śledzenia
    for unmodified_file in script_files:
        print(f"Nie zmieniono pliku skryptu dla: {unmodified_file}")

track_unmodified_files(script_files, gmina_map)

print("Zakończono aktualizację plików konfiguracyjnych.")

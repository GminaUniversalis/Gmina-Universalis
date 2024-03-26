import os
import re

# Ścieżka do folderu z plikami konfiguracyjnymi krajów
config_folder = "C:\\Users\\oskar\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\Gmina Universalis\\common\\countries"

# Ścieżka do folderu z listami imion
names_folder = os.path.dirname(os.path.abspath(__file__))

# Funkcja do odczytywania listy imion z pliku
def read_names_list(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        names = file.readlines()
    # Usunięcie białych znaków i pustych linii
    names = [name.strip() for name in names if name.strip()]
    return names


# Funkcja do aktualizowania pliku konfiguracyjnego kraju
def update_country_config(file_path, names_list):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Znajdź sekcje z imionami w pliku konfiguracyjnym
    monarch_names_section = re.search(r"monarch_names\s*=\s*\{.*?\}", content, re.DOTALL)
    leader_names_section = re.search(r"leader_names\s*=\s*\{.*?\}", content, re.DOTALL)

    if monarch_names_section:
        # Zastąp istniejące imiona nową listą
        updated_monarch_names = 'monarch_names = {\n' + '\n'.join(names_list) + '\n}'
        content = re.sub(monarch_names_section.group(0), updated_monarch_names, content)

    if leader_names_section:
        # Zastąp istniejące imiona nową listą
        updated_leader_names = 'leader_names = {\n' + '\n'.join(names_list) + '\n}'
        content = re.sub(leader_names_section.group(0), updated_leader_names, content)

    # Zapisz zaktualizowany plik
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Funkcja do odczytywania tagów województw z pliku 00_gmina_countries.txt
def read_region_tags(file_path):
    region_tags = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                tag, region = line.split("=")
                tag = tag.strip()
                region = region.strip().replace('"', '')  # Usunięcie cudzysłowów
                region_tags[tag] = region
    return region_tags

# Ścieżka do pliku 00_gmina_countries.txt
file_path = "00_gmina_countries.txt"

# Wczytaj tagi województw
region_tags = read_region_tags(file_path)

# Wydrukuj region_tags
print(region_tags)


# Pobierz tagi województw
region_tags = read_region_tags("00_gmina_countries.txt")

# Liczniki
total_files = 0
modified_files = 0

# Przetwarzanie każdego kraju
for filename in os.listdir(config_folder):
    if filename.endswith(".txt"):
        total_files += 1
        country_file_path = os.path.join(config_folder, filename)
        # Pobierz tag kraju z nazwy pliku
        country_tag = filename.split(".")[0]
        # Sprawdź, czy istnieje plik konfiguracyjny dla tego kraju
        if os.path.exists(country_file_path):
            # Sprawdź, czy dla tego kraju istnieje przypisane województwo
            if country_tag[:3] in region_tags:
                region_file = os.path.join(names_folder, region_tags[country_tag[:3]] + ".py")
                # Sprawdź, czy istnieje plik z listą imion dla tego województwa
                if os.path.exists(region_file):
                    # Wczytaj listę imion dla danego województwa
                    names_list = read_names_list(region_file)
                    # Zaktualizuj plik konfiguracyjny kraju
                    update_country_config(country_file_path, names_list)
                    modified_files += 1
                    print(f"Aktualizacja pliku konfiguracyjnego dla {filename} zakończona.")
                else:
                    print(f"Brak pliku z listą imion dla województwa przypisanego do {filename}.")
            else:
                print(f"Brak przypisanego województwa dla {filename}.")
        else:
            print(f"Plik konfiguracyjny dla {filename} nie istnieje.")

# Podsumowanie
print(f"\nPodsumowanie:")
print(f"Liczba plików do modyfikacji: {total_files}")
print(f"Liczba zmodyfikowanych plików: {modified_files}")
print(f"Liczba pozostałych do modyfikacji: {total_files - modified_files}")




# print(f"Regiontag: {region_tags}")
print(f"Regiontag: {names_list}")
import os
import re

# Funkcja do przekształcenia nazwisk
def transform_name(name):
    return name.capitalize()

# Szukana nazwa zmiennej
target_variable = "monarch_names"

# Pobranie ścieżki do bieżącego katalogu
current_directory = os.getcwd()

# Lista plików w bieżącym folderze
files = [os.path.join(current_directory, f) for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f)) and not f.endswith('.py')]

# Przeszukiwanie plików
for file_name in files:
    with open(file_name, 'r+', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(rf"{target_variable}\s*=\s*{{([^}}]+)}}", re.DOTALL)
        matches = pattern.findall(content)
        if matches:
            for match in matches:
                replaced_match = re.sub(r'"([^"]+)"', lambda x: f'"{transform_name(x.group(1))}"', match)
                new_content = content.replace(match, replaced_match)
            file.seek(0)
            file.write(new_content)
            file.truncate()

print("Zakończono przetwarzanie plików.")

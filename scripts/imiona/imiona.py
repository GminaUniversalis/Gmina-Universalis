import os
import re

# Ścieżka do bieżącego folderu
folder_path = os.getcwd()

# Kompilacja wzorca wyrażenia regularnego do wyszukiwania klamry
pattern = re.compile(r'monarch_names\s*=\s*{([^}]*)}', re.DOTALL)

# Funkcja do konwersji imion na małe litery z pierwszą dużą literą
def convert_to_lowercase(match):
    names = match.group(1)
    names_lower = "\n".join([name.capitalize() for name in names.split('\n')])
    return f'monarch_names = {{\n{names_lower}\n}}'

# Przechodzenie przez wszystkie pliki w bieżącym katalogu
for filename in os.listdir(folder_path):
    # Sprawdzenie, czy element jest plikiem (a nie katalogiem)
    if os.path.isfile(filename):
        try:
            # Otwarcie i odczytanie pliku
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                # Szukanie wzorca w zawartości pliku
                match = pattern.search(content)
                if match:
                    # Konwersja imion na małe litery z pierwszą dużą literą
                    modified_content = pattern.sub(convert_to_lowercase, content)
                    print(f'Znaleziono "monarch_names" w pliku: {filename}')
                    print('Zawartość po konwersji imion na małe litery z pierwszą dużą literą:')
                    print(modified_content)
        except UnicodeDecodeError:
            print(f'Nie można odczytać pliku {filename} z powodu błędu kodowania.')
        except Exception as e:
            print(f'Wystąpił błąd przy próbie odczytu pliku {filename}: {e}')

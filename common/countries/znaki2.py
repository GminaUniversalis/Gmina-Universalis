import os
import codecs

# Definicja mapowania znaków
character_map = {
    'Ą': '¥',
    'ą': '¹',
    'Ń': '¼',
    'ń': 'ª',
    'Ł': 'µ',
    'ł': '³',
    'Ż': '¯',
    'ż': '¿',
    'Ź': 'Ä',
    'ź': 'Ÿ',
    'Ś': 'Œ',
    'ś': 'œ',
    'Ć': '¶',
    'ć': '¾',
    'Ę': '‡',
    'ę': '²'
}

# Ścieżka do folderu z plikami
folder_path = '.'  # Aktualny folder, można zmienić na inny folder

# Iteracja przez pliki w folderze
for filename in os.listdir(folder_path):
    if filename != 'znaki.py' and os.path.isfile(os.path.join(folder_path, filename)):
        print(f"Przetwarzanie pliku: {filename}")

        # Odczyt zawartości pliku z kodowaniem 'latin-1' (Windows-1252)
        with codecs.open(os.path.join(folder_path, filename), 'r', encoding='latin-1') as file:
            content = file.read()

        # Zamiana znaków z drugiej kolumny na odpowiadające im znaki z pierwszej kolumny
        modified_content = ''
        for char in content:
            modified_char = character_map.get(char)
            if modified_char is not None:
                modified_content += modified_char
            else:
                modified_content += char  # Pozostawiamy nieznane znaki bez zmiany

        # Zapis zmodyfikowanego pliku z kodowaniem 'latin-1' (Windows-1252)
        with codecs.open(os.path.join(folder_path, filename), 'w', encoding='Windows-1252', errors='ignore') as file:
            file.write(modified_content)

print("Zamiana zakończona.")

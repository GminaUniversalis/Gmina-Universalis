import os

# Ścieżka do folderu z plikami (tutaj bieżący folder)
folder_path = '.'

# Wczytaj zawartość pliku nazwiska.txt
try:
    with open(os.path.join(folder_path, 'nazwiska.txt'), 'r', encoding='utf-8') as file:
        nazwiska_lines = file.readlines()
except FileNotFoundError:
    print("Plik nazwiska.txt nie został znaleziony.")
    exit()

# Przygotuj zawartość do wstawienia - każde nazwisko zmodyfikowane i rozdzielone spacjami
nazwiska_content = " ".join(f"'{line.strip().capitalize()}': ''" for line in nazwiska_lines if line.strip())

# Przejście przez wszystkie pliki .txt w folderze, oprócz nazwiska.txt
for filename in os.listdir(folder_path):
    if filename.endswith('.txt') and filename != 'nazwiska.txt':
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()

            # Sprawdź, czy w pliku znajduje się słownik leader_names
            if 'leader_names = {' in content:
                # Wyszukaj i zastąp istniejący słownik nową zawartością
                start_index = content.find('leader_names = {') + len('leader_names = {')
                end_index = content.find('}', start_index)
                updated_content = content[:start_index] + nazwiska_content + content[end_index:]
            else:
                # Dodaj słownik leader_names na końcu pliku, jeśli nie istnieje
                updated_content = content + f'\nleader_names = {{{nazwiska_content}}}'
            
            # Zapisz zmodyfikowaną zawartość do pliku
            file.seek(0)
            file.write(updated_content)
            file.truncate()

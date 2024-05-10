import os

# Ustawienie ścieżki względnej do folderu z plikami
directory_path = os.path.join(os.path.dirname(__file__), '..', 'history', 'provinces')

def modify_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='utf-8') as file:
                content = file.readlines()
                trade_goods_value = None
                has_unknown_trade_good = False

                for line in content:
                    if 'trade_goods =' in line:
                        trade_goods_value = line.split('=')[1].strip()
                        # Sprawdź, czy wartość trade_goods nie jest 'unknown'
                        if trade_goods_value == 'unknown':
                            trade_goods_value = None
                            has_unknown_trade_good = True
                            break  # Przejdź do następnego pliku

                if trade_goods_value or has_unknown_trade_good:
                    # Usuń obecne linie set_province_flag
                    content = [line for line in content if 'set_province_flag = has_' not in line]

                    if not has_unknown_trade_good:
                        # Dodaj nowe linie, jeśli wartość trade_goods nie jest 'unknown'
                        content.append('set_province_flag = has_static_trade_good\n')
                        content.append(f'set_province_flag = has_{trade_goods_value}_trade_good\n')

                    # Zapis zmodyfikowanej zawartości
                    file.seek(0)
                    file.writelines(content)
                    file.truncate()

# Uruchomienie funkcji
modify_files_in_directory(directory_path)

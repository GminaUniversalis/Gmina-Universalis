import csv

# Słownik przyporządkowujący kody województw do ich nazw
wojewodztwa = {
    "02": "Dolnoslaskie",
    "04": "Kujawsko-Pomorskie",
    "06": "Lubelskie",
    "08": "Lubuskie",
    "10": "Lodzkie",
    "12": "Malopolskie",
    "14": "Mazowieckie",
    "16": "Opolskie",
    "18": "Podkarpackie",
    "20": "Podlaskie",
    "22": "Pomorskie",
    "24": "Slaskie",
    "26": "Swietokrzyskie",
    "28": "Warminsko-Mazurskie",
    "30": "Wielkopolskie",
    "32": "Zachodniopomorskie",
}

# Funkcja do przetwarzania plików CSV
def przetwarzaj_plik(sciezka_pliku, is_female):
    with open(sciezka_pliku, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # Pomija nagłówek
        for row in reader:
            woj = row[0]
            imie = row[1]
            liczba = int(row[2]) * (-1 if is_female else 1)
            if woj in wojewodztwa:
                nazwa_pliku = wojewodztwa[woj] + ".py"
                with open(nazwa_pliku, "a", encoding='utf-8') as plik:
                    plik.write(f'"{imie}" = {liczba}\n')

# Przetwarzanie plików
przetwarzaj_plik("imiona_damskie.csv", True)
przetwarzaj_plik("imiona_meskie.csv", False)

#Dziala z plikiem prov_names_l_english.ymllocalisation\prov_names_l_english.yml

def main():
    input_file_name = input("Podaj nazwę pliku wejściowego: ")
    output_file_name = input("Podaj nazwę pliku wynikowego: ")

    try:
        with open(input_file_name, 'r') as input_file:
            lines = input_file.readlines()
    except FileNotFoundError:
        print("Nie można znaleźć podanego pliku wejściowego.")
        return

    print("Wczytano zawartość pliku wejściowego.")

    prov_values_dict = {}

    for line in lines:
        if "PROV" in line and ":0" in line:
            prov_start = line.find("PROV")
            prov_end = line.find(":0", prov_start)
            if prov_start != -1 and prov_end != -1:
                text_between_prov_and_0 = line[prov_start + len("PROV"):prov_end]
                # Usuwamy tekst wewnątrz cudzysłowów przed analizą
                while '"' in text_between_prov_and_0:
                    start_quote = text_between_prov_and_0.find('"')
                    end_quote = text_between_prov_and_0.find('"', start_quote + 1)
                    if start_quote != -1 and end_quote != -1:
                        text_between_prov_and_0 = text_between_prov_and_0[:start_quote] + text_between_prov_and_0[end_quote + 1:]

                prov_values = text_between_prov_and_0.split()
                filtered_prov_values = []

                for value in prov_values:
                    if '"' not in value:
                        filtered_prov_values.append(value)

                # Konwertujemy listę wartości na string, aby móc ją użyć jako klucz w słowniku
                prov_values_str = " ".join(filtered_prov_values)

                # Jeśli dany zestaw wartości po słowie "PROV" już istnieje w słowniku, dodajemy linię do wynikowego pliku
                if prov_values_str in prov_values_dict:
                    prov_values_dict[prov_values_str].append(line)
                # W przeciwnym razie dodajemy nowy zestaw wartości do słownika i zapisujemy linię
                else:
                    prov_values_dict[prov_values_str] = [line]

    # Wybieramy tylko te linie, które mają więcej niż jedno wystąpienie zestawu wartości
    filtered_lines = [line for values_list in prov_values_dict.values() if len(values_list) > 1 for line in values_list]

    try:
        with open(output_file_name, 'w') as output_file:
            output_file.writelines(filtered_lines)
    except Exception as e:
        print("Wystąpił błąd podczas zapisywania do pliku wynikowego:", e)
        return

    print("Zapisano przefiltrowane linie do pliku", output_file_name)

if __name__ == "__main__":
    main()

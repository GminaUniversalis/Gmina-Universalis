def process_file(input_file, output_file):
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        for line in f_input:
            # Usunięcie białych znaków na początku i na końcu linii
            line = line.strip()
            
            # Sprawdzenie, czy linia rozpoczyna się od "PROV"
            if line.startswith("PROV"):
                # Dodanie "_ADJ" po słowie "PROV"
                line_with_adj = line.replace("PROV", "PROV_ADJ", 1)
                
                # Zapisanie oryginalnej linii
                f_output.write(line + '\n')
                # Zapisanie linii z "_ADJ"
                f_output.write(line_with_adj + '\n')
            else:
                # Jeśli linia nie rozpoczyna się od "PROV", zachowaj ją bez zmian
                f_output.write(line + '\n')

if __name__ == "__main__":
    input_file = input("Podaj nazwę pliku wejściowego: ")
    output_file = input("Podaj nazwę pliku wyjściowego: ")
    process_file(input_file, output_file)
    print("Operacja zakończona pomyślnie.")

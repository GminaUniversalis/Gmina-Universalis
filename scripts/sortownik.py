def main():
    input_file_name = input("Podaj nazwę pliku wejściowego: ")
    output_file_name = input("Podaj nazwę pliku wynikowego: ")

    try:
        with open(input_file_name, 'r') as input_file:
            numbers = [line.strip() for line in input_file.readlines()]
    except FileNotFoundError:
        print("Nie można znaleźć podanego pliku wejściowego.")
        return
    
    numbers.sort()

    try:
        with open(output_file_name, 'w') as output_file:
            output_file.write(' '.join(numbers))
    except Exception as e:
        print("Wystąpił błąd podczas zapisywania do pliku wynikowego:", e)
        return

    print("Liczby zostały posortowane i zapisane do pliku", output_file_name)

if __name__ == "__main__":
    main()

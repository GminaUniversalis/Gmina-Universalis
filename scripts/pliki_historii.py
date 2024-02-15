#Wymaga listi prowincji (ID Nazwa)
def generate_files_from_list(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split('-')
        if len(parts) == 2:
            number, name = parts
            file_name = f"{number.strip()}-{name.strip()}.txt"
            with open(file_name, 'w') as new_file:
                new_file.write("discovered_by = western\n")
                new_file.write("discovered_by = eastern\n")
                new_file.write("discovered_by = ottoman\n")

generate_files_from_list("lista.txt")
import os
from pathlib import Path

def load_tags_and_paths(filename):
    """Wczytuje informacje, tworząc mapowanie liter do nazw plików oraz liter do województw."""
    tag_to_files = {}
    tag_to_wojewodztwo = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if "=" in line:
                tag, path = line.split("=")
                tag = tag.strip()
                path = Path(path.strip().strip('"'))
                first_letter = tag[0]
                if first_letter not in tag_to_files:
                    tag_to_files[first_letter] = []
                tag_to_files[first_letter].append(path)
                if "województwo".lower() in path.stem.lower() or tag.endswith("00"):  # Zakładamy, że to jest województwo
                    tag_to_wojewodztwo[first_letter] = path.stem
    return tag_to_files, tag_to_wojewodztwo

def find_brackets(content, keyword):
    """Znajduje indeksy otwierającej i zamykającej klamry dla podanego słowa kluczowego."""
    opening_bracket_index = content.find(f"{keyword} = {{")

    if opening_bracket_index == -1:
        return None, None

    # Szukamy zamykającej klamry
    bracket_level = 1
    index = opening_bracket_index + len(keyword) + 2
    while index < len(content):
        if content[index] == '{':
            bracket_level += 1
        elif content[index] == '}':
            bracket_level -= 1
            if bracket_level == 0:
                return opening_bracket_index, index
        index += 1

    # Nie znaleziono zamykającej klamry
    return None, None

def remove_existing_brackets(content, keyword):
    """Usuwa istniejące klamry i komentarze nad nimi."""
    opening_index, closing_index = find_brackets(content, keyword)
    if opening_index is not None and closing_index is not None:
        return content[:opening_index] + content[closing_index + 1:]
    else:
        return content

def update_country_files(tag_to_files, tag_to_wojewodztwo, base_countries_path, base_names_path):
    for tag, files in tag_to_files.items():
        wojewodztwo_name = tag_to_wojewodztwo.get(tag, None)
        if wojewodztwo_name:
            for file_path in files:
                country_file_path = base_countries_path / file_path.relative_to("countries")
                names_file_path = base_names_path / f"{wojewodztwo_name}.txt"
                if country_file_path.exists() and names_file_path.exists():
                    with open(names_file_path, 'r', encoding='utf-8') as names_file:
                        names_content = names_file.readlines()

                    with open(country_file_path, 'r', encoding='utf-8') as country_file:
                        content = country_file.readlines()

                    with open(country_file_path, 'w', encoding='utf-8') as country_file:
                        found_monarch_names = False
                        found_leader_names = False
                        for line in content:
                            # Sprawdź, czy linia zawiera monarch_names lub leader_names
                            if "monarch_names" in line:
                                found_monarch_names = True
                            elif "leader_names" in line:
                                found_leader_names = True

                            # Jeśli znaleziono jedno z nich, zignoruj kolejne linie aż do zamknięcia klamry
                            if found_monarch_names or found_leader_names:
                                if "}" in line:
                                    found_monarch_names = False
                                    found_leader_names = False
                                continue
                            else:
                                # Sprawdź, czy linia zawiera komentarz związany z monarch_names lub leader_names
                                if "#" in line and ("monarch_names" in line or "leader_names" in line):
                                    if "# Lista imion z pliku:" in line:
                                        continue
                                    else:
                                        country_file.write(line)
                                else:
                                    country_file.write(line)

                        # Dodaj nowe imiona
                        country_file.write("\n# Lista imion z pliku: {}\n".format(names_file_path.name))

                        country_file.write("monarch_names = {\n")
                        for name in names_content:
                            country_file.write(f'    {name.strip()}\n')
                        country_file.write("}\n")

                        country_file.write("\nleader_names = {\n")
                        for name in names_content:
                            country_file.write(f'    {name.strip()}\n')
                        country_file.write("}\n")

                    print(f"Updated names in {country_file_path}")
                else:
                    if not country_file_path.exists():
                        print(f"Country file not found: {country_file_path}")
                    if not names_file_path.exists():
                        print(f"Names file not found: {names_file_path}")
                    if country_file_path.exists() and not names_file_path.exists():
                        with open(country_file_path, 'a', encoding='utf-8') as country_file:
                            country_file.write("# Lista imion z pliku: {}\n".format(names_file_path.name))
                            country_file.write("monarch_names = {\n")
                            for name in names_content:
                                country_file.write(f'    {name.strip()}\n')
                            country_file.write("}\n")

                            country_file.write("\nleader_names = {\n")
                            for name in names_content:
                                country_file.write(f'    {name.strip()}\n')
                            country_file.write("}\n")
                        print(f"Updated names in {country_file_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    base_countries_path = Path("C:/Users/oskar/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/Gmina Universalis/common/countries")
    base_names_path = script_dir.parent / "imiona"

    tags_file_path = script_dir / "00_gmina_countries.txt"
    tag_to_files, tag_to_wojewodztwo = load_tags_and_paths(tags_file_path)

    update_country_files(tag_to_files, tag_to_wojewodztwo, base_countries_path, base_names_path)

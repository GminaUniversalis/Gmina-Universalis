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

def update_country_files(tag_to_files, tag_to_wojewodztwo, base_countries_path, base_names_path):
    for tag, files in tag_to_files.items():
        wojewodztwo_name = tag_to_wojewodztwo.get(tag, None)
        if wojewodztwo_name:
            for file_path in files:
                country_file_path = base_countries_path / file_path.relative_to("countries")
                names_file_path = base_names_path / f"{wojewodztwo_name}.txt"
                if country_file_path.exists() and names_file_path.exists():
                    with open(names_file_path, 'r', encoding='utf-8') as names_file:
                        names_content = names_file.read()

                    with open(country_file_path, 'r+', encoding='utf-8') as country_file:
                        content = country_file.read()
                        
                        # Sprawdzamy, czy klamry monarch_names i leader_names istnieją
                        monarch_opening_index, monarch_closing_index = find_brackets(content, "monarch_names")
                        leader_opening_index, leader_closing_index = find_brackets(content, "leader_names")

                        # Aktualizujemy zawartość klamr lub dodajemy je, jeśli nie istnieją
                        updated_content = content
                        if monarch_opening_index is not None and monarch_closing_index is not None:
                            updated_content = (
                                content[:monarch_opening_index] +
                                f"# Lista imion z pliku: {names_file_path.name}\n" +
                                f"monarch_names = {{\n{names_content}\n}}\n" +
                                content[monarch_closing_index + 1:]
                            )
                        else:
                            updated_content += f"# Lista imion z pliku: {names_file_path.name}\n"
                            updated_content += f"monarch_names = {{\n{names_content}\n}}\n"

                        if leader_opening_index is not None and leader_closing_index is not None:
                            updated_content = (
                                content[:leader_opening_index] +
                                f"leader_names = {{\n{names_content}\n}}\n" +
                                content[leader_closing_index + 1:]
                            )
                        else:
                            updated_content += f"leader_names = {{\n{names_content}\n}}\n"

                        # Zapisujemy zmienioną zawartość do pliku
                        country_file.seek(0)
                        country_file.write(updated_content)
                        country_file.truncate()
                        print(f"Updated names in {country_file_path}")
                else:
                    if not country_file_path.exists():
                        print(f"Country file not found: {country_file_path}")
                    if not names_file_path.exists():
                        print(f"Names file not found: {names_file_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    base_countries_path = Path("C:/Users/oskar/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/Gmina Universalis/common/countries")
    base_names_path = script_dir.parent / "imiona"

    tags_file_path = script_dir / "00_gmina_countries.txt"
    tag_to_files, tag_to_wojewodztwo = load_tags_and_paths(tags_file_path)

    update_country_files(tag_to_files, tag_to_wojewodztwo, base_countries_path, base_names_path)

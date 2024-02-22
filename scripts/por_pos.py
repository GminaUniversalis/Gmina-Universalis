import re

def read_positions(file_path):
    positions = {}
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = re.compile(r'(\d+)={\s*position={([\d.\s]+)}', re.DOTALL)
    matches = pattern.findall(content)

    for match in matches:
        id, position_values = match
        positions[int(id)] = list(map(float, position_values.split()))

    return positions

def find_same_positions(old_positions, new_positions, ids_to_ignore):
    same_positions = []
    changed_positions = []
    for id, old_position in old_positions.items():
        if id in new_positions:
            if old_position == new_positions[id] and id not in ids_to_ignore:
                same_positions.append(id)
            elif id not in ids_to_ignore:
                changed_positions.append(id)
    return same_positions, changed_positions

def read_ids_to_ignore(file_path):
    ids_to_ignore = set()
    with open(file_path, 'r') as file:
        for line in file:
            ids_in_line = line.strip().split()
            for id_str in ids_in_line:
                if id_str.isdigit():
                    ids_to_ignore.add(int(id_str))
    return ids_to_ignore

def main():
    old_positions_path = 'positions_old.txt'
    new_positions_path = 'positions.txt'
    ids_to_ignore_path = 'ids_to_ignore.txt'
    output_path = 'same_positions.txt'
    changed_positions_output_path = 'changed_positions.txt'

    old_positions = read_positions(old_positions_path)
    new_positions = read_positions(new_positions_path)
    ids_to_ignore = read_ids_to_ignore(ids_to_ignore_path)

    same_positions, changed_positions = find_same_positions(old_positions, new_positions, ids_to_ignore)

    total_ids = len(set(old_positions.keys()) | set(new_positions.keys()))
    ignored_count = len(ids_to_ignore)
    unchanged_ids = len(same_positions)
    changed_ids = len(changed_positions)
    total_effective_ids = total_ids - ignored_count
    total_changed_and_same = changed_ids + unchanged_ids
    percentage_changed = (changed_ids / (total_ids - ignored_count)) * 100 if total_ids - ignored_count > 0 else 0
    percentage_changed_including_ignored = (changed_ids / total_ids) * 100 if total_ids > 0 else 0

    with open(output_path, 'w') as output_file:
        output_file.write(f"Total IDs: {total_ids}\n")
        output_file.write(f"Ignored IDs: {ignored_count}\n")
        output_file.write(f"Unchanged IDs (excluding ignored): {unchanged_ids}\n")
        output_file.write(f"Changed IDs (excluding ignored): {changed_ids}\n")
        output_file.write(f"Percentage of changed IDs (excluding ignored): {percentage_changed:.2f}%\n")
        output_file.write(f"Percentage of changed IDs (including ignored): {percentage_changed_including_ignored:.2f}%\n")
        output_file.write("\nList of IDs with same positions:\n")
        for id in same_positions:
            output_file.write(f"{id}\n")

    with open(changed_positions_output_path, 'w') as changed_positions_output_file:
        changed_positions_output_file.write("List of IDs with changed positions:\n")
        for id in changed_positions:
            changed_positions_output_file.write(f"{id}\n")

    print(f"Wszystkie prowincje {total_ids}")
    print(f"Ilość ignorowanych prov: {ignored_count}")
    print(f"Niezmienione prov: {unchanged_ids}")
    print(f"Ilość zrobionych prowincji: {changed_ids}")
    print(f"Prowincje bez prov morskich/wastelandów: {total_effective_ids}")
    print(f"Zrobione procentowo (bez ignorowanych): {percentage_changed:.2f}%")
    print(f"Zrobione procentowo (z ignorowanymi): {percentage_changed_including_ignored:.2f}%")
    print(f"Zapisano do: {output_path}")
    print(f"Zapisano zmienione do: {changed_positions_output_path}")

if __name__ == "__main__":
    main()


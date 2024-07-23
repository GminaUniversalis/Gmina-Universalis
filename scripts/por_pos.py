import os
os.chdir(os.path.dirname(por_pos.py))

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
    same_positions_all = []
    changed_positions_water = []
    for id, old_position in old_positions.items():
        if id in new_positions:
            if old_position == new_positions[id] and id in ids_to_ignore:
                same_positions_all.append(id)
            elif old_position != new_positions[id] and id in ids_to_ignore:
                changed_positions_water.append(id)
            elif old_position == new_positions[id] and id not in ids_to_ignore:
                same_positions.append(id)
            elif id not in ids_to_ignore:
                changed_positions.append(id)
    return same_positions_all, same_positions, changed_positions, changed_positions_water

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
    old_positions_path = 'positions_old.txt'  #Positions before
    new_positions_path = 'positions.txt' #Positions after
    ids_to_ignore_path = 'ids_to_ignore.txt' #Aka water provinces
    output_path = 'same_positions.txt'
    changed_positions_output_path = 'changed_positions.txt'
    output_water = "water_positions.txt"
    output_water_changed = "water_positions_changed.txt"

    old_positions = read_positions(old_positions_path)
    new_positions = read_positions(new_positions_path)
    ids_to_ignore = read_ids_to_ignore(ids_to_ignore_path)

    same_positions_all, same_positions, changed_positions, changed_positions_water = find_same_positions(old_positions, new_positions, ids_to_ignore)

    total_ids = len(set(new_positions.keys()))
    ignored_count = len(ids_to_ignore)
    unchanged_ids = len(same_positions)
    all_unchanged_ids = len(same_positions_all)
    changed_ids = len(changed_positions)
    changed_ids_water = len(changed_positions_water)
    
    # Counting
    changed_ids_in_ignored = sum(1 for id in changed_positions if id in ids_to_ignore)
    unchanged_water_id = all_unchanged_ids - unchanged_ids
    water_id_changed = changed_ids_water / ignored_count * 100 if ignored_count > 0 else 0
    total_effective_ids = total_ids - ignored_count
    total_changed_and_same = changed_ids + unchanged_ids + changed_ids_water
    percentage_changed = (changed_ids / total_effective_ids) * 100 if total_effective_ids > 0 else 0
    percentage_changed_including_ignored = (changed_ids + changed_ids_water) / total_ids * 100 if total_ids > 0 else 0

# Save results to file
    with open(output_path, 'w') as output_file:
        output_file.write(f"All provinces: {total_ids}\n")
        output_file.write(f"Ignored prov: {ignored_count}\n")
        output_file.write(f"Non water prov: {total_effective_ids}\n\n")

        output_file.write(f"Prov done: {changed_ids}\n")
        output_file.write(f"Prov left to do: {unchanged_ids}\n")
        output_file.write(f"Water done: {changed_ids_water}%\n")
        output_file.write(f"Water left to do: {unchanged_water_id}\n")
        output_file.write(f"Done total: {total_changed_and_same}\n\n")

        output_file.write(f"Percentage done (non water): {percentage_changed:.2f}%\n")
        output_file.write(f"Percentage done (water): {water_id_changed:.2f}%\n")
        output_file.write(f"Percentage done (all): {percentage_changed_including_ignored:.2f}%\n")
        output_file.write("\nList of IDs with same positions:\n")
        for id in same_positions:
            output_file.write(f"{id}\n")

    with open(changed_positions_output_path, 'w') as changed_positions_output_file:
        changed_positions_output_file.write("List of IDs with changed positions:\n")
        for id in changed_positions:
            changed_positions_output_file.write(f"{id}\n")

    with open(output_water, 'w') as water_output_file:
        water_output_file.write("List of IDs with water positions:\n")
        for id in same_positions_all:
            water_output_file.write(f"{id}\n")

    with open(output_water_changed, 'w') as water_output_file:
        water_output_file.write("List of IDs with water positions:\n")
        for id in changed_positions_water:
            water_output_file.write(f"{id}\n")

    # Print results
    print(f"All provinces: \033[36m{total_ids}\033[0m")
    print(f"Ignored prov: \033[33m{ignored_count}\033[0m")
    print(f"Non water prov: \033[37m{total_effective_ids}\033[0m\n")

    print(f"Prov done: \033[32m{changed_ids}\033[0m")
    print(f"Prov left to do: \033[31m{unchanged_ids}\033[0m")
    print(f"Water done: \033[34m{changed_ids_water}\033[0m")
    #print(f"Water done: \033[36m{ignored_count - unchanged_water_id}?\033[0m")
    print(f"Water left to do: \033[31m{unchanged_water_id}\033[0m")
    print(f"Done total: \033[1m{total_changed_and_same}\033[0m\n")

    print(f"Percentage done (non water): \033[33m{percentage_changed:.2f}%\033[0m")
    print(f"Percentage done (water): \033[33m{water_id_changed:.2f}%\033[0m")
    print(f"Percentage done (all): \033[33m{percentage_changed_including_ignored:.2f}%\033[0m\n")

    print(f"This info will be saved in that file ")
    print(f"Unchanged prov saved to: {output_path}")
    print(f"Changed prov saved to: {changed_positions_output_path}")
    print(f"Water prov saved to: {output_water}\n")
    print(f"Modified water prov saved to: {output_water_changed}")

if __name__ == "__main__":
    main()
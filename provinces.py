import pandas as pd
import math
import os


def read_data(filepath):
    data = pd.read_csv(filepath)
    data = data.rename(columns={
            "Prov": "prov",
            "trade good ": "trade good",
            "Center of Trade": "cot",
            "Local Airport": "local airport",
            "Airport": "airport",
            "Border Crossing": "border crossing",
            "Mountain Pass": "mountain pass",
            "Isthmus": "isthmus",
            "River Tributary": "river tributary",
            "River Estruary": "river estruary",
        }
    )
    return data


def adjust_data(data):
    trade_good_replacements = {
        'Grain': 'gu_wheat',
        'Fish': 'fish',
        'Naval supplies': 'naval_supplies',
        'Cloth': 'cloth',
        'Copper': 'copper',
        'Iron': 'iron',
        'Glass': 'glass',
        'Paper': 'paper',
        'Salt': 'salt',
        'Sugar': 'sugar',
        'Wool': 'wool',
        'Fur': 'fur',
        'Coal': 'gu_coal',
        'Livestock': 'gu_poultry',
        'Mushrooms': 'gu_mushrooms',
        'Fruits': 'gu_fruits',
        'Vegetables': 'gu_vegetables',
        'Dairy': 'gu_dairy',
        'Oscypek': 'gu_oscypek',
        'Lumber': 'gu_lumber',
        'Stone': 'gu_stone',
        'Apiculture': 'gu_apiculture',
        'Horses': 'gu_horses',
        'Amber': 'gu_amber',
        'Beer': 'gu_beer',
        'Vodka': 'gu_vodka',
        'Tourists': 'gu_tourists',
        'Ceramics': 'gu_ceramics',
        'Hemp': 'gu_hemp',
        'Sulfur': 'gu_sulfur',
        'Oil': 'gu_oil',
        'Wine': 'wine',
        'Gold': 'gold',
        'Unknown': 'unknown',
        'Wheat': 'gu_wheat',
        'Triticale': 'gu_triticale',
        'Barley': 'gu_barley',
        'Maize': 'gu_maize',
        'Poultry': 'gu_poultry',
        'Pigs': 'gu_pigs',
        'Cattle': 'gu_cattle',
        'Metalworking': 'gu_metalworking',
        'Chemicals': 'gu_chemicals',
        'Consumer Goods': 'gu_consumer_goods',
        'Confectionery': 'gu_confectionery',
        'Software': 'gu_software',
        'Finances': 'gu_finances',
        'Woodworking': 'gu_woodworking',
        'Electronics': 'gu_electronics',
        'Processed Food': 'gu_processed_food',
        'Vehicles': 'gu_vehicles',
        'Euro': 'unknown',
        '0': 'unknown',
    }

    terrain_replacements = {
        'Farmlands': 'farmlands',
        'Woods': 'woods',
        'Forest': 'forest',
        'Marsh': 'marsh',
        'Hills': 'hills',
        'Mountain': 'mountain',
        'Grasslands': 'grasslands',
        'Coastline': 'coastline',
        'Drylands': 'drylands',
        'Desert': 'desert',
        'Highlands': 'highlands',
        'Steppe': 'steppe',
        'Urban': 'urban',
        'High Urban': 'high_urban',
        'Floodplains': 'floodplains',
        'Crossing': 'crossing',
    }


    data['trade good'] = data['trade good'].map(trade_good_replacements).fillna(data['trade good'])
    data['latent trade good'] = data['latent trade good'].map(trade_good_replacements).fillna(data['latent trade good'])
    data['terrain'] = data['terrain'].map(terrain_replacements).fillna(data['terrain'])
    return data


def data_to_dict(data):
    return data.to_dict(orient='records')


def adjust_provinces(provinces):
    for province in provinces:
        for key, value in province.items():
            if type(value) != str and math.isnan(value):
                province[key] = None

        if type(province['trade good']) != str:
            province['trade good'] = None
        
        if type(province['latent trade good']) != str or province['latent trade good'] == 'unknown':
            province['latent trade good'] = None

        if province['tax']:
            province['tax'] = int(province['tax'])
        if province['prod']:
            province['prod'] = int(province['prod'])
        if province['manpower']:
            province['manpower'] = int(province['manpower'])
        if not province['terrain'] or province['terrain'] == "0":
            province['terrain'] = None
    return provinces


def find_file(id):
    parent_path = os.listdir("history/provinces")
    for file in parent_path:
        if file.startswith(str(id)):
            return file
    return None


def modify_provinces(provinces):
    for province in provinces:
        id = province['id']
        file = find_file(id)

        if not file:
            continue
        
        latent_trade_goods = province['latent trade good']
        has_latent_trade_goods = False

        with open(f"history/provinces/{file}", 'r') as f:
            data = f.readlines()

        for line, content in enumerate(data):
            if 'base_tax' in content and province['tax']:
                data[line] = f"base_tax = {province['tax']}\n"
            elif 'base_production' in content and province['prod']:
                data[line] = f"base_production = {province['prod']}\n"
            elif 'base_manpower' in content and province['manpower']:
                data[line] = f"base_manpower = {province['manpower']}\n"
            elif content.startswith('trade_goods = ') and province['trade good']:
                data[line] = f"trade_goods = {province['trade good']}\n" 
            elif content.startswith('latent_trade_goods = ') and latent_trade_goods:
                has_latent_trade_goods = True
                data[line] = f"latent_trade_goods = {{ {latent_trade_goods} }}\n"
        
        if latent_trade_goods and not has_latent_trade_goods:
            if f"\n" not in data[-1]:
                data[-1] = data[-1] + "\n"
            data.append(f"latent_trade_goods = {{ {latent_trade_goods} }}\n")

        with open(f"history/provinces/{file}", 'w') as f:
            f.writelines(data)


def modify_terrains(provinces):
    terrains = {
        'farmlands': [],
        'woods': [],
        'forest': [],
        'marsh': [],
        'hills': [],
        'mountain': [],
        'grasslands': [],
        'coastline': [],
        'drylands': [],
        'desert': [],
        'highlands': [],
        'steppe': [],
        'urban': [],
        'high_urban': [],
        'floodplains': [],
        'crossing': [],
    }
    for province in provinces:
        id = province['id']
        terrain = province['terrain']
        if terrain:
            terrains[terrain].append(id)

    with open(f"map/terrain.txt", 'r') as f:
        data = f.readlines()

    for terrain_type in terrains.keys():
        list_of_provinces = " ".join(str(p) for p in terrains[terrain_type])
        overwrite = False

        for line, content in enumerate(data):
            if f"{terrain_type} " in content:
                overwrite = True
            if overwrite and f"terrain_override" in content:
                data[line] = f"\t\tterrain_override = {{ {list_of_provinces} }}\n"
                break

    with open(f"map/terrain.txt", 'w') as f:
            f.writelines(data)


data = read_data('Trade Goods.csv')
data = adjust_data(data)
provinces = data_to_dict(data)
provinces = adjust_provinces(provinces)
# modify_provinces(provinces)
# modify_terrains(provinces)
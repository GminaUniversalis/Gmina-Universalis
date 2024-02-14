# GminaPainter is a tool for updating provinces with csv file
# Author: Wojciech "Shogun" Adamiec

HEADER = """
  ________          .__                 __________         .__           __                   
 /  _____/   _____  |__|  ____  _____   \______   \_____   |__|  ____  _/  |_   ____  _______  
/   \  ___  /     \ |  | /    \ \__  \   |     ___/\__  \  |  | /    \ \   __\_/ __ \ \_  __ \ 
\    \_\  \|  Y Y  \|  ||   |  \ / __ \_ |    |     / __ \_|  ||   |  \ |  |  \  ___/  |  | \/ 
 \______  /|__|_|  /|__||___|  /(____  / |____|    (____  /|__||___|  / |__|   \___  > |__|    
        \/       \/          \/      \/                 \/          \/             \/          

"""

import typer
import pandas as pd
import math
import os
from typing_extensions import Annotated


class GminaPainter:
    COLUMNS = {
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
    TRADE_GOOD_REPLACEMENTS = {
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
    TERRAIN_REPLACEMENTS = {
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
    TERRAINS = {
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
    PROPER_TRADE_GOODS = set(TRADE_GOOD_REPLACEMENTS.values())

    def __init__(self, filepath) -> None:
        self.data = None
        self.provinces = None
        self._read_data(filepath)
        self._adjust_data()
        self._data_to_dict()
        self._adjust_provinces()

    def _read_data(self, filepath):
        self.data = pd.read_csv(filepath)
        self.data = self.data.rename(columns=self.COLUMNS)

    def _adjust_data(self):
        self.data['trade good'] = self.data['trade good'].map(self.TRADE_GOOD_REPLACEMENTS).fillna(self.data['trade good'])
        self.data['latent trade good'] = self.data['latent trade good'].map(self.TRADE_GOOD_REPLACEMENTS).fillna(self.data['latent trade good'])
        self.data['terrain'] = self.data['terrain'].map(self.TERRAIN_REPLACEMENTS).fillna(self.data['terrain'])


    def _data_to_dict(self):
        self.provinces = self.data.to_dict(orient='records')

    def _adjust_provinces(self):
        for province in self.provinces:
            for key, value in province.items():
                if type(value) != str and math.isnan(value):
                    province[key] = None

            self._handle_trade_goods_exceptions(province)
            self._handle_dev_and_terrain_corner_cases(province)
            self._handle_cots(province)

    def _handle_trade_goods_exceptions(self, province):
        if type(province['trade good']) != str:
            province['trade good'] = None

        if type(province['latent trade good']) != str or province['latent trade good'] == 'unknown' or province['latent trade good'] not in GminaPainter.PROPER_TRADE_GOODS:
            province['latent trade good'] = None

    def _handle_dev_and_terrain_corner_cases(self, province):
        if province['tax']:
            province['tax'] = int(province['tax'])
        if province['prod']:
            province['prod'] = int(province['prod'])
        if province['manpower']:
            province['manpower'] = int(province['manpower'])
        if not province['terrain'] or province['terrain'] == "0":
            province['terrain'] = None
    
    def _handle_cots(self, province):
        if province['cot']:
            province['cot'] = int(province['cot'])
        if not province['cot']:
            province['cot'] = 0

    def _find_file(self, id):
        parent_path = os.listdir("history/provinces")
        for file in parent_path:
            if file.startswith(str(id)):
                return file
        return None

    def modify_dev(self):
        for province in self.provinces:
            id = province['id']
            file = self._find_file(id)

            if not file:
                continue

            with open(f"history/provinces/{file}", 'r') as f:
                data = f.readlines()

            for line, content in enumerate(data):
                if 'base_tax' in content and province['tax']:
                    data[line] = f"base_tax = {province['tax']}\n"
                elif 'base_production' in content and province['prod']:
                    data[line] = f"base_production = {province['prod']}\n"
                elif 'base_manpower' in content and province['manpower']:
                    data[line] = f"base_manpower = {province['manpower']}\n"
                
            with open(f"history/provinces/{file}", 'w') as f:
                f.writelines(data)
    
    def modify_trade_goods(self):
        for province in self.provinces:
            id = province['id']
            file = self._find_file(id)

            if not file:
                continue
            
            with open(f"history/provinces/{file}", 'r') as f:
                data = f.readlines()

            for line, content in enumerate(data):
                if content.startswith('trade_goods = ') and province['trade good']:
                    data[line] = f"trade_goods = {province['trade good']}\n" 
                    break
        
            with open(f"history/provinces/{file}", 'w') as f:
                f.writelines(data)
    
    def modify_center_of_trades(self):
        for province in self.provinces:
            id = province['id']
            file = self._find_file(id)

            cot_level = province['cot']
            to_remove = not bool(cot_level)
            to_add = bool(cot_level)

            if not file:
                continue
            
            with open(f"history/provinces/{file}", 'r') as f:
                data = f.readlines()

            if to_remove:
                for line, content in enumerate(data):
                    if content.startswith('center_of_trade ='):
                        data[line] = f"\n" 
                        break
            
            if to_add:
                for line, content in enumerate(data):
                    if content.startswith('center_of_trade ='):
                        data[line] = f"center_of_trade = {cot_level}\n" 
                        break
                else:
                    data.append(f"center_of_trade = {cot_level}\n")
                
            with open(f"history/provinces/{file}", 'w') as f:
                f.writelines(data)
    
    def modify_latent_trade_goods(self):
        for province in self.provinces:
            id = province['id']
            file = self._find_file(id)

            if not file:
                continue
            
            latent_trade_goods = province['latent trade good']
            has_latent_trade_goods = False

            with open(f"history/provinces/{file}", 'r') as f:
                data = f.readlines()

            if latent_trade_goods:
                for line, content in enumerate(data):
                    if content.startswith('latent_trade_goods = '):
                        has_latent_trade_goods = True
                        data[line] = f"latent_trade_goods = {{ {latent_trade_goods} }}\n"
                        break
            else:
                for line, content in enumerate(data):
                    if content.startswith('latent_trade_goods = '):
                        data[line] = f"\n"
                        break
            
            if latent_trade_goods and not has_latent_trade_goods:
                if f"\n" not in data[-1]:
                    data[-1] = data[-1] + "\n"
                data.append(f"latent_trade_goods = {{ {latent_trade_goods} }}\n")

            with open(f"history/provinces/{file}", 'w') as f:
                f.writelines(data)

    def modify_terrains(self):
        for province in self.provinces:
            id = province['id']
            terrain = province['terrain']
            if terrain:
                self.TERRAINS[terrain].append(id)

        with open(f"map/terrain.txt", 'r') as f:
            data = f.readlines()

        for terrain_type in self.TERRAINS.keys():
            list_of_provinces = " ".join(str(p) for p in self.TERRAINS[terrain_type])
            overwrite = False

            for line, content in enumerate(data):
                if f"{terrain_type} " in content:
                    overwrite = True
                if overwrite and f"terrain_override" in content:
                    data[line] = f"\t\tterrain_override = {{ {list_of_provinces} }}\n"
                    break

        with open(f"map/terrain.txt", 'w') as f:
                f.writelines(data)


def main(
        all: Annotated[bool, typer.Option("--all", "-a", help="Update all.")] = False,
        dev: Annotated[bool, typer.Option("--dev", "-d", help="Update dev.")] = False,
        trade_goods: Annotated[bool, typer.Option("--goods", "-g", help="Update trade goods.")] = False,
        latent_trade_goods: Annotated[bool, typer.Option("--latent", "-l", help="Update latent trade goods.")] = False,
        terrains: Annotated[bool, typer.Option("--terrains", "-t", help="Update terrains types.")] = False,
        center_of_trades: Annotated[bool, typer.Option("--centers", "-c", help="Update center of trades.")] = False,
    ):
    gmina_painter = GminaPainter('scripts/Trade Goods.csv')
    
    if all or dev:
        print(f"OVERWRITING DEV")
        gmina_painter.modify_dev()

    if all or trade_goods:
        print(f"OVERWRITING TRADE GOODS")
        gmina_painter.modify_trade_goods()
    
    if all or latent_trade_goods:
        print(f"OVERWRITING LATENT TRADE GOODS")
        gmina_painter.modify_latent_trade_goods()
        
    if all or terrains:
        print(f"OVERWRITING TERRAINS")
        gmina_painter.modify_terrains()
    
    if all or center_of_trades:
        print(f"OVERWRITING CENTER OF TRADES")
        gmina_painter.modify_center_of_trades()
        

if __name__ == "__main__":
    print(HEADER)
    typer.run(main)

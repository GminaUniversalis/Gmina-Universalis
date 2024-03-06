import re
from typing import Dict


class Record:

    positionToCompare = [1,1,1,1,1,1,1, 1,1,1,1,1,1,1]
    rotationToCompare = [1,1,1,1,1,1,1]
    heightToCompare =   [1,1,1,1,1,1,1] 

    def __init__(self, recordID, position, rotation, height):



        self.recordID  = recordID
        self.position = position
        self.rotation = rotation
        self.height = height

    def __eq__(self, __o: object) -> bool:

        if self.recordID != __o.recordID:
            return False

        if ( len( self.position) == len( __o.position ) ):
            for x in range ( len(self.position )):
                if Record.positionToCompare[x] == True:
                    if self.position[x] != __o.position[x]:
                        return False

        if ( len( self.rotation) == len( __o.rotation ) ):
            for x in range ( len(self.rotation )):
                if Record.rotationToCompare[x] == True:
                    if self.rotation[x] != __o.rotation[x]:
                        return False

        if ( len( self.height) == len( __o.height ) ):
            for x in range ( len(self.height )):
                if Record.heightToCompare[x] == True:
                    if self.height[x] != __o.height[x]:
                        return False

        return True


def readRecords(file_path):
    listOfRecord = []
    with open(file_path, 'r') as file:
        content = file.read()

    patternPosition = re.compile(r'position={\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*}', re.DOTALL)
    matchesPosition = patternPosition.findall(content)

    patternRotation = re.compile(r'rotation={\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*}', re.DOTALL)
    matchesRotation = patternRotation.findall(content)

    patternHeight = re.compile(r'height={\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*}', re.DOTALL)
    matchesHeight = patternHeight.findall(content)


    for recordID in range(len(matchesPosition)):

        recordPosition = matchesPosition[recordID]
        recordRotation = matchesRotation[recordID]
        recordHeight   = matchesHeight[recordID]
        record  = Record(recordID+1, recordPosition, recordRotation, recordHeight)
        listOfRecord.append(record)

    return listOfRecord


def readIgnoredIndex(file_path):
    ids_to_ignore = set()
    with open(file_path, 'r') as file:
        for line in file:
            ids_in_line = line.strip().split()
            for id_str in ids_in_line:
                if id_str.isdigit():
                    ids_to_ignore.add(int(id_str))
    return ids_to_ignore

def CalculateThings(firstList, secondList, indexToIgnore , indexToCalculate = None):

    changedIDs = []
    if (indexToCalculate == None):
        for x in range ( len(firstList) ):
            if firstList[x].recordID not in indexToIgnore:
                if  firstList[x] != secondList[x]:
                    changedIDs.append(x)
    else:
        for x in indexToCalculate:
            if x not in indexToIgnore:
                if  firstList[x-1] != secondList[x-1]:
                    changedIDs.append(x)
    return changedIDs


def main():
    old_positions_path = 'positions_old.txt'
    new_positions_path = 'positions.txt'
    #old_positions_path = 'positionsTest2.txt'
    #new_positions_path = 'positionsTest1.txt'
    ids_to_ignore_path = 'ids_to_ignore.txt'
    output_path = 'same_positions.txt'
    changed_positions_output_path = 'changed_positions.txt'
    output_water = "water_positions.txt"
    output_water_changed = "water_positions_changed.txt"

    oldRecords = readRecords(old_positions_path)
    newRecords = readRecords(new_positions_path)
    idsToIgnore = readIgnoredIndex(ids_to_ignore_path)



    totalIDs = len(oldRecords)
    ignoredIDs = len(idsToIgnore)
    effectiveIDs = totalIDs - ignoredIDs
    results = CalculateThings(oldRecords,newRecords, idsToIgnore)
    resultsForWater = CalculateThings(oldRecords,newRecords,[],idsToIgnore)
    changedIDs = len(results)
    toDoIDs = effectiveIDs - changedIDs
    totalDone =  changedIDs + ignoredIDs

    print(f"All provinces:{totalIDs}")
    print(f"Ignored prov: {ignoredIDs}")
    print(f"Non water prov:{effectiveIDs}")

    print(f"Prov done: {changedIDs}")
    print(f"Prov left to do: {toDoIDs}")
    #print(f"Water done: \033[36m{ignored_count - unchanged_water_id}\033[0m")
    #print(f"Water done: \033[34m{changed_ids_water}?\033[0m")    
    #print(f"Water left to do: \033[36m{unchanged_water_id}\033[0m")
    print(f"Done total: {totalDone}\n")

    #print(f"Percentage done (non water): \033[33m{percentage_changed:.2f}%\033[0m")
    #print(f"Percentage done (water): \033[33m{water_id_changed:.2f}%\033[0m")
    #print(f"Percentage done (all): \033[33m{percentage_changed_including_ignored:.2f}%\033[0m\n")

    #print(f"This info will be saved in that file ")
    #print(f"Unchanged prov saved to: {output_path}")
    #print(f"Changed prov saved to: {changed_positions_output_path}")
    #print(f"Water prov saved to: {output_water}\n")
    #print(f"Modified water prov saved to: {output_water_changed}")


if __name__ == "__main__":
    main()
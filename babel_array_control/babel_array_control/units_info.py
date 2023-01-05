from pathlib import Path
import csv

array_map = None


def load_array_map():
    arr_map = {}
    map_file_path = Path(__file__).parent.resolve() / 'data/array_map.csv'

    with open(map_file_path, 'r') as map_file:
        lines = map_file.readlines()[1:]

        for values in csv.reader(lines, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            index, language, priority, musical = values
            arr_map[index] = {
                'index': int(index),
                'language': language,
                'priority': int(priority),
                'musical': musical.strip() == 'TRUE',
            }

    return arr_map


def get_units_by_priority(priority):
    global array_map

    if array_map is None:
        array_map = load_array_map()

    units = []
    for index in array_map:
        info = array_map[index]

        if info['priority'] == priority:
            units.append(info)

    return units


def get_musical_units():
    global array_map

    if array_map is None:
        array_map = load_array_map()

    units = []
    for index in array_map:
        info = array_map[index]

        if info['musical']:
            units.append(info)

    return units

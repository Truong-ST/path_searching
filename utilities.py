import csv
import yaml


def set_configuration(file_yaml):
    """
    :return: dictionary of information in file yaml
    """
    with open(file_yaml, 'r') as f_yaml:
        config_dict = yaml.safe_load(f_yaml)

        return config_dict


file_configuration_yaml = 'configuration.yaml'
config_dict = set_configuration(file_configuration_yaml)

width = config_dict['width']
height = config_dict['height']
block = config_dict['block']
margin = config_dict['margin']


def get_topographic(fileName):
    """
    :param fileName: csv
    :return: list of rock in topographic
    """
    topographic = []
    fileCSV = open(fileName, 'r')
    reader = csv.reader(fileCSV)

    for row in reader:
        tmp = (int(row[0]), int(row[1]))
        topographic.append(tmp)

    return topographic


def scale_coordinate(list_coordinate, ratio, bias):
    scaled_list = []

    for coord in list_coordinate:
        tmp = [0, 0]
        tmp[0] = coord[1]*ratio + bias
        tmp[1] = coord[0]*ratio + bias
        scaled_list.append(tmp)

    return scaled_list


def pos_to_real_coord(pos):
    """
    :param pos:
    :return: coord
    """
    tmp = [0, 0]
    tmp[0] = pos[1]*block+margin
    tmp[1] = pos[0]*block+margin

    return [tmp[0], tmp[1], tmp[0]+block, tmp[1]+block]


def coord_to_pos(coord):
    return (coord // block).astype(int)




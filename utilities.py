import csv
import yaml


file_configuration_yaml = 'configuration.yaml'


def set_configuration():
    """
    :return: dictionary of information in file yaml
    """
    with open(file_configuration_yaml, 'r') as f_yaml:
        config_dict = yaml.safe_load(f_yaml)

        return config_dict


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

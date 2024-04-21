from ruamel.yaml import YAML
from configs import data_path


def read_yaml(file_name):

    full_file = data_path + "\\" + file_name

    with open(full_file, 'r', encoding='utf-8') as f:
        yaml = YAML(typ='safe')
        data = yaml.load(f)

    print(data)
    return data


read_yaml('table_data.yml')

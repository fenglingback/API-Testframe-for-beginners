from ruamel.yaml import YAML
from configs import data_path
import json as _json


class GetData:

    def __init__(self) -> None:
        self._full_file_path = None



    def _format_path(self, file_name, isMock):

        if isMock:
            self._full_file_path = data_path + "\\Mock\\" + file_name
        else:
            self._full_file_path = data_path + "\\Real\\" + file_name



    def _read_yaml(self) -> dict:

        with open(self._full_file_path, 'r', encoding='utf-8') as f:
            yaml = YAML(typ='safe')
            data = yaml.load(f)

        # data = _json.dumps(data, indent=4)
        # print(data)
        return data



    def _format_data(self) -> list:
        origin_data = self._read_yaml()
        end_data = []

        for url, else_data in origin_data.items():
            for other_data in else_data:
                temp_dict = {}
                for i, (path, canshu) in enumerate(other_data.items()):
                    full_url = url + path
                    temp_dict['url'] = full_url
                    for key, val in canshu.items():
                        temp_dict[key] = val
                    end_data.append(temp_dict)


        # print("\n" + _json.dumps(end_data, indent=4))
        return end_data
            



    def return_data_from(self, file_name, isMock: bool = False):
        self._format_path(file_name, isMock)
        return self._format_data()



getdata = GetData()




if __name__ == '__main__':
    
    getdata.return_data_from('pet_data.yml', isMock=False)

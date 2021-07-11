import json
from gila.gila import Gila

gila_instance = Gila()

def get_field(file, field):
    gila_instance.set_config_file("json_files/" + file + '.json')
    gila_instance.set_config_type('.json')
    gila_instance.read_config_file()

    key = gila_instance.get(field)
    return key

def create_field(file, channel_identifier, emoji, role_id):
    json_data = ""

    with open("json_files/" +file + '.json', 'a') as json_file:
        json.dump(json_data, json_file)
        print(json_data)

#

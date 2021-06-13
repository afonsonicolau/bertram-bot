import json
from gila.gila import Gila

gila_instance = Gila()
gila_instance.set_config_file('secrets.json')
gila_instance.set_config_type('.json')
gila_instance.read_config_file()


def get_field(field):
    key = gila_instance.get(field)
    return key

import string
import random
import messages
import sql
import json


def plate_generator():
    plate = ""
    i = 1

    while i <= 8:
        if i == 3 or i == 4 or i == 5:
            plate += random.choice(string.ascii_uppercase)
        else:
            plate += str(random.randint(0, 9))

        i += 1

    return plate


async def givecar(identifier, car_name, plate, vehicle_props, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute(
            "SELECT * FROM users WHERE identifier = %(identifier)s", {'identifier': identifier})
        player_data = cursor.fetchone()

        if player_data == None:
            await messages.embeded_messages(message, "Dar um bote", "Erro", "Não existe sequer uma pessoa com o 'identificador' inserido.")
        else:
            plate_exists = ""
            if plate is not None:
                cursor.execute(
                    "SELECT plate FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
                plate_exists = cursor.fetchone()
            else:
                while plate_exists is not None:
                    plate = plate_generator()
                    cursor.execute(
                        "SELECT plate FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
                    plate_exists = cursor.fetchone()

            if plate_exists is None:
                jsoned_vehicle_props = json.loads(vehicle_props)
                jsoned_vehicle_props['plate'] = plate
                altered_vehicle_props = json.dumps(jsoned_vehicle_props)

                sql.insert_data(
                    "INSERT INTO owned_vehicles (identifier, plate, vehicleprops) VALUES(%(identifier)s, %(plate)s, %(vehicleprops)s);",
                    {'identifier': identifier, 'plate': plate, 'vehicleprops': altered_vehicle_props}
                )

                playername = player_data[1]
                await messages.embeded_messages(message, "Dar um bote", "Sucesso", "O tal '" + car_name + "' de matrícula '" + plate + "' foi dado ao jogador '" + playername + "', ok?")
            else:
                await messages.embeded_messages(message, "Dar um bote", "Erro", "A matrícula '" + plate + "' já existe, logo não dá, né.")

        sql.close_connection()

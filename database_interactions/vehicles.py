import string
import random
import discord_interactions.messages as messages
import services.sql as sql
import json
from datetime import datetime


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

async def get_vehicles(identifier, first_name, last_name, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute("SELECT identifier, firstname, lastname FROM users WHERE identifier = %(identifier)s OR firstname LIKE %(first_name)s AND lastname LIKE %(last_name)s", {
            'identifier': identifier,
            'first_name': first_name,
            'last_name': last_name
            })

        parsed_identifier = cursor.fetchone()

        if parsed_identifier is not None:
            cursor.execute("SELECT plate, garage, vehicle_name FROM owned_vehicles WHERE owner = %(identifier)s", {'identifier': parsed_identifier[0]})
            vehicle_data = cursor.fetchall()

            if len(vehicle_data) > 0:
                vehicles_info = ""

                for data in vehicle_data:
                    vehicles_info += "\nMatrícula - " + data[0] + ' | Garagem - ' + data[1] + ' | Modelo - ' + data[2]

                await messages.embeded_messages(message, "Veículos de um personagem", "Sucesso", "Os seguintes veículos do '" + parsed_identifier[1] + " " + parsed_identifier[2] + "' foram encontrados: \n" + vehicles_info)
            else:
                await messages.embeded_messages(message, "Veículos de um personagem", "Erro", "O personagem '" + parsed_identifier[1] +  " " + parsed_identifier[2] + "' não tem qualquer veículo.")
        else:
            await messages.embeded_messages(message, "Veículos de um personagem", "Erro", "Não foi possível encontrar qualquer personagem.")

        #sql.close_connection()


async def give_car(identifier, car_model, car_name, plate, vehicle_props, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute("SELECT firstname, lastname FROM users WHERE identifier = %(identifier)s", {'identifier': identifier})
        player_data = cursor.fetchone()

        if player_data == None:
            await messages.embeded_messages(message, "Dar um bote", "Erro", "Não existe sequer uma pessoa com o 'identificador' inserido.")
        else:
            plate_exists = ""
            if plate is not None:
                cursor.execute("SELECT plate FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
                plate_exists = cursor.fetchone()
            else:
                while plate_exists is not None:
                    plate = plate_generator()
                    cursor.execute("SELECT plate FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
                    plate_exists = cursor.fetchone()

            if plate_exists is None:
                jsoned_vehicle_props = json.loads(vehicle_props)
                jsoned_vehicle_props['plate'] = plate
                jsoned_vehicle_props = json.dumps(jsoned_vehicle_props)
                date_now = datetime.today().strftime('%Y-%m-%d')
                health = "[{'value':100,'part':'brakes'},{'value':100,'part':'radiator'},{'value':100,'part':'clutch'},{'value':100,'part':'transmission'},{'value':100,'part':'electronics'},{'value':100,'part':'driveshaft'},{'value':100,'part':'fuelinjector'},{'value':1000,'part':'engine'}]"

                sql.run_query(
                    "INSERT INTO owned_vehicles (owner, plate, vehicle, date, model, gotKey, state, garage, vehicle_name, health, trailerdata) VALUES(%(owner)s, %(plate)s, %(vehicle)s, %(date_now)s, %(car_model)s, 1, 2, 'A', %(car_name)s, %(health)s, 0);",
                    {'owner': str(identifier), 'plate': str(plate), 'vehicle': jsoned_vehicle_props, 'car_model': car_model, 'car_name': car_name[1], 'date_now': date_now, 'health': health}
                )

                playername = player_data[0] + " " + player_data[1]
                await messages.embeded_messages(message, "Dar um bote", "Sucesso", "O tal '" + car_name[1] + "' de matrícula '" + plate + "' foi dado ao jogador '" + playername + "', ok?")
            else:
                await messages.embeded_messages(message, "Dar um bote", "Erro", "A matrícula '" + plate + "' já existe, logo não dá, né.")

        #sql.close_connection()


async def change_garage(plate, garage, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute("SELECT plate FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
        plate_exists = cursor.fetchone()

        if plate_exists is not None:
            sql.run_query("UPDATE owned_vehicles SET state = '2', garage = %(garage)s WHERE plate = %(plate)s;", {
                            'garage': garage, 'plate': plate}
                         )
            await messages.embeded_messages(message, "Mudar garagem de um veículo", "Sucesso", "O veículo de matrícula '" + plate + "' está agora na garagem '" + garage + "'.")
        else:
            await messages.embeded_messages(message, "Mudar garagem de um veículo", "Erro", "A matrícula '" + plate + "' nem sequer existe.")


async def delete_vehicle(plate, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute("SELECT plate, is_deleted FROM owned_vehicles WHERE plate = %(plate)s", {'plate': plate})
        plate_exists = cursor.fetchone()

        if plate_exists is not None:
            if plate_exists[1] is None:
                sql.run_query("UPDATE owned_vehicles SET is_deleted = NOW() WHERE plate = %(plate)s;", {'plate': plate})
                await messages.embeded_messages(message, "Remover veículo", "Sucesso", "O veículo de matrícula '" + plate + "' foi removido, até à próxima.")
            else:
                await messages.embeded_messages(message, "Remover veículo", "Erro", "Este veículo meio que já foi removido, digo eu.")
        else:
            await messages.embeded_messages(message, "Remover veículo", "Erro", "A matrícula '" + plate + "' não existe não.")

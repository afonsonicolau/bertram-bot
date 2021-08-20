from sys import stderr
import discord
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Other scripts
import messages
import vehicles.vehicles as vehicles
import jsoner.json_files as json_files
import player_characters
import deployer.deploy_commits as deploy_commit
# import ssh_connection

# Open and close SSH connection
# ssh_connection.open_connection()

# ssh_connection.close_connection()

# Spreadsheet scope and sheet
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json_files.get_field('googlecredentials'), scope)
client_sheets = gspread.authorize(credentials)
sheet = client_sheets.open('Modelos - TNLRP').sheet1

# Discord bot client
client = discord.Client()

# When Bertram starts
@client.event
async def on_ready():
    print('Hello World, I am {0.user}'.format(client))

# When chat has a new message
@client.event
async def on_message(message):
    # Verifies if message is from Bertram
    if message.author == client.user:
        return

    if message.content.startswith('<@!852648286602919964>') or message.content.startswith('<@852648286602919964>') or message.content.startswith('<@&862828368411754517>'):
        await messages.add_emoji(message, 'thinking')

        user_message = message.content
        message_splitted = user_message.split()
        bot_command = message_splitted[1] if 1 < len(message_splitted) else 'invalid'

        # All TNLRP commands related
        if message.channel.id in json_files.get_field('projects.tnlrp.authorized_channels'):
            is_tnlrp_manager = message.author.id in json_files.get_field('projects.tnlrp.managers')
            is_tnlrp_deployer = message.author.id in json_files.get_field('projects.tnlrp.deployers')
            special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            # Give a car to a character
            if bot_command == 'darbote' and len(message_splitted) >= 4 and is_tnlrp_manager:
                identifier = message_splitted[2]

                # Parse plate in case one was inputed
                plate = message_splitted[4] if 4 < len(message_splitted) else None
                if plate is not None and (len(plate) > 8 or special_characters.search(plate) is not None):
                    await messages.embeded_messages(message, "Dar um veículo", "Erro", "A 'matrícula' só pode ter 8 caracteres e não pode ter símbolos, duh.")
                    return

                # Parse model inputed to get it's name and props
                car_model = None
                models = sheet.col_values(4)
                for model in models:
                    if model == message_splitted[3]:
                        car_model = sheet.find(message_splitted[3])
                        car_name = sheet.row_values(car_model.row)
                        vehicle_props = sheet.cell(car_model.row, 6).value
                        break

                if re.search('^[1-5]{1}:([\a-zA-Z\][0-9]{15})$', identifier) and car_model is not None:
                    await vehicles.give_car(identifier, message_splitted[3], car_name, plate, vehicle_props, message)
                else:
                    await messages.embeded_messages(message, "Dar um veículo", "Erro", "O 'identificador' ou o 'veículo' não estão corretos, aprende a escrever.")
            # Change vehicle's garage
            elif bot_command == 'mudargaragem' and len(message_splitted) >= 3 and is_tnlrp_manager:
                plate = message_splitted[2]
                garage = message_splitted[3] if 3 < len(message_splitted) else None
                possible_garages = ['A', 'B', 'C', 'D', 'E']

                # Garage parsing
                if garage is None:
                    garage = 'A'
                elif garage is not None and garage not in possible_garages:
                    await messages.embeded_messages(message, "Mudar garagem de um veículo", "Erro", "A garagem '" + garage + "' não existe, obviamente.")
                    return

                if len(plate) <= 8 and special_characters.search(plate) is None:
                    await vehicles.change_garage(plate, garage, message)
                else:
                    await messages.embeded_messages(message, "Mudar garagem de um veículo", "Erro", "A 'matrícula' inserida não é válida.")
            # Get character vehicle's
            elif bot_command == 'carrinhos' and len(message_splitted) >= 3 and is_tnlrp_manager:
                steamid, first_name, last_name = ""

                if re.search('^[1-5]{1}:([\a-zA-Z\][0-9]{15})$', message_splitted[2]):
                    steamid = message_splitted[2]
                else:
                    if message_splitted[2] is None or message_splitted[3] is None:
                        await messages.embeded_messages(message, "Veículos de um personagem", "Erro", "O nome inserido é muito ambíguo.")

                        return
                    else:
                        first_name, last_name += '%'
                        first_name += message_splitted[2]
                        last_name += message_splitted[3]

                        first_name, last_name += '%'

                await vehicles.get_vehicles(steamid, first_name, last_name, message)
            # Change vehicle 'is_deleted' field to 'now' timestamp
            elif bot_command == 'xaubote' and len(message_splitted) == 3 and is_tnlrp_manager:
                plate = message_splitted[2]

                if len(plate) <= 8 and special_characters.search(plate) is None:
                    await vehicles.delete_vehicle(plate, message)
                else:
                    await messages.embeded_messages(message, "Mudar garagem de um veículo", "Erro", "A 'matrícula' inserida não é válida.")
            # Get player characters
            elif bot_command == 'personagens' and len(message_splitted) == 3 and is_tnlrp_manager:
                steamid = message_splitted[2]

                if re.search('([\a-zA-Z\][0-9]{15})$', steamid):
                    await player_characters.get_character(steamid, message)
                else:
                    await messages.embeded_messages(message, "Personagens de um jogador", "Erro", "O 'steamid' inserido é inválido.")
            # Add player to multichar/Remove multichar from player
            elif bot_command == 'multichar' and len(message_splitted) == 4 and is_tnlrp_manager:
                action = message_splitted[2]
                steamid = message_splitted[3]

                if re.search('^([\a-zA-Z\][0-9]{15})$', steamid):
                    if action == 'dar' or action == 'tirar':
                        await player_characters.manage_multichar(steamid, action, message)
                    else:
                        await messages.embeded_messages(message, "Multichar", "Erro", "Ação inválida, só podes 'dar' ou 'tirar.")
                else:
                    await messages.embeded_messages(message, "Multichar", "Erro", "O 'steamid' não é válido não.")
            elif bot_command == 'deploy' and is_tnlrp_deployer:
                commit_hash = message_splitted[2]
                at_symbol = message_splitted[3]
                project_to_deploy = message_splitted[4]

                await deploy_commit.verify_data(message, commit_hash, at_symbol, project_to_deploy)
            # Help
            elif bot_command == 'ajuda-me' and is_tnlrp_manager:
                await messages.embeded_messages(message, "Ajuda do Bertram", "Sucesso", "Estou a ver que precisas de uma ajudinha, heis como funciono:\n -> Para me chamares basta fazer **@Bertram <comando> <identificador> (opcionais)**\n___Comandos disponíves___:\n  - darbote <identificador> <veículo> (matrícula) \n  - mudargaragem <matrícula> (garagem - padrão A) \n  - carrinhos <identificador ou nome>\n  - personagens <steamid>\n\n Estes são os comandos que tenho configurados, por enquanto.")
            # In case commands are wrong or user doesn't have permissions
            else:
                await messages.embeded_messages(message, "Algo errado", "Erro", "Se não deu tens duas opções, ou não sabes usar os meus comandos ou não tens permissões, simples.")


client.run(json_files.get_field('token'))

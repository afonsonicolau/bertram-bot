import discord
import re
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector
from mysql.connector import Error

# Load JSON Secrets
secrets = open('secrets.json')
secretdata = json.load(secrets)

# SQL Connection
try:
    connection = mysql.connector.connect(host='localhost', database='bertramtest', user='bertram', password=secretdata['bertramredentials'])
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        connection.close()

# Spreadsheet scope and sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(secretdata['googlecredentials'], scope)
clientsheet = gspread.authorize(credentials)
sheet = clientsheet.open('Modelos - TNLRP').sheet1

# Discord bot client
client = discord.Client()

@client.event
async def on_ready():
  print('Hello World, I am {0.user}'.format(client))

@client.event
async def on_message(message):
    # Verifies is message is from Bertram
    if message.author == client.user:
        return

    if message.content.startswith('<@!852648286602919964>'):
        usermessage = message.content
        messagesplitted = usermessage.split()

        botcommand = ''
        botcommand = messagesplitted[1] if 0 <= 1 < len(messagesplitted) else 'invalid'

        if botcommand == 'darbote' and len(messagesplitted) >= 4:
            steamid = messagesplitted[2]
            plate = messagesplitted[4] if 0 <= 4 < len(messagesplitted) else None
            carmodel = None
            models = sheet.col_values(4)
            for model in models:
                if model == messagesplitted[3]:
                    carmodel = sheet.find(messagesplitted[3])
                    carname = sheet.cell(carmodel.row, 2).value
                    vehicleprops = sheet.cell(carmodel.row, 6).value
                    break

            if re.search('[1-5]:([\a-zA-Z\][0-9]{15})$', steamid) and carmodel is not None:
                await givecar(steamid, carmodel.value, carname, plate, vehicleprops, message)
            else:
                await embededmessages(message, "Dar um veículo", "Erro", "O 'steamid' ou o 'veículo' não estão corretos, aprende a escrever.")
        elif botcommand == 'invalid':
            await embededmessages(message, "Inválida", "Erro", "Acho que se escreveres algo válido funciona.")

async def givecar(steamid, carmodel, carname, plate, vehicleprops, message):
    # Verify in database first if steamid is valid.
    connection.connect()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE identifier = %(identifier)s", { 'identifier': steamid })
        record = cursor.fetchone()
        if record == None:
            await embededmessages(message, "Dar um bote", "Erro", "Não existe sequer uma pessoa com o 'steamid' inserido porra.")
        else:
            if plate is None:
                plate = "69AIB696"

            playername = record[1]
            await embededmessages(message, "Dar um bote", "Sucesso", "O tal '" + carname + "' de matrícula '" + plate + "' foi dado ao " + playername + ", ok?")

        connection.close()

async def embededmessages(message, action, state, description):
    # Prepare discord embeded message
    embed=discord.Embed(title="Bertram - O Mordomo")

    if state == "Sucesso":
        embed.color=discord.Color.green()
    elif state == "Erro":
        embed.color=discord.Color.red()

    embed.set_thumbnail(url="https://static.wikia.nocookie.net/disneyjessieseries/images/3/3e/J110.jpg/revision/latest/scale-to-width-down/286?cb=20120324031248")
    embed.add_field(name="Pedido feito por", value=message.author.name + "#" + message.author.discriminator, inline=False)
    embed.add_field(name="Ação", value=action, inline=True)
    embed.add_field(name="Estado", value=state, inline=True)
    embed.add_field(name="Mensagem", value=description, inline=False)
    embed.set_footer(text="Powered by Bertram - 2021")

    await message.channel.send(embed=embed)

client.run(secretdata['token'])

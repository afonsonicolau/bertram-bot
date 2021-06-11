import discord
import os
import re

client = discord.Client()

@client.event
async def on_ready():
    print('Hello World, I am {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('<@!852648286602919964>'):
        usermessage = message.content
        messagesplited = usermessage.split()
        botcommand = messagesplited[1]

        if re.search('[1-5]:([\a-zA-Z\][0-9]{15})$', messagesplited[2]):
            if botcommand == "darbote":
                await givecar(messagesplited[2], messagesplited[3], message)
        else:
            # Prepare discord message embedment
            embed = discord.Embed(title="Bertram - O Mordomo", color=discord.Color.red())
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/disneyjessieseries/images/3/3e/J110.jpg/revision/latest/scale-to-width-down/286?cb=20120324031248")
            embed.add_field(name="Pedido feito por", value=message.author.name + "#" + message.author.discriminator, inline=False)
            embed.add_field(name="Ação", value="Dar um veículo", inline=True)
            embed.add_field(name="Estado", value="Erro", inline=True)
            embed.add_field(name="Mensagem", value="Parece que alguém se enganou a inserir o identificador de um jogador, não?", inline=False)
            embed.set_footer(text="Powered by Bertram - 2021")

            await message.channel.send(embed = embed)

async def givecar(steamid, carmodel, message):
    embed = discord.Embed(title="Bertram - O Mordomo", color=discord.Color.green())
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/disneyjessieseries/images/3/3e/J110.jpg/revision/latest/scale-to-width-down/286?cb=20120324031248")
    embed.add_field(name="Pedido feito por", value=message.author.name + "#" + message.author.discriminator, inline=False)
    embed.add_field(name="Ação", value="Dar um veículo", inline=True)
    embed.add_field(name="Estado", value="Sucesso", inline=True)
    embed.add_field(name="Mensagem", value="Muito bem, não foi assim tão difícil.", inline=False)
    embed.set_footer(text="Powered by Bertram - 2021")

    await message.channel.send(embed = embed)

client.run(os.getenv('TOKEN'))

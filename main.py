import discord
import os
import re

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
      messagesplited = usermessage.split()

      # Verify if array has enough indexes
      if len(messagesplited) == 4:
        botcommand = messagesplited[1]
        steamid = messagesplited[2]
        carmodel = messagesplited[3]

        if re.search('[1-5]:([\a-zA-Z\][0-9]{15})$', steamid):
          if botcommand == "darbote":
            await givecar(steamid, carmodel, message)
        else:
          await embededmessages(message, "Dar um veículo", "Erro", "Alguém inseriu um identificador de um jogador errado, não foi?")
      else:
        await embededmessages(message, "Nenhuma", "Erro", "O formato da mensagem deverá ser: @Bertram <ação> <steamid> <objeto/veículo>")
        return
      
async def givecar(steamid, carmodel, message):
  # Verify in database first if steamid is valid.
  await embededmessages(message, "Dar um veículo", "Sucesso", "Muito bem, não foi assim tão difícil")

async def embededmessages(message, action, state, description):
  # Prepare discord message embedment
  if state == "Sucesso":
    embed=discord.Embed(title="Bertram - O Mordomo", 
    color=discord.Color.green())
  elif state == "Erro":
    embed=discord.Embed(title="Bertram - O Mordomo", 
    color=discord.Color.red())

  embed.set_thumbnail(url="https://static.wikia.nocookie.net/disneyjessieseries/images/3/3e/J110.jpg/revision/latest/scale-to-width-down/286?cb=20120324031248")
  embed.add_field(name="Pedido feito por", value=message.author.name + "#" + message.author.discriminator, inline=False)
  embed.add_field(name="Ação", value=action, inline=True)
  embed.add_field(name="Estado", value=state, inline=True)
  embed.add_field(name="Mensagem", value=description, inline=False)
  embed.set_footer(text="Powered by Bertram - 2021")

  await message.channel.send(embed = embed)

client.run(os.getenv('TOKEN'))

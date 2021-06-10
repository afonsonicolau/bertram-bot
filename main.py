import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Hello World, I am {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('<@!852648286602919964>'):
      await message.channel.send('Hello user!')

client.run(os.getenv('TOKEN'))

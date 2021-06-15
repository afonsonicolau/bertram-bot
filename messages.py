import discord

emojis = {'thinking': '🤔',
          'success': '✅',
          'error': '❌'}


async def embeded_messages(message, action, state, description):
    # Prepare discord embeded message
    embed = discord.Embed(title="Bertram - O Mordomo")

    if state == "Sucesso":
        embed.color = discord.Color.green()
        await add_emoji(message, 'success')
    elif state == "Erro":
        embed.color = discord.Color.red()
        await add_emoji(message, 'error')

    embed.set_thumbnail(url="https://static.wikia.nocookie.net/disneyjessieseries/images/3/3e/J110.jpg/revision/latest/scale-to-width-down/286?cb=20120324031248")
    embed.add_field(name="Pedido feito por", value=message.author.name + "#" + message.author.discriminator, inline=False)
    embed.add_field(name="Ação", value=action, inline=True)
    embed.add_field(name="Estado", value=state, inline=True)
    embed.add_field(name="Mensagem", value=description, inline=False)
    embed.set_footer(text="Powered by Bertram - 2021")

    await message.channel.send(embed=embed)


async def add_emoji(message, emoji_requested):
    # Prepare emoji to add to message
    emoji = emojis[emoji_requested]

    await message.add_reaction(emoji)

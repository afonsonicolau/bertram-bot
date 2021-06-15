import sql
import messages


async def get_character(steamid, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()
        cursor.execute("SELECT * FROM users WHERE identifier LIKE %(steamid)s", {'steamid': '%' + steamid})
        characters = cursor.fetchall()

        if len(characters) > 0:
            formatted_characters = ""

            for character in characters:
                formatted_characters += "\nIdentificador - " + character[0] + " | Nome - " + character[1]

            await messages.embeded_messages(message, "Personagens de um jogador", "Sucesso", "As seguintes personagens foram encontradas: \n" + formatted_characters)
        else:
            await messages.embeded_messages(message, "Personagens de um jogador", "Erro", "O 'steamid' inserido não consta em nenhum personagem.")

        sql.close_connection()

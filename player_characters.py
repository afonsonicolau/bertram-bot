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

async def manage_multichar(steamid, action, message):
    if sql.open_connection():
        cursor = sql.connect_cursor()

        cursor.execute("SELECT * FROM multichar_donators WHERE steamid = %(steamid)s", {'steamid': steamid})
        steamid_exists = cursor.fetchone()

        if action == 'dar':
            if steamid_exists is None:
                cursor.execute("SELECT identifier FROM users WHERE identifier LIKE %(steamid)s", {'steamid': '%' + steamid})
                player = cursor.fetchone()
                print(player)
                if player is not None:
                    sql.run_query("INSERT INTO multichar_donators(steamid) VALUES(%(steamid)s);", {'steamid': steamid})
                    await messages.embeded_messages(message, "Adicionar ao multichar", "Sucesso", "O jogador com o 'steamid' '" + steamid + "' tem agora permissão para ter mais personagens.")
                else:
                    await messages.embeded_messages(message, "Adicionar ao multichar", "Erro", "Não existe nenhum jogador com o 'steamid', logo não.")
            else:
                await messages.embeded_messages(message, "Adicionar ao multichar", "Erro", "Este 'steamid' já tem acesso a 'multichars'.")
        elif action == 'tirar':
            if steamid_exists is not None:
                sql.run_query("CALL remove_multichar(%(steamid)s)", {'steamid': steamid})
                await messages.embeded_messages(message, "Retirar do multichar", "Sucesso", "O jogador com o 'steamid' '" + steamid + "' foi retirado dos 'multichars'.")
            else:
                await messages.embeded_messages(message, "Retirar do multichar", "Erro", "Este 'steamid' nem está nos 'multichars' quanto mais.")

        sql.close_connection()

import os
import os
from sys import path
import jsoner.json_files as json_files
import messages
import subprocess


async def verify_data(message, commit_hash, at_symbol, project_to_deploy):
    project_valid = project_to_deploy in json_files.get_field('projects')

    if at_symbol == '@' and project_valid:
        path_to_deploy = json_files.get_field('projects.' + project_to_deploy + '.path_to_deploy')
        # Go to folder directory
        os.chdir(path_to_deploy)
        # Check if commit hash is valid
        verify = os.system('git reset --hard ' + commit_hash)

        if verify == 0:
            await messages.embeded_messages(message, "Deploy", "Sucesso", "O commit **" + commit_hash + "** está agora em efeito no projeto " + project_to_deploy.upper() + ".")
        else:
            await messages.embeded_messages(message, "Deploy", "Erro", "O commit **" + commit_hash + "** não é correto de facto.")
    else:
        await messages.embeded_messages(message, "Deploy", "Erro", "O comando de deploy é o seguinte:\n `@Bertram deploy <commit> @ <projeto>`\n\nTenta outra vez e verifica se o projeto é válido:\n-> tnlrp.")

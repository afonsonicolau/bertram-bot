import os
import os
import json_files
import messages


async def verify_data(message, commit_hash, at_symbol, project_to_deploy):
    project_valid = project_to_deploy in json_files.get_field('secrets', 'projects')

    if at_symbol == '@' and project_valid:
        path_to_deploy = json_files.get_field('secrets', 'projects.' + project_to_deploy + '.path_to_deploy')
        # Go to folder directory
        os.chdir(path_to_deploy)
        # Check if commit hash is valid
        os.system('git cat-file commit ' + commit_hash)
        # Reset code and pull commit hash
        os.system('git reset --hard ' + commit_hash)

        await messages.embeded_messages(message, "Deploy", "Sucesso", "O commit **" + commit_hash + "** está agora em efeito.")
    else:
        await messages.embeded_messages(message, "Deploy", "Erro", "O comando de deploy é o seguinte:\n `@Bertram deploy <commit> @ <projeto>`\n\nTenta outra vez.")

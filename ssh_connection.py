import json_files
# SSH
import paramiko

ssh_client = paramiko.SSHClient()


def open_connection():
    # SSH private key
    ssh_private_key = paramiko.RSAKey.from_private_key_file('/home/nicolau/.ssh/id_rsa')

    ssh_client.load_host_keys('/home/nicolau/.ssh/known_hosts')
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    ssh_client.connect(hostname=json_files.get_field('ssh.ip'),
                       port=22,
                       username=json_files.get_field('ssh.username'),
                       pkey=ssh_private_key)

    stdin, stdout, stderr = ssh_client.exec_command('hostname')
    print(f'STDOUT: {stdout.read().decode("utf8")}')

    stdin.close()
    stdout.close()
    stderr.close()


def close_connection():
    ssh_client.close()

import datetime
import subprocess

'''Esse pequeno código tem o proposito de realizar uma pequena auditória em um sistema Linux. 
Alguns dos comandos devem ser realizados com permissões sudo'''

whoami = 'who' #Mostra usuario atuais no sistema
ipconfig = 'ip a' #Mostra configurações de ip
netstat_all = 'netstat -antu' #Mostra conexões TCP e UDP ativas no sistema
netstat_established = "netstat -antu | grep 'ESTABLISHED'" #Mostra conexões estabelecidas
last = 'last -a | head' #Verifica os últimos logins
crontabs = 'sudo ls -la /etc/cron.d /etc/cron.daily' #Verifica se tem alguma persistência no sistema
journalctl = 'sudo journalctl -u ssh' #Verifica logins SSH em sistemas modernos
auth_log = 'sudo grep -iE "authentication failure|failed password" auth.log' #Verifica falhas de login SSH
diskusage = 'df -h' #Verifica espaço em disco.

def commands(terminalinput):
    #Interpreta cada string como um comando do Shell.
    terminaloutput = subprocess.run(terminalinput, capture_output=True, text=True, shell=True)
    if terminaloutput.returncode == 0:
        print(f'Salvando retorno do comando {terminalinput}')
        with open(f'logs.{atual}', 'a') as log: #Salva o output em um arquivo logs com a data atual do sistema.
            log.write(f'{'='*20}Salvando retorno do comando {terminalinput}{'='*20}\n{terminaloutput.stdout}\n')
    else:
        print(f'erro ao executar {terminaloutput}')

atual = datetime.date.today() #Pega a data atual


#Utilizando threading, é possível fazer com que outros comandos rodem enquanto o tracert não é finalizado.
commands(whoami)
commands(ipconfig)
commands(netstat_all)
commands(netstat_established)
commands(last)
commands(crontabs)
commands(journalctl)
commands(diskusage)

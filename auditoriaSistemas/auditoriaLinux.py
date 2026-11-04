from datetime import datetime
import subprocess
import sys, os
import threading

'''Esse pequeno código tem o proposito de realizar uma pequena auditória em um sistema Linux. 
Esse script deve ser realizado com um usuário com permissões administrativas.'''

lista_cores = ['\033[91m', #Vermelho
'\033[92m', #Verde
'\033[93m', #Amarelo
'\033[1m', #Negrito
'\033[0m',] #Finaliza a cor

commands_dict = {'usuarios logados':'w', #Mostra usuarios logados no sistema
                           'ipconfig':'ip a',#Mostra configurações de ip
                           'CPU_usage':'ps -eo pid,ppid,user,cmd --sort=-%cpu | head -20', #Filtra pelos processos com maior consumo de CPU
                           'ss_conexoes_processos':'ss -tunap', #Mostra todas as conexões e seus processos associados a cada conexão
                           'ss_portas':"ss -tunl", #Mostra as portas escutando
                           'last':'last -a | head', #Verifica os últimos logins
                           'usuarios_root':'awk -F: \'$3==0\' /etc/passwd', #Mostra usuarios com permissao root no sistema.
                           'crontabs':'sudo ls -la /etc/cron* ', #Verificação das crontabs com o intuito de verificar se há algum executável de persistência no sistema
                           'systemd_services':'systemctl list-unit-files --state=enabled', #Verifica os serviços habilitados e gerenciados pelo systemd.
                           'systemd_timers':'systemctl list-timers', #Verifica quando foi ativado cada recurso "unit"
                           'journalctl':f'journalctl -u ssh -u sshd --no-pager --since "7 days ago"', #Verifica logins SSH em sistemas modernos
                           'procura_SUID':'find / -perm -4000 -type f 2>/dev/null', #Procura por arquivos com SUID habilitado em todo o sistema.
                           'auth_log':'grep -iE "authentication failure|failed password" /var/log/auth.log || sudo grep -iE "authentication failure|failed password" /var/log/secure', # Verifica falhas de login SSH em sistema Ubuntu/Debian ou CentOS/RHEL
                           'diskusage':'df -h'} #Verifica espaço em disco

if os.geteuid() != 0:  # Block if que faz a checagem do usuário atual. Esse script deve ser rodado como root.
    print(f'{lista_cores[3]}Este script precisa ser executado como root ou utilizando o préfixo "sudo".{lista_cores[4]}')
    sys.exit(1)

def commands(terminalinput):

    #Interpreta cada string como um comando do Shell.
    terminaloutput = subprocess.run(terminalinput, capture_output=True, text=True, shell=True)

    if terminaloutput.returncode == 0 or (terminaloutput.returncode == 1 and terminaloutput.stdout):
        print(f'{lista_cores[1]}Salvando retorno do comando {terminalinput}{lista_cores[4]}')
        with open(f'logs.{datetime.now().strftime("%Y-%m-%d")}', 'a') as log: #Salva o output em um arquivo logs com a data atual do sistema.
            log.write(f'{'='*20}Salvando retorno do comando {terminalinput}{'='*20}\n{terminaloutput.stdout}\n')
    else:
        print(f'{lista_cores[0]}Erro ao executar o comando {terminalinput}.\n\t- ERROR: {terminaloutput.stderr}{lista_cores[4]}')


# Executa a função commands para realizar a varredura inicial no sistema.

try:
    for c in commands_dict.values():
        chore1 = threading.Thread(target=commands, args=(c,))
        chore1.start()
except Exception as e:
    print('Não foi possível realizar a varredura completa.')
except KeyboardInterrupt as e:
    print('A execução do programa foi cancelada. Os resultados foram salvos no arquivo de logs.')

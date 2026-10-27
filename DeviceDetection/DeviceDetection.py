# Caso esteja utilizando a IDE Pycharm, importe as bibliotecas scapy.layers.12 e scapy.sendrecv para importar os m[odulos ARP, Ether e srp.
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import json
from datetime import datetime
from time import sleep
import pandas as pd
import sys

# Caso esteja utilizando a IDE Visual Studio, import os módulos do scapy da seguinte forma:
#from scapy.all import ARP, ETHER, srp

#Qual é o nome e a extensão(xlsx, xlsm, xls) do arquivo que contêm os dispositivos confiáveis?

escolha = input(""" Selecione uma opção:
[0] - Selecionar um arquivo em formato xlsx para realizar a Leitura dos hosts confiáveis. O arquivo deve conter duas colunas nomeadas de IP e MAC
[1] - Encerra o programa.
> """)[0] #Define a escolha do usuário.

if escolha in "0":
    planilha = input('Nome do arquivo+extensão: ')
    df = pd.read_excel(planilha)  # Define a planilha
    trusted_devices = dict(zip(df["IP"], df["MAC"])) #Cria o dicionário mapeando a coluna de IP para a coluna de MAC
    #O formato ficará da forma:
    # trusted_devices = {"192.168.3.1": "hostname ou MACADDRESS","192.168.3.114": "hostname ou MACADDRESS"}

if escolha in "1":
    print('Parando o programa...')
    sys.exit()

#trusted_devices = {"192.168.3.1": "Router","192.168.3.114": "Meu PC"}

input_rede = input('Defina a rede que deseja realizar o scan:\n'
                       '(Ex: 192.168.0.1/24)\n> ')


def scan(rede):
    arp_protocol = ARP(pdst=rede) #A classe pdsf descobre o MAC address através de um IP na mesma LAN. Trabalha na camada 2
    ether = Ether(dst="FF:FF:FF:FF:FF:FF") #Faz um broadcast a procura do MAC address na rede especificada. Trabalha na camada 3.
    pacote = ether / arp_protocol #O frame Ethernet encapsula o Pacote ARP.

    #Envia dados e recebe respostas
    resultado = srp(pacote, timeout=2, verbose=0)[0] #Envia pacotes com um timeout de 2 segundos; define o output para 1. Pega somente o item do index 0, que é o mais importante para nós.

    devices = [] #Essa lista armazena dicionários com IP e MAC address dos dispositivos da rede.
    for e, r in resultado:
        devices.append({
            'IP': r.psrc, #Guarda o IP de origem da ARP Reply
            'MAC': r.hwsrc #Guarda o MAC de origem da ARP Reply
        })

    devices.append({'IP': '192.168.3.166',
                    'MAC': 'AA:FF:DD:EE:CC:XX'}) #Utilizada para teste

    return devices


#Função para detectar dispositivos novos e desconhecidos.
def detect_notrust(devices2):
    """Faz uma varredura na rede e detecta os dispositivos que não estão na variável trusted_devices"""
    unknown = []
    for dev in devices2:
        ip = dev['IP']
        mac = dev['MAC']
        if ip not in trusted_devices and mac not in trusted_devices:
            unknown.append(dev)

    return unknown


def relatorio(resultados_dispositivos):
    arquivo = f"network_report_{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.json"

    #Abre o arquivo em formato json para salvar os dados estruturados.
    with open(arquivo, 'w') as f:
        json.dump(resultados_dispositivos, f, indent=4) #Escreve um objeto Python em um arquivo com o formato json.
        print(f'[+] Relatório salvo em {arquivo}')


def main():
    #Execução do código
    found_devices = scan(input_rede) #Define a rede que será escaneada

    print('Escaneando rede local...')
    sleep(2)

    print('Verificando dispositivos desconhecidos na rede...\n')
    sleep(2)
    new_devices = detect_notrust(found_devices)


    if new_devices:
        print("[!] Dispositivos não reconhecidos foram encontrados na rede:")
        for devs in new_devices:
            print(f"\t* {devs['IP']} - {devs['MAC']}")
        relatorio(new_devices)
    else:
        print("[+] Nenhum dispositivo desconhecido encontrado.")


if __name__ == "__main__":
    main()

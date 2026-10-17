import socket

target_list = list()
target_ports = list()

def scan(chosen_host, chosen_port):
    for c in chosen_host: #Esse loop passa pelos hosts primeiro escaneando porta por porta.
        print('=' * 40)
        print(f'Scan do Ativo: {c}')
        for port in chosen_port: #Esse loop passa pelas portas
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(0.5) #Tempo maximo de espera em cada porta
            connection = client.connect_ex((c, port)) #Com connect_ex, voce nao utiliza os bloco de try e except, no lugar voce utilizara if e else statements
            if connection == 0:
                print(f'[+] Host: {c} | Porta {port} ABERTA!')
                client.close()
            else:
                print(f'[-] Host: {c} | Porta {port} FECHADA!')


while True:
    target1 = input('Quais ou Qual IP(s)/host(s) você deseja escanear?\n(Coloque um valor nulo ( ) caso não deseje fornecer mais valores.\n> ')
    target_list.append(target1)
    if target1 in '':
        #Nesse bloco if, caso o último valor seja um valor nulo ( ), o loop será quebrado é o último valor da lista será apagado, que é o valor NULO. Com isso, o valor nulo não passará para a função.
        del target_list[-1]
        print('\n\n'*2)
        break


while True:
    # Bloco de try e except para lidar com as portas
    try:
        ports = input('Quais portas deseja realizar o scan?\n\t(A opção 0 seleciona as portas mais comuns de serviço.\n\t(Coloque [ ] caso tenha finalizado a lista de portas.\n> ')
        if ports.isdecimal():
            ports = int(ports)
            target_ports.append(ports)
            if ports == 0:
                target_ports = [21,22,23,53,80,110,123,143,161,25,443]
                break
        elif len(target_ports) == 0:
            print('Forneça ao menos um valor de porta para ser escaneado.')
        elif ports in ' ':
            break
    except KeyboardInterrupt:
        print('Execução cancelada.')
        #continue
    except Exception as E:
        print(f'Erro no código {E}')


scan(target_list, target_ports)

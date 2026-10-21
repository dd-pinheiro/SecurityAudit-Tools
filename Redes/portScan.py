import socket
import threading
import csv
from queue import Queue
from datetime import datetime
from time import sleep

#Cores
lista_cores = ['\033[91m', #Vermelho
'\033[92m', #Verde
'\033[93m', #Amarelo
'\033[1m', #Negrito
'\033[0m',] #Finaliza a cor


def get_banner(ip, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, porta))
        banner = s.recv(1024).decode(errors="ignore").strip() #Recebe o conteúdo de bytes e traduz para string.
        s.close()
        return banner if banner else "sem banner" #retorna o Banner caso seja "TRUE", caso contrário retorna a string "sem banner"
    except:
        return "sem resposta"


def service_identifier(banner):
    """Essa função tenta identificar o serviço que está rodando no sistema. Essa função é importante pois alguns serviços não estão setados em suas portas padrões."""
    format_banner = banner.lower()
    if "http" in format_banner:
        return "HTTP"
    elif "ftp" in format_banner:
        return "FTP"
    elif "ssh" in format_banner:
        return "SSH"
    elif "smtp" in format_banner:
        return "SMTP"
    elif "imap" in format_banner:
        return "IMAP"
    elif "pop3" in format_banner:
        return "POP3"
    else:
        return "N/A"


def scan(chosen_host, chosen_port, resultados):
    """Essa função realiza a varredura, obtêm Banners e o tipo de serviço da porta.
    A variável 'resultados' será utilizada para agregar na função de relatorio"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((chosen_host, chosen_port))
        banner = get_banner(chosen_host, chosen_port)
        service = service_identifier(banner)
        resultados.append((chosen_port, service, banner)) #Essa variavel será utilizada para armazenar as informacoes nos arquivos de texto.
        print(f'Porta {chosen_port} -> {lista_cores[1]}[OPEN]{lista_cores[4]} | Servico: {service} | Banner: \033[4m{banner}{lista_cores[4]}')
        sock.close()
    except:
        resultados.append((chosen_port, 'CLOSED', ""))
        print(f'Porta {chosen_port} -> {lista_cores[0]}FECHADA!{lista_cores[4]}')




#Funcao de threads utilizada para acelerar o processo.
def threads_process(ip, portas):
    resultados = []
    threads_list = []
    queue = Queue() #Cria uma fila segura para os threads que serao utilziados nessa funcao
    for porta in portas:
        queue.put(porta)

    def work_threads():
        while not queue.empty():
            porta = queue.get()
            scan(ip, porta, resultados)
            queue.task_done()


    # Ajuda a fazer a varredura simultânea das portas.
    for _ in range(min(20, len(portas))):
        t = threading.Thread(target=work_threads)
        t.start()
        threads_list.append(t)

    queue.join() # assim que o loop de threading for finalizado, ele volta para Queue. Isso irá continuar até o fim da varredura de portas.
    return resultados

# Função utilizada para escrever o resultado em um relatório.
def relatorio(ip, resultados):
    data_atual = datetime.now().strftime('%Y-%m-%d') #Pega a data atual no formato YY-MM-DD
    texto = f"report_{ip}_{data_atual}.txt" #salva o arquivo com o nome da URL
    planilha = f"report_{ip}_{data_atual}.csv"

    print(f'{lista_cores[2]}\nSalvando resultados...{lista_cores[4]}')
    sleep(3)

    #Abre o arquivo txt e salva o conteúdo.
    with open(texto, "w", encoding="utf-8") as f:
        f.write(f"Relatório de Varredura do alvo: {ip}\nData: {datetime.now()}\n\n")
        for porta, serv, banner in resultados:
            f.write(f"Porta {porta:5} | Serviço: {serv:10} | Banner: {banner}")

    with open(planilha, "w", encoding="utf-8") as f:
        writer = csv.writer(f) #Come
        writer.writerow(["Porta", "Serviço", "Banner"]) #Coloca o nome das colunas
        for porta, serv, banner in resultados:
            writer.writerow([porta, serv, banner])

    print(f"\n{lista_cores[2]}Relatórios salvos:\n- {texto}\n- {planilha}{lista_cores[4]}")


def varrer_alvos(targets, portas):
    for target in targets:
        print(f"\n{lista_cores[3]}{'*-' * 10}Varredura do alvo: \033[4m{target}\033[0m {'*-' * 10}{lista_cores[4]}")
        resultados = threads_process(target, portas)
        relatorio(target, resultados)



def main():
    targets_input = input('Quais ou Qual IP(s)/host(s) você deseja escanear? (Separe por vírgula caso tenha mais de um)\n> ')
    targets = [t.strip() for t in targets_input.split(",")] #Tira espaçamentos e transforma em uma lista.
    escolha_ports_input = input('Deseja prosseguir com a escolha de portas padrões do código? [S/N]')

    if escolha_ports_input in 'Ss':
        default_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 1521, 3389, 3306, 8080, 27017]

    else:
        #Esse bloco de código trabalha com as portas que o usuário desejar.
        ports_input = input('Em quais portas deseja realizar o scan? (Separe por vírgula caso tenha mais de uma)\n> ')
        default_ports = [p.strip() for p in ports_input.split(",")] #Transforma em uma lista
        default_ports = [int(p) for p in default_ports] #Transforma todos os valores da lista em numericos.

    varrer_alvos(targets, default_ports)


if __name__ == "__main__":
    main()

# Apresentação

Essa é uma pequena ferramenta em Python que utiliza principalmente a biblioteca **Scapy** do Python, e tem como função realizar a varredura na rede Local com o intuíto de descobrir hosts novos que não são considerados confiáveis.
Abaixo, segue algumas caracteristicas da ferramenta:
- Aceita entrada de um arquivo xlsx/xls do usuário.
- Utiliza a biblioteca pandas para realizar a leitura do arquivo
- Utiliza a biblioteca Scapy, mais especificamente com o módulo ARP para descobrir dispositivos não confiáveis na rede
- Salva os dispositivos novos/não confiáveis em um relatório em formato json.

## Pontos de atenção
O script deve ser executado com permissões administrativas. Além disso, é necessário instalar as seguintes bibliotecas em seu sistema para que o código rode a biblioteca Scapy sem erros:
- Scapy
- pandas
- openpyxl

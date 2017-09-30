#### IMPORTANTE : esse codigo pressupoe que os modulos ja estabeleceram conexao. Uma nova versao deve vir com
#### o estabelecimento da conexao dos modulos de forma automatizada.
#### A conexao pode ser realizada a partir de uma serie de instrucoes que serao explicitadas aqui em uma versao posterior


import time
import serial as ser
import re
import random
import string

DEBUG = True
##### Mudar aqui embaixo com o numero da porta
# Depende de qual o sistema operacional rodando
#node = ser.Serial('/dev/ttyusb0', timeout=3)
node = ser.Serial('COM3', timeout=3)
node.baudrate = 115200

##### Teste da comunicação
my_string = b'AT\r\n'
condition = False
while not condition:
    node.write(my_string)
    n = node.readline()
    resposta = node.read(5)
    if DEBUG:
        print(resposta)
    condition = b'OK' in resposta
#############################


if DEBUG:
    print(resposta)
    node.write(b'AT+CWMODE?\r\n')
    time.sleep(0.08)
    resposta = node.read(100)  # Numero grande pra ser maior que o buffer


# Esse input apenas ajuda na geracao do nome do arquivo final, para posteriormente identifica-lo mais facilmente
dis = input('Distancia :')

# Usado na geracao do nome do arquivo e para determinar o tamanho do pacote aleatorio a ser enviado
tamanho_do_pacote = int(input('Tamanho do pacote :'))

# Esse input apenas ajuda na geracao do nome do arquivo final, para posteriormente identifica-lo mais facilmente
versao = input('Versao :')

node.write(b'AT+CWLIF\r\n') #Comando para identificar o endereço de ip do outro modulo wifi

time.sleep(0.08)

resposta = node.readline()
if DEBUG :
    print(resposta)
# Os readlines a seguir apenas servem para esvaziar o buffer
# O comentário abaixo é para a IDE nao reclamar
# noinspection PyRedeclaration
n = node.readline()
if DEBUG :
    print(n)
n = node.readline()
if DEBUG :
    print (n)

    
# Usando re (regular expressions) para encontrar o endereço de ip do outro modulo
ip = re.findall(r"[0-9]+(?:\.[0-9]+){3}", str(resposta))
if len(ip) != 1:
    if DEBUG:
        print(ip)

# Vetor que ira armazenar as medidas
medidas = []
pacotes_perdidos = 0
pacotes_enviados = 0

# Alterar aqui caso seja necessario enviar um numero menor/maior de pacotes
# NOTA : Para valores acima de 100, perde-se a conexão entre os modulos rapidamente.
MAX_PACOTES = 80


#gera um pacote aleatorio para ser enviado. Pode ser colocado dentro do loop while se for interessante gerar um pacote diferente por teste
random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(0, tamanho_do_pacote)])


# Tempo apenas para verificar os DEBUGs desse programa, ir ate o outro modulo e verificar os DEUBGs dele
time.sleep(10)


for i in range(0, MAX_PACOTES):
    my_string = b'AT+CIPSEND=0,' + bytes(str(tamanho_do_pacote), 'utf-8') + b'\r\n'
    
    # Envia para o modulo o comando de envio
    node.write(my_string)

    # Esvaziar o buffer ajuda a evitar problemas no envio de comandos
    n = node.read(100)
    
    # Envia o pacote
    node.write(b'>' + bytes(random, 'utf-8') + b'\r\n')
    t_antes = time.time()
    condition = False
    tempo_limite = time.time() + 15
    while (time.time() < tempo_limite) and not condition:
        n = node.readline()
        if DEBUG:
            print('n : ')
        if DEBUG:
            print(n)
            
        # Quando um pacote eh recebido, o codigo que ele manda é "+IPD" e o resto do pacote
        # Como o modulo conectado ao Arduino nem sempre exibe o comando certo, procurar apenas pelo + se mostrou
        # eficiente e mais garantido. Se o Arduino for substituido por outro FTDI, pode-se comentar essa linha e descomentar a proxima
        condition = '+' in str(n)
        #condition = '+IPD' in str(n)

        
    t_depois = time.time()
    if not condition:
        pacotes_perdidos += 1
    else:
        medidas.append((t_depois - t_antes))
        """ print(medidas)  """
        pacotes_enviados += 1
        
# Pode-se descomentar essa linha para Debugging, mas ela demora a ser executada ao final 
#if DEBUG : print(medidas)

print('Enviados : ' + str(pacotes_enviados))
print('Perdidos : ' + str(pacotes_perdidos))
print('Distancia : ' + dis)

filename = 'INDOR_TEMPO_DE_ENVIO_' + dis + '_' + str(tamanho_do_pacote) + '_' + str(versao)
f = open(filename, 'w')
for item in medidas:
    f.write(str(item) + '\n')
f.write('Enviados : ' + str(pacotes_enviados) + '\n')
f.write('Perdidos : ' + str(pacotes_perdidos) + '\n')
f.write('Distancia : ' + dis + '\n')
f.close()

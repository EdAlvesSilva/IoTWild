#### IMPORTANTE : esse codigo pressupoe que os modulos ja estabeleceram conexao. Uma nova versao deve vir com
#### o estabelecimento da conexao dos modulos de forma automatizada.
#### A conexao pode ser realizada a partir de uma serie de instrucoes que serao explicitadas aqui em uma versao posterior

import time
import serial as ser
import re
import random
import string
from numpy import mean

DEBUG = False
# Mudar aqui embaixo com o numero da porta
node = ser.Serial('COM4', timeout=3)
node.baudrate = 115200

t_medio = []

# Teste da comunicação
my_string = b'AT\r\n'
condition = False
while not condition:
    node.write(my_string)
    n = node.readline()
    resposta = node.read(5)
    if DEBUG:
        print(resposta)
    condition = b'OK' in resposta

if DEBUG:
    print(resposta)
    node.write(b'AT+CWMODE?\r\n')
    time.sleep(0.08)
    resposta = node.read(100)  # Numero grande pra ser maior que o buffer


node.write(b'AT+CWLIF\r\n')  # Comando para identificar o endereço de ip do outro modulo wifi

time.sleep(0.08)

resposta = node.readline()
if DEBUG:
    print(resposta)
# Os readlines a seguir apenas servem para esvaziar o buffer
# O comentário abaixo é para a IDE nao reclamar
# noinspection PyRedeclaration
n = node.readline()
if DEBUG:
    print(n)
n = node.readline()
if DEBUG:
    print(n)

ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(resposta))  # Usando re para encontrar o endereço de ip do outro modulo
if len(ip) != 1:
    if DEBUG:
        print(ip)
n_medidas = []
medidas = []
pacotes_perdidos = 0
pacotes_enviados = 0

time.sleep(10)

for j in range(10, 130, 10):
    random_bytes = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(0, j)])
    for i in range(0, 40):
        my_string = b'AT+CIPSEND=' + bytes(str(j), 'utf-8') + b'\r\n'
        node.write(my_string)
        node.readline()
        n = node.read(100)
        time.sleep(0.0001)
        node.write(bytes(random_bytes, 'utf-8') + b'\r\n')
        t_antes = time.time()
        condition = False
        tempo_limite = time.time() + 10
        while (time.time() < tempo_limite) and not condition:
            n = node.readline()
            if DEBUG:
                print('n : ')
                print(n)
            condition = '+IPD' in str(n)
        t_depois = time.time()
        if not condition:
            pacotes_perdidos += 1
        else:
            medidas.append((t_depois - t_antes))
            pacotes_enviados += 1
        time.sleep(0.0001)
    n_medidas.append(j/mean(medidas))
    t_medio.append(mean(medidas))
    del medidas[:]
    print('Tamanho do pacote : ' + str(j))
    print('Enviados : ' + str(pacotes_enviados))
    print('Perdidos : ' + str(pacotes_perdidos))
    pacotes_enviados = 0
    pacotes_perdidos = 0
node.write(b'AT+CIPSEND=5\r\n')
time.sleep(0.008)
node.write(b'F!M\r\n')
filename = str(input("Digite o nome do arquivo : ")) + '.txt'
f = open(filename, 'w')
iteravel = 0
for i in range(0,len(n_medidas)-1):
    iteravel += 10
    f.write(str(n_medidas[i]) + ',' + str(iteravel) + ',' + str(t_medio[i]) + '\n')
f.close()

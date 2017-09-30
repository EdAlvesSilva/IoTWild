#### IMPORTANTE : esse codigo pressupoe que os modulos ja estabeleceram conexao. Uma nova versao deve vir com
#### o estabelecimento da conexao dos modulos de forma automatizada.
#### A conexao pode ser realizada a partir de uma serie de instrucoes que serao explicitadas aqui em uma versao posterior

import time
import serial as ser
import random
import string

DEBUG = True

##### Mudar aqui embaixo com o numero da porta
# Depende de qual o sistema operacional rodando
sensor = ser.Serial('/dev/ttyusb0', timeout=3)
#sensor = ser.Serial('COM3', timeout=3)

sensor.baudrate = 115200


my_string = b'AT\r\n'
condition = False
while not condition:
    sensor.write(my_string)
    n = sensor.readline()
    resposta = sensor.read(5)
    if DEBUG: print(resposta)
    condition = ((resposta == b'OK\r\n') or (resposta == b'\r\nOK\r'))

sensor.write(b'AT+CWMODE?\r\n')
time.sleep(0.08)
resposta = sensor.read(100)  # Numero grande pra ser maior que o buffer
if DEBUG: print(resposta)

dis = input('Distancia :')
filename = '..\TEMPO_DE_PROC_' + dis + '_'
f = open(filename, 'w')
medidas = []
pacotes_recebidos = 0
a = True
while a :
    pacote_recebido = sensor.read()
    if '+IPD' in str(pacote_recebido) :
        t_antes = time.time()
        if 'F!M' in str(pacote_recebido) :
            a = False

            break
        pacote_recebido.replace(b'+IPD,', b'')
        if pacote_recebido[2] == b':' :
            tamanho_do_pacote = int(pacote_recebido[0:1])
        else :
            tamanho_do_pacote = int(pacote_recebido[0:2])
        random_bytes = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(0, tamanho_do_pacote - 2)])
        my_bytes = b'AT+CIPSEND=' + bytes(tamanho_do_pacote) + b'\r\n'
        #sensor.write(bytes(random_bytes,'utf-8') + b'\r\n')
        sensor.write(b'' + bytes(random, 'utf-8') + b'\r\n')
        t_depois = time.time()
        medidas.append(t_depois - t_antes)
        f.write(medidas[pacotes_recebidos])
        pacotes_recebidos += 1
        f.write( 'Pacotes recebidos : ' + str(pacotes_recebidos))
f.write( 'Pacotes recebidos : ' + str(pacotes_recebidos))
f.close()


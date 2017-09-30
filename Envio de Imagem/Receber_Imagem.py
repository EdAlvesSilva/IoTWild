#### IMPORTANTE : esse codigo pressupoe que os modulos ja estabeleceram conexao. Uma nova versao deve vir com
#### o estabelecimento da conexao dos modulos de forma automatizada.
#### A conexao pode ser realizada a partir de uma serie de instrucoes que serao explicitadas aqui em uma versao posterior

import time
import serial as ser
import re

DEBUG = True

sensor = ser.Serial('COM4', timeout=3)
sensor.baudrate = 115200

my_string = b'AT\r\n'
condition = False
while not condition:
    sensor.write(my_string)
    n = sensor.readline()
    resposta = sensor.read(5)
    if DEBUG:
        print(resposta)
    condition = ((resposta == b'OK\r\n') or (resposta == b'\r\nOK\r'))

sensor.write(b'AT+CWMODE?\r\n')
time.sleep(0.08)
resposta = sensor.read(100)  # Numero grande pra ser maior que o buffer
if DEBUG:
    print(resposta)

filename = 'Copia.png'
f = open(filename, 'wb')

while True:
    pacote_recebido = sensor.read(200)
    if 'F!M' in str(pacote_recebido):
        f.close()
        exit()
    for text in re.findall(r'\+IPD,([0-4],)?\d+:', str(pacote_recebido)):
        pacote_recebido.replace(bytes(text, 'utf8'), b'')
    f.write(pacote_recebido)

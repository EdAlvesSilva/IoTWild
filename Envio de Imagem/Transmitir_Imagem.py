#### IMPORTANTE : esse codigo pressupoe que os modulos ja estabeleceram conexao. Uma nova versao deve vir com
#### o estabelecimento da conexao dos modulos de forma automatizada.
#### A conexao pode ser realizada a partir de uma serie de instrucoes que serao explicitadas aqui em uma versao posterior

import time
import serial as ser

# import re
# import random
# import string
# from numpy import mean

DEBUG = True
# Mudar aqui embaixo com o numero da porta
node = ser.Serial('COM4', timeout=3)
node.baudrate = 115200

# Teste da comunicação
my_byte_string = b'ATE1\r\n'
condition = False
while not condition:
    node.write(my_byte_string)
    n = node.readline()
    resposta = node.read(5)
    if DEBUG:
        print(resposta)
    condition = b'OK' in resposta
# node.write(b'AT+CIPSTART="UDP","192.168.4.2",1002,1000,2\n')
# print(node.readline())
# print(node.readline())
# print(node.readline())
# print(node.readline())
i = 0
with open('iu.jpg', 'rb') as f:
    my_bytes = f.read(122)
    while len(my_bytes):
        time.sleep(1.1)
        g = bytes(str(len(my_bytes)), 'utf-8')
        node.write(b'AT+CIPSEND=0,' + g + b'\r\n')
        # print(my_bytes)
        # noinspection PyRedeclaration
        #        for i in range(0, 5):
        #            print(node.readline())
        time.sleep(0.008)
        node.write(b'' + my_bytes + b'\r\n')
        print(i)
        i += 1
        my_bytes = f.read(120)

time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')
time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')
time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')
time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')
time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')
time.sleep(2)
node.write(b'AT+CIPSEND=0,5\r\n')
time.sleep(0.01)
node.write(b'FIM\r\n')

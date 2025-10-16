# TCP client
import socket
import logging
import time
import sys
import random
import string

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)

def mesaj_random(length = 6):       #generarea unui mesaj random din 6 litere
    return "".join(random.choices(string.ascii_letters, k = length))
try:
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)    #conexiunea
    time.sleep(3)

    while True:
        mesaj = mesaj_random()      #se genereaza un mesaj random
        sock.send(mesaj.encode('utf-8'))    #se trimite catre server, intr-un format acceptat
        logging.info('Content trimis: "%s"', mesaj)     
        data = sock.recv(1024)      #primeste de la server pana la 1024 bytes
        logging.info('Content primit: "%s"', data.decode('utf-8'))
        time.sleep(2)               #asteapta

finally:
    logging.info('closing socket')
    sock.close()

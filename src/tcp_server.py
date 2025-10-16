# TCP Server
import socket
import logging
import time
import random
import string

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)
sock.bind(server_address)       #leaga socketul de adresa specificata; serverul asculta pe portul 10000, ip 198.7.0.2
logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)
sock.listen(5)              #serverul asculta pentru conexiuni, cu maxim 5 conexiuni in coada

def mesaj_random(length = 6):   #generarea unui mesaj random de 6 litere
    return "".join(random.choices(string.ascii_letters, k = length))

try:
    while True:
        logging.info('Asteptam conexiuni...')
        conexiune, address = sock.accept()      #asteapta o conexiune si, cand apare, o accepta
        logging.info("Handshake cu %s", address)    #se face handshake
        time.sleep(2)
        try:
            while True:
                mesaj = conexiune.recv(1024)      #serverul primeste un mesaj in formatul potrivit
                logging.info('Server a primit mesajul: "%s"', mesaj.decode('utf-8'))
                raspuns = mesaj_random()            #trimite un mesaj random catre client
                conexiune.send(raspuns.encode())    #intr-un format potrivit
                logging.info('Raspuns trimis: "%s"', raspuns)
            
        finally:
            logging.info("Conexiunea cu adresa " + str(address) + " inchisa")
            conexiune.close()
finally:
    sock.close()

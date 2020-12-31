import socket
import struct
import time
import keyboard

BufferSize=1024
client_port = 13117


"""
client connects to TCP server, and sends keyboard keys to server.
@:param addr: address of TCP server
@:param port: TCP server's port received by UDP server
"""
def connectTCP(addr,port):
    #TCP
    team_name = "Shikses"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", client_port))
    msg = "\n"+team_name
    client.connect((addr[0],port))
    client.send(msg.encode("utf-8"))

    #game-mode
    data, address = client.recvfrom(BufferSize)
    data = data.decode()
    print(data)

    # send as much as letters as you can
    start_time = time.time()
    while time.time()-start_time<=10:
        try:
            input1 = keyboard.read_key()
            if input1:
                input1 = bytes(input1, 'utf-8')
                client.send(input1)
        except Exception as e:
            print("Server disconnected, listening for offer requests...")
            break

    # game is over by server msg
    print(client.recvfrom(BufferSize)[0].decode())
    print("Server disconnected, listening for offer requests...")


"""
create an UDP connection with UDP server, and when port received - tries to connect to TCP server.
"""
def start():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", client_port))

    # udp connection
    print("Client started, listening for offer requests...")
    data, addr = client.recvfrom(BufferSize)

    if len(data)==8:
        data = struct.unpack('IBH', data)

        # tcp connection
        if(hex(data[0])=="0xfeedbeef" and hex(data[1])=="0x2"):
            port = data[2]
            print("Received offer from "+str(addr[0])+", attempting to connect...")
            connectTCP(addr,port)

        #reject msg
        elif (hex(data[0])!="0xfeedbeef"):
            pass





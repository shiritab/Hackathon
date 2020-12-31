import socket
import threading
import time
import random
import server_udp_final
import client_final

BufferSize=1024
our_port = 2106

# Stage 5
# connection - socket type of client
# address - ip and port of client
# group1, group2 - dictionaries
def handleClient(connection, address, group1, group2):
    connected = True
    while connected:
        # reveive team's name
        msg = connection.recv(BufferSize)
        msg_without_break_line = msg.decode()

        # into random group
        if len(group1) < 1:
            group1[connection] = msg_without_break_line
        elif len(group2) < 1:
            group2[connection] = msg_without_break_line
        else:
            num = random.randint(1,2)
            if num == 1:
                group1[connection] = msg_without_break_line
            if num == 2:
                group2[connection] = msg_without_break_line
        connected=False

# Stage 8 
# gets input from client, calculates count of letters sent and updates.
def handleInput(connection, address, charCounter_group1, charCounter_group2, group1, group2):
    connected = True
    while connected:
        msg = connection.recv(BufferSize)
        msg = msg.decode()
        if connection in group1:
            charCounter_group1 += len(msg)
        elif connection in group2:
            charCounter_group2 += len(msg)
        connected=False


def game_mode(server,group1, group2):
    charCounter_group1 = 0
    charCounter_group2 = 0
    
    """ Stage 6: print name of groups"""
    group1_sockets = list(group1.keys())
    group2_sockets = list(group2.keys())
    total_clients = group1_sockets+group2_sockets
    msg_part1 = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    msg_part2 = "\nGroup 2:\n==\n"
    msg_part3 = "Start pressing keys on your keyboard as fast as you can!!"
    for sock in group1_sockets:
        msg_part1+=group1[sock]+"\n"
    for sock in group2_sockets:
        msg_part2+=group2[sock]+"\n"
    final_msg = msg_part1+msg_part2+msg_part3
    for client in total_clients:
        client.send(final_msg.encode("utf-8"))

    """ Stage7: game time - client is going to send letters as many as possible
    while counts to 10 seconds, every 3 seconds we do timeout and then check if we haven't passed 10 seconds alreay."""
    start_time = time.time()
    while time.time()-start_time<=10:
        server.settimeout(3)
        server.listen()
        try:
            connection, address = server.accept()
            data=connection.recv(BufferSize)
            if(data):
                data2=data.decode()
                print(data2)
            thread = threading.Thread(target = handleInput, args=(connection,address, charCounter_group1, charCounter_group2, group1, group2))
            thread.start()
        except socket.timeout:
            continue
   

    """ Stage 9: server calculates which group wins, the most characters the better."""
    msg_part1 = "\nGame over!\nGroup 1 typed in "+ str(charCounter_group1) +" characters. Group 2 typed in "+ str(charCounter_group2) +" characters.\n"
    if charCounter_group1>charCounter_group2:
        msg_part2 = "Group 1 wins!\n"
        msg_part3 = "Congratulations to the winners:\n==\n"
        for sock in group1_sockets:
            msg_part3+=group1[sock]+"\n"
    elif charCounter_group2>charCounter_group1:
        msg_part2 = "Group 2 wins!\n"
        msg_part3 = "Congratulations to the winners:\n==\n"
        for sock in group2_sockets:
            msg_part3+=group2[sock]+"\n"
    else:
        msg_part2 = "It's a tie!\n"
        msg_part3 = ""

    # send for each client connected to server - summary msg.
    final_msg = msg_part1+msg_part2+msg_part3
    for client in total_clients:
        client.send(final_msg.encode("utf-8"))


"""
TCP server creates an connection with clients, and when 10 seconds are passed - games begin.
"""
def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_name = socket.gethostbyname(socket.gethostname())
    group1 = {}
    group2 = {}

    server.bind((server_name,our_port))

    # start both threads for server_udp and client
    threading.Thread(target=server_udp_final.start).start()
    client_thread = threading.Thread(target=client_final.start)
    client_thread.start()

    #connecting to clients  
    while True:
        start_time = time.time()
        while time.time()-start_time<=10:
            server.settimeout(1)
            server.listen()
            try:
                connection, address = server.accept() 
                thread = threading.Thread(target = handleClient, args=(connection,address, group1, group2))
                thread.start()
            except socket.timeout:
                continue

        print("\u001b[32mgame mode time!!!!\u001b[0m") 
        game_mode(server,group1, group2)
        group1={}
        group2={}

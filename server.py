import socket, json, threading, time
from permament_variables import CHAR_WIDTH,S_WIDTH,S_HEIGHT,PORT,IP_ADDRESS,cameray,camerax

"""Name: recv_from_client
    Parameter:client = socket.socket,client_list = list
    Return: None
    Purpose: This allows the player to send information to the server and then it will send it to the other player"""

def recv_from_client(client,client_list):
    while True:
        data = client.recv(1024)
        if not data:
            continue
        else:
            instruction = data.decode()
            command_list = instruction.split("#")
            for command in command_list:
                if command != "":
                    command_dct=json.loads(command)
                    for c in client_list:
                        if c != client:
                            c.send((json.dumps(command_dct)+"#").encode())
            print(command_list)

client_list = []
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS,PORT))
    s.listen(1)
    print("Server is setup and listening on port",PORT)
    while True:
        connection, address = s.accept()
        client_list.append(connection)
        print(connection)
        print(address)
        threading.Thread(target=recv_from_client, args=(connection,client_list)).start()
        if len(client_list) > 1:
            print("2 Players connected")
            middle_width = (camerax / 2)-16
            middle_height = (cameray / 2)-16
            msg = {"Command":"SETUP","Data":{"Player":1,"PlayerType":"Ranged","PlayerX":middle_width,"PlayerY":middle_height, "EnemyType":"Melee","EnemyX":middle_width+200,"EnemyY":middle_height}}
            client_list[0].send(json.dumps(msg).encode())
            msg = {"Command": "SETUP", "Data": {"Player":2,"PlayerType":"Melee","PlayerX": middle_width, "PlayerY": middle_height, "EnemyRanged":"Melee","EnemyX": middle_width-200, "EnemyY": middle_height}}
            client_list[1].send(json.dumps(msg).encode())
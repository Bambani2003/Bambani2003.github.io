import socket
import sys
from _thread import *
import TT_game

server = "10.7.164.182"
port = 6969
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)                                         # Number of poeple allowed to connect.
print("Server started.")
print("Waiting for connection....")


def read_pos():
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(10, TT_game.HEIGHT//2 - TT_game.PADDLE_HEIGHT//2),(TT_game.WIDTH - 10 - TT_game.PADDLE_WIDTH, TT_game.HEIGHT//2 - TT_game.PADDLE_HEIGHT//2)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode("utf-8"))
            pos[player] = data
            if not data:
                print("Disconnected!")             # Baic failsafe to stop inf loops etc.
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Lost connection!")
    conn.close()

current_player = 0


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread (threaded_client, (conn, current_player))
    current_player += 1
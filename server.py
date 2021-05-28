import pickle
import socket
import threading
import sys
import pickle
from game_elements import *
from game import Game

# message types:

POPUP = 'popup'
JOIN = 'join'
DEAL_HAND = 'deal_hand'
BID = 'bid'
PLAY_CARD = 'play_card'
INIT = 'init'
SHOW_DISCARD = 'show_discard'
SHOW_TALON = 'show_talon'
BIDDING = 'Bidding'
GAME_PHASE = 'game_phase'
STARTED = 'started'
SORTING = 'sorting'


server = "192.168.178.24"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error:
    str(socket.error)

# s.listen takes the number of possible connections as an argument
s.listen(3)
print("Waiting for a connection, server started")

players = []
connected = set()
idCount = 0


def threaded_client(conn, p, game):
    conn.send(str.encode(str(p)))
    game.add_player(Player(p))

    while True:
        try:
            data = conn.recv(4096 * 8)
            try:
                data = data.decode()

                if not data:
                    break
                else:
                    # TODO! milyen bejövő data lehet?

                    if data == "test":
                        print("in test msg handling")
                        game.new_popup(data)
                    elif data == SORTING:
                        print("in sorting msg handling")
                        game.players[p].change_sorting()

                    elif data == "bid":
                        print("bid accept called")
                        game.accept_bid()
                    elif data == "pickup":
                        print("pickup called")
                        game.pickup()
                    elif data == "passz":
                        print("pass called")
                        game.passz()

                    # TODO! game_phase-ek állítása

                    if game.game_phase in [STARTED, INIT] and len(game.players) == 3:
                        game.initialize()

                    conn.sendall(pickle.dumps(game))

            except:
                try:
                    data = pickle.loads(data)
                    for p in game.players:
                        if p.name == data.name:
                            p.update_all(data)
                    conn.sendall(pickle.dumps(game))

                except:
                    e = sys.exc_info()
                    print("server error in incoming message handling ", e)
                    break
        except:
            e = sys.exc_info()
            print(e)
            break

    print("Lost connection")
    conn.close()


game = Game()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0

    client_thread = threading.Thread(target = threaded_client, args = (conn, currentPlayer, game))
    client_thread.start()
    currentPlayer += 1

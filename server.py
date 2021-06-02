import pickle
import socket
import threading
import sys
import pickle
from game_elements import *
from game import Game
import time


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
PLAY = "play"




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
            data = conn.recv(4096 * 16)
            try:
                data = data.decode()

                if not data:
                    break
                else:
                    try:
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
                        elif data == "card_was_played":
                            print("card_was_played called")
                            game.play_card()
                            conn.sendall(pickle.dumps(game))
                            if len(game.cards_on_the_table) == 3:
                                print("all 3 players played a cards, invoking card collection")
                                time.sleep(2)
                                game.collect_played_cards()
                            else:
                                print("not all players played yet")
                        elif data.split(":")[0] == "adu":
                            print("adu msg received")
                            game.selected_game.adu = data.split(":")[1]
                            if hasattr(game.selected_game, 'has_40_at_start'):
                                game.selected_game.check_for_40()
                            if hasattr(game.selected_game, 'has_20_at_start'):
                                game.selected_game.check_for_20()

                        elif data == "husznegyven":
                            game.getHuszNegyven(game.selected_game.adu)
                        elif data.split(":")[0] == "kontra":
                            game.kontra(data.split(":")[1])
                        if game.game_phase in [STARTED, INIT] and len(game.players) == 3:
                            game.initialize()

                        conn.sendall(pickle.dumps(game))
                    except:
                        e = sys.exc_info()
                        print("data was: ", data, type(data))
                        print("server error in incoming string message handling ", e)
                        break

            except:
                try:
                    data = pickle.loads(data)
                    for p in game.players:
                        if p.name == data.name:
                            p.update_all(data)
                    conn.sendall(pickle.dumps(game))

                except:
                    e = sys.exc_info()
                    print("data was: ", data, type(data))
                    print("server error in incoming object message handling ", e)
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

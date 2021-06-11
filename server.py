import socket
import threading
import sys
import pickle
from game_elements import *
from game import Game
import time
import struct







def threaded_client(conn, p, game):
    conn.send(str.encode(str(p)))
    game.add_player(Player(p))

    while True:
        try:
            # data = conn.recv(4096 * 64)
            # send data

            # receive game object
            recv_data_size = struct.unpack('>I', conn.recv(4))[0]
            recv_data_id = struct.unpack('>I', conn.recv(4))[0]
            recv_payload = b""
            remaining_payload_size = recv_data_size
            while remaining_payload_size != 0:
                recv_payload += conn.recv(remaining_payload_size)
                remaining_payload_size = recv_data_size - len(recv_payload)
            if not type(recv_payload) == str():
                result = pickle.loads(recv_payload)
                data = pickle.loads(result)
            else:
                data = recv_payload


            if recv_data_id == 0:
                try:
                    # TODO! milyen bejövő data lehet?
                    if data == "test":
                        print("in test msg handling")
                        game.new_popup(data)
                    elif data.split(":")[0] == 'name':
                        p = int(data.split(":")[1])
                        n = data.split(":")[2]
                        names = []
                        for x in game.players:
                            names.append(x.name)
                        if n not in names:
                            game.players[p].name = n
                        else:
                            game.players[p].name = n + str(len(game.players))

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
                        serialized_payload = pickle.dumps(game)
                        conn.sendall(struct.pack('>I', len(serialized_payload)))
                        conn.sendall(struct.pack('>I', 2))
                        conn.sendall(serialized_payload)
                        if len(game.cards_on_the_table) == 3:
                            print("all 3 players played a cards, invoking card collection")
                            time.sleep(2)
                            game.collect_played_cards()
                        else:
                            print("not all players played yet")
                    elif data.split(":")[0] == "adu":
                        print("adu msg received")
                        game.selected_game.adu = data.split(":")[1]

                    elif data == "husznegyven":
                        game.getHuszNegyven(game.selected_game.adu)
                    elif data.split(":")[0] == "kontra":
                        game.kontra(data.split(":")[1])
                    elif data == "reset":
                        game.display_results()
                    if game.game_phase in [STARTED, INIT] and len(game.players) == 3:
                        game.initialize()



                except:
                    e = sys.exc_info()
                    print("data was: ", data, type(data))
                    print("server error in incoming string message handling ", e)
                    break

            elif recv_data_id == 1:
                try:
                    # print("should have received a player object")
                    # print("data type:", type(data))
                    # print("data:", data)
                    for p in game.players:
                        if p.name == data.name:
                            p.update_all(data)


                except:
                    e = sys.exc_info()
                    print("data was: ", data, type(data))
                    print("server error in incoming object message handling ", e)
                    break


            serialized_payload = pickle.dumps(game)
            conn.sendall(struct.pack('>I', len(serialized_payload)))
            conn.sendall(struct.pack('>I', 2))
            conn.sendall(serialized_payload)

        except:
            e = sys.exc_info()
            print(e)
            break

    print("Lost connection")
    conn.close()






def server(password = 'pirosulti'):

    # message types:
    global POPUP
    global JOIN
    global DEAL_HAND
    global BID
    global PLAY_CARD
    global INIT
    global SHOW_DISCARD
    global SHOW_TALON
    global BIDDING
    global GAME_PHASE
    global STARTED
    global SORTING
    global PLAY
    global players
    global connected
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



    # server_ip = "192.168.178.24"
    server_ip = "83.160.108.8"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
    except socket.error:
        print("socket error")
        str(socket.error)

    # s.listen takes the number of possible connections as an argument
    s.listen(3)
    print("Waiting for a connection, server started")

    players = []
    connected = set()
    idCount = 0

    game = Game()


    currentPlayer = 0
    while True:
        conn, addr = s.accept()

        result = conn.recv(4096).decode()
        print("password should have been received: ", result)
        if result != password:
            conn.send(str.encode('authentication failed'))
            conn.close()
        else:
            conn.sendall(str.encode('authenticated'))

            print("Connected to:", addr)

            idCount += 1
            p = 0

            client_thread = threading.Thread(target = threaded_client, args = (conn, currentPlayer, game))
            client_thread.start()
            currentPlayer += 1


# server()
from game_elements import *
import random

STARTED = 'started'
INIT = 'init'
BIDDING = 'bidding'

class Game(object):
    def __init__(self):
        self.players = []
        self.game_phase = STARTED
        self.card_played = []
        self.selected_game = None
        self.popups = ["", "", "", "", ""]
        self.deck = Deck()


    def new_popup(self, msg):
        self.popups.pop(0)
        self.popups.append(msg)

    def get_popups(self):
        return self.popups

    def update_game_phase(self, phase):
        self.game_phase = phase

    def get_game_phase(self):
        return self.game_phase

    def update_selected_game(self, selection):
        self.selected_game = selection

    def get_selected_game(self):
        return self.selected_game

    def add_player(self, player):
        self.players.append(player)

    def initialize(self):
        self.game_phase = BIDDING
        print("game init")
        self.deck.shuffle()
        print("shuffle done")
        if self.players[0].is_dealer == False and self.players[1].is_dealer == False and self.players[2].is_dealer == False:
            print("choosing dealer randomly")
            x = random.choice([0,1,2])
            self.players[x].is_dealer = True
            print("isdealer set true: ", self.players[x].is_dealer)
            print("x, player, player.isdealer", x, self.players[x].name, self.players[x].is_dealer)
        self.deal_hands()
        for p in self.players:
            p.sort_hand()

        print("init done")

    def deal_hands(self):
        print("in deal-hands")
        if self.players[0].is_dealer:
            print("p0 is dealer")
            self.players[2].set_hand(self.deck.cards[0:12])
            self.players[2].is_active = True
            self.new_popup(str(self.players[2].name) + " kezd")
            self.players[0].set_hand(self.deck.cards[12:22])
            self.players[1].set_hand(self.deck.cards[22:32])

        elif self.players[1].is_dealer:
            print("p1 is dealer")
            self.players[0].set_hand(self.deck.cards[0:12])
            self.players[0].is_active = True
            self.new_popup(str(self.players[0].name) + " kezd")
            self.players[2].set_hand(self.deck.cards[12:22])
            self.players[1].set_hand(self.deck.cards[22:32])

        elif self.players[2].is_dealer:
            print("p2 is dealer")
            self.players[1].set_hand(self.deck.cards[0:12])
            self.players[1].is_active = True
            self.new_popup(str(self.players[1].name) + " kezd")
            self.players[2].set_hand(self.deck.cards[12:22])
            self.players[0].set_hand(self.deck.cards[22:32])
        print("deal_hands done")
    def reset(self):
        #TODO! save game details for later
        self.game_phase = STARTED
        self.card_played = []
        self.selected_game = None
        self.new_popup("Új játék")

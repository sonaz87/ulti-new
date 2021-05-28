from game_elements import *
import random

STARTED = 'started'
INIT = 'init'
BIDDING = 'bidding'
PLAY = 'play'


class Game(object):
    def __init__(self):
        self.players = []
        self.game_phase = STARTED
        self.card_played = []
        self.selected_game = None
        self.popups = [" ", " ", " ", " ", " "]
        self.deck = Deck()
        self.talon = []
        self.bidding_list = ["", "", ""]
        self.current_game = 'No Game'
        self.vallalo = ""
        self.possible_games = {
            'No Game' : [0],
            'Passz' : [1, Passz()],
            'Piros passz' : [2, PirosPassz()],
            'Negyven-száz' : [3, NegyvenSzaz()],
            'Ulti' : [4, Ulti()],
            'Betli' : [5, Betli()],
            'Durchmarsch' : [6, Durchmarsch()],
            'Színtelen durchmarsch' : [6, SzintelenDurchmarsch()],
            'Negyven-száz Ulti' : [7, NegyvenSzazUlti()],
            'Piros negyven-száz' : [8, PirosNegyvenSzaz()],
            'Húsz-száz' : [9, HuszSzaz()],
            'Piros ulti' : [10, PirosUlti()],
            'Negyven-száz durchmarsch' : [11, NegyvenSzazDurchmarsch()],
            'Ulti durchmarsch' : [11, UltiDurchmarsch()],
            'Rebetli' : [12, Rebetli()],
            'Húsz-száz ulti' : [13, HuszSzazUlti()],
            'Redurchmarsch' : [14, ReDurchmarsch()],
            'Piros durchmarsch' : [14, PirosDurschmarsch()],
            'Negyven-száz ulti durschmarsch' : [15, NegyvenSzazUltiDurchmarsch()],
            'Húsz-száz durchmarsch' : [16, HuszSzazDurchmarsch()],
            'Piros negyven-száz ulti' : [17, PirosNegyvenSzazUlti()],
            'Piros húsz-száz' : [18, PirosHuszSzaz()],
            'Húsz-száz ulti durchmarsch' : [19, HuszSzazUltiDurchmarsch()],
            'Piros negyven-száz durchmarsch' : [20, PirosNegyvenSzazDurchmarsch()],
            'Piros ulti durchmarsch' : [20, PirosUltiDurchmarsch()],
            'Terített betli' : [21, TeritettBetli()],
            'Piros húsz-száz ulti' : [22, PirosHuszSzazUlti()],
            'Terített durchmarsch' : [23, TeritettDurchmarsch()],
            'Színtelen terített durchmarsch' : [23, SzintelenTeritettDurchmarsch()],
            'Piros negyven-száz ulti durchmarsch' : [24, PirosNegyvenSzazUltiDurchmarsch()],
            'Piros húsz-száz durchmarsch' : [25, PirosHuszSzazDurchmarsch()],
            'Terített negyven-száz durchmarsch' : [26, TeritettNegyvenSzazDurchmarsch()],
            'Terített ulti durchmarsch' : [26, TeritettUltiDurchMarsch()],
            'Terített negyven-száz ulti durchmarsch' : [27, TeritettNegyvenSzazUltiDurchmarsch()],
            'Terített piros negyven-száz durchmarsch' : [28, TeritettPirosNegyvenSzazDurchmarsch()],
            'Terített piros ulti durchmarsch' : [28, PirosTeritettNegyvenSzazUltiDurchmarsch()],
            'Terített húsz-száz durchmarsch' : [28, TeritettHuszSzazDurchmarsch()],
            'Piros ulti durchmarsch húsz-száz' : [29, PirosUltiDurchmarschHuszSzaz()],
            'Terített ulti durchmarsch húsz-száz' : [29, TeritettUltiDurchmarschHuszSzaz()],
            'Piros terített negyven-száz ulti durchmarsch' : [30, PirosTeritettNegyvenSzazUltiDurchmarsch()],
            'Piros terített durchmarsch húsz-száz' : [31, PirosTeritettDurchmarschHuszSzaz()],
            'Piros terített ulti durchmarsch húsz-száz' : [32, PirosTeritettUltiDurchmarschHuszSzaz()]
        }

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
        if self.players[0].is_dealer is False and self.players[1].is_dealer is False and self.players[2].is_dealer is False:
            print("choosing dealer randomly")
            x = random.choice([0, 1, 2])
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
            self.players[2].wants_to_bid = True
            self.new_popup(str(self.players[2].name) + " kezd")
            self.players[0].set_hand(self.deck.cards[12:22])
            self.players[1].set_hand(self.deck.cards[22:32])

        elif self.players[1].is_dealer:
            print("p1 is dealer")
            self.players[0].set_hand(self.deck.cards[0:12])
            self.players[0].is_active = True
            self.players[0].wants_to_bid = True
            self.new_popup(str(self.players[0].name) + " kezd")
            self.players[2].set_hand(self.deck.cards[12:22])
            self.players[1].set_hand(self.deck.cards[22:32])

        elif self.players[2].is_dealer:
            print("p2 is dealer")
            self.players[1].set_hand(self.deck.cards[0:12])
            self.players[1].is_active = True
            self.players[1].wants_to_bid = True
            self.new_popup(str(self.players[1].name) + " kezd")
            self.players[2].set_hand(self.deck.cards[12:22])
            self.players[0].set_hand(self.deck.cards[22:32])
        print("deal_hands done")
        active_counter = 0
        for p in self.players:
            if p.is_active:
                active_counter += 1
        assert active_counter == 1, "active players amount bad after deal hands"

    def accept_bid(self):
        print("accept bid started")
        for p in self.players:
            if p.is_active:
                print("active player found")
                self.current_game = p.licit_selected[:]
                self.bidding_list.pop(0)
                self.bidding_list.append(p.licit_selected)
                self.talon = p.selected_cards[:]
                for c in p.selected_cards:
                    p.hand.remove(c)

                self.vallalo = str(p.name)
                p.selected_cards.clear()
                p.wants_to_bid = False
                p.is_active = False
                p.licit_selected = None
                print(self.bidding_list)
                self.players[self.players.index(p)-1].is_active = True
                break
        active_counter = 0
        for p in self.players:
            if p.is_active:
                active_counter += 1
        assert active_counter == 1, "active players amount bad after accept_bid"
        print("accept bid completed")

    def pickup(self):
        print("pickup started")
        for p in self.players:
            if p.is_active:
                p.wants_to_bid = True
                for c in self.talon:
                    p.hand.append(c)
                    p.selected_cards.append(c)
                    p.sort_hand()
                self.talon.clear()
        print("pickup completed")

    def passz(self):
        print("pass started")
        for p in self.players:
            if p.is_active:
                self.bidding_list.pop(0)
                self.bidding_list.append("passz")
                p.is_active = False
                self.players[self.players.index(p) - 1].is_active = True
                break
        print(self.bidding_list)
        if self.bidding_list == ["passz", "passz", "passz"]:
            self.game_phase = PLAY
            for p in self.players:
                if p.name == self.vallalo:
                    p.is_active = True
        active_counter = 0
        for p in self.players:
            if p.is_active:
                active_counter += 1
        assert active_counter == 1, "active players amount bad after passz"
        print("pass completed")

    def reset(self):
        # TODO! save game details for later
        self.game_phase = STARTED
        self.card_played = []
        self.selected_game = None
        self.current_game = 'No Game'
        self.new_popup("Új játék")

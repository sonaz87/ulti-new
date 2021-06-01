from game_elements import *
import random
import copy
import time
import sys

STARTED = 'started'
INIT = 'init'
BIDDING = 'bidding'
PLAY = 'play'

class Game(object):
    def __init__(self):
        self.players = []
        self.game_phase = STARTED
        self.selected_game = None
        self.popups = [" ", " ", " ", " ", " "]
        self.deck = Deck()
        self.talon = []
        self.bidding_list = ["", "", ""]
        self.current_game = 'No Game'
        self.vallalo = ""
        self.card_played = None
        self.cards_on_the_table = []
        self.possible_games = {
            'No Game' : [0],
            'Passz' : [1, Passz(self.players)],
            'Piros passz' : [2, PirosPassz(self.players)],
            'Negyven-száz' : [3, NegyvenSzaz(self.players)],
            'Ulti' : [4, Ulti(self.players)],
            'Betli' : [5, Betli(self.players)],
            'Durchmarsch' : [6, Durchmarsch(self.players)],
            'Színtelen durchmarsch' : [6, SzintelenDurchmarsch(self.players)],
            'Negyven-száz Ulti' : [7, NegyvenSzazUlti(self.players)],
            'Piros negyven-száz' : [8, PirosNegyvenSzaz(self.players)],
            'Húsz-száz' : [9, HuszSzaz(self.players)],
            'Piros ulti' : [10, PirosUlti(self.players)],
            'Negyven-száz durchmarsch' : [11, NegyvenSzazDurchmarsch(self.players)],
            'Ulti durchmarsch' : [11, UltiDurchmarsch(self.players)],
            'Rebetli' : [12, Rebetli(self.players)],
            'Húsz-száz ulti' : [13, HuszSzazUlti(self.players)],
            'Redurchmarsch' : [14, ReDurchmarsch(self.players)],
            'Piros durchmarsch' : [14, PirosDurschmarsch(self.players)],
            'Negyven-száz ulti durschmarsch' : [15, NegyvenSzazUltiDurchmarsch(self.players)],
            'Húsz-száz durchmarsch' : [16, HuszSzazDurchmarsch(self.players)],
            'Piros negyven-száz ulti' : [17, PirosNegyvenSzazUlti(self.players)],
            'Piros húsz-száz' : [18, PirosHuszSzaz(self.players)],
            'Húsz-száz ulti durchmarsch' : [19, HuszSzazUltiDurchmarsch(self.players)],
            'Piros negyven-száz durchmarsch' : [20, PirosNegyvenSzazDurchmarsch(self.players)],
            'Piros ulti durchmarsch' : [20, PirosUltiDurchmarsch(self.players)],
            'Terített betli' : [21, TeritettBetli(self.players)],
            'Piros húsz-száz ulti' : [22, PirosHuszSzazUlti(self.players)],
            'Terített durchmarsch' : [23, TeritettDurchmarsch(self.players)],
            'Színtelen terített durchmarsch' : [23, SzintelenTeritettDurchmarsch(self.players)],
            'Piros negyven-száz ulti durchmarsch' : [24, PirosNegyvenSzazUltiDurchmarsch(self.players)],
            'Piros húsz-száz durchmarsch' : [25, PirosHuszSzazDurchmarsch(self.players)],
            'Terített negyven-száz durchmarsch' : [26, TeritettNegyvenSzazDurchmarsch(self.players)],
            'Terített ulti durchmarsch' : [26, TeritettUltiDurchMarsch(self.players)],
            'Terített negyven-száz ulti durchmarsch' : [27, TeritettNegyvenSzazUltiDurchmarsch(self.players)],
            'Terített piros negyven-száz durchmarsch' : [28, TeritettPirosNegyvenSzazDurchmarsch(self.players)],
            'Terített piros ulti durchmarsch' : [28, PirosTeritettNegyvenSzazUltiDurchmarsch(self.players)],
            'Terített húsz-száz durchmarsch' : [28, TeritettHuszSzazDurchmarsch(self.players)],
            'Piros ulti durchmarsch húsz-száz' : [29, PirosUltiDurchmarschHuszSzaz(self.players)],
            'Terített ulti durchmarsch húsz-száz' : [29, TeritettUltiDurchmarschHuszSzaz(self.players)],
            'Piros terített negyven-száz ulti durchmarsch' : [30, PirosTeritettNegyvenSzazUltiDurchmarsch(self.players)],
            'Piros terített durchmarsch húsz-száz' : [31, PirosTeritettDurchmarschHuszSzaz(self.players)],
            'Piros terített ulti durchmarsch húsz-száz' : [32, PirosTeritettUltiDurchmarschHuszSzaz(self.players)]
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

                self.vallalo = self.get_active_player_index()
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
                if self.bidding_list == ["passz", "passz", "passz"]:
                    self.game_phase = PLAY
                    self.selected_game = self.possible_games[self.current_game][1]
                    self.selected_game.vallalo = self.vallalo
                    self.selected_game.talon = self.talon
                    print("play phase started")
                    break
                else:
                    p.is_active = False
                    self.players[self.players.index(p) - 1].is_active = True
                    break
        print(self.bidding_list)

        active_counter = 0
        for p in self.players:
            if p.is_active:
                active_counter += 1
        assert active_counter == 1, "active players amount bad after passz"
        print("pass completed")

    def play_card(self):
        # active_counter = 0
        # for p in self.players:
        #     if p.is_active:
        #         active_counter += 1
        # assert active_counter == 1, "active players amount bad when starting play_card"
        try:
            x = self.get_active_player_index()
            print("in play_card: active player index is :", x)
            if len(self.players[x].selected_cards) == 1 and self.players[x].card_played == None:
                self.players[x].hand.remove(self.players[x].selected_cards[0])
                self.players[x].card_played = copy.deepcopy(self.players[x].selected_cards[0])
                self.card_played = [copy.deepcopy(self.players[x].selected_cards[0]), x]
                self.players[x].selected_cards.clear()
                self.cards_on_the_table.append([self.players[x].card_played, x])
                self.players[x].is_active = False
                if len(self.cards_on_the_table) < 3:
                    self.players[x - 1].is_active = True
                    self.new_popup(str(self.players[x - 1].name) + " jön")
                    print("next active player set, player activeness at end of play_card: ", self.players[0].is_active,self.players[1].is_active, self.players[2].is_active )
                print("cards on the table: ", self.cards_on_the_table)

        except:
            print("error in game.play_card")
            e = sys.exc_info()
            print(e)
            pass
    def get_active_player_index(self):
        index = []
        for p in self.players:
            if p.is_active:
                index.append(self.players.index(p))
        print("in get_active_player_index: ", 0, self.players[0].is_active, 1, self.players[1].is_active, 2, self.players[2].is_active)
        if len(index) == 1:
            return index[0]
        else:
            should_be_active =  self.cards_on_the_table[-1][1] -1
            for p in self.players:
                p.is_active = False
            self.players[should_be_active].is_active = True
            return should_be_active

    # def move_card_to_middle(self):
    #     print("in game.move_card_to_middle")
    #     print("players animation completed: ")
    #     for p in self.players:
    #         print(p.animation_completed)
    #     if self.players[0].animation_completed and self.players[1].animation_completed and self.players[2].animation_completed:
    #         print("animation completed for all players")
    #         print("self.card_played :", self.card_played)
    #         self.cards_on_the_table.append([self.card_played[0], self.get_active_player_index()])
    #         self.card_played = None
    #         for p in self.players:
    #             p.animation_completed = False
    #     print("game.move_card_to_middle completed")
    #     print("cards in the middle and type: ", self.cards_on_the_table, type(self.cards_on_the_table[0]))


    def who_won_round(self):
        if issubclass(type(self.selected_game), Szines):
            adus = []
            for c in self.cards_on_the_table:
                if c[0].color == self.selected_game.adu:
                    adus.append(c)
            if len(adus) == 1:
                return adus[0][1]
            elif len(adus) == 2:
                if adus[0][0].bigger_than(adus[1][0], self.selected_game.number_values):
                    return adus[0][1]
                else:
                    return adus[1][1]
            elif len(adus) == 3:
                if adus[0][0].bigger_than(adus[1][0], self.selected_game.number_values) and adus[0][0].bigger_than(adus[2][0], self.selected_game.number_values):
                    return adus[0][1]
                elif adus[1][0].bigger_than(adus[0][0], self.selected_game.number_values) and adus[1][0].bigger_than(adus[2][0], self.selected_game.number_values):
                    return adus[1][1]
                else:
                    return adus[2][1]
            elif len(adus) == 0:
                cards_to_consider = [self.cards_on_the_table[0]]
                if self.cards_on_the_table[1][0].color == self.cards_on_the_table[0][0].color:
                    cards_to_consider.append(self.cards_on_the_table[1])
                if self.cards_on_the_table[2][0].color == self.cards_on_the_table[0][0].color:
                    cards_to_consider.append(self.cards_on_the_table[2])
                if len(cards_to_consider) == 1:
                    return cards_to_consider[0][1]
                elif len(cards_to_consider) == 2:
                    if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values):
                        return cards_to_consider[0][1]
                    else:
                        return cards_to_consider[1][1]
                else:
                    if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values) and cards_to_consider[0][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                        return cards_to_consider[0][1]
                    elif cards_to_consider[1][0].bigger_than(cards_to_consider[0][0], self.selected_game.number_values) and cards_to_consider[1][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                        return cards_to_consider[1][1]
                    else:
                        return cards_to_consider[2][1]


        else:
            cards_to_consider = [self.cards_on_the_table[0]]
            if self.cards_on_the_table[1][0].color == self.cards_on_the_table[0][0].color:
                cards_to_consider.append(self.cards_on_the_table[1])
            if self.cards_on_the_table[2][0].color == self.cards_on_the_table[0][0].color:
                cards_to_consider.append(self.cards_on_the_table[2])
            if len(cards_to_consider) == 1:
                return cards_to_consider[0][1]
            elif len(cards_to_consider) == 2:
                if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values):
                    return cards_to_consider[0][1]
                else:
                    return cards_to_consider[1][1]
            else:
                if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values) and \
                        cards_to_consider[0][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                    return cards_to_consider[0][1]
                elif cards_to_consider[1][0].bigger_than(cards_to_consider[0][0], self.selected_game.number_values) and \
                        cards_to_consider[1][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                    return cards_to_consider[1][1]
                else:
                    return cards_to_consider[2][1]



    def collect_played_cards(self):
        # megnézi, ki vitte, berakja a discardjába
        # ha van adu: a legnagyobb adu nyer
        # ha nincs: a legnagyobb alapszín nyer

        for i in self.cards_on_the_table:
            for p in self.players:
                if i[0] in p.hand:
                    p.hand.remove(i[0])

        x = self.who_won_round()
        self.new_popup(self.players[x].name + " vitte")
        print(self.players[x].name + " has won this round")
        self.players[x].discard.append(self.cards_on_the_table[:])
        if self.selected_game.round == 10:
            self.selected_game.player_points[x] += 10
            self.selected_game.evaluate()
            self.display_results()

        self.selected_game.round += 1

        for p in self.players:
            p.card_played = None
            p.is_active = False
        self.players[x].is_active = True
        self.cards_on_the_table.clear()

        print("dicards after collect_played_cards")
        for p in self.players:
            print(p.name, p.discard)




        #TODO display_results()

    def display_results(self):
        print("need to display results")

    def reset(self):
        # TODO! save game details for later
        print("reset called")
        # self.game_phase = STARTED
        # self.card_played = []
        # self.selected_game = None
        # self.current_game = 'No Game'
        # self.new_popup("Új játék")

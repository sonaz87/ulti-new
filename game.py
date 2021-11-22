import pygame

from game_elements import *
import random
import copy
import time
import sys
import csv
import traceback

STARTED = 'started'
INIT = 'init'
BIDDING = 'bidding'
PLAY = 'play'
END = 'end'

class Game(object):
    # global last_round_won
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
        self.cards_played_since_last_kontra = 0
        self.card_played = None
        self.cards_on_the_table = []
        self.last_round_won = None
        self.possible_games = {
            'No Game' : [0],
            'Passz' : [1, Passz(self.players, self.last_round_won)],
            'Piros passz' : [2, PirosPassz(self.players, self.last_round_won)],
            'Negyven-száz' : [3, NegyvenSzaz(self.players, self.last_round_won)],
            'Ulti' : [4, Ulti(self.players, self.last_round_won)],
            'Betli' : [5, Betli(self.players, self.last_round_won)],
            'Durchmarsch' : [6, Durchmarsch(self.players, self.last_round_won)],
            'Színtelen durchmarsch' : [6, SzintelenDurchmarsch(self.players, self.last_round_won)],
            'Negyven-száz Ulti' : [7, NegyvenSzazUlti(self.players, self.last_round_won)],
            'Piros negyven-száz' : [8, PirosNegyvenSzaz(self.players, self.last_round_won)],
            'Húsz-száz' : [9, HuszSzaz(self.players, self.last_round_won)],
            'Piros ulti' : [10, PirosUlti(self.players, self.last_round_won)],
            'Negyven-száz durchmarsch' : [11, NegyvenSzazDurchmarsch(self.players, self.last_round_won)],
            'Ulti durchmarsch' : [11, UltiDurchmarsch(self.players, self.last_round_won)],
            'Rebetli' : [12, Rebetli(self.players, self.last_round_won)],
            'Húsz-száz ulti' : [13, HuszSzazUlti(self.players, self.last_round_won)],
            'Redurchmarsch' : [14, ReDurchmarsch(self.players, self.last_round_won)],
            'Piros durchmarsch' : [14, PirosDurschmarsch(self.players, self.last_round_won)],
            'Negyven-száz ulti durschmarsch' : [15, NegyvenSzazUltiDurchmarsch(self.players, self.last_round_won)],
            'Húsz-száz durchmarsch' : [16, HuszSzazDurchmarsch(self.players, self.last_round_won)],
            'Piros negyven-száz ulti' : [17, PirosNegyvenSzazUlti(self.players, self.last_round_won)],
            'Piros húsz-száz' : [18, PirosHuszSzaz(self.players, self.last_round_won)],
            'Húsz-száz ulti durchmarsch' : [19, HuszSzazUltiDurchmarsch(self.players, self.last_round_won)],
            'Piros negyven-száz durchmarsch' : [20, PirosNegyvenSzazDurchmarsch(self.players, self.last_round_won)],
            'Piros ulti durchmarsch' : [20, PirosUltiDurchmarsch(self.players, self.last_round_won)],
            'Terített betli' : [21, TeritettBetli(self.players, self.last_round_won)],
            'Piros húsz-száz ulti' : [22, PirosHuszSzazUlti(self.players, self.last_round_won)],
            'Terített durchmarsch' : [23, TeritettDurchmarsch(self.players, self.last_round_won)],
            'Színtelen terített durchmarsch' : [23, SzintelenTeritettDurchmarsch(self.players, self.last_round_won)],
            'Piros negyven-száz ulti durchmarsch' : [24, PirosNegyvenSzazUltiDurchmarsch(self.players, self.last_round_won)],
            'Piros húsz-száz durchmarsch' : [25, PirosHuszSzazDurchmarsch(self.players, self.last_round_won)],
            'Terített negyven-száz durchmarsch' : [26, TeritettNegyvenSzazDurchmarsch(self.players, self.last_round_won)],
            'Terített ulti durchmarsch' : [26, TeritettUltiDurchMarsch(self.players, self.last_round_won)],
            'Terített negyven-száz ulti durchmarsch' : [27, TeritettNegyvenSzazUltiDurchmarsch(self.players, self.last_round_won)],
            'Terített piros negyven-száz durchmarsch' : [28, TeritettPirosNegyvenSzazDurchmarsch(self.players, self.last_round_won)],
            'Terített piros ulti durchmarsch' : [28, PirosTeritettUltiDurchmarsch(self.players, self.last_round_won)],
            'Terített húsz-száz durchmarsch' : [28, TeritettHuszSzazDurchmarsch(self.players, self.last_round_won)],
            'Piros ulti durchmarsch húsz-száz' : [29, PirosUltiDurchmarschHuszSzaz(self.players, self.last_round_won)],
            'Terített ulti durchmarsch húsz-száz' : [29, TeritettUltiDurchmarschHuszSzaz(self.players, self.last_round_won)],
            'Piros terített negyven-száz ulti durchmarsch' : [30, PirosTeritettNegyvenSzazUltiDurchmarsch(self.players, self.last_round_won)],
            'Piros terített durchmarsch húsz-száz' : [31, PirosTeritettDurchmarschHuszSzaz(self.players, self.last_round_won)],
            'Piros terített ulti durchmarsch húsz-száz' : [32, PirosTeritettUltiDurchmarschHuszSzaz(self.players, self.last_round_won)]
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

    def get_player_number_from_ip(self, ip):
        for p in self.players:
            if p.ip == ip:
                return self.players.index(p)
        return None

    def initialize(self):
        """
        this function initializes the game by setting game_phase to BIDDING, randomly choosing a dealer if there is none
        and then dealing cards to all players

        :return:
        """
        self.game_phase = BIDDING
        print(" [*] game init started")
        self.deck.shuffle()
        if self.players[0].is_dealer is False and self.players[1].is_dealer is False and self.players[2].is_dealer is False:
            x = random.choice([0, 1, 2])
            self.players[x].is_dealer = True
        else:
            for i in range(3):
                if self.players[i].is_dealer == True:
                    self.players[i].is_dealer = False
                    self.players[i-1].is_dealer = True
                    break

        self.deal_hands()
        for p in self.players:
            p.sort_hand()
        print(" [*] game init completed")

    def deal_hands(self):
        """
        this function deals 10-10 cards to the dealer and the player on the dealer's left
        and 12 to the one on the dealer's right
        :return:
        """
        print(" [*] deal_hands started")
        for p in self.players:
            p.is_active = False
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
        print(" [*] deal_hands completed")
        # active_counter = 0
        # for p in self.players:
        #     if p.is_active:
        #         active_counter += 1
        # assert active_counter == 1, "active players amount bad after deal hands"


    def accept_bid(self):
        """
        this function accepts a bid from a player and advances the active player
        :return:
        """

        print(" [*] acdept_bid started")
        p = self.get_active_player_index()
        self.current_game = self.players[p].licit_selected[:]
        self.bidding_list.pop(0)
        self.bidding_list.append(self.players[p].licit_selected)
        self.talon = self.players[p].selected_cards[:]
        for c in self.players[p].selected_cards:
            self.players[p].hand.remove(c)

        self.vallalo = p
        data = [self.players[p].hand, self.players[p].licit_selected, self.talon]
        self.log_step("bidding.log", data)
        self.players[p].selected_cards.clear()
        self.players[p].wants_to_bid = False
        self.players[p].is_active = False
        self.players[p].licit_selected = None
        print(self.bidding_list)
        self.players[p-1].is_active = True
        print(" [*] acdept_bid completed")

    def pickup(self):
        """
        this function appends the game.talon to the active players's hand
        and sets them as the active bidder
        :return:
        """
        print(" [*] pickup started")
        p = self.get_active_player_index()
        data = [self.players[p].hand, self.players[p].licit_selected]
        self.log_step("pickup.log", data)
        self.new_popup(self.players[p].name + " felvette")
        self.players[p].wants_to_bid = True
        for c in self.talon:
            self.players[p].hand.append(c)
            self.players[p].selected_cards.append(c)
            self.players[p].sort_hand()
        self.talon.clear()
        print(" [*] pickup completed")

    def passz(self):
        """
        this function is triggered when passz is called. it advances the active player
        if 3 passz moves were made consecutively it either starts the game (if any game than Passz was chosen)
        or resets the game
        :return:
        """
        print(" [*] passz started")
        p = self.get_active_player_index()
        self.bidding_list.pop(0)
        self.bidding_list.append("passz")
        if self.bidding_list == ["passz", "passz", "passz"]:
            if self.current_game == 'Passz':
                self.restart_because_no_bidding()

            else:
                self.game_phase = PLAY
                self.selected_game = self.possible_games[self.current_game][1]
                self.selected_game.vallalo = self.vallalo
                self.selected_game.talon = self.talon
                self.selected_game.vedok = [0,1,2]
                self.selected_game.vedok.remove(int(self.selected_game.vallalo))
                print("play phase started")
        else:
            self.players[p].is_active = False
            self.players[p - 1].is_active = True
        print(self.bidding_list)
        self.new_popup(self.players[p].name + " passzolt")

        active_counter = 0
        print(" [*] passz completed")


    def restart_because_no_bidding(self):
        """
        this function resets the game when there was no bids on games higher than Passz
        the dealer remains the same

        :return:
        """
        print(" [*] restart_because_no_bidding started")
        self.bidding_list = ["", "", ""]
        self.vallalo = ""
        self.card_played = None
        self.cards_on_the_table.clear()
        self.selected_game = None
        self.current_game = 'No Game'
        self.new_popup("Új játék")
        self.talon.clear()
        self.game_phase = BIDDING

        for p in self.players:
            p.hand.clear()
            p.discard.clear()
            p.card_played = None
            p.selected_cards.clear()
            p.licit_selected = None
            p.adu_selected = None

        self.deck.shuffle()
        self.deal_hands()

        for p in self.players:
            p.sort_hand()
            p.licit_selected = None
        print(" [*] restart_because_no_bidding completed")


    def play_card(self):
        """
        This function gets the active player and moves their selected card to the card_played and cards_on_the_table lists
        removing the card fro the players hand and selected_card vars
        if less than 3 cards have been played including the current one, it advances the active player

        :return:
        """
        print(" [*] play_card started")
        try:
            x = self.get_active_player_index()
            if len(self.players[x].selected_cards) == 1 and self.players[x].card_played == None:
                self.players[x].card_played = copy.deepcopy(self.players[x].selected_cards[0])
                data = [self.players[x].hand, self.players[x].card_played, self.cards_on_the_table, self.selected_game]
                self.log_step("play_card.log", data)
                self.card_played = [copy.deepcopy(self.players[x].selected_cards[0]), x]
                self.players[x].hand.remove(self.players[x].selected_cards[0])
                self.players[x].selected_cards.clear()
                self.cards_on_the_table.append([self.players[x].card_played, x])
                self.new_popup(self.players[x].name + ": " + str(self.players[x].card_played))
                self.players[x].is_active = False
                if len(self.cards_on_the_table) < 3:
                    self.players[x - 1].is_active = True
                    self.new_popup(str(self.players[x - 1].name) + " jön")
                self.cards_played_since_last_kontra += 1
            else:
                print(" [*] in play_card: active player selected and played cards: ", self.players[x].selected_cards, self.players[x].card_played)
            self.remove_discards_from_hand()

            print(" [*] play_card completed")
        except:
            print("error in game.play_card")
            stack = traceback.extract_stack()
            (filename, line, procname, text) = stack[-1]
            print("procname: ", procname)
            print("filename: ", filename)
            print("line", line)
            print("text: ", text)
            pass

    def get_active_player_index(self):
        """
        this function gets the active player:
        if not only one is marked active, it checks based on game events to identify the correct one
        :return: int, the index of the active player in game.players
        """
        index = []
        for p in self.players:
            if p.is_active:
                index.append(self.players.index(p))
        # print(" [*] in get_active_player_index: ", 0, self.players[0].is_active, 1, self.players[1].is_active, 2, self.players[2].is_active)
        if len(index) == 1:
            return index[0]
        else:
            if len(self.cards_on_the_table) == 0:
                for p in self.players:
                    p.is_active = False
                self.players[self.last_round_won].is_active = True
                return self.last_round_won
            else:
                x = self.cards_on_the_table[-1][1]
                for p in self.players:
                    p.is_active = False
                self.players[x-1].is_active = True


            # print(" [*] in get_active_player_index after fix: ", 0, self.players[0].is_active, 1, self.players[1].is_active, 2,self.players[2].is_active)
            return x

    def accept_terites(self, x):
        print(" [*] accept terites started")
        self.selected_game.accept_terites.append(int(x))
        if self.selected_game.vedok[0] in self.selected_game.accept_terites and self.selected_game.vedok[1] in self.selected_game.accept_terites:
            if isinstance(self.selected_game, Szines):
                last_round = []
                for p in self.players:
                    for c in p.hand:
                        last_round.append([copy.deepcopy(c), self.players.index(p)])
                        p.hand.remove(c)
                self.players[self.selected_game.vallalo].discard.append(last_round)
            # TODO játék végét meghívni
            print("[*] game end - accept_terites trigger")
            self.selected_game.player_points[self.selected_game.vallalo] += 10
            self.game_phase = END
            self.selected_game.evaluate()
            data = [self.selected_game]
            self.log_step("completed_game.log", data)
            self.display_results()
        print(" [*] accept terites completed")

    def who_won_round(self):
        """
        evaluates who won a given round after 3 cards have been played

        :return: int, the index in game.players who won the round
        """
        print(" [*] who_won_round started")
        if issubclass(type(self.selected_game), Szines):
            adus = []
            for c in self.cards_on_the_table:
                if c[0].color == self.selected_game.adu:
                    adus.append(c)
            if len(adus) == 1:
                print(" [*] who_won_round completed")
                return adus[0][1]
            elif len(adus) == 2:
                if adus[0][0].bigger_than(adus[1][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return adus[0][1]
                else:
                    print(" [*] who_won_round completed")
                    return adus[1][1]
            elif len(adus) == 3:
                if adus[0][0].bigger_than(adus[1][0], self.selected_game.number_values) and adus[0][0].bigger_than(adus[2][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return adus[0][1]
                elif adus[1][0].bigger_than(adus[0][0], self.selected_game.number_values) and adus[1][0].bigger_than(adus[2][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return adus[1][1]
                else:
                    print(" [*] who_won_round completed")
                    return adus[2][1]
            elif len(adus) == 0:
                cards_to_consider = [self.cards_on_the_table[0]]
                if self.cards_on_the_table[1][0].color == self.cards_on_the_table[0][0].color:
                    cards_to_consider.append(self.cards_on_the_table[1])
                if self.cards_on_the_table[2][0].color == self.cards_on_the_table[0][0].color:
                    cards_to_consider.append(self.cards_on_the_table[2])
                if len(cards_to_consider) == 1:
                    print(" [*] who_won_round completed")
                    return cards_to_consider[0][1]
                elif len(cards_to_consider) == 2:
                    if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values):
                        print(" [*] who_won_round completed")
                        return cards_to_consider[0][1]
                    else:
                        print(" [*] who_won_round completed")
                        return cards_to_consider[1][1]
                else:
                    if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values) and cards_to_consider[0][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                        print(" [*] who_won_round completed")
                        return cards_to_consider[0][1]
                    elif cards_to_consider[1][0].bigger_than(cards_to_consider[0][0], self.selected_game.number_values) and cards_to_consider[1][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                        print(" [*] who_won_round completed")
                        return cards_to_consider[1][1]
                    else:
                        print(" [*] who_won_round completed")
                        return cards_to_consider[2][1]


        else:
            cards_to_consider = [self.cards_on_the_table[0]]
            if self.cards_on_the_table[1][0].color == self.cards_on_the_table[0][0].color:
                cards_to_consider.append(self.cards_on_the_table[1])
            if self.cards_on_the_table[2][0].color == self.cards_on_the_table[0][0].color:
                cards_to_consider.append(self.cards_on_the_table[2])
            if len(cards_to_consider) == 1:
                print(" [*] who_won_round completed")
                return cards_to_consider[0][1]
            elif len(cards_to_consider) == 2:
                if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return cards_to_consider[0][1]
                else:
                    print(" [*] who_won_round completed")
                    return cards_to_consider[1][1]
            else:
                if cards_to_consider[0][0].bigger_than(cards_to_consider[1][0], self.selected_game.number_values) and \
                        cards_to_consider[0][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return cards_to_consider[0][1]
                elif cards_to_consider[1][0].bigger_than(cards_to_consider[0][0], self.selected_game.number_values) and \
                        cards_to_consider[1][0].bigger_than(cards_to_consider[2][0], self.selected_game.number_values):
                    print(" [*] who_won_round completed")
                    return cards_to_consider[1][1]
                else:
                    print(" [*] who_won_round completed")
                    return cards_to_consider[2][1]


    def remove_discards_from_hand(self):
        """
        this function collects all cards in the discards and if any of them are still present in a player's hand, removes them

        :return:
        """
        print(" [*] remove_discards_from_hand started")
        discards = []
        for p in self.players:
            for this_round in p.discard:
                for c in this_round:
                    discards.append(c[0])

        for c in self.cards_on_the_table:
            discards.append(c[0])

        for c in discards:
            for p in self.players:
                if c in p.hand:
                    p.hand.remove(c)
        print(" [*] remove_discards_from_hand started")

    def collect_played_cards(self):
        """
        this function is used to collect the cards once 3 of them were played, determine the winner and move them to the discard
        the next active player will be the winner
        :return:
        """
        # megnézi, ki vitte, berakja a discardjába
        # ha van adu: a legnagyobb adu nyer
        # ha nincs: a legnagyobb alapszín nyer
        print("[*] collect_played_cards started")
        for i in self.cards_on_the_table:
            for p in self.players:
                if i[0] in p.hand:
                    p.hand.remove(i[0])
                if i[0] in p.selected_cards:
                    p.selected_cards.remove(i[0])
        x = self.who_won_round()
        self.new_popup(self.players[x].name + " vitte")
        self.last_round_won = x
        self.players[x].discard.append(self.cards_on_the_table[:])
        if self.selected_game.round == 10 or (len(self.players[0].hand) == 0 and len(self.players[1].hand) == 0 and len(self.players[2].hand) == 0):
            print("[*] - collect_played_cards : round 10 trigger")
            self.selected_game.player_points[x] += 10
            self.game_phase = END
            self.selected_game.evaluate()
            data = [self.selected_game]
            self.log_step("completed_game.log", data)
            self.display_results()
        self.selected_game.round += 1
        for p in self.players:
            p.card_played = None
            p.is_active = False
        self.players[x].is_active = True
        self.cards_on_the_table.clear()

        self.remove_discards_from_hand()
        for p in self.players:
            print(p.name, p.discard)

        if hasattr(self.selected_game, 'can_be_lost'):
            if self.selected_game.can_be_lost:
                print("game can be lost instantly")
                if self.selected_game.is_game_lost():
                    print("game is lost")
                    self.game_phase = END
                    print("evaluate")
                    self.selected_game.evaluate()
                    print("display results")
                    self.display_results()
        print("[*] collect_played_cards completed")

    def getHuszNegyven(self, adu):
        """
        This function checks if the active player has any 20 or 40 in their hand, and if yes, updates the
        game.selected_game.player_points
        """

        print("[*] getHuszNegyven started")
        x = self.get_active_player_index()
        if x not in self.selected_game.bemondtak:
            colordict = {
                'zold' : 'Zöld',
                'tok' : 'Tök',
                'makk' : "Makk",
                'piros' : 'Piros'
                }
            husz = 0
            negyven = 0
            for key, value in colordict.items():
                if value + " felső" in self.players[x].hand and value + " király" in self.players[x].hand:
                    if key == adu:
                        self.selected_game.player_points[x] += 40
                        negyven += 1
                    else:
                        self.selected_game.player_points[x] += 20
                        husz += 1
            if negyven == 1:
                self.new_popup(self.players[x].name + ": van negyvenem")
            if husz > 0:
                if husz == 1:
                    husz_str= "egy"
                elif husz == 2:
                    husz_str = "két"
                else:
                    husz_str = "három"
                self.new_popup(self.players[x].name + ": van " + husz_str + " húszam")
            self.selected_game.bemondtak.append(x)
            for y in range(3):
                print("player ", y , " points: ", self.selected_game.player_points[y])
            print("[*] getHuszNegyven completed")


    def get_next_kontra(self, jatek):
        for i in range(15):
            if not self.selected_game.kontra[jatek][i][1] or not self.selected_game.kontra[jatek][i][2]:
                return i


    def kontra(self, jatek):
        """
        This function sets the kontra one step higher if triggered
        Szines games are countered collectively by defenders
        Szintelen games are countered individually

        :param jatek: the name of the game component being countered
        :return:
        """

        print("[*] kontra started")
        # num = int(num)
        # print("selected_game.jatek_lista", self.selected_game.jatek_lista)
        # jatek = self.selected_game.jatek_lista[num]


        print("jatek", jatek)
        if isinstance(self.selected_game, Szines):
            print("színes játék")

            if self.selected_game.round == 1:
                print("2")
                self.selected_game.kontra[jatek][1][1] = True
                self.selected_game.kontra[jatek][1][2] = True
                self.selected_game.jatekok[jatek][1] = 1

            elif self.selected_game.round == 2:
                print("3")
                self.selected_game.kontra[jatek][2][1] = True
                self.selected_game.kontra[jatek][2][2] = True
                self.selected_game.jatekok[jatek][1] = 2


        else:
            print("színtelen játék")

            if self.selected_game.round == 1:
                print('2')
                x = self.get_active_player_index()
                kontra_index = self.selected_game.vedok.index(x) + 1
                self.selected_game.kontra[jatek][1][kontra_index] = True
                self.selected_game.jatekok[jatek][1] = 1

            else:
                print("3")
                self.selected_game.kontra[jatek][2][1] = True
                self.selected_game.jatekok[jatek][1] = 2


        self.new_popup(self.players[self.get_active_player_index()].name + " - " + self.selected_game.kontra_alap[self.selected_game.round][0] + " " + str(jatek))
        self.cards_played_since_last_kontra = 0
        print("4")
        for i in self.selected_game.kontra.keys():
            print(self.selected_game.kontra[i])
        print("[*] kontra completed")

    def display_results(self):
        """
        this function waits until every player has chosen to start a new game
        while displaying results (in client)
        and then calling reset

        :return:
        """

        print("[*] display_results started")
        if not self.players[0].ready_for_next_round or not self.players[1].ready_for_next_round or not self.players[2].ready_for_next_round:
            pass

        else:
            self.reset()
        print("[*] display_results completed")

    def reset(self):
        """
        this function resets the game after a turn has been completed

        :return:
        """

        # TODO! save game details for later
        print("[*] reset started")

        self.talon.clear()
        self.bidding_list = ["", "", ""]
        self.vallalo = ""
        self.card_played = None
        self.cards_on_the_table.clear()
        del self.selected_game
        self.selected_game = None
        self.current_game = 'No Game'
        self.new_popup("Új játék")


        for p in self.players:
            p.hand.clear()
            p.discard.clear()
            p.card_played = None
            p.selected_cards.clear()
            p.wants_to_bid = False
            p.licit_selected = None
            p.adu_selected = None
            p.ready_for_next_round = False

        self.initialize()
        print("[*] reset completed")

    def log_step(self, filename, data):
        with open(filename, 'a', encoding= 'UTF-8', newline='') as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(data)
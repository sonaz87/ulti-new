# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:25:07 2021

@author: lor
"""

from random import shuffle
import copy
# from random import choices
# import pygame
# import sys
# import json


SZINES = 'szines'
SZINTELEN = 'szintelen'


class Player(object):
    def __init__(self, name):
        self.name = str(name)
        self.is_dealer = False
        self.is_active = False
        self.hand = []
        self.discard = []
        self.sorting = SZINES
        self.card_played = None
        self.points = 0
        self.animation_completed = False
        self.selected_cards = []
        self.wants_to_bid = False
        self.licit_selected = None
        self.adu_selected = None
        self.ready_for_next_round = False

    def update_all(self, other):
        self.is_dealer = other.is_dealer
        self.is_active = other.is_active
        self.hand = other.hand[:]
        self.discard = other.discard
        self.sorting = other.sorting
        self.points = other.points
        self.selected_cards = other.selected_cards[:]
        self.wants_to_bid = other.wants_to_bid
        self.licit_selected = other.licit_selected
        self.animation_completed = other.animation_completed
        self.adu_selected = other.adu_selected
        self.ready_for_next_round = other.ready_for_next_round

    def get_name(self):
        return self.name

    def set_dealer(self, val):
        self.is_dealer = val

    def get_dealer(self):
        return self.is_dealer

    def set_active(self, val):
        self.is_active = val

    def get_active(self):
        return self.is_active

    def set_hand(self, cards):
        self.hand = cards[:]

    def play_card(self, card):
        x = self.hand.pop(card)
        return x

    def to_discard(self, cards):
        self.discard.extend(cards)

    def get_discard(self):
        return self.discard

    def change_sorting(self):
        if self.sorting == SZINES:
            self.sorting = SZINTELEN
        else:
            self.sorting = SZINES

    def sort_hand(self):
        COLOR_NUMBER = dict()
        VALUE_NUMBER = dict()

        if self.sorting == SZINES:
            VALUES = ["hetes", "nyolcas", "kilences", "also", "felso", "kiraly", "tizes", "asz"]
        elif self.sorting == SZINTELEN:
            VALUES = ["hetes", "nyolcas", "kilences", "tizes", "also", "felso", "kiraly", "asz"]

        COLORS = ['zold', 'makk', 'tok', 'piros']

        for i in range(len(COLORS)):
            COLOR_NUMBER.update({COLORS[i]: i})
        for i in range(len(VALUES)):
            VALUE_NUMBER.update({VALUES[i]: i})

        self.hand.sort(key=lambda x: (COLOR_NUMBER[x.color], VALUE_NUMBER[x.value]))

    def update_points(self, num):
        self.points += num

    def __str__(self):
        return self.name


class Card(object):
    def __init__(self, color, value, name, numvalue):
        self.color = color
        self.value = value
        self.img = None
        self.name = name
        self.numvalue = numvalue

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def __eq__(self, name):
        if self.name == name:
            return True
        else:
            return False

    def bigger_than(self, other, values):
        # print("in bigger.than")
        # print("self value", values.index(self.value))
        # print("other value", values.index(other.value))
        if values.index(self.value) > values.index(other.value) and self.color == other.color:
            return True
        else:
            False


    def set_img(self, image):
        self.img = image

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def get_img(self):
        return self.img


class Message(object):
    def __init__(self, message_type, player, body):
        self.message_type = message_type
        self.player = player
        self.body = body

    def __str__(self):
        return self.message_type + " " + self.body

    def __repr__(self):
        return self.message_type + " : " + self.body + " from " + str(self.player)


class Popup(object):
    def __init__(self, player, message):
        self.player = player
        self.message = message

    def get_player(self):
        return self.player

    def get_message(self):
        return self.message

    def __len__(self):
        return len(self.message)


class Deck(object):

    def __init__(self):
        VALUES = ["hetes", "nyolcas", "kilences", "tizes", "also", "felso", "kiraly", "asz"]
        COLORS = ['zold', 'makk', 'tok', 'piros']
        NAME_VALUES = ["hetes", "nyolcas", "kilences", "tízes", "alsó", "felső", "király", "ász"]
        NAME_COLORS = ['Zöld', 'Makk', 'Tök', 'Piros']
        self.cards = []
        for i in range(len(COLORS)):
            for j in range(len(VALUES)):
                self.cards.append(Card(COLORS[i], VALUES[j], NAME_COLORS[i] + " " + NAME_VALUES[j], VALUES.index(VALUES[j])))

    def shuffle(self):
        shuffle(self.cards)

    def deal(self, player, start_number, stop_number):
        hand = self.cards[start_number, stop_number]
        return (player, hand)


class Alapjatek(object):
    def __init__(self, players):
        self.vallalo = None
        self.player_points = [0, 0, 0]
        self.players = players
        self.talon = None
        self.can_be_lost = False
        self.vedok = list()
        self.kontra_alap = {
            0 : ['', True],
            1 : ['Kontra', False, False],
            2 : ['Rekontra', False],
            3 : ['Szubkontra', False, False],
            4 : ['Mordkontra', False],
            5 : ['Hirskontra', False, False],
            6 : ['Fedák Sári', False],
            7 : ['Kerekes bicikli', False, False],
            8 : ['Darth Vader', False],
            9 : ['Krúdy-fröccs', False, False],
            10 : ['Chuck Norris', False]
        }
        self.kontra = dict()

class Szines(Alapjatek):
    def __init__(self, players):
        super().__init__(players)
        self.number_values = ["hetes", "nyolcas", "kilences", "also", "felso", "kiraly", "tizes", "asz"]
        self.adu = None
        self.round = 1

    def set_adu(self, adu):
        self.adu = adu

    def is_valid_choice(self, cards_on_the_table, card_to_be_played, hand):

        def is_color_available(color_to_match, hand):
            for card in hand:
                if card.color == color_to_match:
                    return True
            return False

        def has_bigger_card(card1, hand):
            for c in hand:
                if c.bigger_than(card1,self.number_values):
                    return True
            return False

        # ha incs lenn semmi

        if len(cards_on_the_table) == 0:
            return True

        # ha egy kártya van lenn

        elif len(cards_on_the_table) == 1:
            if is_color_available(cards_on_the_table[0][0].color, hand):
                if cards_on_the_table[0][0].color != card_to_be_played.color:
                    return False
                else:
                    # print("both cards have the same color")
                    # print("card on the table", cards_on_the_table[0][0])
                    # print("selected card", card_to_be_played)
                    # print("is card to be played bigger?", card_to_be_played.bigger_than(cards_on_the_table[0][0],self.number_values))
                    if has_bigger_card(cards_on_the_table[0][0], hand):
                        # (print("have bigger card in hand"))
                        if card_to_be_played.bigger_than(cards_on_the_table[0][0],self.number_values):
                            return True
                        else:
                            return False
                    else:
                        # print("itt")
                        # print("no bigger cards, color will do")
                        if card_to_be_played.color == cards_on_the_table[0][0].color:
                            return True
                        else:
                            return False
            else:
                if is_color_available(self.adu, hand):
                    if card_to_be_played.color == self.adu:
                        return True
                    else:
                        return False
                else:
                    return True
        # ha két kártya van lenn
        elif len(cards_on_the_table) == 2:
            # mindkét kártya adu
            if cards_on_the_table[0][0].color == self.adu and cards_on_the_table[1][0].color == self.adu:
                if is_color_available(self.adu, hand):
                    if cards_on_the_table[0][0].bigger_than(cards_on_the_table[1][0],self.number_values):
                        if has_bigger_card(cards_on_the_table[0][0], hand):
                            if card_to_be_played.bigger_than(cards_on_the_table[0][0],self.number_values) and card_to_be_played.color == self.adu:
                                return True
                            else:
                                return False
                        else:
                            if card_to_be_played.color == self.adu:
                                return True
                            else:
                                return False
                    else:
                        if has_bigger_card(cards_on_the_table[1][0], hand):
                            if card_to_be_played.bigger_than(cards_on_the_table[1][0],self.number_values) and card_to_be_played.color == self.adu:
                                return True
                            else:
                                return False
                        else:
                            if card_to_be_played.color == self.adu:
                                return True
                            else:
                                return False
                else:
                    return True

            # ha az első adu, a másik nem:
            elif cards_on_the_table[0][0].color == self.adu and cards_on_the_table[1][0].color != self.adu:
                if is_color_available(self.adu, hand):
                    if has_bigger_card(cards_on_the_table[0][0], hand):
                        if card_to_be_played.color == self.adu and card_to_be_played.bigger_than(cards_on_the_table[0][0],self.number_values):
                            return True
                        else:
                            return False
                    else:
                        if card_to_be_played.color == self.adu:
                            return True
                        else:
                            return False
                else:
                    return True

        # ha mindkettő nem adu
            #TODO megnézni azt az esetet, ha a második kártya bedobott lap - ezt itt átnézni rendesen, mert szar
            elif cards_on_the_table[0][0].color != self.adu and cards_on_the_table[1][0].color != self.adu:
                if is_color_available(cards_on_the_table[0][0].color, hand):
                    if cards_on_the_table[0][0].color == cards_on_the_table[1][0].color:
                        if cards_on_the_table[0][0].bigger_than(cards_on_the_table[1][0],self.number_values):
                            if has_bigger_card(cards_on_the_table[0][0], hand):
                                if card_to_be_played.bigger_than(cards_on_the_table[0][0], self.number_values) and card_to_be_played.color == cards_on_the_table[0][0].color:
                                    return True
                                else:
                                    return False
                            else:
                                if card_to_be_played.color == cards_on_the_table[0][0].color:
                                    return True
                                else:
                                    return False
                        else:
                            if has_bigger_card(cards_on_the_table[1][0], hand):
                                if card_to_be_played.bigger_than(cards_on_the_table[1][0], self.number_values) and card_to_be_played.color == cards_on_the_table[1][0].color:
                                    return True
                                else:
                                    return False
                            else:
                                if card_to_be_played.color == cards_on_the_table[1][0].color:
                                    return True
                                else:
                                    return False
                    else:
                        if has_bigger_card([cards_on_the_table[0][0]],self.number_values):
                            if card_to_be_played.bigger_than(cards_on_the_table[0][0], self.number_values) and card_to_be_played.color == cards_on_the_table[0][0].color:
                                return True
                            else:
                                return False
                        else:
                            if card_to_be_played.color == cards_on_the_table[0][0].color:
                                return True
                            else:
                                return False


                else:
                    if is_color_available(self.adu, hand):
                        if card_to_be_played.color == self.adu:
                            return True
                        else:
                            return False
                    else:
                        return True
            # ha az első nem adu, a második igen
            elif cards_on_the_table[0][0].color != self.adu and cards_on_the_table[1][0].color == self.adu:
                if is_color_available(cards_on_the_table[0][0].color, hand):
                    if card_to_be_played.color == cards_on_the_table[0][0].color:
                        return True
                    else:
                        return False
                else:
                    if is_color_available(self.adu, hand):
                        if has_bigger_card(cards_on_the_table[1][0], hand):
                            if card_to_be_played.color == self.adu and card_to_be_played.bigger_than(cards_on_the_table[1][0],self.number_values):
                                return True
                            else:
                                return False

                        else:
                            if card_to_be_played.color == self.adu:
                                return True
                            else:
                                return False

                    else:
                        return True




class Szintelen(Alapjatek):
    def __init__(self, players):
        super().__init__(players)
        self.number_values = ["hetes", "nyolcas", "kilences", "tizes", "also", "felso", "kiraly", "asz"]


class Passz(Szines):
    def __init__(self, players):
        super().__init__(players)
        self.adu = None
        self.points = 1
        self.can_be_lost = False
        self.vanHuszNegyven = True
        self.bemondtak = []
        self.name = "Passz"
        self.jatekok = {"Passz" : [False, 0]}
        self.jatek_lista = ["Passz"]
        self.csendes_szaz_lehet = True
        self.csendes_ulti_lehet = True
        self.csendes_duri_lehet = True
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})


    def set_adu(self, adu):
        self.adu = adu

    def evaluate(self):
        print("pass evaluate started")
        print("player discards:")
        for p in self.players:
            print(p.discard)


        for i in range(len(self.players)):
            print("i, player[i].discard = ", i, self.players[i].discard)
            for turn in self.players[i].discard:
                print("turn: ", turn)
                for card in turn:
                    print("card:", card[0])
                    if card[0].value in ['tizes', 'asz']:
                        print("pontot ér")
                        self.player_points[i] += 10
        vallalo_points = self.player_points[self.vallalo]
        vedo_points = 0

        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g]:
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        for i in self.player_points:
            print("player points after counting discard:", i)
            if self.player_points.index(i) != self.vallalo:
                vedo_points += i

        for card in self.talon:
            if card.value in ["tizes", "asz"]:
                vedo_points += 10

        if vallalo_points > vedo_points:
            self.jatekok["Passz"][0] = True
            print("vallalo nyert: ", self.vallalo, vallalo_points)
            print("védő pontok:", vedo_points)
            if vallalo_points < 100:
                self.players[self.vallalo].points += self.points * 2 * 2 ** self.jatekok["Passz"][1]
                for p in self.players:
                    if self.players.index(p) != self.vallalo:
                        p.points -= self.points * 2 ** self.jatekok["Passz"][1]
            else:
                print("csendes száz")
                self.players[self.vallalo].points += self.points * 2 * 2 ** self.jatekok["Passz"][1] *2
                for p in self.players:
                    if self.players.index(p) != self.vallalo:
                        p.points -= self.points * 2 ** self.jatekok["Passz"][1] * 2
        else:
            print("vedok nyertek, védő pontok: ", vedo_points)
            print("vállaló pontok: ", vallalo_points)
            if vedo_points < 100:
                self.players[self.vallalo].points -= self.points * 2 * 2 ** self.jatekok["Passz"][1]
                for p in self.players:
                    if self.players.index(p) != self.vallalo:
                        p.points += self.points * 2 ** self.jatekok["Passz"][1]
            else:
                print("csendes száz")
                self.players[self.vallalo].points -= self.points * 2 * 2 ** self.jatekok["Passz"][1] * 2
                for p in self.players:
                    if self.players.index(p) != self.vallalo:
                        p.points += self.points * 2 ** self.jatekok["Passz"][1] * 2

        if len(self.players[self.vedok[0]].discard) == 0 and len(self.players[self.vedok[1]].discard) == 0:
            print("csendes duri")
            self.players[self.vallalo].points += 6
            self.players[self.vedok[0]].points -= 3
            self.players[self.vedok[1]].points -= 3
        colors = {
            "zold": "Zöld",
            "makk": "Makk",
            "tok": "Tök",
            "piros": "Piros"
        }

        if colors[self.adu] + " hetes" in self.players[self.vallalo].discard[-1] and last_round_won == self.vallalo:
            print("csendes ulti")
            self.players[self.vallalo].points += 4
            self.players[self.vedok[0]].points -= 2
            self.players[self.vedok[1]].points -= 2


class PirosPassz(Passz):
    def __init__(self, players):
        super().__init__(players)
        self.adu = 'piros'
        self.points = 2
        self.name = "Passz"


class NegyvenSzaz(Szines):
    def __init__(self, players):
        super().__init__(players)
        self.adu = None
        self.points = 4
        self.can_be_lost = False
        self.vanHuszNegyven = False
        self.name = "Negyven-száz"
        self.jatekok = {"Negyven-száz": [False, 0]}
        self.jatek_lista = ["Negyven-száz"]
        self.csendes_ulti_lehet = True
        self.csendes_duri_lehet = True
        self.has_40_at_start = False

    def check_for_40(self):
        colors = {
            "zold": "Zöld",
            "makk": "Makk",
            "tok": "Tök",
            "piros": "Piros"
        }
        if colors[self.adu] + " felső" in self.players[self.vallalo].hand and colors[self.adu] + " király" in self.players[self.vallalo].hand:
            self.has_40_at_start = True

    def evaluate(self):
        pass


class Ulti(Szines):
    pass


class Betli(Szintelen):
    pass


class Durchmarsch(Szines):
    pass


class SzintelenDurchmarsch(Szintelen):
    pass


class NegyvenSzazUlti(Szines):
    pass


class PirosNegyvenSzaz(Szines):
    pass


class HuszSzaz(Szines):
    pass


class PirosUlti(Szines):
    pass


class NegyvenSzazDurchmarsch(Szines):
    pass


class UltiDurchmarsch(Szines):
    pass


class Rebetli(Szintelen):
    pass


class HuszSzazUlti(Szines):
    pass


class ReDurchmarsch(Szintelen):
    pass


class PirosDurschmarsch(Szines):
    pass


class NegyvenSzazUltiDurchmarsch(Szines):
    pass


class HuszSzazDurchmarsch(Szines):
    pass


class PirosNegyvenSzazUlti(Szines):
    pass


class PirosHuszSzaz(Szines):
    pass


class HuszSzazUltiDurchmarsch(Szines):
    pass


class PirosNegyvenSzazDurchmarsch(Szines):
    pass


class PirosUltiDurchmarsch(Szines):
    pass


class TeritettBetli(Szintelen):
    pass


class PirosHuszSzazUlti(Szines):
    pass


class TeritettDurchmarsch(Szines):
    pass


class SzintelenTeritettDurchmarsch(Szintelen):
    pass


class PirosNegyvenSzazUltiDurchmarsch(Szines):
    pass


class PirosHuszSzazDurchmarsch(Szines):
    pass


class TeritettNegyvenSzazDurchmarsch(Szines):
    pass


class TeritettUltiDurchMarsch(Szines):
    pass


class TeritettNegyvenSzazUltiDurchmarsch(Szines):
    pass


class TeritettPirosNegyvenSzazDurchmarsch(Szines):
    pass


class TeritettHuszSzazDurchmarsch(Szines):
    pass


class PirosUltiDurchmarschHuszSzaz(Szines):
    pass


class TeritettUltiDurchmarschHuszSzaz(Szines):
    pass


class PirosTeritettNegyvenSzazUltiDurchmarsch(Szines):
    pass


class PirosTeritettDurchmarschHuszSzaz(Szines):
    pass


class PirosTeritettUltiDurchmarschHuszSzaz(Szines):
    pass

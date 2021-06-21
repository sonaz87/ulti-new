# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:25:07 2021

@author: lor
"""

from random import shuffle
import copy
import traceback
# from random import choices
# import pygame
# import sys
# import json


SZINES = 'szines'
SZINTELEN = 'szintelen'


class Player(object):
    def __init__(self, name, ip):
        self.name = str(name)
        self.ip = str(ip)
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
        self.name = other.name
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

    def set_name(self, name):
        self.name = name

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
        # print("self, other:", self, other)
        # print("tyoes:", type(self), type(other))
        # print("self value", values.index(self.value))
        # print("other value", values.index(other.value))
        if values.index(self.value) > values.index(other.value) and self.color == other.color:
            return True
        else:
            return False


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
    def __init__(self, players, lrw):
        self.vallalo = None
        self.player_points = [0, 0, 0]
        self.players = players
        self.talon = None
        self.round = 1
        self.can_be_lost = False
        self.vedok = list()
        self.kontra_alap = {
            0 : ['', True, True],
            1 : ['Kontra', False, False],
            2 : ['Rekontra', False]
        }
        self.kontra = dict()
        self.teritett = False
        self.last_round_won = lrw
        self.csendes_szaz_lehet = False
        self.csendes_ulti_lehet = False
        self.csendes_duri_lehet = False

class Szines(Alapjatek):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
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
                if c.bigger_than(card1, self.number_values):
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

            elif cards_on_the_table[0][0].color != self.adu and cards_on_the_table[1][0].color != self.adu:
                print("1")
                if is_color_available(cards_on_the_table[0][0].color, hand):
                    print("2")
                    if cards_on_the_table[0][0].color == cards_on_the_table[1][0].color:
                        print("3")
                        if cards_on_the_table[0][0].bigger_than(cards_on_the_table[1][0],self.number_values):
                            print("4")
                            if has_bigger_card(cards_on_the_table[0][0], hand):
                                print("5")
                                if card_to_be_played.bigger_than(cards_on_the_table[0][0], self.number_values) and card_to_be_played.color == cards_on_the_table[0][0].color:
                                    print("6")
                                    return True
                                else:
                                    print("7")
                                    return False
                            else:
                                print("8")
                                if card_to_be_played.color == cards_on_the_table[0][0].color:
                                    print("9")
                                    return True
                                else:
                                    print("10")
                                    return False
                        else:
                            print("11")
                            if has_bigger_card(cards_on_the_table[1][0], hand):
                                print("12")
                                if card_to_be_played.bigger_than(cards_on_the_table[1][0], self.number_values) and card_to_be_played.color == cards_on_the_table[1][0].color:
                                    print("13")
                                    return True
                                else:
                                    print("14")
                                    return False
                            else:
                                print("15")
                                if card_to_be_played.color == cards_on_the_table[1][0].color:
                                    print("16")
                                    return True
                                else:
                                    print("17")
                                    return False
                    else:
                        print("18")
                        if has_bigger_card([cards_on_the_table[0][0]], hand):
                            print("19")
                            print("cards on the table:", cards_on_the_table)
                            print("card to be played: ", card_to_be_played)
                            if card_to_be_played.bigger_than(cards_on_the_table[0][0], self.number_values) and card_to_be_played.color == cards_on_the_table[0][0].color:
                                print("20")
                                return True
                            else:
                                print("21")
                                return False
                        else:
                            print("22")
                            if card_to_be_played.color == cards_on_the_table[0][0].color:
                                print("22")
                                return True
                            else:
                                print("23")
                                return False


                else:
                    print("24")
                    if is_color_available(self.adu, hand):
                        print("25")
                        if card_to_be_played.color == self.adu:
                            print("26")
                            return True
                        else:
                            print("27")
                            return False
                    else:
                        print("28")
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
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.number_values = ["hetes", "nyolcas", "kilences", "tizes", "also", "felso", "kiraly", "asz"]
        self.round = 1


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

        # ha nincs lenn semmi

        if len(cards_on_the_table) == 0:
            return True

        elif len(cards_on_the_table) == 1:
            if is_color_available(cards_on_the_table[0][0].color, hand):
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
            return True

        elif len(cards_on_the_table) == 2:
            if is_color_available(cards_on_the_table[0][0].color, hand):
                if cards_on_the_table[0][0].color == cards_on_the_table[1][0].color:
                    if cards_on_the_table[0][0].bigger_than(cards_on_the_table[1][0], self.number_values):
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
                    elif cards_on_the_table[1][0].bigger_than(cards_on_the_table[0][0], self.number_values):
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
                    if has_bigger_card(cards_on_the_table[0][0], hand):
                        if card_to_be_played.bigger_than(cards_on_the_table[0][0], self.number_values) and card_to_be_played.color == \
                                cards_on_the_table[0][0].color:
                            return True
                        else:
                            return False
                    else:
                        if card_to_be_played.color == cards_on_the_table[0][0].color:
                            return True
                        else:
                            return False
            else:
                return True





class Passz(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
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
        self.csendes_szaz = False
        self.csendes_ulti = [False, False, int()]
        self.csendes_duri = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})


    def set_adu(self, adu):
        self.adu = adu

    def evaluate(self):
        vedo_points, vallalo_points = self.evaluate_passz(self.points)
        self.evaluate_csendes_szaz(vedo_points, vallalo_points, 1)
        self.evaluate_csendes_ulti(2)
        self.evaluate_csendes_duri(3)

    def evaluate_passz(self, points):
        print("pass evaluate started")
        print("player discards:")
        print("vedok", self.vedok)
        print("vallalo", self.vallalo)

        for p in self.players:
            print(p.discard)


        for i in range(len(self.players)):
            for turn in self.players[i].discard:
                for card in turn:
                    if card[0].value in ['tizes', 'asz']:
                        self.player_points[i] += 10
        vallalo_points = self.player_points[self.vallalo]
        vedo_points = 0

        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        for card in self.talon:
            if card.value in ["tizes", "asz"]:
                vedo_points += 10

        for i in self.player_points:
            print("player points after counting discard and talon:", i)
            if self.player_points.index(i) != self.vallalo:
                vedo_points += i

        if vallalo_points > vedo_points:
            self.jatekok["Passz"][0] = True
            print("vallalo nyert: ", self.vallalo, vallalo_points)
            print("védő pontok:", vedo_points)
            print("vallao player points: ", self.players[self.vallalo].points)
            print("kontra szorzó: ", self.jatekok["Passz"][1])
            self.players[self.vallalo].points += points * 2 * (2 ** self.jatekok["Passz"][1])
            for p in self.players:
                if self.players.index(p) != self.vallalo:
                    p.points -= points * (2 ** self.jatekok["Passz"][1])
        else:
            print("vedok nyertek, védő pontok: ", vedo_points)
            print("vállaló pontok: ", vallalo_points)
            self.players[self.vallalo].points -= points * 2 * (2 ** self.jatekok["Passz"][1])
            for p in self.players:
                if self.players.index(p) != self.vallalo:
                    p.points += points * (2 ** self.jatekok["Passz"][1])

        return vedo_points, vallalo_points

    # csendes duri
    def evaluate_csendes_duri(self, points):
        print(" [*] evaluate csendes duri started")
        if self.round == 10:
            if len(self.players[self.vedok[0]].discard) == 0 and len(self.players[self.vedok[1]].discard) == 0:
                print("csendes duri sikerült")
                self.players[self.vallalo].points += points * 2
                self.players[self.vedok[0]].points -= points
                self.players[self.vedok[1]].points -= points
                self.csendes_duri = True
        print(" [*] evaluate csendes duri completed")

    # csendes ulti
    # az első, hogy volt-e próbálkozás, a második, hogy sikerült-e, a harmadik, hogy kinek
    def evaluate_csendes_ulti(self, points):
        print(" [*] evaluate csendes ulti started")
        if self.round == 10:

            colors = {
                "zold": "Zöld",
                "makk": "Makk",
                "tok": "Tök",
                "piros": "Piros"
                }
            for element in self.players[self.last_round_won].discard[-1]:
                if colors[self.adu] + " hetes" in element:
                    if self.last_round_won == element[1]:
                        if [colors[self.adu] + " hetes", self.vallalo] in self.players[self.last_round_won].discard[-1] and self.last_round_won == self.vallalo:
                            #sikerült a csendes ulti
                            print("sikerült a csendes ulti")
                            self.csendes_ulti = [True, True, element[1]]
                            self.players[element[1]].points += points * 2
                            for i in range(3):
                                if i == element[1]:
                                    continue
                                else:
                                    self.players[i].points -= points
                    else:
                        print("bukott a csendes ulti")
                        self.csendes_ulti = [True, False, element[1]]
                        self.players[element[1]].points -= points * 2 * 2
                        for i in range(3):
                            if i == element[1]:
                                continue
                            else:
                                self.players[i].points -= points * 2
        print(" [*] evaluate csendes ulti completed")




    def evaluate_csendes_szaz(self, vedo_points, vallalo_points, points):
        print(" [*] evaluate csendes 100 started")
        if self.round == 10:
            if vallalo_points >= 100:
                print("vállaló csendes száz")
                self.csendes_szaz = True
                self.players[self.vallalo].points += 2 * points
                for n in self.vedok:
                    self.players[n].points -= points


            elif vedo_points >= 100:
                print("védő csendes száz")
                self.csendes_szaz = True
                self.players[self.vallalo].points -= 2 * points
                for n in self.vedok:
                    self.players[n].points += points
        print(" [*] evaluate csendes 100 completed")




class PirosPassz(Passz):
    def __init__(self, players, lrw ):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.points = 2
        self.name = "Passz"
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        vedo_points, vallalo_points = Passz.evaluate_passz(self, 2)
        Passz.evaluate_csendes_szaz(self, vedo_points, vallalo_points, 2)
        Passz.evaluate_csendes_ulti(self, 4)
        Passz.evaluate_csendes_duri(self, 6)

class NegyvenSzaz(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 4
        self.can_be_lost = False
        self.vanHuszNegyven = False
        self.name = "Negyven-száz"
        self.jatekok = {"Negyven-száz": [False, 0]}
        self.jatek_lista = ["Negyven-száz"]
        self.csendes_ulti_lehet = True
        self.csendes_duri_lehet = True
        self.csendes_szaz_lehet = False
        self.csendes_ulti = [False, False, int()]
        self.csendes_duri = False
        self.has_40_at_start = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        self.evaluate_negyven_szaz(4)
        Passz.evaluate_csendes_ulti(self, 2)
        Passz.evaluate_csendes_duri(self, 3)

    def evaluate_negyven_szaz(self, points):
        colors = {
            "zold": "Zöld",
            "makk": "Makk",
            "tok": "Tök",
            "piros": "Piros"
        }
        #getting highest kontra
        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        felso = False
        kiraly = False
        for p in self.players:
            for thisround in p.discard:
                for card in thisround:

                    if colors[self.adu] + " felső" == card[0] and card[1] == self.vallalo:
                        felso = True
                    if colors[self.adu] + " király" == card[0] and card[1] == self.vallalo:
                        kiraly = True

        vallalo_points = self.player_points[self.vallalo]
        if felso and kiraly:
            vallalo_points += 40

        for thisround in self.players[self.vallalo].discard:
            for card in thisround:
                if card[0].value in ["tizes", "asz"]:
                    vallalo_points += 10

        if felso and kiraly and vallalo_points > 100:
            # negyven-száz nyerve
            self.jatekok["Negyven-száz"][0] = True
            self.players[self.vallalo].points += points * 2 * (2 ** self.jatekok["Negyven-száz"][1])
            for i in self.vedok:
                self.players[i].points -= points * (2 ** self.jatekok["Negyven-száz"][1])

        else:
            self.jatekok["Negyven-száz"][0] = True
            self.players[self.vallalo].points -= points * 2 * (2 ** self.jatekok["Negyven-száz"][1])
            for i in self.vedok:
                self.players[i].points += points * (2 ** self.jatekok["Negyven-száz"][1])





class Ulti(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 4
        self.can_be_lost = False
        self.vanHuszNegyven = True
        self.bemondtak = []
        self.name = "Ulti"
        self.jatekok = {"Passz": [False, 0],
                        "Ulti": [False, 0]
                        }
        self.jatek_lista = ["Passz", "Ulti"]
        self.csendes_szaz_lehet = True
        self.csendes_duri_lehet = True
        self.csendes_szaz = False
        self.csendes_duri = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})


    def evaluate(self):
        vedo_points, vallalo_points = Passz.evaluate_passz(self, 1)
        self.evaluate_ulti(4)
        Passz.evaluate_csendes_szaz(self, vedo_points, vallalo_points, 1)
        Passz.evaluate_csendes_duri(self, 3)

    def evaluate_ulti(self, points):
        colors = {
            "zold": "Zöld",
            "makk": "Makk",
            "tok": "Tök",
            "piros": "Piros"
        }

        print(" [*] ulti pontozás")
        print("vállaló, védők:", self.vallalo, self.vedok)
        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra


        for card in self.players[self.vallalo].discard[-1]:
            if card[0] == colors[self.adu] + " hetes":
                self.jatekok["Ulti"][0] = True

        if self.jatekok["Ulti"][0] == True:
            # sikerült az ulti
            self.players[self.vallalo].points += points * 2 * (2 ** self.jatekok["Ulti"][1])
            for i in self.vedok:
                self.players[i].points -= points * (2 ** self.jatekok["Ulti"][1])
            for i in self.players:
                print("ulti pontozás után", i.name, i.points)
        else:
            self.players[self.vallalo].points -= 2 * points * 2 * (2 ** self.jatekok["Ulti"][1])
            for i in self.vedok:
                self.players[i].points += 2 * points * (2 ** self.jatekok["Ulti"][1])
            for i in self.players:
                print("ulti pontozás után", i.name, i.points)

class Betli(Szintelen):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 5
        self.can_be_lost = True
        self.vanHuszNegyven = False
        self.name = "Betli"
        self.jatekok = {"Betli": [False, 0]
                        }
        self.jatek_lista = ["Betli"]
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        self.evaluate_betli(5)


    def evaluate_betli(self, points):

        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        if len(self.players[self.vallalo].discard) == 0:
            self.jatekok["Betli"][0] = True

            # ha nem volt kontra:
            if self.jatekok['Betli'][1] == 0:
                self.players[self.vallalo].points += points * 2
                for i in self.vedok:
                    self.players[i].points -= points
            # ha kontra volt
            if self.jatekok["Betli"][1] == 1:
                if self.kontra["Betli"][1][1] and not self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2)
                    self.players[self.vedok[0]].points -= points *2
                    self.players[self.vedok[1]].points -= points

                if not self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2)
                    self.players[self.vedok[0]].points -= points
                    self.players[self.vedok[1]].points -= points * 2

                if self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points * 2 * 2
                    self.players[self.vedok[0]].points -= points * 2
                    self.players[self.vedok[1]].points -= points * 2

            if self.jatekok["Betli"][1] == 2:
                if self.kontra["Betli"][1][1] and not self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2 * 2)
                    self.players[self.vedok[0]].points -= points * 2 * 2
                    self.players[self.vedok[1]].points -= points

                if not self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2 * 2)
                    self.players[self.vedok[0]].points -= points
                    self.players[self.vedok[1]].points -= points * 2 * 2

                if self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    self.players[self.vallalo].points += points * 2 * 2 * 2
                    self.players[self.vedok[0]].points -= points * 2 * 2
                    self.players[self.vedok[1]].points -= points * 2 * 2

        else:
            # ha nem volt kontra:
            if self.jatekok['Betli'][1] == 0:
                self.players[self.vallalo].points -= points * 2
                for i in self.vedok:
                    self.players[i].points += points
            # ha kontra volt
            if self.jatekok["Betli"][1] == 1:
                if self.kontra["Betli"][1][1] and not self.kontra["Betli"][1][2]:
                    print("a")
                    self.players[self.vallalo].points -= points + (points * 2)
                    self.players[self.vedok[0]].points += points * 2
                    self.players[self.vedok[1]].points += points

                if not self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    print("b")
                    self.players[self.vallalo].points -= points + (points * 2)
                    self.players[self.vedok[0]].points += points
                    self.players[self.vedok[1]].points += points * 2

                if self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    print("c")
                    self.players[self.vallalo].points -= points * 2 * 2
                    self.players[self.vedok[0]].points += points * 2
                    self.players[self.vedok[1]].points += points * 2

            if self.jatekok["Betli"][1] == 2:
                if self.kontra["Betli"][1][1] and not self.kontra["Betli"][1][2]:
                    print("d")
                    self.players[self.vallalo].points -= points + (points * 2 * 2)
                    self.players[self.vedok[0]].points += points * 2 * 2
                    self.players[self.vedok[1]].points += points

                if not self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    print("e")
                    self.players[self.vallalo].points -= points + (points * 2 * 2)
                    self.players[self.vedok[0]].points += points
                    self.players[self.vedok[1]].points += points * 2 * 2

                if self.kontra["Betli"][1][1] and self.kontra["Betli"][1][2]:
                    print("f")
                    self.players[self.vallalo].points -= points * 2 * 2 * 2
                    self.players[self.vedok[0]].points += points * 2 * 2
                    self.players[self.vedok[1]].points += points * 2 * 2

    def is_game_lost(self):
        if len(self.players[self.vallalo].discard) == 0:
            return False
        else:
            return True

class Durchmarsch(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 6
        self.can_be_lost = True
        self.vanHuszNegyven = False
        self.bemondtak = []
        self.name = "Durchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        self.csendes_szaz_lehet = False
        self.csendes_ulti_lehet = True
        self.csendes_duri_lehet = False
        self.csendes_ulti = [False, False, int()]
        for j in self.jatekok.keys():
            self.kontra.update({j: copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        self.evaluate_durchmarsch(6)
        Passz.evaluate_csendes_ulti(self, 2)

    def evaluate_durchmarsch(self, points):
        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        lost = False
        for i in self.vedok:
            if len(self.players[i].discard) != 0:
                lost = True

        if not lost:
            self.jatekok["Durchmarsch"][0] = True
            self.players[self.vallalo].points += points * 2 * (2 ** self.jatekok["Durchmarsch"][1])
            for i in self.vedok:
                self.players[i].points -= points * (2 ** self.jatekok["Durchmarsch"][1])
        else:
            self.players[self.vallalo].points -= points * 2 * (2 ** self.jatekok["Durchmarsch"][1])
            for i in self.vedok:
                self.players[i].points += points * (2 ** self.jatekok["Durchmarsch"][1])



    def is_game_lost(self):
        for i in self.vedok:
            if len(self.players[i].discard) != 0:
                return True
        return False

class SzintelenDurchmarsch(Szintelen):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 6
        self.can_be_lost = True
        self.vanHuszNegyven = False
        self.bemondtak = []
        self.name = "Színtelen Durchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        self.csendes_szaz_lehet = False
        self.csendes_ulti_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j: copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        self.evaluate_durchmarsch(6)

    def evaluate_durchmarsch(self, points):

        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        lost = False
        for i in self.vedok:
            if len(self.players[i].discard) != 0:
                lost = True

        if not lost:
            # ha nem volt kontra:
            if self.jatekok['Durchmarsch'][1] == 0:
                self.players[self.vallalo].points += points * 2
                for i in self.vedok:
                    self.players[i].points -= points
            # ha kontra volt
            if self.jatekok["Durchmarsch"][1] == 1:
                if self.kontra["Durchmarsch"][1][1] and not self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2)
                    self.players[self.vedok[0]].points -= points * 2
                    self.players[self.vedok[1]].points -= points

                if not self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2)
                    self.players[self.vedok[0]].points -= points
                    self.players[self.vedok[1]].points -= points * 2

                if self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points * 2 * 2
                    self.players[self.vedok[0]].points -= points * 2
                    self.players[self.vedok[1]].points -= points * 2

            if self.jatekok["Durchmarsch"][1] == 2:
                if self.kontra["Durchmarsch"][1][1] and not self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2 * 2)
                    self.players[self.vedok[0]].points -= points * 2 * 2
                    self.players[self.vedok[1]].points -= points

                if not self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points + (points * 2 * 2)
                    self.players[self.vedok[0]].points -= points
                    self.players[self.vedok[1]].points -= points * 2 * 2

                if self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points += points * 2 * 2 * 2
                    self.players[self.vedok[0]].points -= points * 2 * 2
                    self.players[self.vedok[1]].points -= points * 2 * 2

        else:
            # ha nem volt kontra:
            if self.jatekok['Durchmarsch'][1] == 0:
                self.players[self.vallalo].points -= points * 2
                for i in self.vedok:
                    self.players[i].points += points
            # ha kontra volt
            if self.jatekok["Durchmarsch"][1] == 1:
                if self.kontra["Durchmarsch"][1][1] and not self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points + (points * 2)
                    self.players[self.vedok[0]].points += points * 2
                    self.players[self.vedok[1]].points += points

                if not self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points + (points * 2)
                    self.players[self.vedok[0]].points += points
                    self.players[self.vedok[1]].points += points * 2

                if self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points * 2 * 2
                    self.players[self.vedok[0]].points += points * 2
                    self.players[self.vedok[1]].points += points * 2

            if self.jatekok["Durchmarsch"][1] == 2:
                if self.kontra["Durchmarsch"][1][1] and not self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points + (points * 2 * 2)
                    self.players[self.vedok[0]].points += points * 2 * 2
                    self.players[self.vedok[1]].points += points

                if not self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points + (points * 2 * 2)
                    self.players[self.vedok[0]].points += points
                    self.players[self.vedok[1]].points += points * 2 * 2

                if self.kontra["Durchmarsch"][1][1] and self.kontra["Durchmarsch"][1][2]:
                    self.players[self.vallalo].points -= points * 2 * 2 * 2
                    self.players[self.vedok[0]].points += points * 2 * 2
                    self.players[self.vedok[1]].points += points * 2 * 2

    def is_game_lost(self):
        lost = False
        for i in self.vedok:
            if len(self.players[i].discard) != 0:
                lost = True
        return lost


class NegyvenSzazUlti(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 4
        self.can_be_lost = False
        self.vanHuszNegyven = False
        self.name = "Negyven-száz ulti"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Ulti"]
        self.csendes_ulti_lehet = False
        self.csendes_duri_lehet = True
        self.csendes_szaz_lehet = False
        self.csendes_duri = False
        self.has_40_at_start = False
        for j in self.jatekok.keys():
            self.kontra.update({j: copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 4)
        Ulti.evaluate_ulti(self, 4)
        Passz.evaluate_csendes_duri(self, 3)


class PirosNegyvenSzaz(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'


    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Passz.evaluate_csendes_ulti(self, 4)
        Passz.evaluate_csendes_duri(self, 6)

class HuszSzaz(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = None
        self.points = 8
        self.can_be_lost = False
        self.vanHuszNegyven = False
        self.name = "Húsz-száz"
        self.jatekok = {"Húsz-száz": [False, 0]}
        self.jatek_lista = ["Húsz-száz"]
        self.csendes_ulti_lehet = True
        self.csendes_duri_lehet = True
        self.csendes_ulti = [False, False, int()]
        self.csendes_duri = False
        self.has_40_at_start = False
        for j in self.jatekok.keys():
            self.kontra.update({j: copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        self.evaluate_husz_szaz(8)
        Passz.evaluate_csendes_ulti(self, 2)
        Passz.evaluate_csendes_duri(self, 3)

    def evaluate_husz_szaz(self, points):

        for g in self.jatekok.keys():
            highest_kontra = 0
            for key, value in self.kontra[g].items():
                if True in value:
                    highest_kontra = key
            self.jatekok[g][1] = highest_kontra

        colors = {
            "zold": "Zöld",
            "makk": "Makk",
            "tok": "Tök",
            "piros": "Piros"
        }
        husz = False
        for key, value in colors.items():
            if key == self.adu:
                continue
            felso, kiraly = False, False
            for i in range(3):
                for thisround in self.players[i].discard:
                    for card in thisround:
                        if card[0] == colors[key] + " felső" and card[1] == self.vallalo:
                            felso = True
                        if card[0] == colors[key] + " király" and card[1] == self.vallalo:
                            kiraly = True
            if felso and kiraly:
                husz = True

        vallalo_points = self.player_points[self.vallalo]
        if husz:
            vallalo_points += 20


        for thisround in self.players[self.vallalo].discard:
            for card in thisround:
                if card[0].value in ["tizes", "asz"]:
                    vallalo_points += 10

        if husz and vallalo_points >= 100:
            # húsz-száz nyerve
            self.jatekok["Húsz-száz"][0] = True
            self.players[self.vallalo].points += points * 2 * (2 ** self.jatekok["Húsz-száz"][1])
            for i in self.vedok:
                self.players[i].points -= points * (2 ** self.jatekok["Húsz-száz"][1])

        else:
            self.jatekok["Húsz-száz"][0] = True
            self.players[self.vallalo].points -= points * 2 * (2 ** self.jatekok["Húsz-száz"][1])
            for i in self.vedok:
                self.players[i].points += points * (2 ** self.jatekok["Húsz-száz"][1])



class PirosUlti(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.bemondtak = []
        self.vanHuszNegyven = True


    def evaluate(self):
        vedo_points, vallalo_points = Passz.evaluate_passz(self, 2)
        Ulti.evaluate_ulti(self, 8)
        Passz.evaluate_csendes_szaz(self, vedo_points, vallalo_points, 2)
        Passz.evaluate_csendes_duri(self, 6)


class NegyvenSzazDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.csendes_duri_lehet = False
        self.name = "Negyven-száz durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Durchmarsch": [False, 0]}
        self.jatek_lista = ["Negyven-száz", "Durchmarsch"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 6)
        Passz.evaluate_csendes_ulti(self, 2)

class UltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.csendes_duri_lehet = False
        self.name = "Ulti durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Durchmarsch": [False, 0]}
        self.jatek_lista = ["Ulti", "Durchmarsch"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 6)


class Rebetli(Betli):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Rebetli"
        self.jatekok = {"Betli": [False, 0]}
        self.jatek_lista = ["Betli"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Betli.evaluate_betli(self, 10)


class HuszSzazUlti(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.csendes_szaz_lehet = False
        self.name = "Húsz-száz ulti"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Ulti": [False, 0]}
        self.jatek_lista = ["Húsz-száz", "Ulti"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 4)
        HuszSzaz.evaluate_husz_szaz(self, 8)
        Passz.evaluate_csendes_duri(self, 3)


class ReDurchmarsch(SzintelenDurchmarsch):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Redurchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        SzintelenDurchmarsch.evaluate_durchmarsch(self, 12)


class PirosDurschmarsch(Durchmarsch):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.name = "Durchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        self.csendes_szaz_lehet = True
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Durchmarsch.evaluate_durchmarsch(self, 12)
        Passz.evaluate_csendes_ulti(self, 8)


class NegyvenSzazUltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.csendes_szaz_lehet = False
        self.name = "Negyven-száz ulti durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0],
                        "Durchmarsch" : [False, 0]}
        self.jatek_lista = ["Negyven-száz", "Ulti", "Durchmarsch"]
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 4)
        Ulti.evaluate_ulti(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 6)


class HuszSzazDurchmarsch(HuszSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.csendes_szaz_lehet = False
        self.name = "Húsz-száz durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]}
        self.jatek_lista = ["Húsz-száz", "Durchmarsch"]
        self.csendes_ulti = [False, False, int()]
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 6)
        Passz.evaluate_csendes_ulti(self, 2)

class PirosNegyvenSzazUlti(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.points = 4
        self.can_be_lost = False
        self.vanHuszNegyven = False
        self.name = "Negyven-száz ulti"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Ulti"]
        self.csendes_szaz_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Ulti.evaluate_ulti(self, 8)


class PirosHuszSzaz(HuszSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Húsz-száz"
        self.jatekok = {"Húsz-száz": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz"]
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Passz.evaluate_csendes_ulti(self, 4)
        Passz.evaluate_csendes_duri(self, 6)


class HuszSzazUltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Húsz-száz ulti durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Ulti" : [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Ulti", "Durchmarsch"]
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 8)
        Ulti.evaluate_ulti(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 6)


class PirosNegyvenSzazDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.name = "Negyven-száz durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Durchmarsch" : [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Durchmarsch"]
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 12)
        Passz.evaluate_csendes_ulti(self, 4)


class PirosUltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.adu = 'piros'
        self.name = "Ulti durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Ulti", "Durchmarsch"]
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 12)


class TeritettBetli(Betli):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített betli"
        self.jatekok = {"Betli": [False, 0]}
        self.jatek_lista = ["Betli"]
        self.teritett = True
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Betli.evaluate_betli(self, 20)


class PirosHuszSzazUlti(HuszSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Húsz-száz ulti"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Ulti": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Ulti"]
        self.adu = 'piros'
        self.csendes_ulti_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Ulti.evaluate_ulti(self, 8)
        Passz.evaluate_csendes_duri(self, 6)

class TeritettDurchmarsch(Szines):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített durchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        self.teritett = True
        self.csendes_ulti_lehet = True
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Durchmarsch.evaluate_durchmarsch(self, 24)


class SzintelenTeritettDurchmarsch(SzintelenDurchmarsch):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített színtelen durchmarsch"
        self.jatekok = {"Durchmarsch": [False, 0]}
        self.jatek_lista = ["Durchmarsch"]
        self.teritett = True
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        SzintelenDurchmarsch.evaluate_durchmarsch(self, 24)

class PirosNegyvenSzazUltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Negyven-száz ulti durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Ulti", "Durchmarsch"]
        self.adu = 'piros'
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Ulti.evaluate_ulti(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 12)

class PirosHuszSzazDurchmarsch(HuszSzazDurchmarsch):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Húsz-száz durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Durchmarsch"]
        self.adu = 'piros'
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Durchmarsch.evaluate_durchmarsch(self, 12)
        Passz.evaluate_csendes_ulti(self, 4)

class TeritettNegyvenSzazDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített negyven-száz durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Durchmarsch"]
        self.teritett = True
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class TeritettUltiDurchMarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített ulti durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Ulti", "Durchmarsch"]
        self.teritett = True
        self.csendes_szaz_lehet = True
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 24)

class TeritettNegyvenSzazUltiDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített negyven-száz ulti durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Ulti", "Durchmarsch"]
        self.teritett = True
        self.csendes_duri_lehet = False
        self.csendes_ulti_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 4)
        Ulti.evaluate_ulti(self, 4)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class TeritettPirosNegyvenSzazDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített negyven-száz durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Durchmarsch"]
        self.teritett = True
        self.csendes_duri_lehet = False
        self.adu = 'piros'
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class TeritettHuszSzazDurchmarsch(HuszSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített húsz-száz durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Durchmarsch"]
        self.teritett = True
        self.csendes_szaz_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)

class PirosUltiDurchmarschHuszSzaz(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Ulti húsz-száz durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Ulti", "Húsz-száz", "Durchmarsch"]
        self.adu = 'piros'
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 8)
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Durchmarsch.evaluate_durchmarsch(self, 12)


class PirosTeritettUltiDurchmarsch(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített Ulti Durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Ulti", "Durchmarsch"]
        self.teritett = True
        self.csendes_duri_lehet = False
        self.csendes_ulti_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)
        Passz.evaluate_csendes_szaz(4)

class TeritettUltiDurchmarschHuszSzaz(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített ulti húsz-száz durchmarsch"
        self.jatekok = {"Ulti": [False, 0],
                        "Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Ulti", "Húsz-száz", "Durchmarsch"]
        self.teritett = True
        self.csendes_szaz_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        Ulti.evaluate_ulti(self, 4)
        HuszSzaz.evaluate_husz_szaz(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class PirosTeritettNegyvenSzazUltiDurchmarsch(NegyvenSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített Negyven-száz ulti durchmarsch"
        self.jatekok = {"Negyven-száz": [False, 0],
                        "Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Negyven-száz", "Ulti", "Durchmarsch"]
        self.adu = 'piros'
        self.teritett = True
        self.csendes_duri_lehet = False
        self.csendes_ulti_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        NegyvenSzaz.evaluate_negyven_szaz(self, 8)
        Ulti.evaluate_ulti(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class PirosTeritettDurchmarschHuszSzaz(HuszSzaz):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített Húsz-száz durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Durchmarsch"]
        self.adu = 'piros'
        self.teritett = True
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Durchmarsch.evaluate_durchmarsch(self, 24)


class PirosTeritettUltiDurchmarschHuszSzaz(Ulti):
    def __init__(self, players, lrw):
        super().__init__(players, lrw)
        self.name = "Terített Húsz-száz ulti durchmarsch"
        self.jatekok = {"Húsz-száz": [False, 0],
                        "Ulti": [False, 0],
                        "Durchmarsch": [False, 0]
                        }
        self.jatek_lista = ["Húsz-száz", "Ulti", "Durchmarsch"]
        self.adu = 'piros'
        self.teritett = True
        self.csendes_szaz_lehet = False
        self.csendes_duri_lehet = False
        for j in self.jatekok.keys():
            self.kontra.update({j : copy.deepcopy(self.kontra_alap)})

    def evaluate(self):
        HuszSzaz.evaluate_husz_szaz(self, 16)
        Ulti.evaluate_ulti(self, 8)
        Durchmarsch.evaluate_durchmarsch(self, 24)

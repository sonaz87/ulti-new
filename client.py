import pygame
import sys
from network import Network
from game_elements import *

# pygame inits:
pygame.font.init()
pygame.display.init()


# message types:

POPUP = 'popup'
JOIN = 'join'
DEAL_HAND = 'deal_hand'
BID = 'bid'
PLAY_CARD = 'play_card'
INIT = 'init'
SHOW_DSCARD = 'show_discard'
SHOW_TALON = 'show_talon'
BIDDING = 'bidding'
GAME_PHASE = 'game_phase'
SORTING = 'sorting'
SZINES = "szines"
SZINTELEN = 'szintelen'

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)
DARK_GREY = (50,50,50)
LIGHT_GREY = (200, 200, 200)
popup_text = 'Test'
popup_msg = ''

# fonts

fontObj = pygame.font.Font('C:/Windows/Fonts/Calibri.ttf', 32)
fontObj2 = pygame.font.Font('C:/Windows/Fonts/Calibri.ttf', 12)
fontObj3 = pygame.font.Font('C:/Windows/Fonts/Calibri.ttf', 18)
fontObjLicit = pygame.font.Font('C:/Windows/Fonts/Calibri.ttf', 18)
fontObj3.set_bold(True)
fontObjLicit.bold

# test button

textSurfaceObj = fontObj.render(popup_text, True, WHITE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

# popup messages
popupSurf1 = fontObj2.render('Placeholder1', True, WHITE)
popupSurf2 = fontObj2.render('Placeholder2', True, WHITE)
popupSurf3 = fontObj2.render('Placeholder3', True, WHITE)
popupSurf4 = fontObj2.render('Placeholder4', True, WHITE)
popupSurf5 = fontObj2.render('Placeholder5', True, WHITE)
popupRectObj1 = popupSurf1.get_rect()
popupRectObj2 = popupSurf1.get_rect()
popupRectObj3 = popupSurf1.get_rect()
popupRectObj4 = popupSurf1.get_rect()
popupRectObj5 = popupSurf1.get_rect()
popupRectObj1.center = (1300, 400)
popupRectObj2.center = (1300, 420)
popupRectObj3.center = (1300, 440)
popupRectObj4.center = (1300, 460)
popupRectObj5.center = (1300, 480)

licitConfirmButtonSurf = fontObj.render('OK', True, WHITE)
licitConfirmButtonRect = licitConfirmButtonSurf.get_rect()
licitConfirmButtonRect.center = (700, 550)

width, height = 1400, 900

DISPLAYSURF = pygame.display.set_mode((1400, 900), 0, 32)
pygame.display.set_caption('Ulti')
table_img = pygame.image.load(r'D:/python projects/ulti/GUI/images/table.jpg')

clientNumber = 0
card_images = dict()

deck = Deck()

for card in deck.cards:
    card_images.update({card.color + card.value: pygame.image.load(
        'D:/python projects/ulti/GUI/images/' + card.color + card.value + '.jpg')})


def redrawWindow(DISPLAYSURF, game, player):
    global sortButton
    global licitConfirmButton
    global cards_to_display
    global licit_items
    global pickUpTalonButton
    global passInBiddingButton


    popupSurf1 = fontObj2.render(game.get_popups()[0], True, WHITE)
    popupSurf2 = fontObj2.render(game.get_popups()[1], True, WHITE)
    popupSurf3 = fontObj2.render(game.get_popups()[2], True, WHITE)
    popupSurf4 = fontObj2.render(game.get_popups()[3], True, WHITE)
    popupSurf5 = fontObj2.render(game.get_popups()[4], True, WHITE)

    DISPLAYSURF.blit(table_img, (0, 0))
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(popupSurf1, popupRectObj1)
    DISPLAYSURF.blit(popupSurf2, popupRectObj2)
    DISPLAYSURF.blit(popupSurf3, popupRectObj3)
    DISPLAYSURF.blit(popupSurf4, popupRectObj4)
    DISPLAYSURF.blit(popupSurf5, popupRectObj5)

    # name tags:
    try:
        if player == 0:
            p1NameSurf = fontObj.render(str(game.players[0].name) + " - " + str(game.players[0].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[1].name) + " - " + str(game.players[1].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[2].name) + " - " + str(game.players[2].points), True, WHITE)
        elif player == 1:
            p1NameSurf = fontObj.render(str(game.players[1].name) + " - " + str(game.players[1].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[2].name) + " - " + str(game.players[2].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[0].name) + " - " + str(game.players[0].points), True, WHITE)
        elif player == 2:
            p1NameSurf = fontObj.render(str(game.players[2].name) + " - " + str(game.players[2].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[0].name) + " - " + str(game.players[0].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[1].name) + " - " + str(game.players[1].points), True, WHITE)
    except:
        p1NameSurf = fontObj.render("Várakozás a többiekre", True, WHITE)
        p2NameSurf = fontObj.render("Várakozás a többiekre", True, WHITE)
        p3NameSurf = fontObj.render("Várakozás a többiekre", True, WHITE)

    p1NameRect = p1NameSurf.get_rect()
    p2NameRect = p2NameSurf.get_rect()
    p3NameRect = p3NameSurf.get_rect()

    p1NameRect.top = (800)
    p1NameRect.right = (1350)
    p2NameRect.top = (34)
    p2NameRect.left = (50)
    p3NameRect.top = (34)
    p3NameRect.right = (1350)

    DISPLAYSURF.blit(p1NameSurf, p1NameRect)
    DISPLAYSURF.blit(p2NameSurf, p2NameRect)
    DISPLAYSURF.blit(p3NameSurf, p3NameRect)

    pickUpTalonSurf = fontObj.render('Felveszem!', True, WHITE)
    passInBiddingSurf = fontObj.render(
        "Mehet!" if game.bidding_list[1] == 'passz' and game.bidding_list[2] == "passz" else "Passz", True, WHITE)
    pickUpTalonRect = pickUpTalonSurf.get_rect()
    passInBiddingRect = passInBiddingSurf.get_rect()
    pickUpTalonRect.center = (450, 600)
    passInBiddingRect.center = (650, 600)


    cards_to_display = []
    if len(game.players[player].hand) > 0:
        sortSurf = fontObj3.render(
            'Rendezés színtelenre' if game.players[player].sorting == SZINES else "Rendezés színesre", True, BLACK)
        sortRect = sortSurf.get_rect()
        sortRect.left = 30
        sortRect.bottom = 600
        sortButton = pygame.draw.rect(DISPLAYSURF, GREY, sortRect)
        game.players[player].sort_hand()
        for card in game.players[player].hand:
            cardSurf = card_images[card.color + card.value]
            cardRect = cardSurf.get_rect()
            cards_to_display.append([cardSurf, cardRect, card])
    if len(cards_to_display) > 0:
        displacement = 50
        for i in range(len(cards_to_display)):
            if cards_to_display[i][2] in game.players[player].selected_cards:
                cards_to_display[i][1].bottom = 840
            else:
                cards_to_display[i][1].bottom = 890
            cards_to_display[i][1].left = displacement
            DISPLAYSURF.blit(cards_to_display[i][0], cards_to_display[i][1])
            displacement += 80

        pygame.draw.rect(DISPLAYSURF, GREY, sortButton)
        DISPLAYSURF.blit(sortSurf, sortRect)

    # game display objects
    if game.game_phase == BIDDING:
        try:
            selectedGameSurf = fontObj.render(game.vallao + " - " + game.current_game, True, WHITE)
            selectedGameRect = selectedGameSurf.get_rect()
            selectedGameRect.center = (700, 50)
            DISPLAYSURF.blit(selectedGameSurf, selectedGameRect)
        except:
            pass


    if game.game_phase == BIDDING and game.players[player].is_active:
        # akar-e licitálni:
        if game.current_game == "Piros terített ulti durchmarsch húsz-száz":
            n.send("passz")
        if not game.players[player].wants_to_bid:
            pickUpTalonButton = pygame.draw.rect(DISPLAYSURF, GREY, pickUpTalonRect)
            passInBiddingButton = pygame.draw.rect(DISPLAYSURF, GREY, passInBiddingRect)
            DISPLAYSURF.blit(pickUpTalonSurf, pickUpTalonRect)
            DISPLAYSURF.blit(passInBiddingSurf, passInBiddingRect)
        # választható játékokat felkínálni
        if game.players[player].wants_to_bid:
            licit_items = []
            licit_displacement = 80
            for key in game.possible_games.keys():
                if game.possible_games[key][0] > game.possible_games[game.current_game][0]:
                    licitSurf = fontObjLicit.render(key, True, RED if key == game.players[player].licit_selected else BLACK)
                    licitRect = licitSurf.get_rect()
                    licit_items.append([licitSurf, licitRect, key])

            licit_box = pygame.draw.rect(DISPLAYSURF, LIGHT_GREY, (500, 70, 400, 500))
            if len(licit_items) > 0:
                for element in licit_items:
                    if licit_items.index(element) > 20:
                        break
                    element[1].centerx = 700
                    element[1].top = licit_displacement
                    DISPLAYSURF.blit(element[0], element[1])
                    licit_displacement += 18

                if game.players[player].licit_selected != None and len(game.players[player].selected_cards) == 2:
                    licitConfirmButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, licitConfirmButtonRect)
                    DISPLAYSURF.blit(licitConfirmButtonSurf, licitConfirmButtonRect)



    pygame.display.update()


def main():
    global sortButton
    run = True
    clock = pygame.time.Clock()
    n = Network(server, port)
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            e = sys.exc_info()[0]
            print(e)
            run = False
            print("Couldn't get game")
            break

        redrawWindow(DISPLAYSURF, game, player)


        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            if mouseClicked and textRectObj.collidepoint(mousex, mousey):
                msg = n.send('test')

            # sorting button
            try:
                if mouseClicked and sortButton.collidepoint(mousex, mousey):
                    if game.players[player].sorting == SZINTELEN:
                        game.players[player].sorting = SZINES
                    else:
                        game.players[player].sorting = SZINTELEN
                    game = n.send_player_object(game.players[player])

            except:
                e = sys.exc_info()
                print("error in soring button event handling")
                print(e)
                pass

            # card selection

            try:
                if game.players[player].is_active:
                    card_select_list = []
                    for i in range(len(cards_to_display)):
                        if mouseClicked and cards_to_display[i][1].collidepoint(mousex, mousey):
                            card_select_list.append(i)
                    if len(card_select_list) == 2:
                        if card_select_list[0] > card_select_list[1]:
                            card_select_list.pop(1)
                        else:
                            card_select_list.pop(0)

                    if len(card_select_list) != 0:
                        if game.players[player].hand[card_select_list[0]] in game.players[player].selected_cards:
                            game.players[player].selected_cards.remove(game.players[player].hand[card_select_list[0]])
                        else:
                            if game.game_phase == BIDDING:
                                if len(game.players[player].selected_cards) < 2:
                                    if game.players[player].hand[card_select_list[0]] not in game.players[player].selected_cards:
                                        game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])
                                if len(game.players[player].selected_cards) == 2:
                                    if game.players[player].hand[card_select_list[0]] not in game.players[player].selected_cards:
                                        game.players[player].selected_cards.pop(0)
                                        game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])
                                        #TODO! a lejátszási fázisra is megírni
                    game = n.send_player_object(game.players[player])
            except:
                e = sys.exc_info()
                print("error in card selection event handling")
                print(e)
                pass

            # bidding selection
            try:
                if game.game_phase == BIDDING and game.players[player].is_active and not game.players[player].wants_to_bid:
                    if mouseClicked and pickUpTalonButton.collidepoint(mousex, mousey):
                        game = n.send("pickup")
                    if mouseClicked and passInBiddingButton.collidepoint(mousex, mousey):
                        game = n.send("passz")
            except:
                e = sys.exc_info()
                print("error in wants to bid selection event handling")
                print(e)
                pass

            if game.game_phase == BIDDING and game.players[player].wants_to_bid:
                try:
                    for i in licit_items:
                        if mouseClicked and i[1].collidepoint(mousex, mousey):
                            if i[2] == game.players[player].licit_selected:
                                pass
                            else:
                                game.players[player].licit_selected = i[2]
                            game = n.send_player_object(game.players[player])

                    if mouseClicked and licitConfirmButtonRect.collidepoint(mousex, mousey):
                        game = n.send("bid")
                except:
                    e = sys.exc_info()
                    print("error in licit selection event handling")
                    print(e)
                    pass

        redrawWindow(DISPLAYSURF, game, player)

server = "192.168.178.24"
port = 5555
main()

import pygame
import sys
from network import Network
from game_elements import *
from pygame.locals import *



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
PLAY = 'play'
END = 'end'

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

playCardConfirmButtonSurf = fontObj.render('OK', True, WHITE)
playCardConfirmButtonRect = licitConfirmButtonSurf.get_rect()
playCardConfirmButtonRect.center = (1050, 800)


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

def getStartAndEndPos(game):
    pass

def move_card(start_pos, end_pos):
    startx = start_pos[0]
    starty = start_pos[1]
    endx = end_pos[0]
    endy = end_pos[1]
    if startx > endx:
        if (startx - endx) % 40 != 0:
            startx =  startx - ((startx - endx) % 40)
        else:
            startx -= 40
    elif startx < endx:
        if (endx - startx) % 40 != 0:
            startx =  startx + ((endx - startx) % 40)
        else:
            startx += 40

    if starty > endy:
        if (starty - endy) % 40 != 0:
            starty =  starty - ((starty - endy) % 40)
        else:
            starty -= 40
    elif starty < endy:
        if (endy - starty) % 40 != 0:
            starty =  starty + ((endy - starty) % 40)
        else:
            starty += 40
    return startx, starty

def collectPlayedCards(game):
    pass


def redrawWindow(DISPLAYSURF, game, player):
    global sortButton
    global licitConfirmButton
    global cards_to_display
    global licit_items
    global pickUpTalonButton
    global passInBiddingButton
    global playCardConfirmButton
    global p0PlayedCardStartPos
    global p1PlayedCardStartPos
    global p2PlayedCardStartPos
    global p0PlayedCardEndPos
    global p1PlayedCardEndPos
    global p2PlayedCardEndPos
    global client_animation_completed
    global aduConfrimRect
    global aduZoldRect
    global aduMakkRect
    global aduTokRect
    global aduConfirmButton
    global huszNegyvenButton
    global kontraButton
    global kontraConfirms
    global cancelKontraButton
    global startOverButton


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
            p1NameSurf = fontObj.render(str(game.players[0].name) + " : " + str(game.players[0].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[1].name) + " : " + str(game.players[1].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[2].name) + " : " + str(game.players[2].points), True, WHITE)
        elif player == 1:
            p1NameSurf = fontObj.render(str(game.players[1].name) + " : " + str(game.players[1].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[2].name) + " : " + str(game.players[2].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[0].name) + " : " + str(game.players[0].points), True, WHITE)
        elif player == 2:
            p1NameSurf = fontObj.render(str(game.players[2].name) + " : " + str(game.players[2].points), True, WHITE)
            p2NameSurf = fontObj.render(str(game.players[0].name) + " : " + str(game.players[0].points), True, WHITE)
            p3NameSurf = fontObj.render(str(game.players[1].name) + " : " + str(game.players[1].points), True, WHITE)
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
            gameDetailSurf = fontObj.render(game.players[int(game.vallalo)].name + " - " + game.current_game, True, WHITE)
            gameDetailRect = gameDetailSurf.get_rect()
            gameDetailRect.center = (700, 30)
            DISPLAYSURF.blit(gameDetailSurf, gameDetailRect)

        except:
            pass
    if game.game_phase == BIDDING and game.players[player].is_active:
        # akar-e licitálni:
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

    # play phase

    if game.game_phase == PLAY:
        try:
            if game.selected_game.adu != None:
                szinek = {
                    'zold': "Zöld",
                    'makk': "Makk",
                    "tok": "Tök",
                    "piros": "Piros"
                }
                gameDetailSurf = fontObj.render(game.players[game.selected_game.vallalo].name + " - " + szinek[game.selected_game.adu] + " " + game.selected_game.name, True, WHITE)
                gameDetailRect = gameDetailSurf.get_rect()
                gameDetailRect.center = (700, 30)
                DISPLAYSURF.blit(gameDetailSurf, gameDetailRect)
            else:
                gameDetailSurf = fontObj.render(game.players[game.selected_game.vallalo].name + " - " + game.selected_game.name, True, WHITE)
                gameDetailRect = gameDetailSurf.get_rect()
                gameDetailRect.center = (700, 30)
                DISPLAYSURF.blit(gameDetailSurf, gameDetailRect)

        except:
            pass

        if game.players[player].is_active:
            try:
                if game.selected_game.is_valid_choice(game.cards_on_the_table, game.players[player].selected_cards[0], game.players[player].hand):
                    playCardConfirmButton = pygame.draw.rect(DISPLAYSURF, GREY, playCardConfirmButtonRect)
                    DISPLAYSURF.blit(playCardConfirmButtonSurf, playCardConfirmButtonRect)
            except:
                # print("error in play phase display")
                # e = sys.exc_info()
                # print(e)
                pass
            # adu választás az első körben
            try:
                if game.selected_game.round == 1 and game.selected_game.adu == None and issubclass(type(game.selected_game), Szines):
                    adu_box = pygame.draw.rect(DISPLAYSURF, LIGHT_GREY, (600, 150, 200, 200))
                    aduTitleSurf = fontObj.render('Válassz adut!', True, WHITE)
                    adutTitleRect = aduTitleSurf.get_rect()
                    aduZoldSurf = fontObj2.render('Zöld', True, WHITE if game.players[player].adu_selected != 'zold' else RED)
                    aduZoldRect = aduZoldSurf.get_rect()
                    aduMakkSurf = fontObj2.render('Makk', True,
                                                  WHITE if game.players[player].adu_selected != 'makk' else RED)
                    aduMakkRect = aduZoldSurf.get_rect()
                    aduTokSurf = fontObj2.render('Tök', True,
                                                  WHITE if game.players[player].adu_selected != 'tok' else RED)
                    aduTokRect = aduZoldSurf.get_rect()
                    adutTitleRect.center = (700, 210)
                    aduZoldRect.center = (700, 240)
                    aduMakkRect.center = (700, 260)
                    aduTokRect.center = (700, 280)

                    aduConfirmSurf = fontObj.render("OK", True, WHITE)
                    aduConfrimRect = aduConfirmSurf.get_rect()
                    aduConfrimRect.center = (700, 350)
                    DISPLAYSURF.blit(aduTitleSurf, adutTitleRect)
                    DISPLAYSURF.blit(aduZoldSurf, aduZoldRect)
                    DISPLAYSURF.blit(aduMakkSurf, aduMakkRect)
                    DISPLAYSURF.blit(aduTokSurf, aduTokRect)
                    if game.players[player].adu_selected != None:
                        aduConfirmButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, aduConfrimRect)
                        DISPLAYSURF.blit(aduConfirmSurf, aduConfrimRect)

            except:
                print("error in displaying adu selection")
                e = sys.exc_info()
                print(e)
                pass
            # húsz - negyven
            try:
                if game.players[player].is_active and game.selected_game.round == 1 and game.selected_game.vanHuszNegyven == True and game.selected_game.adu != None and player not in game.selected_game.bemondtak:
                    huszNegyvenSurf = fontObj.render("Húsz-negyven bemondása", True, WHITE)
                    huszNegyvenRect = huszNegyvenSurf.get_rect()
                    huszNegyvenRect.center = (1100, 700)
                    huszNegyvenButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, huszNegyvenRect)
                    DISPLAYSURF.blit(huszNegyvenSurf, huszNegyvenRect)

            except:
                pass

            # kontrák
            try:
                is_kontra_available = False
                for g in game.selected_game.kontra.keys():
                    # print(" [*]  in kontra display, game.selected_game.kontra[g][game.selected_game.round -1]", game.selected_game.kontra[g][game.selected_game.round -1])
                    if True in game.selected_game.kontra[g][game.selected_game.round -1]:
                        # print("kontra available")
                        is_kontra_available = True
                if is_kontra_available == True and display_kontra == False and game.selected_game.round % 2 == 1 and player != game.selected_game.vallalo:
                    kontraSurf = fontObj.render("Kontra", True, WHITE)
                    kontraRect = kontraSurf.get_rect()
                    kontraRect.center = (1200, 200)
                    kontraButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, kontraRect)
                    DISPLAYSURF.blit(kontraSurf, kontraRect)
                elif is_kontra_available == True and display_kontra == False and game.selected_game.round % 2 == 0 and player == game.selected_game.vallalo:
                    kontraSurf = fontObj.render("Kontra", True, WHITE)
                    kontraRect = kontraSurf.get_rect()
                    kontraRect.center = (1200, 200)
                    kontraButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, kontraRect)
                    DISPLAYSURF.blit(kontraSurf, kontraRect)

                if display_kontra == True:

                        kontraSurfs = []
                        kontraRects = []
                        kontraConfirms = []
                        okSurf = fontObj3.render("OK", True, WHITE)

                        for g in game.selected_game.kontra.keys():
                            kontraSurfs.append(fontObj3.render(g, True, BLACK))
                            kontraRects.append(kontraSurfs[-1].get_rect())

                        pygame.draw.rect(DISPLAYSURF, LIGHT_GREY, (1100, 200, 200, 400))
                        displacement = 250
                        for i in range(len(kontraSurfs)):
                            kontraRects[i].right = 1180
                            kontraRects[i].top = displacement
                            DISPLAYSURF.blit(kontraSurfs[i], kontraRects[i])
                            confirmRect = okSurf.get_rect()
                            confirmRect.left = 1220
                            confirmRect.top = displacement
                            kontraConfirms.append(pygame.draw.rect(DISPLAYSURF, DARK_GREY, confirmRect))
                            DISPLAYSURF.blit(okSurf, confirmRect)
                            displacement += 40

                        cancelkontraSurf = fontObj.render("Mégse", True, WHITE)
                        cancelkontraRect = cancelkontraSurf.get_rect()
                        cancelkontraRect.center = (1200, 530)
                        cancelKontraButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, cancelkontraRect)
                        DISPLAYSURF.blit(cancelkontraSurf, cancelkontraRect)

            except:
                print("error in displaying kontra selection")
                e = sys.exc_info()
                print(e)
                pass


        try:
            if len(game.cards_on_the_table) > 0:
                mid_cards_to_dislpay = []
                # print("mid cards display started")
                for element in game.cards_on_the_table:
                    # print("element: ", element)
                    # print("element[0]", element[0])
                    middleCardSurf = card_images[element[0].color + element[0].value]
                    # print("be")
                    middleCardRect = middleCardSurf.get_rect()
                    # print("bi")
                    mid_cards_to_dislpay.append([[middleCardSurf, middleCardRect], element[1]])
                    # print("ba")
                # print("1")
                # print(mid_cards_to_dislpay)
                for i in mid_cards_to_dislpay:
                    if i[1] == 0:
                        # print("2")
                        i[0][1].center = p0PlayedCardEndPos
                    elif i[1] == 1:
                        # print("3")
                        i[0][1].center = p1PlayedCardEndPos
                    elif i[1] == 2:
                        # print("4")
                        i[0][1].center = p2PlayedCardEndPos
                    DISPLAYSURF.blit(i[0][0], i[0][1])
        except:
            print("error in displaying cards in the middle")
            e = sys.exc_info()[0]
            print(e)
            pass
    if game.game_phase == END:
        if game.players[player].ready_for_next_round == False:
            pygame.draw.rect(DISPLAYSURF, LIGHT_GREY, (200, 100, 1000, 700))
            resultSurfs = []
            resultRects = []
            displacement = 200
            for key, value in game.selected_game.jatekok.items():
                resultSurfs.append(fontObj.render(game.selected_game.kontra[key][0][0] + " " +  key + " - " + ("Nyerve" if value[1] else "Bukva"), True, BLACK))
                resultRects.append(resultSurfs[-1].get_rect())
                resultRects[-1].left = 300
                resultRects[-1].top = displacement
                DISPLAYSURF.blit(resultSurfs[-1], resultRects[-1])

            startOverSurf = fontObj.render("Új játék", True, WHITE)
            startOverRect = startOverSurf.get_rect()
            startOverRect.center = (700, 650)
            startOverButton = pygame.draw.rect(DISPLAYSURF, DARK_GREY, startOverRect)
            DISPLAYSURF.blit(startOverSurf, startOverRect)

    pygame.display.update()


def main():
    global sortButton
    global p0PlayedCardStartPos
    global p1PlayedCardStartPos
    global p2PlayedCardStartPos
    global p0PlayedCardEndPos
    global p1PlayedCardEndPos
    global p2PlayedCardEndPos
    global client_animation_completed
    global display_kontra
    display_kontra = False
    client_animation_completed = False
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
        # defining starting and ending playes for played cards
        try:
            if game.players[0].card_played == None:
                if player == 0:
                    p0PlayedCardStartPos = (700, 750)
                    p0PlayedCardEndPos = (700, 450)
                elif player == 1:
                    p0PlayedCardStartPos = (80, 130)
                    p0PlayedCardEndPos = (600, 400)
                elif player == 2:
                    p0PlayedCardStartPos = (1310, 130)
                    p0PlayedCardEndPos = (800, 400)

            if game.players[1].card_played == None:
                if player == 0:
                    p1PlayedCardStartPos = (1310, 130)
                    p1PlayedCardEndPos = (800, 400)
                elif player == 1:
                    p1PlayedCardStartPos = (700, 750)
                    p1PlayedCardEndPos = (700, 450)
                elif player == 2:
                    p1PlayedCardStartPos = (80, 130)
                    p1PlayedCardEndPos = (600, 400)

            if game.players[2].card_played == None:
                if player == 0:
                    p2PlayedCardStartPos = (80, 130)
                    p2PlayedCardEndPos = (600, 400)
                elif player == 1:
                    p2PlayedCardStartPos = (1310, 130)
                    p2PlayedCardEndPos = (800, 400)
                elif player == 2:
                    p2PlayedCardStartPos = (700, 750)
                    p2PlayedCardEndPos = (700, 450)
        except:
            pass


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
                    # a legnagyobb értékű játékra nem lehet rálicitálni
                    if game.current_game == "Piros terített ulti durchmarsch húsz-száz":
                        n.send("passz")
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
                            # in bidding phase, let player select 2 cards
                            if game.game_phase == BIDDING:
                                if len(game.players[player].selected_cards) < 2:
                                    if game.players[player].hand[card_select_list[0]] not in game.players[player].selected_cards:
                                        game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])
                                if len(game.players[player].selected_cards) == 2:
                                    if game.players[player].hand[card_select_list[0]] not in game.players[player].selected_cards:
                                        game.players[player].selected_cards.pop(0)
                                        game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])
                            # in play phase let player select 1 card only
                            elif game.game_phase == PLAY:
                                if len(game.players[player].selected_cards) < 1:
                                    game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])
                                if len(game.players[player].selected_cards) == 1:
                                    if game.players[player].hand[card_select_list[0]] not in game.players[player].selected_cards:
                                        game.players[player].selected_cards.pop(0)
                                        game.players[player].selected_cards.append(game.players[player].hand[card_select_list[0]])

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

            # play section
            if game.game_phase == PLAY:

                try:
                    if mouseClicked and playCardConfirmButton.collidepoint(mousex, mousey):
                        game = n.send("card_was_played")
                except:
                    pass

                try:
                    if mouseClicked and huszNegyvenButton.collidepoint(mousex, mousey):
                        game = n.send("husznegyven")
                except:
                    pass

                try:
                    if mouseClicked and aduTokRect.collidepoint(mousex, mousey):
                        game.players[player].adu_selected = 'tok'
                        game = n.send_player_object(game.players[player])
                    if mouseClicked and aduZoldRect.collidepoint(mousex, mousey):
                        game.players[player].adu_selected = 'zold'
                        game = n.send_player_object(game.players[player])
                    if mouseClicked and aduMakkRect.collidepoint(mousex, mousey):
                        game.players[player].adu_selected = 'makk'
                        game = n.send_player_object(game.players[player])

                    if mouseClicked and aduConfirmButton.collidepoint(mousex, mousey):
                        game = n.send("adu:" + game.players[player].adu_selected)
                except:
                    pass
                try:
                    if mouseClicked and kontraButton.collidepoint(mousex, mousey):
                        print("kontra clicked")
                        display_kontra = True
                except:
                    pass
                try:
                    for i in range(len(kontraConfirms)):
                        if mouseClicked and kontraConfirms[i].collidepoint(mousex, mousey):
                            game = n.send("kontra:" + str(i))
                except:
                    pass

                try:
                    if mouseClicked and cancelKontraButton.collidepoint(mousex, mousey):
                        display_kontra = False

                except:
                    pass
            try:
                if game.game_phase == END:
                    if mouseClicked and startOverButton.collidepoint(mousex, mousey):
                        game.players[player].ready_for_next_round = True
                        game = n.send_player_object(game.players[player])
                        game = n.send("reset")
            except:
                pass

        redrawWindow(DISPLAYSURF, game, player)

server = "192.168.178.24"
port = 5555
main()

#!/usr/bin/env python
"""blackjack.py: Simulation of the blackjack card game."""

__author__ = "Siddharth Garimella"
__email__ = "sid@students.olin.edu"

from playcards import Card, Deck, Player

import qprompt

STAY_FLAG = False
DOUBLE_FLAG = False
SPLIT_FLAG = False
SPLIT_CARD = None
EXIT_FLAG = False

DEFAULT_BANK = 1000

blackjack_memory = {
    "bank": DEFAULT_BANK,
    "bet": 0,
    "no_cards": 0,
    "cards": [],
    "cards_val": 0,
    "status": "NORMAL",
    "vals": []
}


def card_val(memory, card):
    v = 0
    if str.isdigit(card.number):
        v = int(card.number)
    elif card.number != "A":
        v = 10
    elif memory["cards_val"] + 11 <= 21:
        v = 11
    else:
        v = 1
    return v


def blackjack_update(memory, card):
    # Add card to hand
    memory["cards"].append(card)
    memory["no_cards"] += 1

    # Keep count in memory
    add_val = card_val(memory, card)

    # Describe what the count means
    memory["cards_val"] += add_val
    if memory["cards_val"] == 21 and memory["no_cards"] == 2:
        memory["status"] = "BLACKJACK"
    elif memory["cards_val"] == 21:
        memory["status"] = "21"
    elif memory["cards_val"] > 21:
        memory["status"] = "BUST"
    else:
        memory["status"] = "NORMAL"

    return memory

def betting_round(player):
    bet = qprompt.ask_int("Enter a bet amount less than your bank value of " + str(player.memory["bank"]), valid=lambda x: x <= player.memory["bank"])
    player.memory["bank"] -= bet
    player.memory["bet"] = bet
    qprompt.info("Betted " + str(bet))
    qprompt.pause()
    qprompt.clear()

def decision_round(player):
    s = "Your hand: "
    for card in player.memory["cards"]:
        s += str(card) + " "
    s += " |  "
    s += "Hand value: " + str(player.memory["cards_val"])
    s += "\n"
    qprompt.info(s)

    if player.memory["cards_val"] >= 21:
        options = ["Stay", "Exit"]
        item = qprompt.enum_menu(options).show(header="OPTIONS:")
        print("Selected " + options[int(item)-1] + ".")
        qprompt.hrule()
        return options[int(item)-1]
    else:
        options = ["Hit","Stay","Exit"]
        if player.memory["no_cards"] == 2 and SPLIT_FLAG == False:
            options.append("Double down")
            if player.memory["cards"][0].number == player.memory["cards"][1].number:
                options.append("Split")
        item = qprompt.enum_menu(options).show(header="OPTIONS:")
        print("Selected " + options[int(item)-1] + ".")
        qprompt.clear()
        return options[int(item)-1]

def payout_round(deck, player):
    qprompt.clear()
    payout = 0
    dealer_memory = {
        "bank": DEFAULT_BANK,
        "bet": 0,
        "no_cards": 0,
        "cards": [],
        "cards_val": 0,
        "status": "NORMAL",
        "vals": []
    }
    # the dealer's bank doesn't matter, we can keep reinstantiating
    dealer = Player(ids="Dealer", update=blackjack_update, memory=dealer_memory)
    dealer.receive(deck.draw())
    dealer.receive(deck.draw())

    while dealer.memory["cards_val"] <= 16:
        dealer.receive(d.draw())

    for value in player.memory["vals"]:
        if dealer.memory["cards_val"] > 21:
            if value == 21:
                payout += player.memory["bet"]*2.5
            elif value < 21:
                payout += player.memory["bet"]*2
        elif dealer.memory["cards_val"] == 21:
            payout += 0
        elif value <= 21:
            if value > dealer.memory["cards_val"]:
                payout += player.memory["bet"]*2
                if value == 21:
                    payout += player.memory["bet"]*0.5
            elif value == dealer.memory["cards_val"]:
                payout += player.memory["bet"]
            else:
                payout += 0

    qprompt.info("DEALER GOT: " + str(dealer.memory["cards_val"]))
    qprompt.info("PAYOUT: " + str(payout))
    player.memory["bet"] = 0
    player.memory["bank"] += payout
    player.discard(player.memory)
    player.memory["cards_val"] = 0
    player.memory["cards"] = []
    player.memory["no_cards"] = 0
    player.memory["vals"] = []
    qprompt.pause()
    qprompt.clear()


d = Deck()
player = Player(ids="You", update=blackjack_update, memory=blackjack_memory)

while (not EXIT_FLAG):
    qprompt.clear()
    betting_round(player)

    qprompt.info("DEALING CARDS...")
    player.receive(d.draw())
    player.receive(d.draw())

    while (not STAY_FLAG ) and (not EXIT_FLAG):

        action = decision_round(player)

        if action == "Hit":
            player.receive(d.draw())
        elif action == "Double down":
            player.memory["bank"] -= player.memory["bet"]
            player.memory["bet"] += player.memory["bet"]
            DOUBLE_FLAG = True
        elif action == "Split":
            SPLIT_CARD = player.memory["cards"][1]
            SPLIT_FLAG = True
            player.memory["cards"] = [player.memory["cards"][0]]
            player.memory["no_cards"] = 1
            player.memory["cards_val"] = card_val(player.memory, player.memory["cards"][0])
            player.memory["bet"] = player.memory["bet"]/2
            player.memory["status"] = "SPLIT"
        elif action == "Stay":
            player.memory["vals"].append(player.memory["cards_val"])
            STAY_FLAG = True
            if SPLIT_FLAG:
                STAY_FLAG = False
                player.memory["cards"] = [SPLIT_CARD]
                player.memory["no_cards"] = 1
                player.memory["cards_val"] = card_val(player.memory, player.memory["cards"][0])
                player.memory["bet"] = player.memory["bet"]/2
                player.memory["status"] = "NORMAL"
                SPLIT_FLAG = False
        elif action == "Exit":
            EXIT_FLAG = True

    payout_round(d, player)
    STAY_FLAG = False

qprompt.info("EXITING...")
#!/usr/bin/env python
"""playcards.py: Representation of a standard 52 playing card deck with player utilities."""

__author__ = "Siddharth Garimella"
__email__ = "sid@students.olin.edu"


import random

# Define deck suites and face cards
faces = ["J","Q","K","A"]
suits = ['d','c','h','s'] 

class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    def __str__(self):
        # Get unicode for pretty printing
        return self.number + "/" + self.suit

class Deck:
    def build(self, faces, suits):
        cards = []
        # Add cards to deck
        for face in faces:
            for suit in suits:
                cards.append(Card(number=face,suit=suit))
        for num in range(1,10):
            n = str(num+1) 
            for suit in suits:
                cards.append(Card(number=n,suit=suit))
        # Shuffle deck
        random.shuffle(cards)
        return cards

    def __init__(self):
        self.cards = self.build(faces,suits)
        
    def __str__(self):
        s = ""
        for card in self.cards:
            s += "\n" + str(card) 
        return s

    def draw(self):
        # Draw a card, remove from deck
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            print("Out of cards, using a new deck.")
            self.cards = self.build(faces,suits)
            return self.cards.pop(0)

    def insert(self, card):
        self.cards.append(card)
        return True

class Player:
    def __init__(self, ids, update, memory):
        self.id = ids
        self.cards = []
        # update is a method that defines how a Player's model of a game should be updated with a new card
        self.update = update
        # memory is a dict that contains a running rough tally of score/value in any game 
        self.memory = memory

    def __str__(self):
        s = ""
        s += "\nPlayer " + self.id + " is currently holding cards:"
        for card in self.cards:
            s += "  " + str(card)
        s += "\n------------------------------------------------"
        s += "\n"
        s += str(self.memory)
        return s

    def receive(self, card):
        if self.update is not None:
            self.cards.append(card)
            self.memory = self.update(self.memory, card)
        else:
            self.cards.append(card)

    def discard(self, memory):
        self.cards = []
        self.memory = memory
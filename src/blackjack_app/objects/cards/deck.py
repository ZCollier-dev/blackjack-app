import json
import random

from blackjack_app.objects.cards.card import Card
from blackjack_app.objects.linkedList.linked_list import LinkedList

# has_jokers - Exclude jokers if False - delete from initial_deck
# deck_size - Count up when card added to deck
# __app_dir - Topmost directory of the app
# initial_deck - The full deck accessed from json file

# draw_pile - Queue Data Structure - Linked List - Cards dequeued from queue when drawn
# discard_pile - Linked List - Cards queued from drawn cards - Also includes cards in play

class Deck:
    def __init__(self, app_dir, has_jokers=False):
        self.has_jokers = has_jokers
        self.deck_size = 0
        self.__app_dir = app_dir

        self.draw_pile = LinkedList()
        self.discard_pile = LinkedList()

        self.shuffle_deck()

    def get_deck_json(self): # gets the initial deck from a JSON file in data
        initial_deck_dir = f"{self.__app_dir}/data/json/playing_cards.json" # absolute path to json

        with open(initial_deck_dir, "r") as f:
            initial_deck = json.loads(f.read())

        if not self.has_jokers: # if the deck doesn't have jokers...
            initial_deck.pop(4) # ...kill jokers from list

        self.deck_size = 0

        for suit in initial_deck:
            self.deck_size += len(suit["cards"])
        return initial_deck

    def shuffle_deck(self): # clears the draw and discard piles, takes initial deck and distributes them into draw pile
        self.draw_pile.clear()
        self.discard_pile.clear()

        self.deck = self.get_deck_json()

        while True:
            suit_num = random.randint(0, len(self.deck) - 1)
            card_num = random.randint(0, len(self.deck[suit_num]["cards"]) - 1)

            card = Card(self.deck[suit_num]["suit"],
                        self.deck[suit_num]["cards"][card_num]["name"],
                        self.deck[suit_num]["cards"][card_num]["value"])
            # take note of how dictionaries and lists access data - .cards is not valid for a dictionary
            self.draw_pile.enqueue(card)
            self.deck[suit_num]["cards"].pop(card_num)

            if len(self.deck[suit_num]["cards"]) == 0:
                self.deck.pop(suit_num)

            if len(self.deck) == 0:
                break

        print("Deck shuffled.")

    def draw_card(self, num_of_draws=1):
        drawn_cards = []

        for card_num in range(num_of_draws):
            drawn_card = self.draw_pile.dequeue()
            if drawn_card == False:
                self.shuffle_deck()
                drawn_card = self.draw_pile.dequeue()
            drawn_cards.append(drawn_card)
            self.discard_pile.enqueue(drawn_card)

            card_num += 1

        return drawn_cards

    def __str__(self):

        draw_pile = self.draw_pile.view().split(',')
        discard_pile = self.discard_pile.view().split(',')

        draw_str = "Draw Pile: \n"
        discard_str = "Discard Pile: \n"

        if draw_pile[0] == "":
            draw_str += "Empty."
        else:
            i = 0
            for card in range(len(draw_pile)):
                draw_str += draw_pile[card] + ", "
                i += 1
                if i == 10:
                    draw_str = draw_str.strip(' ')
                    draw_str += "\n"
                    i = 0
            draw_str.strip(', ')

        if discard_pile[0] == "":
            discard_str += "Empty."
        else:
            i = 0
            for card in range(len(discard_pile)):
                discard_str += discard_pile[card] + ", "
                i += 1
                if i == 10:
                    discard_str = discard_str.strip(' ')
                    discard_str += "\n"
                    i = 0
            discard_str.strip(', ')

        return f"{draw_str}\n{discard_str}"

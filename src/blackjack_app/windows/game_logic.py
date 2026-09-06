from blackjack_app.objects.cards.deck import Deck


class GameLogic: # handles most game logic
    def __init__(self, app_dir):
        self.app_dir = app_dir
        self.deck = Deck(self.app_dir)
        self.dealer_hand = [] # dealer or player cards
        self.player_hand = []
        self.dealer_score = 0 # dealer or player total score
        self.player_score = 0

    def resetGame(self):
        self.dealer_hand = []
        self.player_hand = []
        self.dealer_score = 0
        self.player_score = 0

    def cardDrawDealer(self):
        drawn_card = self.deck.draw_card()[0]

        drawn_card = self.checkDuplicateCard(drawn_card)
        drawn_card = self.setFaceCardValue(drawn_card)
        drawn_card = self.switchAceCardTo11(drawn_card)

        self.dealer_hand.append(drawn_card)

        self.dealer_score = self.calculateScore(self.dealer_hand)
        self.dealer_hand = self.checkForAbove21(self.dealer_hand, self.dealer_score)
        self.dealer_score = self.calculateScore(self.dealer_hand)

        return drawn_card

    def cardDrawPlayer(self):
        drawn_card = self.deck.draw_card()[0]

        drawn_card = self.checkDuplicateCard(drawn_card)
        drawn_card = self.setFaceCardValue(drawn_card)
        drawn_card = self.switchAceCardTo11(drawn_card)

        self.player_hand.append(drawn_card)

        self.player_score = self.calculateScore(self.player_hand)
        self.player_hand = self.checkForAbove21(self.player_hand, self.player_score)
        self.player_score = self.calculateScore(self.player_hand)

        return drawn_card

    def calculateScore(self, hand): # calculates score of a hand
        score = 0
        for card in hand:
            score += card.value
        return score

    def setFaceCardValue(self, card): # sets the value of jacks, queens, kings
        card.value = min(card.value, 10)
        return card

    def switchAceCardTo11(self, card): # sets the value of aces to 11. place after setFaceCardValue
        if card.value == 1:
            card.value = 11
        return card

    def switchAceCardTo1(self, card): # sets the value of aces to 1. only used in checkAbove21
        if card.value == 11:
            card.value = 1
        return card

    def checkDuplicateCard(self, drawn_card): # checks for duplicate cards. draws another card if dupe exists. place first.
        for card in self.dealer_hand:
            if card.suit == drawn_card.suit and card.name == drawn_card.name:
                return self.checkDuplicateCard(self.deck.draw_card()[0])

        for card in self.player_hand:
            if card.suit == drawn_card.suit and card.name == drawn_card.name:
                return self.checkDuplicateCard(self.deck.draw_card()[0])

        return drawn_card

    def checkForAbove21(self, hand, score): # checks values for score above 21 and changes aces in hand.
        for card_num in range(len(hand)):
            if score > 21:
                hand[card_num] = self.switchAceCardTo1(hand[card_num])

        return hand

    def checkForBust(self, score): # checks values for score above 21. returns true if bust, false if not
        return score > 21

    def checkForWinner(self):
        if self.dealer_score == self.player_score:
            return "Draw."
        elif self.dealer_score > self.player_score:
            return "Dealer Wins..."
        elif self.player_score == 21:
            return "Player Blackjack!!"
        else:
            return "Player Wins!"

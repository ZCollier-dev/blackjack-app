class Card:
    
    # suit - Spade, Heart, Diamond, Club
    # name - String
    # value - Integer value
    
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value
        self.visible = False
        
    def __str__(self):
        return f"{self.suit}|{self.name}"
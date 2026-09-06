# Blackjack App


A simple game of Blackjack using Python, with PySide6 - an alternative to PyQt5 - as the front-end medium. Uses uv, though it initially did not. Created to learn the process of working with PySide6.

The deck of cards is created using a JSON file containing all the cards. It first shuffles this initial deck into a queue data structure. As the program would need to access only the first data value when drawing/de-queueing a card while simultaneously shifting the rest of the deck further forward, a queue structure was a clear choice.

Then, it draws the initial cards. As cards are drawn, a series of checks are run, such as checking whether a card is a duplicate after a reshuffle to skip it, checking the given hand for values above 21 to change any aces to 1, and checking for busts.

Finally, it determines a winner, whether the player gets a Blackjack, or whether the game ends in a draw.

## Game Rules


At game start, the Player is dealt two cards face up. The Dealer is dealt one card face up, one card face down.

Players then have a choice: they can hit (draw a card) or stand (keep hand as is, Dealer starts drawing cards)

On Stand, Dealer draws cards when under a score of 17. When at or above a score of 17, the Dealer stands and a winner is determined.

The Winner is whoever gets above the other in score, without going above a score of 21. A score of 21 is a Blackjack, a perfect score. It can end in a draw if both the Player and Dealer get a score of 21. If anyone ever draws a gard and gets a score over 21, it is considered a bust and instantly loses.

Notes on scoring: Face cards (Jack, Queen, King) each contribute a score of 10 to the hand they're in. Aces can have a score of either 11 or 1, depending on whether or not an 11 would bring the hand's score above 21.

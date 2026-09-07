
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from blackjack_app.windows.game_logic import GameLogic


class MainWindow(QMainWindow):
    def __init__(self, app_dir) -> None:
        super().__init__()
        self.app_dir = app_dir
        self.logic = GameLogic(app_dir)

        self.icon = QPixmap(f"{self.app_dir}/data/images/cards/card_spades_A.png")

        self.setWindowTitle("BlackJack")
        self.setWindowIcon(self.icon)

        self.main_layout = QVBoxLayout()
        self.dealer_card_layout = QHBoxLayout()
        self.player_card_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()

        self.main_widget = QWidget()
        self.initUI()

        self.gameStart()

    def initUI(self) -> None:
        self.dealer_score_label = QLabel(f"Total: {self.logic.dealer_score}")
        self.player_score_label = QLabel(f"Total: {self.logic.player_score}")

        self.hit_button = QPushButton("Hit", self)
        self.stand_button = QPushButton("Stand", self)
        self.restart_button = QPushButton("Play Again", self)
        self.restart_button.setDisabled(True)
        self.result_label = QLabel("")

        self.main_layout.addWidget(QLabel("Dealer's Hand"))
        self.main_layout.addLayout(self.dealer_card_layout) # dealer cards here
        self.main_layout.addWidget(self.dealer_score_label)

        self.main_layout.addWidget(QLabel("Player's Hand"))
        self.main_layout.addLayout(self.player_card_layout) # player cards here
        self.main_layout.addWidget(self.player_score_label)

        self.main_layout.addWidget(self.result_label)

        self.button_layout.addWidget(self.hit_button)
        self.button_layout.addWidget(self.stand_button)
        self.button_layout.addWidget(self.restart_button)

        self.hit_button.clicked.connect(self.playerHit)
        self.stand_button.clicked.connect(self.playerStand)
        self.restart_button.clicked.connect(self.resetGame)

        self.main_layout.addLayout(self.button_layout)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        with open(f"{self.app_dir}/styles/styles.css", "r") as file:
            self.setStyleSheet(file.read())

    # functions to modify displayed hands, score
    # card_img_str = f"card_{suit}_{name}.png"
    def gameStart(self) -> None:
        self.hit_button.setDisabled(False)
        self.stand_button.setDisabled(False)
        self.restart_button.setDisabled(True)

        self.result_label.setText("Hit to draw a card, Stand to use your current hand.")

        self.logic.resetGame()

        self.addPlayerCard()
        self.addDealerCard()
        self.addPlayerCard()

        self.empty_card = QLabel()
        self.empty_card.setPixmap(
                QPixmap(f"{self.app_dir}/data/images/cards/card_back.png")
                )
        self.dealer_card_layout.addWidget(self.empty_card)

        self.updateDealerScore()
        self.updatePlayerScore()

        # print(self.logic.deck)

    def playerHit(self) -> None: # player draws a card
        self.addPlayerCard()
        self.updatePlayerScore()
        if self.logic.player_score == 21:
            self.playerStand()

    def playerStand(self) -> None: # dealer starts drawing cards until 17
        self.hit_button.setDisabled(True)
        self.stand_button.setDisabled(True)

        # properly removes the widget from the layout
        blank_card = self.dealer_card_layout.takeAt(1)
        if blank_card is not None:
            blank_card_widget = blank_card.widget()
            if blank_card_widget is not None:
                blank_card_widget.deleteLater()

        while self.logic.dealer_score < 17:
            self.addDealerCard()
            self.updateDealerScore()

        if self.logic.dealer_score > 21:
            return
        else:
            self.result_label.setText(self.logic.checkForWinner())
            self.restart_button.setDisabled(False)

    def resetGame(self) -> None: # should delete all cards from ui
        for card_num_p in range(self.player_card_layout.count() - 1, -1, -1):
            card = self.player_card_layout.takeAt(card_num_p)
            if card is not None:
                card_widget = card.widget()
                if card_widget is not None:
                    card_widget.deleteLater()


        for card_num_d in range(self.dealer_card_layout.count() - 1, -1, -1):
            card = self.dealer_card_layout.takeAt(card_num_d)
            if card is not None:
                card_widget = card.widget()
                if card_widget is not None:
                    card_widget.deleteLater()

        self.gameStart()

    def addDealerCard(self) -> None:
        drawn_card = self.logic.cardDrawDealer()
        drawn_card_widget = QLabel()
        drawn_card_widget.setPixmap(
            QPixmap(f"{self.app_dir}/data/images/cards/card_{drawn_card.suit}_{drawn_card.name}.png")
            )

        self.dealer_card_layout.addWidget(drawn_card_widget)

    def addPlayerCard(self) -> None:
        drawn_card = self.logic.cardDrawPlayer()
        drawn_card_widget = QLabel()
        drawn_card_widget.setPixmap(
            QPixmap(f"{self.app_dir}/data/images/cards/card_{drawn_card.suit}_{drawn_card.name}.png")
            )

        self.player_card_layout.addWidget(drawn_card_widget)

    def updateDealerScore(self) -> None:
        self.dealer_score_label.setText(f"Total: {self.logic.dealer_score}")

        if self.logic.checkForBust(self.logic.dealer_score):
            self.result_label.setText("Dealer Bust! Player Wins!")
            self.restart_button.setDisabled(False)

    def updatePlayerScore(self) -> None:
        self.player_score_label.setText(f"Total: {self.logic.player_score}")

        if self.logic.checkForBust(self.logic.player_score):
            self.result_label.setText("Player Bust! Dealer Wins!")
            self.hit_button.setDisabled(True)
            self.stand_button.setDisabled(True)
            self.restart_button.setDisabled(False)

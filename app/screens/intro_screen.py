from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from app.widgets import CenterCard


class IntroScreen(QWidget):
    def __init__(self, title_text: str, body_text: str, button_text: str = "Dalej"):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = CenterCard()
        card_layout = QVBoxLayout(card)

        title = QLabel(title_text)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        body = QLabel(body_text)
        body.setObjectName("body")
        body.setAlignment(Qt.AlignCenter)
        body.setWordWrap(True)

        #przycisk akcji
        self.button = QPushButton(button_text)

        card_layout.addWidget(title)
        card_layout.addWidget(body)
        card_layout.addWidget(self.button)

        layout.addWidget(card)

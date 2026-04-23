from typing import List
from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from app.models import TestSummary
from app.screens.intro_screen import IntroScreen
from app.screens.results_screen import ResultsScreen
from app.screens.test_runner_screen import TestRunnerScreen


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test sprawności psychomotorycznej dla kierowców")
        self.resize(1000, 750)

        self.all_summaries: List[TestSummary] = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.runner = TestRunnerScreen()
        self.runner.main_window = self
        self.results_screen = ResultsScreen()

        self.make_screens()
        self.add_screens()
        self.connect_buttons()

        self.stack.setCurrentWidget(self.screen_welcome)

    def make_screens(self):
        self.screen_welcome = IntroScreen(
            "Test sprawności psychomotorycznej\n"
            "Łukasz Mroczek 198146, Łukasz Orluk 197641",
            "Aplikacja bada prosty i złożony czas reakcji na bodźce optyczne oraz akustyczne.\n\n"
            "Każdy test składa się z opisu, fazy treningowej oraz testu właściwego."
        )

        self.screen_visual_info = IntroScreen(
            "Test 1, prosty czas reakcji optycznej",
            "Po losowym czasie na ekranie pojawi się zielony kolor. "
            "Twoim zadaniem jest jak najszybciej nacisnąć SPACJĘ albo przycisk REAKCJA.\n\n"
            "Nie reaguj przed pojawieniem się zielonego koloru."
        )

        self.screen_audio_info = IntroScreen(
            "Test 2, prosty czas reakcji akustycznej",
            "Po losowym czasie usłyszysz sygnał dźwiękowy. "
            "Twoim zadaniem jest jak najszybciej nacisnąć SPACJĘ albo przycisk REAKCJA.\n\n"
            "Nie reaguj przed sygnałem."
        )

        self.screen_choice_info = IntroScreen(
            "Test 3, złożony czas reakcji optycznej",
            "Po losowym czasie pojawi się strzałka:\n"
            "• dla ← naciśnij klawisz L,\n"
            "• dla → naciśnij klawisz P.\n\n"
            "Jeżeli zareagujesz za wcześnie albo naciśniesz zły klawisz, próba będzie błędna."
        )

    def add_screens(self):
        self.stack.addWidget(self.screen_welcome)
        self.stack.addWidget(self.screen_visual_info)
        self.stack.addWidget(self.screen_audio_info)
        self.stack.addWidget(self.screen_choice_info)
        self.stack.addWidget(self.runner)
        self.stack.addWidget(self.results_screen)

    def connect_buttons(self):

        self.screen_welcome.button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.screen_visual_info)
        )
        
        self.screen_visual_info.button.clicked.connect(self.start_visual_test)
        self.screen_audio_info.button.clicked.connect(self.start_audio_test)
        self.screen_choice_info.button.clicked.connect(self.start_choice_test)

    def start_visual_test(self):
        self.runner.configure(
            "Test 1, prosty czas reakcji optycznej",
            "Naciśnij SPACJĘ lub przycisk, gdy zobaczysz zielony kolor.",
            "simple_visual"
        )
        self.stack.setCurrentWidget(self.runner)

    def start_audio_test(self):
        self.runner.configure(
            "Test 2, prosty czas reakcji akustycznej",
            "Naciśnij SPACJĘ lub przycisk, gdy usłyszysz sygnał dźwiękowy.",
            "simple_audio"
        )
        self.stack.setCurrentWidget(self.runner)

    def start_choice_test(self):
        self.runner.configure(
            "Test 3, złożony czas reakcji optycznej",
            "Dla lewej strzałki naciśnij L, a dla prawej P.",
            "choice_visual"
        )
        self.stack.setCurrentWidget(self.runner)

    def go_next_after_test(self):
        last_name = self.all_summaries[-1].name

        if "Test 1" in last_name:
            self.stack.setCurrentWidget(self.screen_audio_info)
        elif "Test 2" in last_name:
            self.stack.setCurrentWidget(self.screen_choice_info)
        else:
            self.results_screen.set_data(self.all_summaries)
            self.stack.setCurrentWidget(self.results_screen)
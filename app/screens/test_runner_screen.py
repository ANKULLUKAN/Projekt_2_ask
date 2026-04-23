import time
from typing import List

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models import TestSummary, TrialResult
from app.test_logic import random_delay_ms, reaction_time_ms, configure_single_shot_timer


#screeny testow

class TestRunnerScreen(QWidget):

    def __init__(self, parent=None):
        #stworzenie widgetu
        super().__init__(parent)

        self.main_window = None

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        #tytuł testu
        self.title = QLabel("")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        #instrukcje do testu
        self.instruction = QLabel("")
        self.instruction.setObjectName("subtitle")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setWordWrap(True)

        #pasek postępu
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(1)
        self.progress.setValue(0)

        #bodziec
        self.stimulus_label = QLabel("Czekaj na bodziec...")
        self.stimulus_label.setAlignment(Qt.AlignCenter)
        self.stimulus_label.setMinimumHeight(220)
        self.stimulus_label.setObjectName("stimulus")

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)

        self.start_btn = QPushButton("Rozpocznij")
        self.start_btn.clicked.connect(self.start_session)

        self.response_btn = QPushButton("REAKCJA / SPACJA")
        self.response_btn.setMinimumHeight(55)
        self.response_btn.clicked.connect(self.on_space_response)

        button_row = QHBoxLayout()
        button_row.addWidget(self.start_btn)
        button_row.addWidget(self.response_btn)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.instruction)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.stimulus_label)
        self.layout.addWidget(self.info_label)
        self.layout.addLayout(button_row)

        self.phase = "idle"
        self.test_type = ""
        self.is_training = True
        self.training_trials = 3
        self.real_trials = 5
        self.current_trial = 0

        self.results_training: List[TrialResult] = []
        self.results_real: List[TrialResult] = []

        self.waiting_for_stimulus = False
        self.active_stimulus = False
        self.stimulus_start_time = 0.0
        self.current_expected = ""
        self.current_stimulus_type = ""

        self.delay_timer = configure_single_shot_timer(self, self.show_stimulus)
        self.timeout_timer = configure_single_shot_timer(self, self.on_missed_trial)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:

            self.on_space_response()

        elif self.test_type == "choice_visual" and event.key() in (Qt.Key_L, Qt.Key_P):

            self.on_choice_response("LEFT" if event.key() == Qt.Key_L else "RIGHT")
            
        else:
            super().keyPressEvent(event)

    

    def configure(self, title: str, instruction: str, test_type: str):
        self.title.setText(title)
        self.instruction.setText(instruction)
        self.test_type = test_type

        self.phase = "idle"
        self.current_trial = 0
        self.results_training = []
        self.results_real = []

        self.progress.setMaximum(self.training_trials + self.real_trials)
        self.progress.setValue(0)

        self.stimulus_label.setText("Kliknij „Rozpocznij”, aby przejść do fazy treningowej.")
        self.stimulus_label.setStyleSheet("")
        self.info_label.setText(
            "Faza treningowa nie jest oceniana. "
            "Po niej automatycznie rozpocznie się test właściwy."
        )

        self.start_btn.show()
        self.response_btn.show()
        self.setFocus()

    def start_session(self):
        self.start_btn.hide()
        self.is_training = True
        self.phase = "running"
        self.current_trial = 0
        self.info_label.setText("Trening rozpoczęty.")
        self.next_trial()

    def next_trial(self):

        self.progress.setValue(len(self.results_training) + len(self.results_real))

        if self.is_training and self.current_trial >= self.training_trials:

            self.is_training = False
            self.current_trial = 0

            QMessageBox.information(
                self,
                "Koniec treningu",
                "Faza treningowa zakończona. Teraz rozpocznie się test właściwy.",
            )

        if (not self.is_training) and self.current_trial >= self.real_trials:
            self.finish_test()
            return

        self.active_stimulus = False
        self.waiting_for_stimulus = True
        self.current_expected = ""
        self.current_stimulus_type = ""

        self.stimulus_label.setText("Przygotuj się... czekaj na bodziec.")
        self.stimulus_label.setStyleSheet("")
        self.info_label.setText("Zbyt wczesna reakcja będzie liczona jako błąd.")

        self.delay_timer.start(random_delay_ms())

    def show_stimulus(self):

        self.waiting_for_stimulus = False
        self.active_stimulus = True
        self.stimulus_start_time = time.perf_counter()

        if self.test_type == "simple_visual":
            self.show_visual_stimulus()
        elif self.test_type == "simple_audio":
            self.show_audio_stimulus()
        elif self.test_type == "choice_visual":
            self.show_choice_stimulus()

        self.timeout_timer.start(2000)

    def show_visual_stimulus(self):

        self.current_stimulus_type = "zielone światło"
        self.current_expected = "SPACE"
        self.stimulus_label.setText("KLIKNIJ TERAZ!")

        self.stimulus_label.setStyleSheet(
            "background-color: #2ecc71; color: white; border-radius: 12px;"
        )

    def show_audio_stimulus(self):
        self.current_stimulus_type = "dźwięk"
        self.current_expected = "SPACE"
        QApplication.beep()
        self.stimulus_label.setText("Usłyszałeś sygnał — reaguj!")
        self.stimulus_label.setStyleSheet(
            "background-color: #3498db; color: white; border-radius: 12px;"
        )


    def show_choice_stimulus(self):
        self.current_expected = "LEFT" if __import__("random").choice([True, False]) else "RIGHT"
        self.current_stimulus_type = f"strzałka {self.current_expected}"

        if self.current_expected == "LEFT":
            self.stimulus_label.setText("←   NACIŚNIJ L")
        else:
            self.stimulus_label.setText("→   NACIŚNIJ P")

        self.stimulus_label.setStyleSheet(
            "background-color: #f39c12; color: black; border-radius: 12px;"
        )
        self.info_label.setText("Reakcja złożona: L dla lewej, P dla prawej.")


    def register_result(self, result: TrialResult):
        if self.is_training:
            self.results_training.append(result)
        else:
            self.results_real.append(result)

        self.current_trial += 1
        self.progress.setValue(len(self.results_training) + len(self.results_real))
        QTimer.singleShot(900, self.next_trial)

    def too_early_result(self):
        result = TrialResult(
            stimulus_type="brak bodźca",
            correct=False,
            too_early=True,
            expected_response="czekaj",
            actual_response="za wcześnie",
        )

        self.stimulus_label.setText("Za wcześnie!")
        self.stimulus_label.setStyleSheet(
            "background-color: #e74c3c; color: white; border-radius: 12px;"
        )
        self.info_label.setText("To jest błąd przedwczesnej reakcji.")
        self.register_result(result)

    def on_missed_trial(self):
        if not self.active_stimulus:
            return

        self.active_stimulus = False

        result = TrialResult(
            stimulus_type=self.current_stimulus_type,
            correct=False,
            missed=True,
            expected_response=self.current_expected,
            actual_response="brak reakcji",
        )

        self.stimulus_label.setText("Brak reakcji")
        self.stimulus_label.setStyleSheet(
            "background-color: #7f8c8d; color: white; border-radius: 12px;"
        )
        self.info_label.setText("Próba niezaliczona.")
        self.register_result(result)

    def on_space_response(self):
        if self.test_type == "choice_visual":
            self.on_choice_response("SPACE")
            return

        if self.waiting_for_stimulus:
            self.delay_timer.stop()
            self.too_early_result()
            return

        if not self.active_stimulus:
            return

        self.timeout_timer.stop()
        self.active_stimulus = False

        rt_ms = reaction_time_ms(self.stimulus_start_time)

        result = TrialResult(
            stimulus_type=self.current_stimulus_type,
            reaction_time_ms=rt_ms,
            correct=True,
            expected_response="SPACE",
            actual_response="SPACE",
        )

        self.stimulus_label.setText(f"Dobrze! {rt_ms:.1f} ms")
        self.stimulus_label.setStyleSheet(
            "background-color: #16a085; color: white; border-radius: 12px;"
        )
        self.info_label.setText("Poprawna reakcja.")
        self.register_result(result)

    def on_choice_response(self, key_name: str):
        if self.test_type != "choice_visual":
            return

        if self.waiting_for_stimulus:
            self.delay_timer.stop()
            self.too_early_result()
            return

        if not self.active_stimulus:
            return

        self.timeout_timer.stop()
        self.active_stimulus = False

        rt_ms = reaction_time_ms(self.stimulus_start_time)
        correct = key_name == self.current_expected

        result = TrialResult(
            stimulus_type=self.current_stimulus_type,
            reaction_time_ms=rt_ms if correct else None,
            correct=correct,
            expected_response=self.current_expected,
            actual_response=key_name,
        )

        if correct:
            self.stimulus_label.setText(f"Poprawnie! {rt_ms:.1f} ms")
            self.stimulus_label.setStyleSheet(
                "background-color: #16a085; color: white; border-radius: 12px;"
            )
            self.info_label.setText("Poprawna odpowiedź.")
        else:
            self.stimulus_label.setText("Błędny klawisz")
            self.stimulus_label.setStyleSheet(
                "background-color: #c0392b; color: white; border-radius: 12px;"
            )
            self.info_label.setText(
                f"Oczekiwano: {self.current_expected}, otrzymano: {key_name}."
            )

        self.register_result(result)

    def finish_test(self):
        names = {
            "simple_visual": "Test 1, prosty czas reakcji optycznej",
            "simple_audio": "Test 2, prosty czas reakcji akustycznej",
            "choice_visual": "Test 3, złożony czas reakcji optycznej",
        }

        summary = TestSummary(
            name=names[self.test_type],
            training_results=self.results_training.copy(),
            real_results=self.results_real.copy(),
        )

        self.main_window.all_summaries.append(summary)
        self.main_window.go_next_after_test()

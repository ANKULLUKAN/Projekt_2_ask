import random
import time

from PyQt5.QtCore import QTimer


def random_delay_ms() -> int:
    return random.randint(1500, 4000)


def reaction_time_ms(start_time: float) -> float:
    return (time.perf_counter() - start_time) * 1000.0


def configure_single_shot_timer(parent, callback):
    timer = QTimer(parent)
    timer.setSingleShot(True)
    timer.timeout.connect(callback)
    return timer

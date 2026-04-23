import random
import time

from PyQt5.QtCore import QTimer

#losowo ustawiamy czas w ktorym pokaze ise bodziec
def random_delay_ms():
    return random.randint(1000, 4000)

#liczenie reakcji wms
def reaction_time_ms(start_time: float):
    return (time.perf_counter() - start_time) * 1000.0

#ustawiamy timer
def configure_single_shot_timer(parent, callback):

    timer = QTimer(parent)
    timer.setSingleShot(True)
    timer.timeout.connect(callback)
    return timer

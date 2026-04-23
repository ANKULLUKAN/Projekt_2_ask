from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFrame

#wykres z matplotlib ---> pyqt
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(7, 4), tight_layout=True)
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)

#ui
class CenterCard(QFrame):

    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.setMaximumWidth(900)

import statistics
from typing import List

from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from app.models import TestSummary
from app.widgets import MplCanvas


class ResultsScreen(QWidget):

    def __init__(self, parent=None):
        
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.title = QLabel("Wyniki końcowe")
        self.title.setObjectName("title")
        layout.addWidget(self.title)

        self.summary_label = QLabel("")
        self.summary_label.setWordWrap(True)
        self.summary_label.setObjectName("subtitle")
        layout.addWidget(self.summary_label)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Test",
            "Śr. [ms]",
            "Min [ms]",
            "Max [ms]",
            "Mediana [ms]",
            "Odch. std. [ms]",
            "Błędy",
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.canvas = MplCanvas()
        layout.addWidget(self.canvas)

        self.details = QLabel("")
        self.details.setWordWrap(True)
        layout.addWidget(self.details)



    def set_data(self, summaries: List[TestSummary]):
        self.table.setRowCount(len(summaries))

        global_valid_times = []
        global_errors = 0
        names = []
        avgs = []

        for row, summary in enumerate(summaries):
            stats_data = summary.stats()
            errors = summary.total_errors()

            global_valid_times.extend(summary.valid_times())
            global_errors += errors

            names.append(summary.name)
            avgs.append(stats_data["avg"])

            values = [
                summary.name,
                f"{stats_data['avg']:.1f}",
                f"{stats_data['min']:.1f}",
                f"{stats_data['max']:.1f}",
                f"{stats_data['median']:.1f}",
                f"{stats_data['std']:.1f}",
                str(errors),
            ]

            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()

        if global_valid_times:
            global_avg = statistics.mean(global_valid_times)
            best = min(global_valid_times)
            worst = max(global_valid_times)
        else:
            global_avg = best = worst = 0.0

        self.summary_label.setText(
            "Wyniki syntetyczne:\n"
            f"• Łączny średni czas reakcji: {global_avg:.1f} ms\n"
            f"• Najlepszy wynik: {best:.1f} ms\n"
            f"• Najsłabszy wynik: {worst:.1f} ms\n"
            f"• Łączna liczba błędów: {global_errors}"
        )

        self.canvas.ax.clear()
        self.canvas.ax.bar(names, avgs)
        self.canvas.ax.set_title("Średni czas reakcji w poszczególnych testach")
        self.canvas.ax.set_ylabel("Czas [ms]")
        self.canvas.draw()

        analytical_lines = []

        for summary in summaries:
            stats_data = summary.stats()
            analytical_lines.append(
                f"{summary.name}: średnia {stats_data['avg']:.1f} ms, "
                f"mediana {stats_data['median']:.1f} ms, "
                f"poprawnych prób {stats_data['count']}, błędy {summary.total_errors()}."
            )

        self.details.setText("Wyniki analityczne:\n" + "\n".join(analytical_lines))

STYLE = """
QMainWindow, QWidget {
    background-color: #f4f6f8;
    color: #1f2937;
    font-size: 15px;
}

QFrame#card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #d8dee4;
}

QLabel#title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 12px;
}

QLabel#subtitle {
    font-size: 17px;
    margin-bottom: 10px;
}

QLabel#body {
    font-size: 16px;
    line-height: 1.4;
    margin-bottom: 16px;
}

QLabel#stimulus {
    background: white;
    border: 2px dashed #9ca3af;
    border-radius: 12px;
    font-size: 32px;
    font-weight: 700;
    padding: 20px;
}

QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 15px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QProgressBar {
    background: #e5e7eb;
    border-radius: 8px;
    min-height: 18px;
    max-height: 18px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #22c55e;
    border-radius: 8px;
}

QTableWidget {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    gridline-color: #e5e7eb;
}
"""

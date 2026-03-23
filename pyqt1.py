import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SporcuKart(QFrame):
    def __init__(self, isim, takim, brans, enerji):
        super().__init__()

        self.setFixedSize(400, 460)
        self.setStyleSheet("""
            QFrame {
                background-color: #1D2836;
                border-radius: 15px;
                border: 2px solid #7EBBBF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 15, 30, 15)

        isim_label = QLabel(isim)
        isim_label.setFont(QFont("Times New Roman", 24, QFont.Bold))
        isim_label.setStyleSheet("color:#BA8877; border: none;")
        isim_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(isim_label)

        takim_label = QLabel(takim)
        takim_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        takim_label.setStyleSheet("color: #9CA3AF;")
        takim_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(takim_label)

        brans_label = QLabel(brans)
        brans_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        brans_label.setStyleSheet("color: #783E3E;")
        brans_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(brans_label)

        enerji_label = QLabel(f"Enerji: {enerji}")
        enerji_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        enerji_label.setStyleSheet("color: #9CA3AF;")
        enerji_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(enerji_label)
        enerji_bar = QProgressBar()
        enerji_bar.setMinimum(0)
        enerji_bar.setMaximum(100)
        enerji_bar.setValue(enerji)
        enerji_bar.setFixedHeight(20)
        enerji_bar.setTextVisible(False)

        if enerji > 70:
            renk = "#2EA043"
        elif enerji > 40:
            renk = "#F5E158"
        else:
            renk = "#DB0236"

        enerji_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #374151;
                border-radius: 10px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {renk};
                border-radius: 10px;
            }}
        """)
        layout.addWidget(enerji_bar)


app = QApplication(sys.argv)
pencere = QWidget()
pencere.setStyleSheet("background-color: #E0CAD4;")
pencere.setWindowTitle("Kart Testi")

layout = QHBoxLayout(pencere)
kart = SporcuKart("İlkin Aydın", "Galatasaray", "Voleybolcu", 30)
layout.addWidget(kart)

pencere.show()
sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QProgressBar, QScrollArea, QGridLayout,
    QComboBox, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


brans_renk = {
    "Futbol": {
        "background-color":       "#302430",
        "border":   "#3B82F6",
        "bar":      "#3B82F6",
        "isim":     "#FAFADC",
    },
    "Basketbol": {
        "background-color":       "#303F52",
        "border":   "#B8DFF2",
        "bar":      "#F59E0B",
        "isim":     "#F2F5B8",
    },
    "Voleybol": {
        "background-color":       "#66272F",
        "border":   "#9CD6D6",
        "bar":      "#10B981",
        "isim":     "#FADCE1",
    },
}

brans_nitelik = {
    "Futbol":    ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"],
    "Basketbol": ["İkilik",  "Üçlük", "Serbest Atış"],
    "Voleybol":  ["Servis",  "Blok", "Smaç"],
}


def dosya_oku(dosya_yolu="sporcular.txt"):
    sporcular = []
    try:
        with open(dosya_yolu, encoding="utf-8") as f:
            for karakter in f:
                sporcu = karakter.strip().split(",")
                if len(sporcu) != 9:
                    continue
                brans, ad, takim, ozellik1, ozellik2, ozellik3, dayaniklilik, max_enerji, ozel = sporcu
                sporcular.append({
                    "brans":       brans.strip(),
                    "ad":          ad.strip(),
                    "takim":       takim.strip(),
                    "ozellik1":    int(ozellik1),
                    "ozellik2":    int(ozellik2),
                    "ozellik3":    int(ozellik3),
                    "dayaniklilik": int(dayaniklilik),
                    "max_enerji":  int(max_enerji),
                    "ozel_yetenek": ozel.strip(),
                    "enerji":      int(max_enerji),
                })
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {dosya_yolu}")
    return sporcular

class SporcuKart(QFrame):
    def __init__(self, sporcu: dict):
        super().__init__()
        brans = sporcu["brans"]
        renk = brans_renk.get(brans, brans_renk["Futbol"])

        self.setFixedSize(210, 310)
        self.setStyleSheet(f"""
            QFrame {{
                background: {renk['background-color']};
                border_radius: 14px;
                border: 3px solid {renk['border']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        isim_lbl = QLabel(sporcu["ad"])
        isim_lbl.setFont(QFont("VT323 ", 11, QFont.Bold))
        isim_lbl.setStyleSheet(f"color: {renk['isim']}; border;")
        isim_lbl.setAlignment(Qt.AlignCenter)
        isim_lbl.setWordWrap(True)
        layout.addWidget(isim_lbl)

        takim_lbl = QLabel(sporcu["takim"])
        takim_lbl.setFont(QFont("Press Start 2P", 9, QFont.Bold))
        takim_lbl.setStyleSheet("color: #9CA3AF; border: none;")
        takim_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(takim_lbl)

        brans_lbl = QLabel(brans)
        brans_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
        brans_lbl.setStyleSheet("color: #A1B8D6; border:none;")
        layout.addWidget(brans_lbl)
        brans_lbl.setAlignment(Qt.AlignCenter)

        enerji = sporcu["enerji"]
        enerji_lbl = QLabel(f"Enerji  {enerji}")
        enerji_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
        enerji_lbl.setStyleSheet("color: #9CA3AF; border: none;")
        layout.addWidget(enerji_lbl)

        bar = QProgressBar()
        bar.setMinimum(0)
        bar.setMaximum(100)
        bar.setValue(enerji)
        bar.setFixedHeight(7)
        bar.setTextVisible(False)
        if enerji > 70:
            bar_renk = "#2EA043"
        elif enerji > 40:
            bar_renk = "#F5E158"
        else:
            bar_renk = "#DB0236"
        bar.setStyleSheet(f"""
            QProgressBar {{
                background_color: #374151;
                border_radius: 2px;
                border;
            }}
            QProgressBar::chunk {{
                backgorund_color: {bar_renk};
                border_radius: 4px;
            }}
        """)
        layout.addWidget(bar)

        nitelik_adlari = brans_nitelik.get(brans, ["Özellik 1", "Özellik 2", "Özellik 3"])
        degerler = [sporcu["ozellik1"], sporcu["ozellik2"], sporcu["ozellik3"]]

        for ad, deger in zip(nitelik_adlari, degerler):
            satir = QHBoxLayout()
            ad_lbl = QLabel(ad)
            ad_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
            ad_lbl.setStyleSheet("color: #9CA3AF; border: none;")

            deger_lbl = QLabel(str(deger))
            deger_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
            deger_lbl.setStyleSheet(f"color: #E5E7EB; border: none;")
            deger_lbl.setAlignment(Qt.AlignRight)

            satir.addWidget(ad_lbl)
            satir.addStretch()
            satir.addWidget(deger_lbl)
            layout.addLayout(satir)

        alt_satir = QHBoxLayout()

        day_lbl = QLabel(f"Dayanıklılık: {sporcu['dayaniklilik']}")
        day_lbl.setFont(QFont("Press Start 2P", 8))
        day_lbl.setStyleSheet("color: #6B7280; border: none;")
        alt_satir.addWidget(day_lbl)
        alt_satir.addStretch()


class AnaPencere(QWidget):
    def __init__(self, sporcular):
        super().__init__()
        self.tum_sporcular = sporcular
        self.setWindowTitle("Sporcu Kartları")
        self.setMinimumSize(900, 620)
        self.setStyleSheet("background_color: #0A0000 ")

        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(14)
        ust = QHBoxLayout()
        ust.addStretch()

        self.filtre = QComboBox()
        self.filtre.addItems(["Tümü", "Futbol", "Basketbol", "Voleybol"])
        self.filtre.setFixedHeight(32)
        self.filtre.setStyleSheet("""
            QComboBox {
                background_color: #1F2937;
                color: #D1D5DB;
                border: 3px solid #374151;
                border_radius: 8px;
                padding: 0 12px;
                font-size: 13px;
            }
            QComboBox::drop-down { cizgi: none; }
            QComboBox QAbstractItemView {
                background_color: #1F2937;
                color: #D1D5D
                selection-background-color: #374151;
            }
        """)
        self.filtre.currentTextChanged.connect(self.filtrele)
        ust.addWidget(self.filtre)
        ana_layout.addLayout(ust)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background_color: transparent; }")

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(4, 4, 4, 4)

        scroll.setWidget(self.grid_widget)
        ana_layout.addWidget(scroll)

        self.kartlari_goster(self.tum_sporcular)

    def kartlari_goster(self, sporcular):

        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sutun_sayisi = 4
        for i, sporcu in enumerate(sporcular):
            kart = SporcuKart(sporcu)
            self.grid_layout.addWidget(kart, i // sutun_sayisi, i % sutun_sayisi)

    def filtrele(self, secim):
        if secim == "Tümü":
            self.kartlari_goster(self.tum_sporcular)
        else:
            filtrelenmis = [s for s in self.tum_sporcular if s["brans"] == secim]
            self.kartlari_goster(filtrelenmis)

if __name__ == "__main__":
    sporcular = dosya_oku("sporcular.txt")
    if not sporcular:
        sporcular = [
            {"brans": "Futbol", "ad": "Barış Alper Yılmaz", "takim": "Galatasaray", "ozellik1": 78, "ozellik2": 88,
                "ozellik3": 83, "dayaniklilik": 100, "max_enerji": 100, "ozel_yetenek": "Özel", "enerji": 100},
            {"brans": "Basketbol", "ad": "Sertaç Şanlı", "takim": "Beşiktaş", "ozellik1": 89, "ozellik2": 78,
                "ozellik3": 84, "dayaniklilik": 91, "max_enerji": 87, "ozel_yetenek": "Özel", "enerji": 87},
            {"brans": "Voleybol", "ad": "İlkin Aydın", "takim": "Galatasaray", "ozellik1": 85, "ozellik2": 92,
                "ozellik3": 88, "dayaniklilik": 99, "max_enerji": 96, "ozel_yetenek": "Özel", "enerji": 30},
            ]
    app = QApplication(sys.argv)
    pencere = AnaPencere(sporcular)
    pencere.show()
    sys.exit(app.exec_())

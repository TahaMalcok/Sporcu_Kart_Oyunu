import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QProgressBar, QScrollArea, QGridLayout,
    QComboBox, QPushButton, QSizePolicy, QDialog,
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from oyun_motoru import (
    Oyun_Yoneticisi, Kullanici, Bilgisayar, dosya_okuma
)

brans_renk = {
    "Futbol": {
        "background-color": "#302430",
        "border": "#3B82F6",
        "bar": "#3B82F6",
        "isim": "#FAFADC",
    },
    "Basketbol": {
        "background-color": "#303F52",
        "border": "#B8DFF2",
        "bar": "#F59E0B",
        "isim": "#F2F5B8",
    },
    "Voleybol": {
        "background-color": "#66272F",
        "border": "#9CD6D6",
        "bar": "#10B981",
        "isim": "#FADCE1",
    },
}

brans_nitelik = {
    "Futbol": ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"],
    "Basketbol": ["İkilik", "Üçlük", "Serbest Atış"],
    "Voleybol": ["Servis", "Blok", "Smaç"],
}

class BilgisayarKartlariPenceresi(QDialog):
    def __init__(self, kart_listesi):
        super().__init__()
        self.setWindowTitle("Bilgisayar Kartları")
        self.showMaximized()
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color;")

        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)

        baslik = QLabel("Bilgisayar Kartları")
        baslik.setFont(QFont("Press Start 2P", 12, QFont.Bold))
        baslik.setStyleSheet("color: #1C1B1B; border: none;")
        baslik.setAlignment(Qt.AlignCenter)
        ana_layout.addWidget(baslik)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(16)
        grid_layout.setContentsMargins(4, 4, 4, 4)

        sporcular = self._objeleri_sozluge_cevir(kart_listesi)
        sutun_sayisi = 4
        for i, sporcu in enumerate(sporcular):
            kart = SporcuKart(sporcu)
            grid_layout.addWidget(kart, i // sutun_sayisi, i % sutun_sayisi)

        scroll.setWidget(grid_widget)
        ana_layout.addWidget(scroll)

    def _objeleri_sozluge_cevir(self, obje_listesi):
        sozluk_listesi = []
        for kart in obje_listesi:
            if kart.brans == "Futbol":
                ozellik1, ozellik2, ozellik3 = kart.penalti, kart.serbest_vurus, kart.kaleci_karsikarsiya
            elif kart.brans == "Basketbol":
                ozellik1, ozellik2, ozellik3 = kart.ikilik, kart.ucluk, kart.serbest_atis
            else:
                ozellik1, ozellik2, ozellik3 = kart.servis, kart.blok, kart.smac

            sozluk_listesi.append({
                "brans": kart.brans,
                "ad": kart.adi,
                "takim": kart.takim,
                "ozellik1": ozellik1,
                "ozellik2": ozellik2,
                "ozellik3": ozellik3,
                "dayaniklilik": kart.dayaniklilik,
                "max_enerji": kart.max_enerji,
                "ozel_yetenek": kart.ozel_yetenek,
                "enerji": kart.enerji,
                "gercek_obje": kart
            })
        return sozluk_listesi


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

        day_ad_lbl = QLabel("Dayanıklılık")
        day_ad_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
        day_ad_lbl.setStyleSheet("color: #9CA3AF; border: none;")

        day_deger_lbl = QLabel(str(sporcu["dayaniklilik"]))
        day_deger_lbl.setFont(QFont("Press Start 2P", 8, QFont.Bold))
        day_deger_lbl.setStyleSheet("color: #E5E7EB; border: none;")
        day_deger_lbl.setAlignment(Qt.AlignRight)

        alt_satir.addWidget(day_ad_lbl)
        alt_satir.addStretch()
        alt_satir.addWidget(day_deger_lbl)

        layout.addLayout(alt_satir)

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        print("Oyun Motoru Yükleniyor...")
        self.kart_destesi = dosya_okuma()
        self.yonetici = Oyun_Yoneticisi()
        self.yonetici.kart_dagitimi(self.kart_destesi)

        self.kullanici = Kullanici(1, "Kullanıcı", self.yonetici.kullanici_deste)
        self.bilgisayar = Bilgisayar(2, "Bilgisayar", self.yonetici.bilgisayar_deste)

        self.setWindowTitle("Sporcu Kartları")
        self.setMinimumSize(900, 620)
        self.setStyleSheet("background_color: #0A0000 ")

        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(14)
        ust = QHBoxLayout()
        ust.addStretch()

        self.bilgisayargoster = QPushButton("Bilgisayarın Kartlarını Gör")
        self.bilgisayargoster.setFixedHeight(32)
        self.bilgisayargoster.setStyleSheet("""
            QPushButton {
                background-color;
                color: #1C1B1B;
                border: 3px solid #374151;
                border-radius: 8px;
                padding: 0 12px;
                font-size: 13px;
            }
        """)
        self.bilgisayargoster.clicked.connect(self.bilgisayarpencere_ac)
        ust.addWidget(self.bilgisayargoster)

        self.filtre = QComboBox()
        self.filtre.addItems(["Tümü", "Futbol", "Basketbol", "Voleybol"])
        self.filtre.setFixedHeight(32)
        self.filtre.setStyleSheet("""
            QComboBox {
                background_color: #1F2937;
                color: #1C1B1B;
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

        self.tum_sporcular = self.objeleri_sozluge_cevir(self.kullanici.kart_listesi)
        self.kartlari_goster(self.tum_sporcular)

    def bilgisayarpencere_ac(self):
        pencere = BilgisayarKartlariPenceresi(self.bilgisayar.kart_listesi)
        pencere.exec_()

    def objeleri_sozluge_cevir(self, obje_listesi):
        sozluk_listesi = []
        for kart in obje_listesi:
            if kart.brans == "Futbol":
                ozellik1, ozellik2, ozellik3 = kart.penalti, kart.serbest_vurus, kart.kaleci_karsikarsiya
            elif kart.brans == "Basketbol":
                ozellik1, ozellik2, ozellik3 = kart.ikilik, kart.ucluk, kart.serbest_atis
            else:
                ozellik1, ozellik2, ozellik3 = kart.servis, kart.blok, kart.smac

            sporcu_sozluk = {
                "brans": kart.brans,
                "ad": kart.adi,
                "takim": kart.takim,
                "ozellik1": ozellik1,
                "ozellik2": ozellik2,
                "ozellik3": ozellik3,
                "dayaniklilik": kart.dayaniklilik,
                "max_enerji": kart.max_enerji,
                "ozel_yetenek": kart.ozel_yetenek,
                "enerji": kart.enerji,
                "gercek_obje": kart
            }
            sozluk_listesi.append(sporcu_sozluk)
        return sozluk_listesi

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
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())

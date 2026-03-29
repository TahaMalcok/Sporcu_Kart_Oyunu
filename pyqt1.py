import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QProgressBar, QScrollArea, QGridLayout,
    QComboBox, QPushButton, QSizePolicy, QDialog, QMessageBox
)
from PyQt5.QtGui import QFont
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
    def __init__(self, sporcu: dict, ana_pencere=None):
        super().__init__()
        self.sporcu = sporcu
        self.ana_pencere = ana_pencere

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
        isim_lbl.setFont(QFont("Press Start 2P", 11, QFont.Bold))
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
                background-color: #374151;
                border-radius: 2px;
                border;
            }}
            QProgressBar::chunk {{
                background-color: {bar_renk};
                border-radius: 4px;
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

    def mousePressEvent(self, event):
        if self.ana_pencere is not None:
            self.ana_pencere.kart_secildi(self.sporcu)

class BaslangicEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oyun Başlat")
        self.setFixedSize(400, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #4C5775;
            }
            QPushButton {
                background-color: #374151;
                color: white;
                border-radius: 2px;
                padding: 2px;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        self.label = QLabel("Oyuna Hoş Geldin!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Press Start 2P", 15, QFont.Bold))
        self.label.setStyleSheet("color;")

        self.baslat_buton = QPushButton("Oyunu Başlat")
        self.baslat_buton.setFixedHeight(40)

        self.zorluk_secim = QComboBox()
        self.zorluk_secim.addItems(["Kolay", "Orta"])
        self.zorluk_secim.setFixedHeight(35)

        self.baslat_buton.clicked.connect(self.oyunu_baslat)

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(20)
        layout.addWidget(self.zorluk_secim)
        layout.addWidget(self.baslat_buton)
        layout.addStretch()

    def oyunu_baslat(self):
        secilen_zorluk = self.zorluk_secim.currentText()
        self.ana_pencere = AnaPencere(secilen_zorluk)
        self.ana_pencere.show()
        self.close()

class AnaPencere(QWidget):
    def __init__(self, zorluk="Kolay"):
        super().__init__()
        self.zorluk = zorluk
        self.secili_kart = None
        self.tur_sayaci = 0
        self.guncel_brans = None
        self.guncel_nitelik = None

        print("Oyun Motoru Yükleniyor...")
        self.kart_destesi = dosya_okuma()
        self.yonetici = Oyun_Yoneticisi()
        self.yonetici.kart_dagitimi(self.kart_destesi)

        self.kullanici = Kullanici(1, "Kullanıcı", self.yonetici.kullanici_deste)
        self.bilgisayar = Bilgisayar(2, "Bilgisayar", self.yonetici.bilgisayar_deste)

        self.setWindowTitle("Sporcu Kartları")
        self.setMinimumSize(900, 620)
        self.setStyleSheet("background-color: white ")

        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(14)

        skorbord_layout = QHBoxLayout()

        self.kullanici_skor_lbl = QLabel(f"Kullanıcı Skor: {self.kullanici.skor}")
        self.kullanici_skor_lbl.setFont(QFont("Press Start 2P", 12, QFont.Bold))
        self.kullanici_skor_lbl.setStyleSheet("color: #4A324A;")

        self.bilgisayar_skor_lbl = QLabel(f"Bilgisayar Skor: {self.bilgisayar.skor}")
        self.bilgisayar_skor_lbl.setFont(QFont("Press Start 2P", 12, QFont.Bold))
        self.bilgisayar_skor_lbl.setStyleSheet("color: #8A1D32;")

        skorbord_layout.addWidget(self.kullanici_skor_lbl)
        skorbord_layout.addStretch()
        skorbord_layout.addWidget(self.bilgisayar_skor_lbl)

        ana_layout.addLayout(skorbord_layout)
        ust = QHBoxLayout()
        ust.addStretch()

        bilgi_cerceve = QFrame()
        bilgi_cerceve.setStyleSheet("""
        QFrame {
            background-color: #1A1F2E;
            border: 2px solid #374151;
            border-radius: 2px;
        }
    """)
        bilgi_layout = QHBoxLayout(bilgi_cerceve)
        bilgi_layout.setContentsMargins(16, 10, 16, 10)
        bilgi_layout.setSpacing(30)

        self.tur_lbl = QLabel("Tur:")
        self.tur_lbl.setFont(QFont("Press Start 2P", 10, QFont.Bold))
        self.tur_lbl.setStyleSheet("color: white ; border: none;")

        self.brans_lbl = QLabel("Branş:")
        self.brans_lbl.setFont(QFont("Press Start 2P", 10, QFont.Bold))
        self.brans_lbl.setStyleSheet("color: white ; border: none;")

        self.nitelik_lbl = QLabel("Nitelik:")
        self.nitelik_lbl.setFont(QFont("Press Start 2P", 10, QFont.Bold))
        self.nitelik_lbl.setStyleSheet("color: white ; border: none;")

        self.secim_lbl = QLabel("Kart seçilmedi")
        self.secim_lbl.setFont(QFont("Press Start 2P", 9, QFont.Bold))
        self.secim_lbl.setStyleSheet("color: #F87171; border: none;")
        self.secim_lbl.setAlignment(Qt.AlignRight)

        bilgi_layout.addWidget(self.tur_lbl)
        bilgi_layout.addWidget(self.brans_lbl)
        bilgi_layout.addWidget(self.nitelik_lbl)
        bilgi_layout.addStretch()
        bilgi_layout.addWidget(self.secim_lbl)

        ana_layout.addWidget(bilgi_cerceve)

        ust = QHBoxLayout()
        ust.addStretch()

        self.bilgisayargoster = QPushButton("Bilgisayarın Kartlarını Gör")
        self.bilgisayargoster.setFixedHeight(32)
        self.bilgisayargoster.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1C1B1B;
                border: 3px solid #374151;
                border-radius: 2px;
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
                background-color: white;
                color: black;
                border: 3px solid #374151;
                border-radius: 2px;
                padding: 0 12px;
                font-size: 13px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #374151;
            }
        """)
        self.filtre.currentTextChanged.connect(self.filtrele)
        ust.addWidget(self.filtre)
        ana_layout.addLayout(ust)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(4, 4, 4, 4)

        scroll.setWidget(self.grid_widget)
        ana_layout.addWidget(scroll)

        self.tum_sporcular = self.objeleri_sozluge_cevir(self.kullanici.kart_listesi)
        self.kartlari_goster(self.tum_sporcular)

        self.tur_buton = QPushButton("Oyna!")
        self.tur_buton.setFont(QFont("Press Start 2P", 15, QFont.Bold))
        self.tur_buton.setStyleSheet("color: #72CC6A;")
        self.tur_buton.setFixedHeight(40)
        self.tur_buton.clicked.connect(self.tur_oyna)
        ana_layout.addWidget(self.tur_buton, 0)
        self.yeni_tur_baslat()

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
            kart = SporcuKart(sporcu, ana_pencere=self)
            self.grid_layout.addWidget(kart, i // sutun_sayisi, i % sutun_sayisi)

    def filtrele(self, secim):
        if secim == "Tümü":
            self.kartlari_goster(self.tum_sporcular)
        else:
            filtrelenmis = [s for s in self.tum_sporcular if s["brans"] == secim]
            self.kartlari_goster(filtrelenmis)

    def kart_secildi(self, sporcu):
        self.secili_kart = sporcu["gercek_obje"]
        self.secim_lbl.setText(f" {self.secili_kart.adi}")
        self.secim_lbl.setStyleSheet("color: #F87171; border: none;")

    def _bilgi_paneli_guncelle(self, tur_bitti=False):
        if tur_bitti:
            self.tur_lbl.setText(f"Tur: {self.tur_sayaci} ✓")
        else:
            self.tur_lbl.setText(f"Tur: {self.tur_sayaci + 1}")

        if tur_bitti:
            self.secim_lbl.setText("Kartını Seç 'Oyna!'ya bas")
            self.secim_lbl.setStyleSheet("color: #F87171; border: none;")

    def skorlari_guncelle(self):
        self.kullanici_skor_lbl.setText(f"Kullanıcı Skor: {self.kullanici.skor}")
        self.bilgisayar_skor_lbl.setText(f"Bilgisayar Skor: {self.bilgisayar.skor}")
        self.tum_sporcular = self.objeleri_sozluge_cevir(self.kullanici.kart_listesi)
        self.kartlari_goster(self.tum_sporcular)

    def tur_oyna(self):
        if self.secili_kart is None:
            self.secim_lbl.setText("Kart seç!")
            return

        kullanici_sec_kart = self.secili_kart

        if kullanici_sec_kart.brans != self.guncel_brans:
            self.secim_lbl.setText(f"Yanlış branş! {self.guncel_brans} seç!")
            return

        if kullanici_sec_kart.enerji <= 0:
            self.secim_lbl.setText("Bu kartın enerjisi bitmiş!")
            return

        bilgisayar_sec_kart = self.bilgisayar.kart_sec(self.zorluk, self.guncel_brans, self.guncel_nitelik)

        eski_kullanici_skor = self.kullanici.skor
        eski_bilgisayar_skor = self.bilgisayar.skor

        self.yonetici.tur(
            self.guncel_brans,
            self.guncel_nitelik,
            self.kullanici,
            self.bilgisayar,
            kullanici_sec_kart,
            bilgisayar_sec_kart
        )

        kullanici_puan = getattr(kullanici_sec_kart, self.guncel_nitelik)
        bilgisayar_puan = getattr(bilgisayar_sec_kart, self.guncel_nitelik) if bilgisayar_sec_kart else 0
        bilgisayar_ad = bilgisayar_sec_kart.adi if bilgisayar_sec_kart else "Kart Yok"

        if self.kullanici.skor > eski_kullanici_skor:
            kazanan = "Tebrikler! Turu sen kazandın!"
        elif self.bilgisayar.skor > eski_bilgisayar_skor:
            kazanan = "Turu bilgisayar kazandı!"
        else:
            kazanan = "Tur berabere bitti."

        mesaj = f"Karşılaştırılan Nitelik: {self.guncel_nitelik.lower()}\n\n"
        mesaj += f"Kartın: {kullanici_sec_kart.adi} -> {kullanici_puan}\n"
        mesaj += f"Bilgisayar:   {bilgisayar_ad} -> {bilgisayar_puan}\n\n"
        mesaj += f"SONUÇ: {kazanan}"

        mesaj_kutusu = QMessageBox(self)
        mesaj_kutusu.setWindowTitle("Tur Sonucu")
        mesaj_kutusu.setText(mesaj)
        mesaj_kutusu.setFont(QFont("Press Start 2P", 12, QFont.Bold))
        mesaj_kutusu.setStyleSheet("""
            QLabel {
                color: black;
                min-width: 500px;
                min-height: 250px;
            }
        """)
        mesaj_kutusu.setStandardButtons(QMessageBox.Ok)
        mesaj_kutusu.exec_()

        self._bilgi_paneli_guncelle(tur_bitti=True)
        self.tur_sayaci += 1
        self.secili_kart = None
        self.arayuzu_guncelle()

        bitti_mi, sonuc_durumu, kullanici_skor, bilgisayar_skor = self.yonetici.oyun_bitti_mi(self.kullanici, self.bilgisayar)
        if bitti_mi:
            self.oyunu_bitir(sonuc_durumu, kullanici_skor, bilgisayar_skor)
            return

        self.yeni_tur_baslat()

    def yeni_tur_baslat(self):
        self.guncel_brans = self.yonetici.brans_secme()
        self.guncel_nitelik = self.yonetici.nitelik_secme(self.guncel_brans)

        self.brans_lbl.setText(f"Branş: {self.guncel_brans}")
        self.nitelik_lbl.setText(f"Nitelik: {self.guncel_nitelik}")
        self.tur_lbl.setText(f"Tur: {self.tur_sayaci + 1}")
        self.secim_lbl.setText("Kart seç!")

    def arayuzu_guncelle(self):
        self.kullanici_skor_lbl.setText(f"Kullanıcı Skor: {self.kullanici.skor}")
        self.bilgisayar_skor_lbl.setText(f"Bilgisayar Skor: {self.bilgisayar.skor}")
        self.tum_sporcular = self.objeleri_sozluge_cevir(self.kullanici.kart_listesi)
        self.kartlari_goster(self.tum_sporcular)
        self.filtrele(self.filtre.currentText())

    def oyunu_bitir(self, sonuc_durumu, k_skor, b_skor):
        if sonuc_durumu == "Kullanıcı Kazandı!":
            mesaj = f"TEBRİKLER KULLANICI KAZANDI!\nKullanıcı skoru: {k_skor}\nBilgisayar skoru: {b_skor}"
        elif sonuc_durumu == "Bilgisayar Kazandı!":
            mesaj = f"OYUNU BİLGİSAYAR KAZANDI!\nKullanıcı skoru: {k_skor}\nBilgisayar skoru: {b_skor}"
        else:
            mesaj = f"BERABERE!\nKullanıcı skoru: {k_skor}\nBilgisayar skoru: {b_skor}"

        kutu = QMessageBox(self)
        kutu.setWindowTitle("MAÇ SONUCU:")
        kutu.setText(mesaj)
        kutu.setStyleSheet("background-color: #1A1F2E; color: white; font-size: 14px; font-weight: bold;")
        kutu.exec_()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    baslangic = BaslangicEkrani()
    baslangic.show()
    sys.exit(app.exec_())

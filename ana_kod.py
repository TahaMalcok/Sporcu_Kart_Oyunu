from abc import ABC, abstractmethod
from random import randint, random


class Sporcu(ABC):
    def __init__(self, sporcu_id, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek):
        self.sporcu_id = sporcu_id
        self.adi = adi
        self.takim = takim
        self.brans = brans
        self.dayanaklilik = dayaniklilik
        self.enerji = max_enerji
        self.max_enerji = max_enerji
        self.seviye = 1
        self.deneyim_puani = 0
        self.ozel_yetenek = ozel_yetenek
        self.kullanim_sayisi = 0
        self.kazanma_sayisi = 0
        self.kaybetme_sayisi = 0
        self.deneyim = 0

    @abstractmethod
    def sporcu_puani_goster(self):
        pass

    def performans_hesapla(self, secilen_ozellik, ozel_yetenek_bonusu, moral):
        if self.enerji > 70:
            enerji_cezasi = 0
        elif 40 <= self.enerji <= 70:
            enerji_cezasi = -(secilen_ozellik/100) * 10
        elif 0 < self.enerji < 40:
            enerji_cezasi = -(secilen_ozellik/100) * 20

        if moral >= 80:
            moral_bonus = 10
        elif 80 > moral >= 50:
            moral_bonus = 5
        elif 50 > moral:
            moral_bonus = -5

        match self.seviye:
            case 1:
                seviye_bonus = 0
            case 2:
                seviye_bonus = 5
            case 3:
                seviye_bonus = 10

        guncel_ozellik_puani = secilen_ozellik + moral_bonus + ozel_yetenek_bonusu + int(enerji_cezasi) + seviye_bonus
        return guncel_ozellik_puani

    def kart_bilgisi_goster(self):
        print(f"Adı: {self.adi}, Takım: {self.takim}, Branş: {self.brans}, Dayanıklılık: {self.dayanaklilik}, Enerji: {self.enerji}, Özel Yetenek: {self.ozel_yetenek}")

    def enerji_guncelle(self, durum, ozel_yetenek_durum):
        match durum:
            case "Kazandı":
                self.enerji -= 5
            case "Kaybetti":
                self.enerji -=  10
            case "Beraber":
                self.enerji -= 3

        if ozel_yetenek_durum == 1:
            self.enerji -= 5

        if self.enerji < 0:
            self.enerji = 0

    @abstractmethod
    def seviye_kontrol(self):
        if self.deneyim >= 4 and self.seviye<= 3:
            self.seviye += 1
            self.max_enerji += 10
            self.dayanaklilik += 5

    @abstractmethod
    def ozel_yetenek_uygula(self):
        pass

class Futbolcu(Sporcu):
    def __init__(self, sporcu_id, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, penalti, serbest_vurus, kaleci_karsikarsiya):
        super().__init__(sporcu_id, adi, takim, "Futbol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.penalti = penalti
        self.serbest_vurus = serbest_vurus
        self.kaleci_karsikarsiya = kaleci_karsikarsiya

    def sporcu_puani_goster(self):
        print(f"Penaltı{self.penalti}, Serbest Vuruş{self.serbest_vurus}, Kaleci Karşı Karşıya{self.kaleci_karsikarsiya}")

    def seviye_kontrol(self):
        self.penalti += 5
        self.serbest_vurus += 5
        self.kaleci_karsikarsiya += 5

    def ozel_yetenek_uygula(self):
        pass

class Basketbolcu(Sporcu):
    def __init__(self, sporcu_id, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, ikilik, ucluk, serbest_atis):
        super().__init__(sporcu_id, adi, takim, "Basketbol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.ikilik = ikilik
        self.ucluk = ucluk
        self.serbest_atis = serbest_atis
    def sporcu_puani_goster(self):
        print(f"İkilik{self.ikilik}, Üçlük{self.ucluk}, serbest atis{self.serbest_atis}")

    def seviye_kontrol(self):
        self.ikilik += 5
        self.ucluk += 5
        self.serbest_atis += 5

    def ozel_yetenek_uygula(self):
        pass

class Voleybolcu(Sporcu):
    def __init__(self, sporcu_id, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, servis, blok, smac):
        super().__init__(sporcu_id, adi, takim, "Voleybol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.servis = servis
        self.blok = blok
        self.smac = smac
    def sporcu_puani_goster(self):
        print(f"Servis {self.servis}, blok {self.blok}, smac {self.smac}")

    def seviye_kontrol(self):
        self.servis += 5
        self.blok += 5
        self.smac += 5

    def ozel_yetenek_uygula(self):
        pass

def dosya_okuma():
    kart_destesi = []
    id_sayac = 15
    with open ("sporcular.txt", encoding=("utf-8")) as f:
        for karakter in f:
            sporcu = karakter.strip().split(",")
            if len(sporcu) != 9:
                print("Eksik değerli kart!")
            else:
                ad = sporcu[1]
                takim = sporcu[2]
                ozel_yetenek = sporcu[8]
                dayaniklilik = int(sporcu[6])
                max_enerji = int(sporcu[7])
                ozellik1 = int(sporcu[3])
                ozellik2 = int(sporcu[4])
                ozellik3 = int(sporcu[5])
                match sporcu[0]:
                    case "Futbol":
                        yeni_kart = Futbolcu(id_sayac, ad, takim, "Futbol",dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                    case "Basketbol":
                        yeni_kart = Basketbolcu(id_sayac, ad, takim, "Basketbol",dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                    case "Voleybol":
                        yeni_kart = Voleybolcu(id_sayac, ad, takim, "Voleybol",dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                id_sayac += 1
    return kart_destesi

class Oyuncu(ABC):
    def __init__(self, oyuncu_id, oyuncu_adi, kart_listesi):
        self.oyuncu_id = oyuncu_id
        self.oyuncu_adi = oyuncu_adi
        self.moral = 0
        self.skor = 0
        self.kart_listesi = kart_listesi
        self.galibiyet_serisi = 0
        self.kaybetme_serisi = 0

class Kullanici(Oyuncu):
    def __init__(self, oyuncu_id, oyuncu_adi, kart_listesi):
        super().__init__(oyuncu_id, "Kullanıcı", kart_listesi)

    def kart_sec(self):
        pass

class Bilgisayar(Oyuncu):
    def __init__(self, oyuncu_id, oyuncu_adi, kart_listesi):
        super().__init__(oyuncu_id, "Bilgisayar", kart_listesi)

    def kart_sec(self):
        pass

class Oyun_Yoneticisi():
    def __init__(self):
        self.tur_sayisi = 1
        self.kullanici_deste = []
        self.bilgisayar_deste = []

    def kart_dagitimi(self, kart_destesi):
        futbolcular = []
        basketbolcular = []
        voleybolcular = []
        for kart in kart_destesi:
            match kart.brans:
                case "Futbol":
                    futbolcular.append(kart)
                case "Basketbol":
                    basketbolcular.append(kart)
                case "Voleybol":
                    voleybolcular.append(kart)

        random.shuffle(futbolcular)
        random.shuffle(basketbolcular)
        random.shuffle(voleybolcular)

        self.kullanici_deste = futbolcular[:4] + basketbolcular[:4] + voleybolcular[:4]
        self.bilgisayar_deste = futbolcular[4:] + basketbolcular[4:] + voleybolcular[4:]

        random.shuffle(self.kullanici_deste)
        random.shuffle(self.bilgisayar_deste)

        print("Her branştan en az 4 kart olacak şekilde kartlar iki oyuncuya dağıtıldı!")

    def brans_secme(self):
        match self.tur_sayisi:
            case 1:
                guncel_brans = "Futbol"
            case 2:
                guncel_brans = "Basketbol"
            case 3:
                guncel_brans = "Voleybol"
        self.tur_sayisi += 1
        if self.tur_sayisi > 3:
            self.tur_sayisi = 1

        return guncel_brans

    def nitelik_secme(self, guncel_brans):
        f_nitelik = ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"]
        b_nitelik =  ["İkilik", "Üçlük", "Serbest Atış"]
        v_nitelik = ["Servis", "Blok", "Smaç"]

        match guncel_brans:
            case "Futbol":
                sec_nitelik = random.choice(f_nitelik)
            case "Basketbol":
                sec_nitelik = random.choice(b_nitelik)
            case "Voleybol":
                sec_nitelik = random.choice(v_nitelik)

        return sec_nitelik

    def kazanma_durumu(self, kazanan, kaybeden, kart):
        kart.deneyim += 2
        kazanan.skor += 10
        kazanan.galibiyet_serisi += 1
        if 5 > kazanan.galibiyet_serisi >= 3:
            kazanan.skor += 10
        elif kazanan.galibiyet_serisi >= 5:
            kazanan.skor += 20
        if kazanan.galibiyet_serisi == 2:
            kazanan.moral += 10
        elif kazanan.galibiyet_serisi >= 3:
            kazanan.moral += 15
        kaybeden.galibiyet_serisi = 0
        kaybeden.kaybetme_serisi += 1
        if kaybeden.kaybetme_serisi >= 2:
            kaybeden.moral -= 10

    def tur(self, guncel_brans, sec_nitelik):
        kullanici_sec_kart = kullanici.kart_sec()
        bilgisayar_sec_kart = bilgisayar.kart_sec()

        while True:
            if (kullanici_sec_kart.brans != guncel_brans):
                print("Doğru branştan bir kart seçiniz!")
            else:
                break

        k_kart_skoru = kullanici_sec_kart.performans_hesapla(sec_nitelik, 0, kullanici.moral)
        b_kart_skoru = bilgisayar_sec_kart.performans_hesapla(sec_nitelik, 0, bilgisayar.moral)

        if k_kart_skoru > b_kart_skoru:
            self.kazanma_durumu(kullanici, bilgisayar, kullanici_sec_kart)
        elif k_kart_skoru < b_kart_skoru:
            self.kazanma_durumu(bilgisayar, kullanici, bilgisayar_sec_kart)
        else:
            pass

    def kart_karsilastir(self, kullanici_kart, bilgisayar_kart):
        pass

dosya_okuma()


from abc import ABC, abstractmethod

class Sporcu(ABC):
    def __init__(self, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek):
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

    @abstractmethod
    def sporcu_puanı_goster(self):
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

    def enerji_guncelle(self, durum, ozel_yetenek_durum):
        match durum:
            case "Kazandı":
                self.enerji =- 5
            case "Kaybetti":
                self.enerji = -  10
            case "Beraber":
                self.enerji =- 3

        if ozel_yetenek_durum == 1:
            self.enerji =- 5

        if self.enerji < 0:
            self.enerji = 0

class Futbolcu(Sporcu):
    def __init__(self, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, penalti, serbest_vurus, kaleci_karsikarsiya):
        super().__init__(adi, takim, "Futbol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.penalti = penalti
        self.serbest_vurus = serbest_vurus
        self.kaleci_karsikarsiya = kaleci_karsikarsiya

    def sporcu_puanı_goster(self):
        pass

class Basketbolcu(Sporcu):
    def __init__(self, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, ikilik, ucluk, serbest_atis):
        super().__init__(adi, takim, "Basketbol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.ikilik = ikilik
        self.ucluk = ucluk
        self.serbest_atis = serbest_atis

class Voleybolcu(Sporcu):
    def __init__(self, adi, takim, brans, dayaniklilik, max_enerji ,ozel_yetenek, servis, blok, smac):
        super().__init__(adi, takim, "Voleybol", dayaniklilik, max_enerji ,ozel_yetenek)
        self.servis = servis
        self.blok = blok
        self.smac = smac

def dosya_okuma():
    kart_destesi = []
    id_sayac = 283612
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
                        yeni_kart = Futbolcu(ad, takim, dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                    case "Basketbol":
                        yeni_kart = Basketbolcu(ad, takim, dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                    case "Voleybol":
                        yeni_kart = Voleybolcu(ad, takim, dayaniklilik, max_enerji, ozel_yetenek, ozellik1, ozellik2, ozellik3)
                        kart_destesi.append(yeni_kart)
                id_sayac += 1
    return kart_destesi


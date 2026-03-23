enerji = 50
secilen_ozellik = 50

if enerji > 70:
    enerji_cezasi = 0
elif 40 <= enerji <= 70:
    enerji_cezasi = -(secilen_ozellik / 100) * 10
    print(enerji_cezasi)
elif 0 < enerji < 40:
    enerji_cezasi = -(secilen_ozellik / 100) * 20
moral = 97
if moral >= 80:
    moral_bonus = 10
elif 80 > moral >= 50:
    moral_bonus = 5
elif 50 < moral:
    moral_bonus = -5
seviye = 2
match seviye:
    case 1:
        seviye_bonus = 0
    case 2:
        seviye_bonus = 5
    case 3:
        seviye_bonus = 10


ozel_yetenek_bonusu = 0
guncel_ozellik_puani = secilen_ozellik + moral_bonus + ozel_yetenek_bonusu + int(enerji_cezasi) + seviye_bonus
print(f"{secilen_ozellik} + {moral_bonus} + {ozel_yetenek_bonusu} + {int(enerji_cezasi)} + {seviye_bonus}")
print(guncel_ozellik_puani)
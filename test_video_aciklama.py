"""
Test senaryoları - video_aciklama.py
Çalıştırmak için: python test_video_aciklama.py
Her satır: (senaryo adı, girdi, beklenen, gerçek) yazdırır ve sonunda özet verir.
"""
from video_aciklama import (
    zamani_saniyeye_cevir,
    saniyeyi_zamana_cevir,
    bolum_ekle,
    hashtag_temizle,
    aciklama_olustur,
)


def ilk_bolum_reddi():
    return bolum_ekle([], "05:00", "Giriş")[0]


def ayni_zaman_reddi():
    bolumler = []
    bolum_ekle(bolumler, "00:00", "Giriş")
    bolum_ekle(bolumler, "02:55", "Kritik")
    return bolum_ekle(bolumler, "02:55", "Aynı zaman")[0]


def bos_baslik_reddi():
    bolumler = []
    bolum_ekle(bolumler, "00:00", "Giriş")
    return bolum_ekle(bolumler, "01:00", "   ")[0]


def aciklama_metni():
    video = {"ozet": "Özet", "sosyal": {}, "hashtagler": ["#a"]}
    bolumler = [{"saniye": 0, "zaman": "00:00", "baslik": "Giriş"}]
    return aciklama_olustur(video, bolumler)


# (senaryo, girdi, beklenen, çalıştırılacak fonksiyon, tür)
SENARYOLAR = [
    ("1. Geçerli zaman", "02:55", 175,
     lambda: zamani_saniyeye_cevir("02:55"), "normal"),
    ("2. Saatli zaman", "1:05:30", 3930,
     lambda: zamani_saniyeye_cevir("1:05:30"), "normal"),
    ("3. Saniye 59'dan büyük", "01:60", None,
     lambda: zamani_saniyeye_cevir("01:60"), "hatalı/uç"),
    ("4. Üst simge rakam (çökme testi)", "²:00", None,
     lambda: zamani_saniyeye_cevir("²:00"), "hatalı/uç"),
    ("5. Belirsiz saniye hanesi", "1:5", None,
     lambda: zamani_saniyeye_cevir("1:5"), "hatalı/uç"),
    ("6. İlk bölüm 00:00 değil", "05:00 (ilk bölüm)", False,
     ilk_bolum_reddi, "hatalı/uç"),
    ("7. Aynı zaman tekrar", "02:55 (iki kez)", False,
     ayni_zaman_reddi, "hatalı/uç"),
    ("8. Boş başlık", "'   '", False,
     bos_baslik_reddi, "hatalı/uç"),
    ("9. Türkçe hashtag", "Ünlü, İstanbul", ["#ünlü", "#istanbul"],
     lambda: hashtag_temizle("Ünlü, İstanbul"), "normal"),
    ("10. Tekrarlı hashtag", "#Vlog #vlog", ["#vlog"],
     lambda: hashtag_temizle("#Vlog #vlog"), "normal"),
    ("11. Saniyeden zamana", "3930", "1:05:30",
     lambda: saniyeyi_zamana_cevir(3930), "normal"),
    ("12. Açıklama metni", "1 bölüm", "Özet\n\n00:00 Giriş\n\n#a",
     aciklama_metni, "normal"),
]


def main():
    basarili = 0
    for ad, girdi, beklenen, fonksiyon, tur in SENARYOLAR:
        try:
            gercek = fonksiyon()
        except Exception as hata:  # çökerse test başarısız sayılır
            gercek = f"HATA: {type(hata).__name__}"
        durum = "GEÇTİ" if gercek == beklenen else "KALDI"
        if durum == "GEÇTİ":
            basarili += 1
        print(f"[{durum}] {ad} | {tur}\n    girdi={girdi!r} beklenen={beklenen!r} gerçek={gercek!r}")
    print(f"\nSonuç: {basarili}/{len(SENARYOLAR)} senaryo geçti.")


if __name__ == "__main__":
    main()

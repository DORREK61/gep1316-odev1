"""
YouTube Video Açıklaması ve Zaman Damgası Oluşturucu
GEP1316 Kodlama Okuryazarlığı - Ara Değerlendirme Ödevi 1

Kullanıcı video bilgilerini ve bölümleri (zaman damgaları) girer,
program bunları doğrular ve kopyalanıp YouTube'a yapıştırılabilir
bir açıklama metni üretip .txt dosyasına kaydeder.
"""


# ---------------------------------------------------------------
# 1) YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------------

def zamani_saniyeye_cevir(zaman):
    """'dk:sn' veya 'sa:dk:sn' biçimindeki metni saniyeye çevirir.
    Biçim hatalıysa None döndürür."""
    parcalar = zaman.strip().split(":")

    if len(parcalar) not in (2, 3):
        return None

    for parca in parcalar:
        # isdigit() yerine isdecimal(): '²' gibi üst simge rakamları reddetmek için
        if not parca.isdecimal():
            return None

    # Saniye her zaman 2 haneli olmalı ('1:5' belirsizdir, '1:05' doğrudur)
    if len(parcalar[-1]) != 2:
        return None

    sayilar = [int(p) for p in parcalar]

    if len(sayilar) == 2:
        dakika, saniye = sayilar
        saat = 0
    else:
        saat, dakika, saniye = sayilar

    # Dakika ve saniye 0-59 arasında olmalı
    if dakika > 59 or saniye > 59:
        return None

    return saat * 3600 + dakika * 60 + saniye


def saniyeyi_zamana_cevir(toplam_saniye):
    """Saniyeyi '00:00' (1 saatten kısa) veya '1:05:30' biçimine çevirir."""
    saat = toplam_saniye // 3600
    dakika = (toplam_saniye % 3600) // 60
    saniye = toplam_saniye % 60

    if saat > 0:
        return f"{saat}:{dakika:02d}:{saniye:02d}"
    return f"{dakika:02d}:{saniye:02d}"


def bolum_dogrula(bolumler, zaman, baslik):
    """Yeni bölümü kontrol eder. Hata varsa hata mesajı, sorun yoksa None döndürür."""
    saniye = zamani_saniyeye_cevir(zaman)

    if baslik.strip() == "":
        return "Bölüm başlığı boş olamaz."
    elif saniye is None:
        return "Zaman biçimi hatalı. Örnek: 02:55 veya 1:05:30"
    elif len(bolumler) == 0 and saniye != 0:
        return "İlk bölüm 00:00 ile başlamalı (YouTube bölümleri için gerekli)."
    elif len(bolumler) > 0 and saniye <= bolumler[-1]["saniye"]:
        return "Zaman bir önceki bölümden büyük olmalı."
    else:
        return None


def bolum_ekle(bolumler, zaman, baslik):
    """Doğrulama başarılıysa bölümü listeye ekler. (başarılı_mı, mesaj) döndürür."""
    hata = bolum_dogrula(bolumler, zaman, baslik)
    if hata is not None:
        return False, hata

    saniye = zamani_saniyeye_cevir(zaman)
    bolumler.append({
        "saniye": saniye,
        "zaman": saniyeyi_zamana_cevir(saniye),
        "baslik": baslik.strip(),
    })
    return True, "Bölüm eklendi."


def hashtag_temizle(ham_metin):
    """'budapeşte, vlog  gezi' gibi bir metni ['#budapeşte', '#vlog', '#gezi'] listesine çevirir."""
    kelimeler = ham_metin.replace(",", " ").split()
    sonuc = []
    for kelime in kelimeler:
        # Türkçe büyük İ/I harfleri için önce elle çeviriyoruz, yoksa lower() 'İ'yi bozar
        kelime = kelime.lstrip("#").replace("İ", "i").replace("I", "ı")
        etiket = "#" + kelime.lower()
        if etiket != "#" and etiket not in sonuc:
            sonuc.append(etiket)
    return sonuc


def aciklama_olustur(video, bolumler):
    """Video bilgisi (sözlük) ve bölümler (liste) ile açıklama metnini üretir."""
    satirlar = []
    satirlar.append(video["ozet"])
    satirlar.append("")

    for bolum in bolumler:
        satirlar.append(f"{bolum['zaman']} {bolum['baslik']}")
    satirlar.append("")

    if video["sosyal"]:
        satirlar.append("Sosyal Medya Hesaplarım 👇")
        for platform, link in video["sosyal"].items():
            satirlar.append(f"➡️ {platform}: {link}")
        satirlar.append("")

    if video["hashtagler"]:
        satirlar.append(" ".join(video["hashtagler"]))

    return "\n".join(satirlar)


def dosyaya_kaydet(metin, dosya_adi):
    """Metni UTF-8 .txt dosyasına yazar."""
    if not dosya_adi.endswith(".txt"):
        dosya_adi += ".txt"
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        dosya.write(metin)
    return dosya_adi


# ---------------------------------------------------------------
# 2) KULLANICIDAN GİRDİ ALMA (doğrulamalı)
# ---------------------------------------------------------------

def bos_olmayan_al(soru):
    """Kullanıcı boş bırakmayana kadar tekrar sorar."""
    while True:
        cevap = input(soru).strip()
        if cevap != "":
            return cevap
        print("  ⚠ Bu alan boş bırakılamaz, tekrar deneyin.")


def link_al(platform):
    """İsteğe bağlı sosyal medya linki alır. https ile başlamıyorsa uyarır."""
    while True:
        link = input(f"{platform} linki (boş bırakabilirsiniz): ").strip()
        if link == "":
            return None
        if link.startswith("https://") or link.startswith("http://"):
            return link
        print("  ⚠ Link http:// veya https:// ile başlamalı.")


def video_bilgisi_al():
    """Video özeti, sosyal medya linkleri ve hashtag'leri alır, sözlük döndürür."""
    print("\n--- Video Bilgileri ---")
    ozet = bos_olmayan_al("Videonun 1-2 cümlelik özeti: ")

    sosyal = {}
    for platform in ["Instagram", "TikTok"]:
        link = link_al(platform)
        if link is not None:
            sosyal[platform] = link

    ham_hashtag = input("Hashtag'ler (virgül veya boşlukla ayırın): ")
    hashtagler = hashtag_temizle(ham_hashtag)

    return {"ozet": ozet, "sosyal": sosyal, "hashtagler": hashtagler}


def bolum_ekle_menusu(bolumler):
    """Kullanıcıdan zaman ve başlık alıp bölüm eklemeyi dener."""
    zaman = input("Zaman (örn. 02:55): ")
    baslik = input("Bölüm başlığı: ")
    basarili, mesaj = bolum_ekle(bolumler, zaman, baslik)
    simge = "✅" if basarili else "⚠"
    print(f"  {simge} {mesaj}")


def bolumleri_goster(bolumler):
    """Bölümleri biçimli olarak ekrana yazar."""
    if len(bolumler) == 0:
        print("  Henüz bölüm eklenmedi.")
        return
    print(f"\n{'Zaman':<10}Başlık")
    print("-" * 40)
    for bolum in bolumler:
        print(f"{bolum['zaman']:<10}{bolum['baslik']}")
    print(f"\nToplam bölüm sayısı: {len(bolumler)}")


# ---------------------------------------------------------------
# 3) ANA PROGRAM (menü döngüsü)
# ---------------------------------------------------------------

def menuyu_goster():
    print("\n===== VİDEO AÇIKLAMA OLUŞTURUCU =====")
    print("1) Video bilgilerini gir")
    print("2) Bölüm (zaman damgası) ekle")
    print("3) Bölümleri listele")
    print("4) Açıklamayı oluştur ve kaydet")
    print("5) Çıkış")


def main():
    video = None
    bolumler = []

    while True:
        menuyu_goster()
        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            video = video_bilgisi_al()
            print("  ✅ Video bilgileri kaydedildi.")
        elif secim == "2":
            bolum_ekle_menusu(bolumler)
        elif secim == "3":
            bolumleri_goster(bolumler)
        elif secim == "4":
            if video is None:
                print("  ⚠ Önce 1 numaralı seçenekle video bilgilerini girin.")
            elif len(bolumler) == 0:
                print("  ⚠ En az bir bölüm eklemelisiniz.")
            else:
                metin = aciklama_olustur(video, bolumler)
                print("\n" + "=" * 40)
                print(metin)
                print("=" * 40)
                dosya_adi = input("Kaydedilecek dosya adı (örn. aciklama): ").strip()
                if dosya_adi == "":
                    dosya_adi = "aciklama"
                kaydedilen = dosyaya_kaydet(metin, dosya_adi)
                print(f"  ✅ Açıklama '{kaydedilen}' dosyasına kaydedildi.")
        elif secim == "5":
            print("Görüşmek üzere!")
            break
        else:
            print("  ⚠ Geçersiz seçim. Lütfen 1 ile 5 arasında bir sayı girin.")


if __name__ == "__main__":
    main()

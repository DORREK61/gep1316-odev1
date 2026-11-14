# YouTube Video Açıklaması ve Zaman Damgası Oluşturucu

GEP1316 Kodlama Okuryazarlığı – Ara Değerlendirme Ödevi 1 (YZ Destekli Python Mini Uygulaması)

## Ne yapar?

İçerik üreticileri video açıklamalarını ve bölüm (zaman damgası) listelerini genelde elle yazar. Bu komut satırı uygulaması bu işi otomatikleştirir:

- Video özetini, sosyal medya linklerini ve hashtag'leri alır.
- Bölümleri (zaman + başlık) tek tek ekletir ve **doğrular** (YouTube kuralı: ilk bölüm `00:00` olmalı, zamanlar artan sırada olmalı).
- Hepsini YouTube'a yapıştırmaya hazır tek bir açıklama metni hâline getirir, ekranda gösterir ve `.txt` dosyasına kaydeder.

Kullanıcı: kendi videolarını yayınlayan içerik üreticisi (örn. vlog kanalı sahibi).

## Nasıl çalıştırılır?

Python 3.8 veya üzeri yeterlidir, ek kütüphane gerekmez.

```bash
python video_aciklama.py
```

Menü açılır:

```
1) Video bilgilerini gir
2) Bölüm (zaman damgası) ekle
3) Bölümleri listele
4) Açıklamayı oluştur ve kaydet
5) Çıkış
```

Önerilen sıra: 1 → 2 (birkaç kez) → 3 → 4.

Örnek çıktı (`aciklama.txt`):

```
Budapeşte'de 3 gün gezdik, yedik, eğlendik.

00:00 Giriş ve yolculuk
02:55 Gün kritiği

Sosyal Medya Hesaplarım 👇
➡️ Instagram: https://www.instagram.com/ornek/

#budapeşte #istanbul #vlog
```

## Testler

```bash
python test_video_aciklama.py
```

12 senaryo çalışır (7'si hatalı/uç girdi). Sonuç tablosu rapordadır.

## Ödev gereksinimleri nerede?

| Gereksinim | Kodda nerede |
|---|---|
| En az 3 girdi + doğrulama | `bos_olmayan_al`, `link_al`, `bolum_ekle_menusu` (zaman ve başlık doğrulaması) |
| En az 2 karar yapısı (if/elif/else) | `bolum_dogrula`, `main` menüsü |
| En az 1 döngü | `main` içindeki menü döngüsü, `bos_olmayan_al`, `link_al` |
| En az 3 fonksiyon | 12 fonksiyon (`zamani_saniyeye_cevir`, `bolum_ekle`, `aciklama_olustur` vb.) |
| Liste veya sözlük | `bolumler` (sözlük listesi), `video` (sözlük), `sosyal` (sözlük) |
| Biçimli ekran çıktısı ve dosyaya kayıt | `bolumleri_goster`, `dosyaya_kaydet` |

## Dosyalar

- `video_aciklama.py` – uygulama
- `test_video_aciklama.py` – test senaryoları
- `PROMPTLAR.md` – YZ ile çalışma günlüğü
- `README.md` – bu dosya

## Ekran görüntüleri

*(Buraya programı çalıştırırken aldığın 2-3 ekran görüntüsünü ekle: menü, hatalı girdi uyarısı, oluşan açıklama.)*

## Yapay zekâ kullanımı

Bu projede Claude (Anthropic) kod üretimi, test ve hata ayıklama için kullanılmıştır. Ayrıntılar `PROMPTLAR.md` dosyasındadır.

# YZ ile Çalışma Günlüğü (PROMPTLAR)

Araç: Claude (Anthropic), https://claude.ai

> **Not:** "Karar ve gerekçe" bölümleri taslaktır. Teslimden önce kendi cümlelerinle düzenle ve sadece gerçekten yaşadığın şeyleri bırak.

---

## Prompt 1: Ödevi başlatma

**Prompt (olduğu gibi):**
> şimdi bu benim vizem tek kelime bile okumadım bunu nasıl basit hızlı bir şekile yaparız

(Ödev yönergesi ve PDF ile birlikte gönderildi.)

**YZ'nin yanıtı (özet):** Ödevin gereksinimlerini okudu, "YouTube video açıklaması ve zaman damgası oluşturucu" fikrini önerdi (kendi kanalım için gerçekten işime yarayacak, gereksinimlerin hepsine uyuyor). Ardından `video_aciklama.py` dosyasını yazdı: menü döngüsü, doğrulamalı girdiler, bölümleri tutan sözlük listesi, açıklama üretimi ve .txt kaydı.

**Karar ve gerekçe (taslak):** Fikri kabul ettim, çünkü kendi kanalım için gerçek bir ihtiyaca karşılık geliyor ve ödevdeki tüm gereksinimleri (girdi doğrulama, karar yapısı, döngü, fonksiyon, liste/sözlük, dosya kaydı) doğal şekilde içeriyor.

---

## YZ'nin hatasını yakalama (gerçek örnek)

YZ'nin ilk yazdığı kodu uç girdilerle çalıştırınca **üç sorun** çıktı:

1. **Çökme:** Zaman olarak `²:00` (üst simge rakam) girilince program `ValueError` ile çöktü. Sebep: `str.isdigit()` bu karakteri rakam sayıyor ama `int()` sayıya çeviremiyor. **Düzeltme:** `isdecimal()` kullanıldı.
2. **Türkçe harf hatası:** `İstanbul` hashtag'i `#i̇stanbul` (bozuk, birleşik nokta ile) oluyordu, çünkü Python'un `lower()` fonksiyonu Türkçe `İ` harfini doğru küçültmüyor. **Düzeltme:** `İ`→`i` ve `I`→`ı` dönüşümü önce elle yapıldı.
3. **Belirsiz giriş:** `1:5` sessizce `01:05` olarak kabul ediliyordu. **Düzeltme:** saniye hanesi her zaman 2 haneli olmak zorunda.

Düzeltmeden sonra tüm testler yeniden çalıştırıldı (12/12 geçti).

---

## Prompt 2

*(Buraya gerçekten sorduğun bir sonraki prompt'u, YZ yanıtının özetini ve kararını yaz.)*

## Prompt 3

*(...)*

## Prompt 4

*(...)*

## Prompt 5

*(...)*

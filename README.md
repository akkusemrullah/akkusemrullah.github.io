# Travel Planner web sitesi

Sunucu tarafı kodu olmayan, tamamen statik bir site. Çerez, analiz aracı veya dış kaynaklı yazı tipi/kod kullanmaz.

## Yayına almadan önce

1. **APK dosyası:** İmzalı APK'yı `indir/TravelPlanner.apk` adıyla bu klasöre koyun (`indir/APK-BURAYA.txt` dosyasını silebilirsiniz).
   - Cloudflare Pages tek dosya için 25 MB, GitHub Pages 100 MB sınırı koyar. APK bundan büyükse GitHub Releases'e yükleyip
     `index.html` içindeki `indir/TravelPlanner.apk` bağlantılarını o adresle değiştirin.
2. **Sürüm numarası:** Yeni sürümde `index.html` içindeki "Sürüm 1.0.0" metnini güncelleyin.
3. **Hesap silme:** Uygulamada "Profil → Hesabı sil" eklendiğinde `hesap-ve-veri-silme.html` sayfası zaten buna göre yazılmıştır.
   Eklenene kadar e-posta ile silme yöntemi geçerlidir.

## Yayınlama

- **Cloudflare Pages (önerilen):** Bu klasörü "Direct Upload" ile yükleyin. `_redirects` dosyası `/invite/<kod>` davet
  bağlantılarını, `_headers` dosyası güvenlik başlıklarını ve APK indirme türünü ayarlar.
- **GitHub Pages:** Klasörü bir depoya koyun. `_redirects`/`_headers` GitHub Pages'te çalışmaz; davet bağlantıları
  `invite.html?kod=XXXX` biçiminde çalışır.
- Site alan adının kök dizininde (ör. `https://alanadi.com/`) yayınlanmalıdır; `404.html` buna göre ayarlıdır.

## Sayfalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Tanıtım, özellikler, SSS, APK indirme ve kurulum adımları, iOS "yakında" |
| `gizlilik-politikasi.html` / `privacy-policy.html` | Gizlilik Politikası (TR / EN) |
| `kvkk-aydinlatma-metni.html` | KVKK m.10 aydınlatma metni |
| `kullanim-kosullari.html` | Kullanım koşulları ve sorumluluk sınırları |
| `cerez-politikasi.html` | Çerez politikası (çerez kullanılmaz) |
| `hesap-ve-veri-silme.html` | Hesap ve veri silme (Google Play'in istediği sayfa) |
| `kvkk-basvuru.html` | KVKK m.11 başvuru formu (e-posta taslağı üretir, veri göndermez) |
| `acik-kaynak-lisanslari.html` | Açık kaynak lisansları ve veri atıfları |
| `invite.html` | Davet kodu açılış sayfası |

Renkler uygulamanın `Resources/Themes` tokenlarıyla aynıdır; site açık/koyu temayı cihazın ayarına göre seçer.

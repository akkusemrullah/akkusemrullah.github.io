# Travel Planner — Web Sitesi

Travel Planner, seyahatleri tek yerden planlamak için geliştirilmiş bir .NET MAUI mobil uygulamasıdır (EAKSOFT). Bu depo, uygulamanın tanıtım sitesini içerir.

## Uygulama

- Gün gün plan ve sürükle-bırak sıralama
- Harita, günün rotası ve yol tarifi
- Hava durumu ve akıllı bavul önerileri
- Bütçe, çoklu para birimi ve harcama analizi
- Arkadaşlarla harcama bölüşme
- Yapay zekâ ile plan önerisi ve Keşfet'teki hazır planlar
- Davet koduyla seyahat paylaşımı, cihazlar arası eşitleme
- Belgeler, yedekleme, karanlık tema; Türkçe ve İngilizce

Hesapsız kullanılabilir; reklam ve takip yoktur.

## Site

Statik HTML/CSS/JS; çerez, yerel depolama ve dış kaynak yoktur. Tanıtım sayfası, Android APK indirme, yasal belgeler (gizlilik politikası, KVKK aydınlatma metni, açık rıza, kullanım koşulları, yapay zekâ feragatnamesi, çerez ve iade politikaları, lisanslar), hesap silme ve KVKK başvuru sayfalarını içerir.

### Düzenleme

Kökteki `.html` dosyaları üretilir; elle düzenleme. Kaynaklar `src/` altındadır:

- `src/home.html` sade ana sayfa; `src/ozellikler.html` (özellikler ve ekranlar), `src/sss.html`, `src/indir.html` (APK ve kurulum), `src/yasal.html` yasal belgeler, `src/invite.html`, `src/404.html`
- `src/pages/*.html` yasal belgelerin gövdeleri (başta `title`, `lead`, `effective`, `updated` bilgileri)
- Ortak üst menü, alt bilgi ve yasal belge listesi `tools/build.py` içindedir; simgeler `tools/icons.py`

Değişiklikten sonra:

```
python tools/build.py
```

Yasal metinler uygulamadaki *Profil → Yasal ve gizlilik* metinleriyle (TravelPlanner deposu, `Resources/Strings/AppResources.resx`) uyumlu tutulmalıdır; bir metin değişince `updated` tarihini de güncelle.

Telefon görselleri (`assets/img/ekran/`) uygulamanın gerçek ekran görüntüleridir (Samsung S25, örnek veri). Durum çubuğu ve alt hareket çubuğu kırpılır, 720 × 1465 WebP olarak kaydedilir.

### Yayın

- GitHub Pages: `main` dalı.
- emrullahakkus.com.tr/travelplanner/ (Plesk, `tp-site` klasörü): `src/`, `tools/`, `README.md` ve `.git*` dışındaki dosyalar elle yüklenir. Admin paneli ayrı klasördedir (`tp-admin`) ve bu yüklemeye dahil değildir.

© EAKSOFT · Emrullah AKKUŞ

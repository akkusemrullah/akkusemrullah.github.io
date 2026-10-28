#!/usr/bin/env python3
"""Builds the static site: wraps every page in src/ with the shared head, header and footer.

    python3 tools/build.py

Sources:
  src/home.html, src/yasal.html, src/invite.html, src/404.html   page bodies (layout "plain")
  src/pages/*.html                                               legal documents (layout "legal")

Each source starts with an HTML comment holding "key: value" lines (title, description, lead, ...).
In the bodies, {{icon:name}} becomes an inline Lucide icon (tools/icons.py) and
{{phone:file|alt text}} a phone frame around assets/img/ekran/<file>.webp.
The generated .html files sit at the repository root; edit src/, never the output.
Standard library only, no network.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from icons import icon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

EMAIL = "emrullahakkus@gmail.com"
APK_URL = "https://github.com/akkusemrullah/akkusemrullah.github.io/releases/latest/download/TravelPlanner.apk"

# Legal documents in the order the sidebar and the legal hub show them.
DOCS = [
    # file, short label, group, icon, one-line summary
    ("gizlilik-politikasi.html", "Gizlilik Politikası", "veri", "shield",
     "Hangi verileri, hangi amaçla, nerede ve ne kadar süre işlediğimiz."),
    ("kvkk-aydinlatma-metni.html", "KVKK Aydınlatma Metni", "veri", "scale",
     "6698 sayılı Kanun’un 10. maddesi kapsamındaki aydınlatma."),
    ("acik-riza-metni.html", "Açık Rıza Metni", "veri", "check",
     "Yapay zekâ ile planlama ve Google ile giriş için yurt dışına aktarım."),
    ("cerez-politikasi.html", "Çerez Politikası", "veri", "cookie",
     "Sitede çerez, yerel depolama veya takip aracı kullanılmaz."),
    ("kullanim-kosullari.html", "Kullanım Koşulları", "kullanim", "file",
     "Uygulamayı ve siteyi kullanma kuralları, sorumluluklar."),
    ("yapay-zeka-feragatnamesi.html", "Yapay Zekâ Feragatnamesi", "kullanim", "sparkles",
     "Yapay zekâ önerilerinin sınırları ve kullanım hakkı."),
    ("iade-politikasi.html", "İptal ve İade Politikası", "kullanim", "receipt",
     "Uygulama ücretsizdir; abonelik ve ödeme yoktur."),
    ("acik-kaynak-lisanslari.html", "Lisanslar ve atıflar", "kullanim", "code",
     "Kullanılan açık kaynak yazılımlar ve veri kaynakları."),
    ("hesap-ve-veri-silme.html", "Hesap ve veri silme", "haklar", "user-x",
     "Hesabını uygulamadan veya e-postayla silme adımları."),
    ("kvkk-basvuru.html", "KVKK başvuru formu", "haklar", "clipboard",
     "KVKK’nın 11. maddesindeki hakların için başvuru metni hazırla."),
    ("privacy-policy.html", "Privacy Policy (English)", "veri", "globe",
     "English version of the privacy policy."),
]
GROUPS = [
    ("veri", "Gizlilik ve kişisel veriler"),
    ("kullanim", "Kullanım ve sorumluluk"),
    ("haklar", "Haklarınız"),
]
LANG_PAIRS = {"gizlilik-politikasi.html": ("privacy-policy.html", "en", "Read in English"),
              "privacy-policy.html": ("gizlilik-politikasi.html", "tr", "Türkçe sürümü oku")}

LOGO = ('<svg class="logo" aria-hidden="true" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#1E3A8A"/>'
        '<g transform="translate(20 21) scale(.27) translate(-60 -67)">'
        '<path d="M60 112C60 112 22 72 22 46a38 38 0 0 1 76 0c0 26-38 66-38 66Z" fill="#fff"/>'
        '<path d="M37 47 81 28 65 69 57 55Z" fill="#1E3A8A"/>'
        '<path d="M57 55 81 28" stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none"/></g></svg>')

CUR = ' aria-current="page"'
EN = ' hreflang="en" lang="en"'
NAV = [("index.html#ozellikler", "Özellikler"), ("index.html#ekranlar", "Ekranlar"),
       ("index.html#gizlilik", "Gizlilik"), ("index.html#sss", "SSS"), ("yasal.html", "Yasal")]


def esc(s):
    return html.escape(s, quote=True)


def read_source(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"<!--\n(.*?)\n-->\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def expand(body):
    body = re.sub(r"\{\{icon:([\w-]+)\}\}", lambda m: icon(m.group(1)), body)

    def phone(m):
        name, _, alt = m.group(1).partition("|")
        extra = ' loading="lazy" decoding="async"' if not alt.startswith("!") else ' fetchpriority="high"'
        alt = alt.lstrip("!")
        return (f'<div class="phone"><img src="assets/img/ekran/{name}.webp" alt="{esc(alt)}" '
                f'width="720" height="1413"{extra}></div>')
    return re.sub(r"\{\{phone:([^}]+)\}\}", phone, body)


def head(title, desc, lang="tr", extra=""):
    full = title if "Travel Planner" in title else f"{title} – Travel Planner"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
{extra}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#1E3A8A">
<meta name="color-scheme" content="light dark">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Travel Planner">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="assets/img/og-image.png">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'tr_TR'}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/Inter-Bold.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#icerik">İçeriğe geç</a>
"""


def header(active=""):
    links = "".join(
        f'<a href="{href}"{CUR if label == active else ""}>{label}</a>' for href, label in NAV)
    return f"""<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Travel Planner ana sayfa">{LOGO}<span>Travel Planner</span></a>
    <nav id="site-nav" class="nav" aria-label="Ana menü">{links}<a class="btn btn-primary btn-sm nav-cta" href="index.html#indir">{icon("download")}Uygulamayı indir</a></nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menüyü aç/kapat">{icon("menu", "ico i-open")}{icon("x", "ico i-close")}</button>
  </div>
</header>
"""


def footer():
    legal = "".join(f'<li><a href="{f}"{EN if f == "privacy-policy.html" else ""}>{label}</a></li>'
                    for f, label, g, _, _ in DOCS if g in ("veri", "kullanim"))
    rights = "".join(f'<li><a href="{f}">{label}</a></li>' for f, label, g, _, _ in DOCS if g == "haklar")
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html" aria-label="Travel Planner ana sayfa">{LOGO}<span>Travel Planner</span></a>
        <p>Seyahatini tek yerden planla: gün gün plan, harita, bütçe, harcama bölüşme ve belgeler tek uygulamada. Reklam yok, takip yok.</p>
        <p class="foot-pub">Bir <strong>EAKSOFT</strong> uygulamasıdır.</p>
      </div>
      <div>
        <h2>Uygulama</h2>
        <ul>
          <li><a href="index.html#ozellikler">Özellikler</a></li>
          <li><a href="index.html#ekranlar">Ekranlar</a></li>
          <li><a href="index.html#indir">Android APK indir</a></li>
          <li><a href="index.html#sss">Sık sorulan sorular</a></li>
        </ul>
      </div>
      <div>
        <h2>Yasal</h2>
        <ul>{legal}</ul>
      </div>
      <div>
        <h2>Haklarınız ve destek</h2>
        <ul>{rights}
          <li><a href="yasal.html">Tüm yasal belgeler</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span data-year>2026</span> EAKSOFT · Emrullah AKKUŞ. Tüm hakları saklıdır.</span>
      <span>Harita verisi © <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap katkıcıları</a> · OpenMapTiles · OpenFreeMap · Hava verisi <a href="https://open-meteo.com/" rel="noopener">Open-Meteo.com</a> (CC BY 4.0)</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def slug_toc(body):
    return re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)


def legal_page(fname, meta, body):
    en = meta.get("lang") == "en"
    t = {"home": "Home" if en else "Ana sayfa", "legal": "Legal" if en else "Yasal ve haklarınız",
         "eff": "Effective" if en else "Yürürlük", "upd": "Last updated" if en else "Son güncelleme",
         "toc": "On this page" if en else "Bu sayfada", "docs": "Yasal belgeler"}
    toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", txt)}</a></li>' for i, txt in slug_toc(body))
    side = "".join(
        f'<li><a href="{f}"{CUR if f == fname else ""}>{icon(ic)}<span>{label}</span></a></li>'
        for f, label, _, ic, _ in DOCS)
    lang_sw = ""
    if fname in LANG_PAIRS:
        other, lang, label = LANG_PAIRS[fname]
        lang_sw = f'<a class="chip-link" href="{other}" hreflang="{lang}" lang="{lang}">{icon("globe")}{label}</a>'
    dates = ""
    if meta.get("updated"):
        dates = (f'<div class="dates"><span>{t["eff"]}: {meta["effective"]}</span>'
                 f'<span>{t["upd"]}: {meta["updated"]}</span>{lang_sw}</div>')
    doc_lang = ' lang="en"' if en else ""
    return f"""<main id="icerik">
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Konum"><a href="index.html">{t["home"]}</a><span aria-hidden="true">/</span><a href="yasal.html">{t["legal"]}</a></nav>
    <h1{doc_lang}>{meta["title"]}</h1>
    <p class="lead"{doc_lang}>{meta["lead"]}</p>
    {dates}
  </div>
</section>
<div class="wrap doc">
  <aside class="doc-side">
    <details class="toc" open><summary>{t["toc"]}{icon("down")}</summary><ol>{toc}</ol></details>
    <nav class="doc-nav" aria-label="{t["docs"]}"><h2>{t["docs"]}</h2><ul>{side}</ul></nav>
  </aside>
  <article class="prose"{doc_lang}>
{body.strip()}
  </article>
</div>
</main>
"""


def legal_hub_cards():
    out = []
    for g, title in GROUPS:
        cards = "".join(
            f'<a class="doc-card" href="{f}">{icon(ic)}<span><strong>{label}</strong><small>{summary}</small></span>{icon("right", "ico chev")}</a>'
            for f, label, grp, ic, summary in DOCS if grp == g)
        out.append(f'<section class="doc-group" aria-labelledby="g-{g}"><h2 id="g-{g}" class="h3">{title}</h2><div class="doc-cards">{cards}</div></section>')
    return "\n".join(out)


def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", name)


def main():
    for fname, *_ in DOCS:
        meta, body = read_source(os.path.join(SRC, "pages", fname))
        lang = meta.get("lang", "tr")
        write(fname, head(meta["title"], meta["description"], lang) + header("Yasal") + legal_page(fname, meta, expand(body)) + footer())

    for src, out in (("home.html", "index.html"), ("yasal.html", "yasal.html"),
                     ("invite.html", "invite.html"), ("404.html", "404.html")):
        meta, body = read_source(os.path.join(SRC, src))
        body = expand(body).replace("{{legal-hub}}", legal_hub_cards()).replace("{{apk}}", APK_URL).replace("{{email}}", EMAIL)
        extra = ""
        if meta.get("head-script"):
            extra = open(os.path.join(SRC, meta["head-script"]), encoding="utf-8").read().strip() + "\n"
        write(out, head(meta["title"], meta["description"], extra=extra) + header(meta.get("active", "")) + body + footer())


if __name__ == "__main__":
    main()

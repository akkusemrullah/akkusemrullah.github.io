/* TravelPlanner web sitesi — sunucu yok, çerez yok, takip yok. Bu dosya yalnızca tarayıcıda çalışır. */
(function () {
  "use strict";

  // Mobil menü
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // Yıl
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  // Henüz yayında olmayan (iOS) bağlantılar
  document.querySelectorAll('[aria-disabled="true"]').forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); });
  });

  function copyText(text, btn) {
    var done = function () {
      if (!btn) return;
      var old = btn.textContent;
      btn.textContent = btn.getAttribute("data-copied") || "Kopyalandı";
      setTimeout(function () { btn.textContent = old; }, 1800);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(); });
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (e) { /* yok say */ }
      document.body.removeChild(ta);
    }
  }

  // ---------- Davet sayfası: /invite/<kod> veya invite.html?kod=<kod> ----------
  var codeEl = document.getElementById("invite-code");
  if (codeEl) {
    var code = "";
    var m = location.pathname.match(/\/invite\/([^\/?#]+)/i);
    if (m) code = decodeURIComponent(m[1]);
    if (!code) {
      var q = new URLSearchParams(location.search);
      code = q.get("kod") || q.get("code") || "";
    }
    code = code.replace(/[^A-Za-z0-9-]/g, "").toUpperCase().slice(0, 32);
    var has = document.getElementById("invite-has");
    var none = document.getElementById("invite-none");
    if (code) {
      codeEl.textContent = code;
      if (has) has.hidden = false;
      if (none) none.hidden = true;
      var cbtn = document.getElementById("copy-code");
      if (cbtn) cbtn.addEventListener("click", function () { copyText(code, cbtn); });
    }
  }

  // ---------- KVKK başvuru formu (e-posta taslağı üretir, hiçbir yere gönderilmez) ----------
  var form = document.getElementById("kvkk-form");
  if (form) {
    var to = form.getAttribute("data-to");
    var err = document.getElementById("form-error");
    var out = document.getElementById("form-output");
    var pre = document.getElementById("form-text");
    var mail = document.getElementById("form-mail");
    var copyBtn = document.getElementById("form-copy");
    var printBtn = document.getElementById("form-print");
    var val = function (n) { var el = form.elements[n]; return el ? String(el.value || "").trim() : ""; };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var missing = [];
      if (!val("ad")) missing.push("Ad soyad");
      if (!val("eposta") || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val("eposta"))) missing.push("Geçerli bir e-posta adresi");
      var talepler = Array.prototype.slice.call(form.querySelectorAll('input[name="talep"]:checked')).map(function (c) { return c.value; });
      if (!talepler.length) missing.push("En az bir talep");
      if (!val("aciklama")) missing.push("Talebinizin açıklaması");
      if (!form.elements["onay"].checked) missing.push("Bilgilerin doğruluğu onayı");
      if (missing.length) {
        err.textContent = "Lütfen şunları tamamlayın: " + missing.join(", ") + ".";
        err.classList.add("show"); err.focus && err.focus();
        return;
      }
      err.classList.remove("show");
      var today = new Date().toLocaleDateString("tr-TR", { day: "2-digit", month: "long", year: "numeric" });
      var lines = [
        "VERİ SORUMLUSUNA BAŞVURU",
        "6698 sayılı Kişisel Verilerin Korunması Kanunu'nun 11. maddesi kapsamında",
        "",
        "Kime: Travel Planner veri sorumlusu (" + to + ")",
        "Tarih: " + today,
        "",
        "BAŞVURU SAHİBİ",
        "Ad soyad: " + val("ad"),
        "E-posta: " + val("eposta"),
        "Uygulamadaki hesap e-postası (farklıysa): " + (val("hesap") || "-"),
        "Telefon (isteğe bağlı): " + (val("telefon") || "-"),
        "Tebligata esas adres (isteğe bağlı): " + (val("adres") || "-"),
        "Uygulama ile ilişkim: " + (val("iliski") || "-"),
        "",
        "TALEPLERİM",
      ];
      talepler.forEach(function (t) { lines.push("- " + t); });
      lines.push("", "AÇIKLAMA", val("aciklama"), "");
      lines.push("Yanıtın iletilmesini istediğim yöntem: " + (val("yanit") || "E-posta"));
      lines.push("", "Yukarıdaki bilgilerin doğru olduğunu ve başvurunun bana ait kişisel verilere ilişkin olduğunu beyan ederim.", "", "Ad soyad / imza: " + val("ad"));
      var body = lines.join("\n");
      pre.textContent = body;
      var subject = "KVKK Başvurusu - " + val("ad");
      mail.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      out.classList.add("show");
      out.scrollIntoView({ behavior: "smooth", block: "start" });
      copyBtn.onclick = function () { copyText(body, copyBtn); };
      printBtn.onclick = function () { window.print(); };
    });
  }
})();

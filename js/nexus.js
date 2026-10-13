/* Ink & Equity — Nexus behaviour. Plain JS, no dependencies.
   Everything here is enhancement: the site reads and works with this file switched off. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(pointer: fine)").matches;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var clamp = function (n, a, b) { return Math.max(a, Math.min(b, n)); };

  /* ---------- toast ---------- */
  var toastEl = $("#toast"), toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  }

  /* ---------- theme, with an ink spill from the button ---------- */
  var themeBtn = $("#theme");
  var meta = $('meta[name="theme-color"]');
  function paintTheme(t) {
    root.dataset.theme = t;
    paintMeta();
    if (themeBtn) themeBtn.setAttribute("aria-pressed", String(t === "light"));
  }
  paintTheme(root.dataset.theme || "dark");

  /* ---------- colour theme: Theme Studio ---------- */
  var PALETTES = ["ink", "noir", "emerald", "burgundy"];
  var paletteSelects = doc.querySelectorAll("[data-palette-select]");
  function paintMeta() {
    if (meta) meta.setAttribute("content", getComputedStyle(root).getPropertyValue("--bg").trim() || "#0a0f2e");
  }
  function paintPalette(p) {
    if (PALETTES.indexOf(p) < 0) p = "ink";
    if (p === "ink") delete root.dataset.palette; else root.dataset.palette = p;
    for (var i = 0; i < paletteSelects.length; i++) paletteSelects[i].value = p;
    paintMeta();
  }
  paintPalette(store.get("ie-palette") || "ink");
  for (var s = 0; s < paletteSelects.length; s++) {
    paletteSelects[s].addEventListener("change", function (e) {
      store.set("ie-palette", e.target.value);
      paintPalette(e.target.value);
    });
  }
  if (themeBtn) themeBtn.addEventListener("click", function (e) {
    var next = root.dataset.theme === "light" ? "dark" : "light";
    store.set("ie-theme", next);
    if (!doc.startViewTransition || reduce) { paintTheme(next); return; }
    var r = themeBtn.getBoundingClientRect();
    var x = r.left + r.width / 2, y = r.top + r.height / 2;
    var radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var vt = doc.startViewTransition(function () { paintTheme(next); });
    vt.ready.then(function () {
      root.animate(
        { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + radius + "px at " + x + "px " + y + "px)"] },
        { duration: 750, easing: "cubic-bezier(.2,.8,.2,1)", pseudoElement: "::view-transition-new(root)" }
      );
    }).catch(function () {});
  });

  /* ---------- mobile menu ---------- */
  var menuBtn = $("#menu"), nav = $("#nav");
  if (menuBtn && nav) {
    var setMenu = function (open) {
      nav.classList.toggle("open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
    };
    menuBtn.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    doc.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  }

  /* ---------- pointer: lantern on the lattice ---------- */
  var px = innerWidth * 0.62, py = innerHeight * 0.3, pointerQueued = false, hooks = [];
  function frame() {
    pointerQueued = false;
    root.style.setProperty("--mx", px + "px");
    root.style.setProperty("--my", py + "px");
    hooks.forEach(function (h) { h(px, py); });
  }
  function ask() { if (!pointerQueued) { pointerQueued = true; requestAnimationFrame(frame); } }
  if (fine && !reduce) {
    addEventListener("pointermove", function (e) { px = e.clientX; py = e.clientY; ask(); }, { passive: true });
  }
  ask();

  /* ---------- ink-bleed headline ---------- */
  var h = $("[data-ink]");
  if (h) {
    var text = h.textContent.trim();
    h.setAttribute("aria-label", text);
    h.textContent = "";
    var n = 0, chars = [];
    text.split(" ").forEach(function (w, wi, all) {
      var word = doc.createElement("span");
      word.className = "word"; word.setAttribute("aria-hidden", "true");
      w.split("").forEach(function (c) {
        var s = doc.createElement("span");
        s.className = "ch"; s.textContent = c; s.style.setProperty("--i", n++);
        word.appendChild(s); chars.push(s);
      });
      h.appendChild(word);
      if (wi < all.length - 1) h.appendChild(doc.createTextNode(" "));
    });
    requestAnimationFrame(function () { h.classList.add("armed"); });
    if (!reduce) {
      var centres = [];
      var measure = function () {
        /* pin each letter to its resting width so the variable-font axes cannot reflow the headline */
        chars.forEach(function (c) {
          c.style.width = ""; c.style.removeProperty("--b"); c.style.removeProperty("--s"); c.style.removeProperty("--k");
        });
        var widths = chars.map(function (c) { return c.getBoundingClientRect().width; });
        chars.forEach(function (c, i) { c.style.width = widths[i] + "px"; });
        centres = chars.map(function (c) {
          var r = c.getBoundingClientRect();
          return { x: r.left + r.width / 2 + scrollX, y: r.top + r.height / 2 + scrollY };
        });
      };
      var bleed = function (x, y) {
        var X = x + scrollX, Y = y + scrollY;
        for (var i = 0; i < chars.length; i++) {
          var d = Math.hypot(centres[i].x - X, centres[i].y - Y);
          var b = clamp(1 - d / 170, 0, 1); b = b * b;
          var el = chars[i];
          if (b < 0.01) { if (el._b) { el._b = 0; el.style.removeProperty("--b"); el.style.removeProperty("--s"); el.style.removeProperty("--k"); } continue; }
          el._b = b;
          el.style.setProperty("--b", b.toFixed(2));
          el.style.setProperty("--s", Math.round(b * 100));
          el.style.setProperty("--k", b > 0.45 ? 1 : 0);
        }
      };
      var ready = false;
      var arm = function () { measure(); ready = true; };
      setTimeout(arm, 1800);
      addEventListener("resize", function () { if (ready) measure(); });
      if (fine) hooks.push(function (x, y) { if (ready) bleed(x, y); });
      /* one pass of the pen across the headline, so touch screens see it too */
      setTimeout(function () {
        if (!ready) measure();
        var box = h.getBoundingClientRect();
        var t0 = performance.now(), dur = 1700;
        (function sweep(t) {
          var k = clamp((t - t0) / dur, 0, 1);
          bleed(box.left + box.width * (-0.05 + 1.1 * k), box.top + box.height * (0.45 + 0.18 * Math.sin(k * 6)));
          if (k < 1) requestAnimationFrame(sweep);
          else chars.forEach(function (el) { el._b = 0; el.style.removeProperty("--b"); el.style.removeProperty("--s"); el.style.removeProperty("--k"); });
        })(t0);
      }, 1900);
    }
  }

  /* ---------- scroll progress, sequences, arches ---------- */
  var bar = $(".progress"), seqs = $$(".steps, .timeline"), scrollQueued = false;
  function onScroll() {
    scrollQueued = false;
    var max = root.scrollHeight - innerHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? clamp(scrollY / max, 0, 1) : 0) + ")";
    seqs.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = clamp((innerHeight * 0.72 - r.top) / Math.max(r.height, 1), 0, 1);
      el.style.setProperty("--p", p.toFixed(3));
      if (el.classList.contains("timeline")) {
        $$("li", el).forEach(function (li) {
          li.classList.toggle("on", li.getBoundingClientRect().top < innerHeight * 0.72);
        });
      }
    });
  }
  addEventListener("scroll", function () { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener("resize", onScroll);
  onScroll();

  var arches = $$(".arch");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("open"); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    arches.forEach(function (a) { io.observe(a); });
  } else {
    arches.forEach(function (a) { a.classList.add("open"); });
  }

  /* ---------- homepage sections: fade and rise on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); rio.unobserve(e.target); } });
    }, { threshold: 0.08 });
    reveals.forEach(function (r) { rio.observe(r); });
  } else {
    reveals.forEach(function (r) { r.classList.add("in"); });
  }

  /* ---------- the scales: tap to add a weight ---------- */
  $$(".scales-btn").forEach(function (btn) {
    var svg = $(".scales", btn), cap = btn.parentNode.querySelector(".scales-cap");
    var beam = $(".beam", svg), pl = $(".panl", svg), pr = $(".panr", svg);
    var l = 0, r = 0, balances = 0;
    var lines = ["Balanced. Tap again.", "Balanced again.", "Both sides, equally.", "Still level."];
    function place() {
      var a = (r - l) * 9, rad = a * Math.PI / 180, c = Math.cos(rad) * 130, s = Math.sin(rad) * 130;
      beam.style.transform = "rotate(" + a + "deg)";
      pl.style.transform = "translate(" + (200 - c) + "px," + (70 - s) + "px)";
      pr.style.transform = "translate(" + (200 + c) + "px," + (70 + s) + "px)";
    }
    function weight(pan, idx) {
      var g = doc.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "weight");
      var x = (idx - 1) * 34;
      g.innerHTML = '<circle cx="' + x + '" cy="106" r="15"/><text x="' + x + '" y="112">§</text>';
      pan.appendChild(g);
      if (g.animate && !reduce) g.animate([{ transform: "translateY(-150px)", opacity: 0 }, { transform: "translateY(0)", opacity: 1 }], { duration: 520, easing: "cubic-bezier(.3,1.4,.5,1)" });
      return g;
    }
    function reset() {
      $$(".weight", svg).forEach(function (w) { w.remove(); });
      l = r = 0; place();
    }
    place();
    btn.addEventListener("click", function () {
      if (l + r >= 6) { reset(); cap.textContent = "Cleared. Tap to begin again."; svg.classList.remove("balanced"); return; }
      if (l <= r) { weight(pl, l); l++; } else { weight(pr, r); r++; }
      place();
      var even = l === r;
      svg.classList.toggle("balanced", even);
      if (even) { cap.textContent = lines[Math.min(balances++, lines.length - 1)]; }
      else cap.textContent = "One side weighs more.";
    });
  });

  /* ---------- footer maxims ---------- */
  var maxim = $("#maxim");
  if (maxim) {
    var list = [
      ["Audi alteram partem.", "Hear the other side."],
      ["Nemo judex in causa sua.", "No one should be a judge in their own cause."],
      ["Ubi jus ibi remedium.", "Where there is a right, there is a remedy."],
      ["Lex non cogit ad impossibilia.", "The law does not compel the impossible."],
      ["Actus non facit reum nisi mens sit rea.", "An act is not guilty unless the mind is guilty."],
      ["Justitia nemini neganda est.", "Justice is to be denied to no one."]
    ];
    var gloss = $("#maxim-gloss"), i = 0, typing;
    maxim.addEventListener("click", function () {
      i = (i + 1) % list.length;
      var pair = list[i];
      if (gloss) gloss.textContent = pair[1];
      clearInterval(typing);
      if (reduce) { maxim.textContent = pair[0]; return; }
      var k = 0; maxim.textContent = "";
      typing = setInterval(function () {
        maxim.textContent = pair[0].slice(0, ++k);
        if (k >= pair[0].length) clearInterval(typing);
      }, 38);
    });
  }

  /* ---------- notice (information only) ---------- */
  var notice = $("#notice");
  if (notice && store.get("ie-notice") !== "1") {
    notice.hidden = false;
    var ok = $("#notice-ok");
    if (ok) ok.addEventListener("click", function () { store.set("ie-notice", "1"); notice.hidden = true; });
  }

  /* ---------- quirks ---------- */
  function rain() {
    if (reduce) { toast("Order, order."); return; }
    for (var k = 0; k < 42; k++) {
      var s = doc.createElement("span");
      s.className = "rain"; s.textContent = "§"; s.setAttribute("aria-hidden", "true");
      s.style.left = Math.random() * 100 + "vw";
      s.style.fontSize = 14 + Math.random() * 30 + "px";
      s.style.animationDuration = 2.2 + Math.random() * 2.2 + "s";
      s.style.animationDelay = Math.random() * 0.9 + "s";
      doc.body.appendChild(s);
      setTimeout(function (el) { el.remove(); }.bind(null, s), 6000);
    }
    toast("Order, order.");
  }
  var code = "ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,b,a".split(","), pos = 0;
  addEventListener("keydown", function (e) {
    var key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    pos = key === code[pos] ? pos + 1 : (key === code[0] ? 1 : 0);
    if (pos === code.length) { pos = 0; rain(); }
  });
  var logo = $(".logo"), taps = 0, tapTimer;
  if (logo) logo.addEventListener("click", function (e) {
    taps++; clearTimeout(tapTimer);
    tapTimer = setTimeout(function () { taps = 0; }, 900);
    if (taps >= 5) { taps = 0; e.preventDefault(); rain(); }
  });

  var title = doc.title;
  doc.addEventListener("visibilitychange", function () {
    doc.title = doc.hidden ? "Court is in recess" : title;
  });

  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();

  if (window.console && console.log) {
    console.log("%c Ink & Equity ", "background:#0a0f2e;color:#f1ead9;font:600 18px Georgia,serif;padding:6px 10px;border-radius:6px");
    console.log("Reading the source? It is plain HTML, CSS and a little JavaScript. Try the Konami code, or tap the logo five times.");
  }
})();

(function () {
  var q = document.getElementById("lib-q"); if (!q) return;
  var rows = [].slice.call(document.querySelectorAll("table.lib tbody tr"));
  var chips = [].slice.call(document.querySelectorAll(".chip")), area = "";
  var count = document.getElementById("lib-count");
  function run() {
    var t = q.value.trim().toLowerCase(), n = 0;
    rows.forEach(function (r) {
      var ok = (!area || r.getAttribute("data-area") === area) && (!t || r.getAttribute("data-text").indexOf(t) > -1);
      r.hidden = !ok; if (ok) n++;
    });
    count.textContent = n + " of " + rows.length + " shown";
  }
  chips.forEach(function (c) { c.addEventListener("click", function () {
    area = c.getAttribute("data-area");
    chips.forEach(function (o) { o.setAttribute("aria-pressed", o === c ? "true" : "false"); });
    run();
  }); });
  q.addEventListener("input", run); run();
})();

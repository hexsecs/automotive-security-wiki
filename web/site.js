(function () {
  var root = document.documentElement;

  // Theme switch: cycles to the opposite of what is currently showing.
  var sw = document.getElementById("theme-switch");
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function label() {
    if (!sw) return;
    sw.querySelector(".sw-label").textContent = isDark() ? "Dark" : "Light";
    sw.setAttribute("aria-pressed", isDark() ? "true" : "false");
  }
  if (sw) {
    label();
    sw.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("asr-theme", next); } catch (e) {}
      label();
    });
  }

  // Dial readout follows the hovered or focused station.
  document.querySelectorAll(".dial").forEach(function (dial) {
    var out = dial.querySelector(".readout");
    if (!out) return;
    var d = out.querySelector(".r-date"), l = out.querySelector(".r-lead"), c = out.querySelector(".r-conf");
    var initial = [d.textContent, l.textContent, c.textContent];
    function show(a) { d.textContent = a.dataset.date; l.textContent = a.dataset.lead; c.textContent = a.dataset.conf; }
    function reset() { d.textContent = initial[0]; l.textContent = initial[1]; c.textContent = initial[2]; }
    dial.querySelectorAll(".st").forEach(function (a) {
      a.addEventListener("mouseenter", function () { show(a); });
      a.addEventListener("focus", function () { show(a); });
      a.addEventListener("mouseleave", reset);
      a.addEventListener("blur", reset);
    });
  });

  // Archive filters.
  var archive = document.getElementById("archive");
  if (archive) {
    var fs = document.getElementById("f-signal"), fc = document.getElementById("f-conf"), count = document.getElementById("f-count");
    function apply() {
      var sig = fs.getAttribute("aria-pressed") === "true", conf = fc.getAttribute("aria-pressed") === "true", n = 0;
      archive.querySelectorAll(".row").forEach(function (r) {
        var hide = (sig && r.dataset.quiet === "1") || (conf && +r.dataset.conf < 4);
        r.hidden = hide; if (!hide) n++;
      });
      archive.querySelectorAll(".month").forEach(function (m) {
        var el = m.nextElementSibling, any = false;
        while (el && !el.classList.contains("month")) { if (!el.hidden) any = true; el = el.nextElementSibling; }
        m.hidden = !any;
      });
      count.textContent = n + " shown";
    }
    [fs, fc].forEach(function (b) {
      b.addEventListener("click", function () {
        b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
        apply();
      });
    });
  }

  // Source type filter (one at a time).
  var rows = document.getElementById("src-rows");
  if (rows) {
    var btns = document.querySelectorAll(".src-f"), sc = document.getElementById("s-count");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var on = b.getAttribute("aria-pressed") !== "true";
        btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        if (on) b.setAttribute("aria-pressed", "true");
        var n = 0;
        rows.querySelectorAll("tr").forEach(function (tr) {
          var hide = on && tr.dataset.type !== b.dataset.type;
          tr.hidden = hide; if (!hide) n++;
        });
        sc.textContent = n + " records";
      });
    });
  }
})();

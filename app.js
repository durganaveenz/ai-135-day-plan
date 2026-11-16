(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // ---- persistence (all wrapped: storage may be unavailable) ----
  var state = {};
  try { state = JSON.parse(localStorage.getItem("roadmap-progress") || "{}"); } catch (e) {}
  function save() { try { localStorage.setItem("roadmap-progress", JSON.stringify(state)); } catch (e) {} }

  // ---- theme ----
  var root = document.documentElement;
  try { var t = localStorage.getItem("roadmap-theme"); if (t) root.setAttribute("data-theme", t); } catch (e) {}
  $("#themeBtn").addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme:dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("roadmap-theme", next); } catch (e) {}
  });

  // ---- checkboxes + progress ----
  var boxes = $$("input[type=checkbox][data-id]");
  boxes.forEach(function (cb) {
    cb.checked = !!state[cb.dataset.id];
    cb.addEventListener("click", function (e) { e.stopPropagation(); });
    cb.addEventListener("change", function () {
      if (cb.checked) state[cb.dataset.id] = 1; else delete state[cb.dataset.id];
      save(); refresh();
    });
  });
  $$("label.done").forEach(function (l) { l.addEventListener("click", function (e) { e.stopPropagation(); }); });

  function refresh() {
    var overallDone = 0, overallTotal = 0;
    $$("section.phase").forEach(function (ph) {
      var secs = $$("details.topic .sec-done", ph);
      var done = secs.filter(function (c) { return c.checked; }).length;
      overallDone += done; overallTotal += secs.length;
      var pct = secs.length ? Math.round(done / secs.length * 100) : 0;
      $$("[data-bar='" + ph.id + "']").forEach(function (b) { b.style.width = pct + "%"; });
    });
    $$("details.topic").forEach(function (d) {
      var c = $(".sec-done", d);
      d.classList.toggle("done-topic", !!(c && c.checked));
    });
    var all = overallTotal ? Math.round(overallDone / overallTotal * 100) : 0;
    $$("[data-bar='all']").forEach(function (b) { b.style.width = all + "%"; });
    $("#overallText").textContent = overallDone + " / " + overallTotal + " days done (" + all + "%)";
  }

  // ---- routing ----
  var phases = $$("section.phase"), home = $("#home");
  function route() {
    var id = (location.hash || "#home").slice(1);
    var target = phases.filter(function (p) { return p.id === id; })[0];
    home.hidden = !!target;
    phases.forEach(function (p) { p.hidden = p !== target; });
    $$("nav a").forEach(function (a) { a.classList.toggle("active", a.dataset.nav === id); });
    document.body.classList.remove("menu-open");
    if (!$("#search").value) window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", function () { $("#search").value = ""; runSearch(); route(); });

  $("#menuBtn").addEventListener("click", function () { document.body.classList.toggle("menu-open"); });

  // ---- search (across all phases) ----
  var topics = $$("details.topic");
  var cache = topics.map(function (d) { return d.textContent.toLowerCase(); });
  function clearMarks() {
    $$("mark").forEach(function (m) { m.replaceWith(document.createTextNode(m.textContent)); });
  }
  function runSearch() {
    var q = $("#search").value.trim().toLowerCase();
    var info = $("#searchInfo");
    clearMarks();
    if (!q) {
      topics.forEach(function (d) { d.classList.remove("hidden-by-search"); });
      $$(".divider").forEach(function (d) { d.classList.remove("hidden-by-search"); });
      info.textContent = "";
      route();
      return;
    }
    home.hidden = true;
    phases.forEach(function (p) { p.hidden = false; });
    $$("nav a").forEach(function (a) { a.classList.remove("active"); });
    var hits = 0;
    topics.forEach(function (d, i) {
      var match = cache[i].indexOf(q) !== -1;
      d.classList.toggle("hidden-by-search", !match);
      if (match) { hits++; d.open = true; highlight(d, q); }
    });
    $$(".divider, .phase-head, .phase>.callout, .phase>p, .phase>ul, .phase>h4").forEach(function (el) {
      el.classList.add("hidden-by-search");
    });
    phases.forEach(function (p) {
      var any = $$("details.topic:not(.hidden-by-search)", p).length;
      p.hidden = !any;
    });
    info.textContent = hits ? hits + " matching topic" + (hits > 1 ? "s" : "") : "No matches";
  }
  function highlight(el, q) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) {
      if (n.parentNode.closest("summary label,script,style")) continue;
      if (n.nodeValue.toLowerCase().indexOf(q) !== -1) nodes.push(n);
    }
    nodes.slice(0, 40).forEach(function (node) {
      var text = node.nodeValue, lower = text.toLowerCase(), i = lower.indexOf(q);
      var frag = document.createDocumentFragment(), last = 0;
      while (i !== -1) {
        frag.appendChild(document.createTextNode(text.slice(last, i)));
        var m = document.createElement("mark"); m.textContent = text.slice(i, i + q.length);
        frag.appendChild(m);
        last = i + q.length; i = lower.indexOf(q, last);
      }
      frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }
  var timer;
  $("#search").addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(runSearch, 150); });

  refresh();
  route();
})();

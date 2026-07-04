/* Hinata Docs — client interactivity: theme, mobile nav, ⌘K search, copy, scrollspy */
(function () {
  "use strict";
  var CFG = window.HINATA || { lang: "en", noResults: "No results", copy: "Copy", copied: "Copied!" };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- Year ---- */
  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();

  /* ---- Theme ---- */
  var themeBtn = $("#themeToggle");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("hinata-theme", next); } catch (e) {}
  });

  /* ---- Mobile sidebar ---- */
  var sidebar = $("#sidebar"), scrim = $("#scrim"), menuBtn = $("#menuToggle");
  function closeNav() { if (sidebar) sidebar.classList.remove("open"); if (scrim) scrim.classList.remove("open"); }
  function toggleNav() {
    if (!sidebar) return;
    sidebar.classList.toggle("open");
    if (scrim) scrim.classList.toggle("open");
  }
  if (menuBtn) menuBtn.addEventListener("click", toggleNav);
  if (scrim) scrim.addEventListener("click", closeNav);
  $$(".nav-link").forEach(function (a) { a.addEventListener("click", closeNav); });

  /* ---- Copy buttons on code blocks ---- */
  var COPY_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
  var CHECK_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  $$(".prose pre, .prose .codehilite").forEach(function (block) {
    if (block.parentElement && block.parentElement.classList.contains("codehilite")) return;
    var code = block.querySelector("code") || block.querySelector("pre");
    if (!code) return;
    var btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.type = "button";
    btn.innerHTML = COPY_SVG + "<span>" + CFG.copy + "</span>";
    btn.addEventListener("click", function () {
      var text = code.innerText;
      navigator.clipboard.writeText(text).then(function () {
        btn.classList.add("copied");
        btn.innerHTML = CHECK_SVG + "<span>" + CFG.copied + "</span>";
        setTimeout(function () {
          btn.classList.remove("copied");
          btn.innerHTML = COPY_SVG + "<span>" + CFG.copy + "</span>";
        }, 1600);
      });
    });
    block.appendChild(btn);
  });

  /* ---- TOC scroll-spy ---- */
  var tocLinks = $$(".toc-list a");
  if (tocLinks.length) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute("href").slice(1));
      var el = document.getElementById(id);
      if (el) map[id] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          var a = map[en.target.id];
          if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* ---- Search palette ---- */
  var modal = $("#searchModal"), input = $("#searchInput"),
      results = $("#searchResults"), trigger = $("#searchTrigger"),
      searchScrim = $("#searchScrim");
  var INDEX = null, activeIdx = -1, current = [];

  function loadIndex() {
    if (INDEX) return Promise.resolve(INDEX);
    return fetch("/search-index.json").then(function (r) { return r.json(); }).then(function (data) {
      INDEX = data.filter(function (d) { return d.lang === CFG.lang; });
      return INDEX;
    }).catch(function () { INDEX = []; return INDEX; });
  }
  function openSearch() {
    if (!modal) return;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    loadIndex().then(function () { input.focus(); input.select(); });
  }
  function closeSearch() {
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    activeIdx = -1;
  }
  function esc(s) { return s.replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function highlight(text, q) {
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if (i < 0) return esc(text.slice(0, 120));
    var start = Math.max(0, i - 40);
    var snip = (start > 0 ? "…" : "") + text.slice(start, i + q.length + 80);
    return esc(snip).replace(new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
  }
  function render(q) {
    if (!q) { results.innerHTML = '<p class="search-empty">' + (document.querySelector(".search-empty") ? "" : "") + '</p>'; renderEmpty(); return; }
    var ql = q.toLowerCase();
    var scored = [];
    (INDEX || []).forEach(function (d) {
      var t = d.title.toLowerCase(), score = 0;
      if (t.indexOf(ql) >= 0) score += 10;
      if (t.indexOf(ql) === 0) score += 8;
      if ((d.desc || "").toLowerCase().indexOf(ql) >= 0) score += 4;
      if (d.text.toLowerCase().indexOf(ql) >= 0) score += 2;
      if (score > 0) scored.push({ d: d, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    current = scored.slice(0, 12).map(function (s) { return s.d; });
    activeIdx = current.length ? 0 : -1;
    if (!current.length) { results.innerHTML = '<p class="search-empty">' + esc(CFG.noResults) + '</p>'; return; }
    results.innerHTML = current.map(function (d, i) {
      var body = (d.text || "").toLowerCase().indexOf(ql) >= 0 ? d.text : (d.desc || d.text);
      return '<a class="search-result' + (i === 0 ? " active" : "") + '" href="' + d.url + '" data-i="' + i + '">' +
        '<div class="sr-group">' + esc(d.group) + '</div>' +
        '<div class="sr-title">' + esc(d.title) + '</div>' +
        '<div class="sr-snippet">' + highlight(body, q) + '</div></a>';
    }).join("");
    $$(".search-result", results).forEach(function (el) {
      el.addEventListener("mousemove", function () { setActive(parseInt(el.getAttribute("data-i"), 10)); });
    });
  }
  function renderEmpty() {
    var msg = results.getAttribute("data-empty") || "";
    results.innerHTML = '<p class="search-empty">' + msg + "</p>";
  }
  function setActive(i) {
    activeIdx = i;
    $$(".search-result", results).forEach(function (el, idx) { el.classList.toggle("active", idx === i); });
  }

  if (results) {
    var initial = $(".search-empty");
    if (initial) results.setAttribute("data-empty", initial.textContent);
  }
  if (trigger) trigger.addEventListener("click", openSearch);
  if (searchScrim) searchScrim.addEventListener("click", closeSearch);
  if (input) input.addEventListener("input", function () { render(input.value.trim()); });
  if (input) input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); if (current.length) setActive((activeIdx + 1) % current.length); scrollActive(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); if (current.length) setActive((activeIdx - 1 + current.length) % current.length); scrollActive(); }
    else if (e.key === "Enter") { if (activeIdx >= 0 && current[activeIdx]) window.location.href = current[activeIdx].url; }
  });
  function scrollActive() {
    var el = $$(".search-result", results)[activeIdx];
    if (el) el.scrollIntoView({ block: "nearest" });
  }

  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); modal && modal.classList.contains("open") ? closeSearch() : openSearch(); }
    else if (e.key === "Escape") { closeSearch(); closeNav(); }
    else if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") { e.preventDefault(); openSearch(); }
  });
})();

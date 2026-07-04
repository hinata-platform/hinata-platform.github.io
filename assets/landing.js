/* Hinata landing — theme toggle + bilingual (data-en/data-de) switch */
(function () {
  "use strict";
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  var themeBtn = document.getElementById("themeToggle");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("hinata-theme", next); } catch (e) {}
  });

  function apply(lang) {
    document.documentElement.setAttribute("lang", lang);
    var nodes = document.querySelectorAll("[data-en]");
    for (var i = 0; i < nodes.length; i++) {
      var v = nodes[i].getAttribute("data-" + lang);
      if (v != null) nodes[i].textContent = v;
    }
    var label = document.getElementById("langLabel");
    if (label) label.textContent = lang.toUpperCase();
    try { localStorage.setItem("hinata-lang", lang); } catch (e) {}
  }

  var stored = null;
  try { stored = localStorage.getItem("hinata-lang"); } catch (e) {}
  var initial = stored || ((navigator.language || "en").toLowerCase().indexOf("de") === 0 ? "de" : "en");
  apply(initial);

  var langBtn = document.getElementById("langSwitch");
  if (langBtn) langBtn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("lang");
    apply(cur === "de" ? "en" : "de");
  });
})();

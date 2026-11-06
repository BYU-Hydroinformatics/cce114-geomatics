// Feedback tab: build the mailto at click time (so the address is not sitting in the page
// source for scrapers) and close the menu on an outside click or Escape.
(function () {
  function init() {
    var tab = document.querySelector(".feedback-tab");
    if (!tab) { return; }
    var mail = tab.querySelector(".feedback-tab__mail");
    if (mail) {
      mail.addEventListener("click", function (e) {
        e.preventDefault();
        window.location.href = "mailto:" + mail.dataset.u + "@" + mail.dataset.d +
          "?subject=" + mail.dataset.s;
      });
    }
    document.addEventListener("click", function (e) { if (!tab.contains(e.target)) { tab.open = false; } });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { tab.open = false; } });
  }
  if (typeof document$ !== "undefined") { document$.subscribe(init); } else { document.addEventListener("DOMContentLoaded", init); }
})();

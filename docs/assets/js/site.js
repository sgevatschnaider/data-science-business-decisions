(function () {
  "use strict";

  var STORAGE_KEY = "datos-decisiones-progress";
  var THEME_KEY = "datos-decisiones-theme";
  var RESOURCE_ORDER = ["guia", "simulacion", "notebook", "cuestionario", "glosario"];

  function readProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (error) {
      return {};
    }
  }

  function writeProgress(progress) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (error) {
      return;
    }
    document.dispatchEvent(new CustomEvent("course-progress-change"));
  }

  function setComplete(key, complete) {
    var progress = readProgress();
    if (complete) {
      progress[key] = true;
    } else {
      delete progress[key];
    }
    writeProgress(progress);
  }

  function isComplete(key) {
    return Boolean(readProgress()[key]);
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    document.querySelectorAll(".theme-toggle").forEach(function (button) {
      button.textContent = theme === "dark" ? "Tema claro" : "Tema oscuro";
      button.setAttribute(
        "aria-label",
        theme === "dark" ? "Activar tema claro" : "Activar tema oscuro"
      );
    });
  }

  function initTheme() {
    var saved = null;
    try {
      saved = localStorage.getItem(THEME_KEY);
    } catch (error) {
      saved = null;
    }
    var preferred = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
    applyTheme(saved || preferred);
    document.querySelectorAll(".theme-toggle").forEach(function (button) {
      button.addEventListener("click", function () {
        var next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        try {
          localStorage.setItem(THEME_KEY, next);
        } catch (error) {
          applyTheme(next);
          return;
        }
        applyTheme(next);
      });
    });
  }

  function initNavigation() {
    var toggle = document.querySelector(".nav-toggle");
    var navigation = document.querySelector(".site-nav");
    if (!toggle || !navigation) return;
    toggle.addEventListener("click", function () {
      var open = navigation.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "Cerrar" : "Menú";
    });
    navigation.addEventListener("click", function (event) {
      if (event.target.tagName !== "A") return;
      navigation.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "Menú";
    });
  }

  function initModuleSearch() {
    var input = document.querySelector("[data-module-search]");
    if (!input) return;
    var cards = Array.from(document.querySelectorAll("[data-module-card]"));
    var status = document.querySelector("[data-module-count]");
    input.addEventListener("input", function () {
      var query = input.value.trim().toLocaleLowerCase("es");
      var visible = 0;
      cards.forEach(function (card) {
        var match = !query || card.dataset.search.includes(query);
        card.hidden = !match;
        if (match) visible += 1;
      });
      document.querySelectorAll(".course-unit").forEach(function (unit) {
        unit.hidden = !unit.querySelector("[data-module-card]:not([hidden])");
      });
      if (status) {
        status.textContent = visible === 1 ? "1 módulo encontrado" : visible + " módulos encontrados";
      }
    });
  }

  function completedCount() {
    var progress = readProgress();
    return Object.keys(progress).filter(function (key) {
      return progress[key] === true && /^\d{2}:(guia|simulacion|notebook|cuestionario|glosario)$/.test(key);
    }).length;
  }

  function updateGlobalProgress() {
    var total = 15 * RESOURCE_ORDER.length;
    var completed = completedCount();
    var percent = Math.round((completed / total) * 100);
    document.querySelectorAll("[data-global-progress]").forEach(function (element) {
      element.textContent = percent + "%";
    });
    document.querySelectorAll("[data-global-progress-bar]").forEach(function (element) {
      element.style.width = percent + "%";
    });
  }

  function resourcePath(module, resource) {
    var file = {
      guia: "index.html",
      simulacion: "simulacion.html",
      notebook: null,
      cuestionario: "cuestionario.html",
      glosario: "glosario.html"
    }[resource];
    if (resource === "notebook") {
      return "https://colab.research.google.com/github/sgevatschnaider/" +
        "data-science-business-decisions/blob/main/notebooks/" + module.slug + ".ipynb";
    }
    return "modulos/" + module.slug + "/" + file;
  }

  function initResume() {
    var button = document.querySelector("[data-resume]");
    if (!button || !window.COURSE_DATA) return;
    button.addEventListener("click", function () {
      var modules = window.COURSE_DATA.modules;
      for (var i = 0; i < modules.length; i += 1) {
        for (var j = 0; j < RESOURCE_ORDER.length; j += 1) {
          var key = modules[i].id + ":" + RESOURCE_ORDER[j];
          if (!isComplete(key)) {
            window.location.href = resourcePath(modules[i], RESOURCE_ORDER[j]);
            return;
          }
        }
      }
      window.location.href = "proyecto-integrador.html";
    });
  }

  window.CourseProgress = {
    read: readProgress,
    write: writeProgress,
    setComplete: setComplete,
    isComplete: isComplete,
    resources: RESOURCE_ORDER.slice()
  };

  initTheme();
  initNavigation();
  initModuleSearch();
  initResume();
  updateGlobalProgress();
  document.addEventListener("course-progress-change", updateGlobalProgress);
})();

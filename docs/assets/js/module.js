(function () {
  "use strict";

  var body = document.body;
  var moduleId = body.dataset.moduleId;
  var pageKind = body.dataset.pageKind;
  var progress = window.CourseProgress;

  function progressKey(resource) {
    return moduleId + ":" + resource;
  }

  function markVisit() {
    if (!progress || !moduleId) return;
    var mapping = {
      index: "guia",
      simulacion: "simulacion",
      cuestionario: "cuestionario",
      glosario: "glosario"
    };
    if (mapping[pageKind]) {
      progress.setComplete(progressKey(mapping[pageKind]), true);
    }
  }

  function updateModuleProgress() {
    if (!progress || !moduleId) return;
    var resourceKeys = Array.from(
      document.querySelectorAll("[data-progress-item]")
    ).map(function (checkbox) {
      return checkbox.dataset.progressItem;
    });
    if (!resourceKeys.length) {
      resourceKeys = progress.resources.map(progressKey);
    }
    var completed = resourceKeys.filter(function (resourceKey) {
      return progress.isComplete(resourceKey);
    }).length;
    document.querySelectorAll("[data-module-progress]").forEach(function (element) {
      element.textContent = String(completed);
    });
    document.querySelectorAll("[data-module-progress-bar]").forEach(function (element) {
      element.style.width = Math.round((completed / resourceKeys.length) * 100) + "%";
    });
  }

  function initChecklist() {
    if (!progress || !moduleId) return;
    document.querySelectorAll("[data-progress-item]").forEach(function (checkbox) {
      checkbox.checked = progress.isComplete(checkbox.dataset.progressItem);
      checkbox.addEventListener("change", function () {
        progress.setComplete(checkbox.dataset.progressItem, checkbox.checked);
        updateModuleProgress();
      });
    });
  }

  function initGlossary() {
    var input = document.querySelector("[data-glossary-search]");
    if (!input) return;
    var entries = Array.from(document.querySelectorAll("[data-glossary-entry]"));
    var count = document.querySelector("[data-glossary-count]");
    input.addEventListener("input", function () {
      var query = input.value.trim().toLocaleLowerCase("es");
      var visible = 0;
      entries.forEach(function (entry) {
        var match = !query || entry.dataset.search.includes(query);
        entry.hidden = !match;
        if (match) visible += 1;
      });
      if (count) {
        count.textContent = visible === 1 ? "1 término" : visible + " términos";
      }
    });
  }

  function clearQuizStyles(form) {
    form.querySelectorAll(".quiz-option").forEach(function (option) {
      option.classList.remove("correct", "incorrect");
    });
    form.querySelectorAll("[data-question-feedback]").forEach(function (feedback) {
      feedback.textContent = "";
      feedback.classList.remove("visible");
    });
    var result = document.querySelector("[data-quiz-result]");
    if (result) result.hidden = true;
  }

  function initQuiz() {
    var form = document.querySelector("[data-quiz]");
    if (!form) return;
    var questions = Array.from(form.querySelectorAll("[data-question]"));
    var result = document.querySelector("[data-quiz-result]");
    var scoreElement = document.querySelector("[data-quiz-score]");
    var messageElement = document.querySelector("[data-quiz-message]");

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearQuizStyles(form);
      var score = 0;
      var unanswered = 0;

      questions.forEach(function (question) {
        var selected = question.querySelector("input:checked");
        var correctValue = question.dataset.answer;
        var feedback = question.querySelector("[data-question-feedback]");
        question.querySelectorAll(".quiz-option").forEach(function (label) {
          var option = label.querySelector("input");
          if (option.value === correctValue) label.classList.add("correct");
        });
        if (!selected) {
          unanswered += 1;
          feedback.textContent = "Seleccioná una opción. " + question.dataset.explanation;
        } else if (selected.value === correctValue) {
          score += 1;
          feedback.textContent = "Correcto. " + question.dataset.explanation;
        } else {
          selected.closest(".quiz-option").classList.add("incorrect");
          feedback.textContent = "Revisá esta respuesta. " + question.dataset.explanation;
        }
        feedback.classList.add("visible");
      });

      scoreElement.textContent = score + " / " + questions.length;
      if (unanswered > 0) {
        messageElement.textContent = "Quedaron " + unanswered + " preguntas sin responder. Completalas y corregí de nuevo.";
      } else if (score >= 5) {
        messageElement.textContent = "Dominio sólido. Explicá ahora cada respuesta con un ejemplo propio.";
      } else if (score === 4) {
        messageElement.textContent = "Buen avance. Revisá las explicaciones antes de continuar.";
      } else {
        messageElement.textContent = "Volvé a la guía y al glosario, luego realizá un segundo intento.";
      }
      result.hidden = false;
      result.focus();
      if (progress && moduleId && score >= 4 && unanswered === 0) {
        progress.setComplete(progressKey("cuestionario"), true);
      }
    });

    form.addEventListener("reset", function () {
      window.setTimeout(function () {
        clearQuizStyles(form);
      }, 0);
    });
  }

  markVisit();
  initChecklist();
  initGlossary();
  initQuiz();
  updateModuleProgress();
  document.addEventListener("course-progress-change", updateModuleProgress);
})();

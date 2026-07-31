(function () {
  "use strict";

  var root = document.querySelector("[data-rnn-simulation]");
  if (!root) return;

  var timer = null;
  var currentStep = 0;
  var activeProfile = "balanced";

  var scenarios = {
    demand: {
      name: "Demanda semanal",
      description: "Cada entrada representa una demanda normalizada. La RNN combina el dato reciente con el nivel acumulado para construir contexto.",
      labels: ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7"],
      values: [0.18, 0.34, 0.55, 0.42, 0.78, 0.66, 0.84],
      defaults: { activation: "tanh", wx: 1.2, wh: 0.7, bias: -0.15, h0: 0 }
    },
    language: {
      name: "Contexto en una frase",
      description: "Los valores son representaciones didácticas de palabras. El significado del paso actual se modifica por el contexto que llega desde la izquierda.",
      labels: ["no", "fue", "malo", "pero", "mejoró", "mucho"],
      values: [-0.55, 0.08, -0.82, 0.35, 0.92, 0.58],
      defaults: { activation: "tanh", wx: 1.05, wh: 0.82, bias: 0.05, h0: 0 }
    },
    sensor: {
      name: "Señal de un sensor",
      description: "Una señal alternante permite observar si la memoria suaviza el ruido, conserva tendencia o amplifica oscilaciones.",
      labels: ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"],
      values: [0.88, 0.12, 0.82, 0.18, 0.91, 0.22, 0.76, 0.28],
      defaults: { activation: "tanh", wx: 1.15, wh: 0.62, bias: -0.08, h0: 0.1 }
    }
  };

  var profiles = {
    short: { label: "Memoria corta", wx: 1.25, wh: 0.15, bias: 0, h0: 0 },
    balanced: { label: "Equilibrada", wx: 1.15, wh: 0.72, bias: -0.08, h0: 0 },
    persistent: { label: "Persistente", wx: 0.75, wh: 1.08, bias: 0, h0: 0.15 },
    saturated: { label: "Saturación", wx: 2.35, wh: 1.35, bias: 0.65, h0: 0.35 }
  };

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function format(value, digits) {
    if (!Number.isFinite(value)) return "—";
    return new Intl.NumberFormat("es-AR", {
      minimumFractionDigits: digits === undefined ? 2 : digits,
      maximumFractionDigits: digits === undefined ? 2 : digits
    }).format(value);
  }

  function activation(kind, value) {
    if (kind === "sigmoid") return 1 / (1 + Math.exp(-value));
    if (kind === "relu") return Math.max(0, value);
    return Math.tanh(value);
  }

  function activationName(kind) {
    if (kind === "sigmoid") return "sigmoide";
    if (kind === "relu") return "ReLU";
    return "tanh";
  }

  function selectControl(id, label, options) {
    return (
      '<div class="rnn-control">' +
        '<label for="' + id + '">' + label + '</label>' +
        '<select id="' + id + '">' + options.map(function (item) {
          return '<option value="' + item[0] + '">' + item[1] + '</option>';
        }).join("") + '</select>' +
      '</div>'
    );
  }

  function rangeControl(id, label, min, max, value, step, suffix) {
    return (
      '<div class="rnn-control">' +
        '<label for="' + id + '"><span>' + label + '</span>' +
          '<output for="' + id + '" data-output="' + id + '">' + format(value, 2) + (suffix || "") + '</output>' +
        '</label>' +
        '<input id="' + id + '" type="range" min="' + min + '" max="' + max + '" value="' + value + '" step="' + step + '" data-suffix="' + (suffix || "") + '">' +
      '</div>'
    );
  }

  function buildShell() {
    root.innerHTML =
      '<div class="rnn-lab-header">' +
        '<div><h2>Laboratorio de memoria recurrente</h2><p>Todos los parámetros se actualizan en tiempo real.</p></div>' +
        '<span class="rnn-status-badge" data-status>Modo manual</span>' +
      '</div>' +
      '<div class="rnn-workbench">' +
        '<aside class="rnn-controls" aria-label="Controles de la simulación">' +
          '<div class="rnn-control-columns">' +
            '<section class="rnn-control-group">' +
              '<h3>1. Secuencia</h3>' +
              selectControl("rnn-scenario", "Caso", [["demand", "Demanda semanal"], ["language", "Contexto en una frase"], ["sensor", "Señal de sensor"]]) +
              selectControl("rnn-activation", "Activación", [["tanh", "tanh"], ["sigmoid", "Sigmoide"], ["relu", "ReLU"]]) +
              rangeControl("rnn-speed", "Velocidad", 350, 1800, 850, 50, " ms") +
            '</section>' +
            '<section class="rnn-control-group">' +
              '<h3>2. Parámetros</h3>' +
              rangeControl("rnn-wx", "Peso de entrada Wₓ", -2.5, 2.5, 1.15, 0.05, "") +
              rangeControl("rnn-wh", "Peso recurrente Wₕ", -1.5, 1.5, 0.72, 0.05, "") +
              rangeControl("rnn-bias", "Sesgo b", -1.5, 1.5, -0.08, 0.05, "") +
              rangeControl("rnn-h0", "Estado inicial h₀", -1, 1, 0, 0.05, "") +
            '</section>' +
            '<section class="rnn-control-group">' +
              '<h3>3. Experimentos</h3>' +
              '<div class="rnn-preset-grid">' + Object.keys(profiles).map(function (key) {
                return '<button class="rnn-preset-button' + (key === activeProfile ? ' is-active' : '') + '" type="button" data-profile="' + key + '">' + profiles[key].label + '</button>';
              }).join("") + '</div>' +
              '<div class="rnn-control" style="margin-top:0.9rem">' +
                '<label><span>Recorrido temporal</span></label>' +
                '<div class="rnn-transport">' +
                  '<button class="rnn-transport-button" type="button" data-action="previous" aria-label="Paso anterior">◀</button>' +
                  '<button class="rnn-transport-button primary" type="button" data-action="play">▶</button>' +
                  '<button class="rnn-transport-button" type="button" data-action="next" aria-label="Paso siguiente">▶|</button>' +
                  '<button class="rnn-transport-button" type="button" data-action="reset" aria-label="Reiniciar">↺</button>' +
                '</div>' +
              '</div>' +
            '</section>' +
          '</div>' +
        '</aside>' +
        '<div class="rnn-stage" data-stage></div>' +
      '</div>';
  }

  function getControls() {
    return {
      scenario: root.querySelector("#rnn-scenario"),
      activation: root.querySelector("#rnn-activation"),
      speed: root.querySelector("#rnn-speed"),
      wx: root.querySelector("#rnn-wx"),
      wh: root.querySelector("#rnn-wh"),
      bias: root.querySelector("#rnn-bias"),
      h0: root.querySelector("#rnn-h0")
    };
  }

  function readParameters() {
    var controls = getControls();
    return {
      scenario: controls.scenario.value,
      activation: controls.activation.value,
      speed: Number(controls.speed.value),
      wx: Number(controls.wx.value),
      wh: Number(controls.wh.value),
      bias: Number(controls.bias.value),
      h0: Number(controls.h0.value)
    };
  }

  function computeSequence(scenario, params) {
    var previous = params.h0;
    return scenario.values.map(function (input, index) {
      var inputContribution = params.wx * input;
      var memoryContribution = params.wh * previous;
      var z = inputContribution + memoryContribution + params.bias;
      var state = activation(params.activation, z);
      var row = {
        index: index,
        label: scenario.labels[index],
        input: input,
        previous: previous,
        inputContribution: inputContribution,
        memoryContribution: memoryContribution,
        biasContribution: params.bias,
        z: z,
        state: state
      };
      previous = state;
      return row;
    });
  }

  function metric(label, value) {
    return '<div class="rnn-metric"><span>' + label + '</span><strong>' + value + '</strong></div>';
  }

  function contributionRow(label, value, width, kind) {
    return (
      '<div class="rnn-contribution-row">' +
        '<div class="rnn-contribution-label"><span>' + label + '</span><strong>' + format(value, 3) + '</strong></div>' +
        '<div class="rnn-contribution-track"><div class="rnn-contribution-fill ' + kind + '" style="width:' + width + '%"></div></div>' +
      '</div>'
    );
  }

  function chartSvg(rows, activeIndex) {
    var width = 720;
    var height = 250;
    var left = 48;
    var right = 20;
    var top = 20;
    var bottom = 38;
    var plotWidth = width - left - right;
    var plotHeight = height - top - bottom;
    var maxAbs = Math.max(1, rows.reduce(function (maximum, row) {
      return Math.max(maximum, Math.abs(row.input), Math.abs(row.state));
    }, 0));

    function x(index) {
      return rows.length === 1 ? left + plotWidth / 2 : left + (index / (rows.length - 1)) * plotWidth;
    }

    function y(value) {
      return top + ((maxAbs - value) / (2 * maxAbs)) * plotHeight;
    }

    var grid = "";
    [-1, -0.5, 0, 0.5, 1].forEach(function (ratio) {
      var value = ratio * maxAbs;
      grid += '<line class="rnn-chart-grid" x1="' + left + '" y1="' + y(value) + '" x2="' + (width - right) + '" y2="' + y(value) + '"></line>';
      grid += '<text class="rnn-chart-text" x="5" y="' + (y(value) + 4) + '">' + format(value, 1) + '</text>';
    });

    var inputPoints = rows.map(function (row, index) { return x(index) + ',' + y(row.input); }).join(' ');
    var statePoints = rows.map(function (row, index) { return x(index) + ',' + y(row.state); }).join(' ');
    var circles = rows.map(function (row, index) {
      var activeClass = index === activeIndex ? ' rnn-chart-point-active' : '';
      return '<circle class="rnn-chart-point-input' + activeClass + '" cx="' + x(index) + '" cy="' + y(row.input) + '" r="4"></circle>' +
        '<circle class="rnn-chart-point-state' + activeClass + '" cx="' + x(index) + '" cy="' + y(row.state) + '" r="4.5"></circle>' +
        '<text class="rnn-chart-text" text-anchor="middle" x="' + x(index) + '" y="' + (height - 12) + '">' + row.label + '</text>';
    }).join('');

    return (
      '<svg class="rnn-chart" viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-labelledby="rnn-chart-title rnn-chart-desc">' +
        '<title id="rnn-chart-title">Entrada y estado oculto a través del tiempo</title>' +
        '<desc id="rnn-chart-desc">La línea azul representa la secuencia de entrada y la línea verde el estado oculto calculado por la RNN.</desc>' +
        grid +
        '<line class="rnn-chart-axis" x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (height - bottom) + '"></line>' +
        '<line class="rnn-chart-axis" x1="' + left + '" y1="' + y(0) + '" x2="' + (width - right) + '" y2="' + y(0) + '"></line>' +
        '<polyline class="rnn-chart-input" points="' + inputPoints + '"></polyline>' +
        '<polyline class="rnn-chart-state" points="' + statePoints + '"></polyline>' +
        circles +
      '</svg>'
    );
  }

  function diagnosis(params, row) {
    var absWh = Math.abs(params.wh);
    var absZ = Math.abs(row.z);

    if ((params.activation === "tanh" && absZ > 2.6) || (params.activation === "sigmoid" && absZ > 4.2)) {
      return {
        level: "danger",
        title: "Activación saturada",
        text: "El valor previo a la activación es grande. La salida cambia poco aunque modifiques ligeramente la entrada, lo que puede debilitar el aprendizaje por gradiente."
      };
    }
    if (params.activation === "relu" && (absWh > 1 || Math.abs(row.state) > 2.5)) {
      return {
        level: "danger",
        title: "Riesgo de crecimiento inestable",
        text: "ReLU no limita los estados positivos. Con recurrencia intensa, la memoria puede crecer rápidamente y producir gradientes explosivos."
      };
    }
    if (absWh < 0.3) {
      return {
        level: "warning",
        title: "Memoria muy corta",
        text: "El término recurrente aporta poco. La red responde principalmente a la entrada actual y el contexto lejano se pierde con rapidez."
      };
    }
    if (params.wh < -0.65) {
      return {
        level: "warning",
        title: "Memoria oscilante",
        text: "El peso recurrente negativo invierte parte del estado anterior. Esto puede producir alternancia y sensibilidad a pequeñas variaciones."
      };
    }
    if (absWh > 1) {
      return {
        level: "warning",
        title: "Memoria persistente",
        text: "El pasado conserva mucha influencia. Puede ayudar con dependencias largas, pero también aumentar saturación o inestabilidad."
      };
    }
    return {
      level: "good",
      title: "Dinámica equilibrada",
      text: "La entrada y la memoria contribuyen sin dominar por completo. Observá cómo cada nuevo dato corrige gradualmente el contexto acumulado."
    };
  }

  function render() {
    var params = readParameters();
    var scenario = scenarios[params.scenario];
    var rows = computeSequence(scenario, params);
    currentStep = clamp(currentStep, 0, rows.length - 1);
    var row = rows[currentStep];
    var stage = root.querySelector("[data-stage]");

    var timeline = rows.map(function (item, index) {
      var classes = "rnn-token";
      if (index < currentStep) classes += " is-complete";
      if (index === currentStep) classes += " is-active";
      return (
        '<button type="button" class="' + classes + '" data-step="' + index + '" aria-current="' + (index === currentStep ? 'step' : 'false') + '">' +
          '<small>t = ' + (index + 1) + '</small>' +
          '<strong>' + item.label + '</strong>' +
          '<span>x = ' + format(item.input, 2) + '</span>' +
        '</button>'
      );
    }).join("");

    var totalMagnitude = Math.abs(row.inputContribution) + Math.abs(row.memoryContribution) + Math.abs(row.biasContribution) || 1;
    var inputWidth = Math.abs(row.inputContribution) / totalMagnitude * 100;
    var memoryWidth = Math.abs(row.memoryContribution) / totalMagnitude * 100;
    var biasWidth = Math.abs(row.biasContribution) / totalMagnitude * 100;
    var memoryShare = Math.abs(row.memoryContribution) / totalMagnitude;
    var diagnostic = diagnosis(params, row);

    var ledgerRows = rows.map(function (item, index) {
      var rowClass = index === currentStep ? "is-active" : index > currentStep ? "is-future" : "";
      return (
        '<tr class="' + rowClass + '">' +
          '<td>' + (index + 1) + '</td><td>' + item.label + '</td><td>' + format(item.input, 3) + '</td>' +
          '<td>' + format(item.previous, 3) + '</td><td>' + format(item.inputContribution, 3) + '</td>' +
          '<td>' + format(item.memoryContribution, 3) + '</td><td>' + format(item.z, 3) + '</td><td>' + format(item.state, 3) + '</td>' +
        '</tr>'
      );
    }).join("");

    stage.innerHTML =
      '<div class="rnn-scenario-head">' +
        '<div><h3>' + scenario.name + '</h3><p>' + scenario.description + '</p></div>' +
        '<span class="rnn-step-counter">Paso ' + (currentStep + 1) + ' / ' + rows.length + '</span>' +
      '</div>' +
      '<div class="rnn-timeline-wrap"><div class="rnn-timeline" aria-label="Secuencia temporal">' + timeline + '</div></div>' +
      '<div class="rnn-flow-panel">' +
        '<div class="rnn-flow">' +
          '<div class="rnn-source-stack">' +
            '<div class="rnn-node input"><small>Entrada actual</small><strong>xₜ = ' + format(row.input, 3) + '</strong><span>Wₓxₜ = ' + format(row.inputContribution, 3) + '</span></div>' +
            '<div class="rnn-node memory"><small>Memoria previa</small><strong>hₜ₋₁ = ' + format(row.previous, 3) + '</strong><span>Wₕhₜ₋₁ = ' + format(row.memoryContribution, 3) + '</span></div>' +
          '</div>' +
          '<div class="rnn-arrow"><span>→</span><small>combinar</small></div>' +
          '<div class="rnn-node sum"><small>Suma ponderada</small><strong>zₜ = ' + format(row.z, 3) + '</strong><span>incluye b = ' + format(params.bias, 2) + '</span></div>' +
          '<div class="rnn-arrow"><span>→</span><small>φ</small></div>' +
          '<div class="rnn-node activation"><small>Activación</small><strong>' + activationName(params.activation) + '</strong><span>transforma zₜ</span></div>' +
          '<div class="rnn-arrow"><span>→</span><small>actualizar</small></div>' +
          '<div class="rnn-node state"><small>Nuevo estado</small><strong>hₜ = ' + format(row.state, 3) + '</strong><span>memoria para t + 1</span></div>' +
        '</div>' +
      '</div>' +
      '<div class="rnn-formula-panel">' +
        '<span>Sustitución numérica del paso activo</span>' +
        '<strong>hₜ = ' + activationName(params.activation) + '([ ' + format(params.wx, 2) + ' × ' + format(row.input, 2) + ' ] + [ ' + format(params.wh, 2) + ' × ' + format(row.previous, 2) + ' ] + ' + format(params.bias, 2) + ') = ' + format(row.state, 3) + '</strong>' +
      '</div>' +
      '<div class="rnn-analytics-grid">' +
        '<div class="rnn-chart-panel">' +
          '<div class="rnn-panel-title"><strong>Entrada y memoria en el tiempo</strong><div class="rnn-chart-legend"><span><i class="input-line"></i>Entrada xₜ</span><span><i class="state-line"></i>Estado hₜ</span></div></div>' +
          chartSvg(rows, currentStep) +
        '</div>' +
        '<div class="rnn-contribution-panel">' +
          '<div class="rnn-panel-title"><strong>Contribución al estado</strong></div>' +
          '<div class="rnn-contribution-list">' +
            contributionRow("Entrada Wₓxₜ", row.inputContribution, inputWidth, "input") +
            contributionRow("Memoria Wₕhₜ₋₁", row.memoryContribution, memoryWidth, "memory") +
            contributionRow("Sesgo b", row.biasContribution, biasWidth, "bias") +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="rnn-metric-grid">' +
        metric("Entrada xₜ", format(row.input, 3)) +
        metric("Memoria hₜ₋₁", format(row.previous, 3)) +
        metric("Suma zₜ", format(row.z, 3)) +
        metric("Estado hₜ", format(row.state, 3)) +
        metric("Participación memoria", format(memoryShare * 100, 1) + "%") +
      '</div>' +
      '<div class="rnn-ledger-panel">' +
        '<table class="rnn-ledger">' +
          '<thead><tr><th>t</th><th>Elemento</th><th>xₜ</th><th>hₜ₋₁</th><th>Wₓxₜ</th><th>Wₕhₜ₋₁</th><th>zₜ</th><th>hₜ</th></tr></thead>' +
          '<tbody>' + ledgerRows + '</tbody>' +
        '</table>' +
      '</div>' +
      '<p class="rnn-diagnosis ' + (diagnostic.level === "warning" ? "is-warning" : diagnostic.level === "danger" ? "is-danger" : "") + '">' +
        '<strong>' + diagnostic.title + ':</strong><span>' + diagnostic.text + '</span>' +
      '</p>';

    stage.querySelectorAll("[data-step]").forEach(function (button) {
      button.addEventListener("click", function () {
        pause();
        currentStep = Number(button.dataset.step);
        render();
      });
    });

    updateTransport(rows.length);
    updateStatus();
  }

  function updateOutputs() {
    root.querySelectorAll('input[type="range"]').forEach(function (input) {
      var output = root.querySelector('[data-output="' + input.id + '"]');
      if (!output) return;
      var digits = input.id === "rnn-speed" ? 0 : 2;
      output.value = format(Number(input.value), digits) + (input.dataset.suffix || "");
    });
  }

  function updateTransport(length) {
    var previous = root.querySelector('[data-action="previous"]');
    var next = root.querySelector('[data-action="next"]');
    var playButton = root.querySelector('[data-action="play"]');
    previous.disabled = currentStep <= 0;
    next.disabled = currentStep >= length - 1;
    playButton.textContent = timer ? "Ⅱ" : "▶";
    playButton.setAttribute("aria-label", timer ? "Pausar reproducción" : "Reproducir secuencia");
  }

  function updateStatus() {
    var badge = root.querySelector("[data-status]");
    if (!badge) return;
    badge.textContent = timer ? "Reproducción automática" : "Modo manual";
    badge.classList.toggle("is-playing", Boolean(timer));
  }

  function pause() {
    if (timer) window.clearInterval(timer);
    timer = null;
    updateStatus();
  }

  function play() {
    if (timer) {
      pause();
      render();
      return;
    }
    var params = readParameters();
    var length = scenarios[params.scenario].values.length;
    if (currentStep >= length - 1) currentStep = 0;
    timer = window.setInterval(function () {
      var currentParams = readParameters();
      var currentLength = scenarios[currentParams.scenario].values.length;
      if (currentStep >= currentLength - 1) {
        pause();
      } else {
        currentStep += 1;
      }
      render();
    }, params.speed);
    render();
  }

  function applyValues(values) {
    var controls = getControls();
    controls.wx.value = values.wx;
    controls.wh.value = values.wh;
    controls.bias.value = values.bias;
    controls.h0.value = values.h0;
    updateOutputs();
  }

  function applyScenarioDefaults() {
    pause();
    var controls = getControls();
    var scenario = scenarios[controls.scenario.value];
    controls.activation.value = scenario.defaults.activation;
    applyValues(scenario.defaults);
    activeProfile = "";
    currentStep = 0;
    root.querySelectorAll("[data-profile]").forEach(function (button) {
      button.classList.remove("is-active");
    });
    render();
  }

  function applyProfile(key) {
    pause();
    activeProfile = key;
    applyValues(profiles[key]);
    currentStep = 0;
    root.querySelectorAll("[data-profile]").forEach(function (button) {
      button.classList.toggle("is-active", button.dataset.profile === key);
    });
    render();
  }

  function bindEvents() {
    var controls = getControls();

    controls.scenario.addEventListener("change", applyScenarioDefaults);
    controls.activation.addEventListener("change", function () {
      pause();
      currentStep = 0;
      render();
    });

    [controls.wx, controls.wh, controls.bias, controls.h0].forEach(function (input) {
      input.addEventListener("input", function () {
        pause();
        activeProfile = "";
        root.querySelectorAll("[data-profile]").forEach(function (button) {
          button.classList.remove("is-active");
        });
        updateOutputs();
        render();
      });
    });

    controls.speed.addEventListener("input", function () {
      updateOutputs();
      if (timer) {
        pause();
        play();
      }
    });

    root.querySelectorAll("[data-profile]").forEach(function (button) {
      button.addEventListener("click", function () {
        applyProfile(button.dataset.profile);
      });
    });

    root.querySelector('[data-action="previous"]').addEventListener("click", function () {
      pause();
      currentStep = Math.max(0, currentStep - 1);
      render();
    });

    root.querySelector('[data-action="next"]').addEventListener("click", function () {
      pause();
      var params = readParameters();
      var length = scenarios[params.scenario].values.length;
      currentStep = Math.min(length - 1, currentStep + 1);
      render();
    });

    root.querySelector('[data-action="play"]').addEventListener("click", play);

    root.querySelector('[data-action="reset"]').addEventListener("click", function () {
      pause();
      currentStep = 0;
      applyScenarioDefaults();
    });

    document.addEventListener("keydown", function (event) {
      var target = event.target;
      var tag = target && target.tagName ? target.tagName.toLowerCase() : "";
      if (tag === "input" || tag === "select" || tag === "button" || tag === "textarea") return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        root.querySelector('[data-action="next"]').click();
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        root.querySelector('[data-action="previous"]').click();
      } else if (event.key === " ") {
        event.preventDefault();
        play();
      }
    });
  }

  buildShell();
  updateOutputs();
  bindEvents();
  render();
})();

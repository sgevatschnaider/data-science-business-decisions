(function () {
  "use strict";

  var root = document.querySelector("[data-simulation]");
  if (!root) return;

  var moduleId = root.dataset.simulation;
  var palette = ["#0f766e", "#1d4ed8", "#b45309", "#7c3aed", "#be123c", "#15803d"];

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function mean(values) {
    return values.reduce(function (sum, value) { return sum + value; }, 0) / values.length;
  }

  function median(values) {
    var sorted = values.slice().sort(function (a, b) { return a - b; });
    var middle = Math.floor(sorted.length / 2);
    return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
  }

  function quantile(values, probability) {
    var sorted = values.slice().sort(function (a, b) { return a - b; });
    var position = (sorted.length - 1) * probability;
    var base = Math.floor(position);
    var remainder = position - base;
    return sorted[base + 1] === undefined
      ? sorted[base]
      : sorted[base] + remainder * (sorted[base + 1] - sorted[base]);
  }

  function standardDeviation(values) {
    var center = mean(values);
    return Math.sqrt(mean(values.map(function (value) {
      return Math.pow(value - center, 2);
    })));
  }

  function correlation(xs, ys) {
    var mx = mean(xs);
    var my = mean(ys);
    var numerator = 0;
    var dx = 0;
    var dy = 0;
    xs.forEach(function (x, index) {
      numerator += (x - mx) * (ys[index] - my);
      dx += Math.pow(x - mx, 2);
      dy += Math.pow(ys[index] - my, 2);
    });
    return numerator / Math.sqrt(dx * dy || 1);
  }

  function format(value, digits) {
    if (!Number.isFinite(value)) return "-";
    return new Intl.NumberFormat("es-AR", {
      maximumFractionDigits: digits === undefined ? 2 : digits,
      minimumFractionDigits: digits === undefined ? 0 : digits
    }).format(value);
  }

  function mulberry32(seed) {
    return function () {
      var t = seed += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function normal(random) {
    var u = Math.max(random(), 1e-9);
    var v = Math.max(random(), 1e-9);
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function range(id, label, min, max, value, step, suffix) {
    return (
      '<div class="control-row">' +
        '<label for="' + id + '"><span>' + label + '</span>' +
        '<output class="control-value" for="' + id + '" data-value-for="' + id + '">' +
          value + (suffix || "") +
        '</output></label>' +
        '<input id="' + id + '" type="range" min="' + min + '" max="' + max +
          '" value="' + value + '" step="' + step + '" data-suffix="' + (suffix || "") + '">' +
      '</div>'
    );
  }

  function select(id, label, options) {
    return (
      '<div class="control-row"><label for="' + id + '">' + label + '</label>' +
      '<select id="' + id + '">' +
      options.map(function (item) {
        return '<option value="' + item[0] + '">' + item[1] + '</option>';
      }).join("") +
      '</select></div>'
    );
  }

  function checkbox(id, label, checked) {
    return (
      '<div class="control-row switch-row"><label for="' + id + '">' + label + '</label>' +
      '<input id="' + id + '" type="checkbox"' + (checked ? " checked" : "") + "></div>"
    );
  }

  function metric(label, value) {
    return '<div class="metric-card"><span>' + label + '</span><strong>' + value + "</strong></div>";
  }

  function base(title, controls) {
    root.innerHTML =
      '<div class="sim-header"><h2>' + title + '</h2><span class="sim-badge">Parámetros en vivo</span></div>' +
      '<div class="sim-grid">' +
        '<aside class="sim-controls"><h3>Controles</h3>' + controls + '</aside>' +
        '<div class="sim-stage" data-stage></div>' +
      "</div>";
    root.querySelectorAll('input[type="range"]').forEach(function (input) {
      input.addEventListener("input", function () {
        var output = root.querySelector('[data-value-for="' + input.id + '"]');
        if (output) output.value = input.value + (input.dataset.suffix || "");
      });
    });
    return root.querySelector("[data-stage]");
  }

  function listen(update) {
    root.querySelectorAll("input, select").forEach(function (control) {
      control.addEventListener("input", update);
      control.addEventListener("change", update);
    });
  }

  function svg(inner, label, className) {
    return (
      '<svg class="' + (className || "") + '" viewBox="0 0 640 330" role="img" ' +
      'aria-label="' + label + '">' + inner + "</svg>"
    );
  }

  function axes() {
    var lines = "";
    for (var i = 1; i < 5; i += 1) {
      var x = 50 + i * 135;
      var y = 25 + i * 65;
      lines += '<line class="chart-grid" x1="' + x + '" y1="20" x2="' + x + '" y2="285"></line>';
      lines += '<line class="chart-grid" x1="50" y1="' + y + '" x2="600" y2="' + y + '"></line>';
    }
    return lines +
      '<line class="chart-axis" x1="50" y1="285" x2="605" y2="285"></line>' +
      '<line class="chart-axis" x1="50" y1="20" x2="50" y2="285"></line>';
  }

  function polyline(points, className, extra) {
    return '<polyline class="' + className + '" fill="none" stroke-width="2.5" ' +
      'points="' + points.map(function (point) { return point.join(","); }).join(" ") + '" ' +
      (extra || "") + "></polyline>";
  }

  function simulation00() {
    var controls =
      range("seed", "Semilla", 1, 99, 42, 1, "") +
      range("rows", "Filas", 20, 200, 80, 20, "") +
      checkbox("dictionary", "Diccionario de datos", true) +
      checkbox("dependencies", "Dependencias declaradas", true) +
      '<div class="control-row"><button class="button secondary" type="button" data-shuffle>Desordenar etapas</button></div>';
    var stage = base("Flujo reproducible", controls);
    var expected = [
      ["Pregunta", "Definir unidad, horizonte y métrica"],
      ["Datos", "Cargar y validar entradas"],
      ["Preparación", "Transformar dentro del pipeline"],
      ["Análisis", "Calcular evidencia y métricas"],
      ["Decisión", "Interpretar, limitar y registrar"]
    ];
    var order = [0, 1, 2, 3, 4];

    function render() {
      var seed = Number(root.querySelector("#seed").value);
      var rows = Number(root.querySelector("#rows").value);
      var dictionary = root.querySelector("#dictionary").checked;
      var dependencies = root.querySelector("#dependencies").checked;
      var random = mulberry32(seed);
      var sample = Array.from({ length: 5 }, function () {
        return Math.round(random() * 1000) / 10;
      });
      var correctPositions = order.filter(function (value, index) { return value === index; }).length;
      var score = Math.round((correctPositions / 5) * 60 + (dictionary ? 15 : 0) +
        (dependencies ? 15 : 0) + 10);
      var steps = order.map(function (item, position) {
        return (
          '<div class="workflow-step ' + (item === position ? "is-correct" : "") + '" data-position="' + position + '">' +
            '<span>' + String(position + 1).padStart(2, "0") + '</span>' +
            '<div><strong>' + expected[item][0] + '</strong><small>' + expected[item][1] + '</small></div>' +
            '<div class="move-buttons">' +
              '<button type="button" class="tiny-button" data-move="-1" aria-label="Subir etapa">Subir</button>' +
              '<button type="button" class="tiny-button" data-move="1" aria-label="Bajar etapa">Bajar</button>' +
            '</div>' +
          "</div>"
        );
      }).join("");
      stage.innerHTML =
        '<div class="chart-panel"><div class="workflow-list">' + steps + "</div></div>" +
        '<div class="metric-grid">' +
          metric("Reproducibilidad", score + "%") +
          metric("Orden correcto", correctPositions + " / 5") +
          metric("Filas", format(rows, 0)) +
          metric("Muestra repetible", sample.slice(0, 3).join(" · ")) +
        "</div>" +
        '<p class="sim-explanation">' +
          (score === 100
            ? "El flujo está ordenado y sus condiciones están documentadas: otra persona puede reconstruir la evidencia."
            : "La reproducibilidad cae cuando faltan contratos del entorno o las etapas dependen de estados fuera de orden.") +
        "</p>";
      stage.querySelectorAll("[data-move]").forEach(function (button) {
        button.addEventListener("click", function () {
          var position = Number(button.closest("[data-position]").dataset.position);
          var target = position + Number(button.dataset.move);
          if (target < 0 || target >= order.length) return;
          var temporary = order[position];
          order[position] = order[target];
          order[target] = temporary;
          render();
        });
      });
    }
    root.querySelector("[data-shuffle]").addEventListener("click", function () {
      var random = mulberry32(Date.now() % 100000);
      order.sort(function () { return random() - 0.5; });
      render();
    });
    listen(render);
    render();
  }

  function simulation01() {
    var controls =
      range("skew", "Asimetría", 0, 22, 8, 1, "") +
      range("spread", "Dispersión", 5, 35, 15, 1, "") +
      range("extreme", "Valor extremo", 0, 250, 120, 10, "") +
      range("sample", "Tamaño muestral", 60, 300, 180, 20, "");
    var stage = base("Distribución y medidas de centro", controls);

    function render() {
      var skew = Number(root.querySelector("#skew").value) / 10;
      var spread = Number(root.querySelector("#spread").value);
      var extreme = Number(root.querySelector("#extreme").value);
      var sample = Number(root.querySelector("#sample").value);
      var random = mulberry32(87);
      var values = Array.from({ length: sample }, function () {
        var z = normal(random);
        return 70 + z * spread + Math.max(0, z) * skew * spread * 0.55;
      });
      if (extreme > 0) values[0] = 70 + extreme;
      var low = Math.min.apply(null, values);
      var high = Math.max.apply(null, values);
      var bins = Array(18).fill(0);
      values.forEach(function (value) {
        var index = Math.min(17, Math.floor(((value - low) / (high - low || 1)) * 18));
        bins[index] += 1;
      });
      var maxBin = Math.max.apply(null, bins);
      var bars = bins.map(function (count, index) {
        var width = 540 / bins.length - 3;
        var height = (count / maxBin) * 235;
        return '<rect class="chart-primary" opacity="0.78" x="' + (55 + index * (540 / bins.length)) +
          '" y="' + (280 - height) + '" width="' + width + '" height="' + height + '"></rect>';
      }).join("");
      var center = mean(values);
      var middle = median(values);
      var q1 = quantile(values, 0.25);
      var q3 = quantile(values, 0.75);
      var iqr = q3 - q1;
      var flagged = values.filter(function (value) {
        return value < q1 - 1.5 * iqr || value > q3 + 1.5 * iqr;
      }).length;
      function xPosition(value) {
        return 55 + ((value - low) / (high - low || 1)) * 540;
      }
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() + bars +
            '<line class="chart-secondary" stroke-width="3" x1="' + xPosition(center) + '" y1="28" x2="' + xPosition(center) + '" y2="285"></line>' +
            '<line class="chart-accent" stroke-width="3" x1="' + xPosition(middle) + '" y1="28" x2="' + xPosition(middle) + '" y2="285"></line>' +
            '<text class="chart-label" x="60" y="312">Línea azul: media · línea ámbar: mediana</text>',
            "Histograma de la distribución generada con líneas de media y mediana"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Media", format(center, 1)) +
          metric("Mediana", format(middle, 1)) +
          metric("IQR", format(iqr, 1)) +
          metric("Extremos IQR", format(flagged, 0)) +
        "</div>" +
        '<p class="sim-explanation">La media se desplaza más que la mediana cuando crecen la cola o el valor extremo. El resumen debe acompañarse por la forma de la distribución.</p>';
    }
    listen(render);
    render();
  }

  function simulation02() {
    var controls =
      range("missing-rate", "Ausencia objetivo", 5, 50, 25, 5, "%") +
      select("mechanism", "Mecanismo", [["mcar", "MCAR"], ["mar", "MAR por grupo"], ["mnar", "MNAR por valor"]]) +
      select("strategy", "Tratamiento", [["drop", "Eliminar filas"], ["mean", "Media global"], ["median", "Mediana"], ["group", "Media por grupo"]]);
    var stage = base("Matriz de ausencia e imputación", controls);

    function render() {
      var rate = Number(root.querySelector("#missing-rate").value) / 100;
      var mechanism = root.querySelector("#mechanism").value;
      var strategy = root.querySelector("#strategy").value;
      var random = mulberry32(204);
      var rows = Array.from({ length: 144 }, function (_, index) {
        var group = index % 3;
        var value = 40 + group * 15 + normal(random) * 9;
        var probability = rate;
        if (mechanism === "mar") probability = rate * (group === 2 ? 1.8 : 0.6);
        if (mechanism === "mnar") probability = rate * (value > 65 ? 1.8 : 0.55);
        return { group: group, value: value, missing: random() < clamp(probability, 0, 0.9) };
      });
      var observed = rows.filter(function (row) { return !row.missing; });
      var trueMean = mean(rows.map(function (row) { return row.value; }));
      var observedMean = mean(observed.map(function (row) { return row.value; }));
      var replacement = strategy === "median"
        ? median(observed.map(function (row) { return row.value; }))
        : observedMean;
      var groupMeans = [0, 1, 2].map(function (group) {
        var values = observed.filter(function (row) { return row.group === group; })
          .map(function (row) { return row.value; });
        return values.length ? mean(values) : replacement;
      });
      var treatedValues = strategy === "drop"
        ? observed.map(function (row) { return row.value; })
        : rows.map(function (row) {
            if (!row.missing) return row.value;
            return strategy === "group" ? groupMeans[row.group] : replacement;
          });
      var treatedMean = mean(treatedValues);
      var cells = rows.map(function (row) {
        return '<span class="matrix-cell ' + (row.missing ? "missing" : "") +
          '" title="' + (row.missing ? "Faltante" : "Observado") + '"></span>';
      }).join("");
      var actualRate = rows.filter(function (row) { return row.missing; }).length / rows.length;
      stage.innerHTML =
        '<div class="chart-panel"><div class="matrix-grid" aria-label="Matriz de valores observados y faltantes">' +
          cells + '</div><p class="chart-caption">Verde: observado · ámbar: faltante</p></div>' +
        '<div class="metric-grid">' +
          metric("Ausencia real", format(actualRate * 100, 1) + "%") +
          metric("Media verdadera", format(trueMean, 1)) +
          metric("Media tratada", format(treatedMean, 1)) +
          metric("Sesgo", format(treatedMean - trueMean, 2)) +
        "</div>" +
        '<p class="sim-explanation">' +
          (mechanism === "mcar"
            ? "Con ausencia aleatoria, el promedio observado fluctúa pero no sigue sistemáticamente un grupo o valor."
            : "El patrón de ausencia contiene estructura. Una imputación global puede esconder diferencias y reducir artificialmente la dispersión.") +
        "</p>";
    }
    listen(render);
    render();
  }

  function simulation03() {
    var controls =
      select("outlier-method", "Método", [["iqr", "Rango intercuartílico"], ["z", "Puntuación z"]]) +
      range("outlier-threshold", "Umbral", 10, 30, 15, 1, "") +
      range("outlier-value", "Observación extrema", 120, 600, 360, 20, "");
    var stage = base("Detección y sensibilidad", controls);

    function render() {
      var method = root.querySelector("#outlier-method").value;
      var threshold = Number(root.querySelector("#outlier-threshold").value) / 10;
      var extreme = Number(root.querySelector("#outlier-value").value);
      var random = mulberry32(303);
      var values = Array.from({ length: 42 }, function () { return 100 + normal(random) * 14; });
      values.push(extreme);
      var center = mean(values);
      var sd = standardDeviation(values);
      var q1 = quantile(values, 0.25);
      var q3 = quantile(values, 0.75);
      var iqr = q3 - q1;
      var flagged = values.map(function (value) {
        return method === "iqr"
          ? value < q1 - threshold * iqr || value > q3 + threshold * iqr
          : Math.abs((value - center) / (sd || 1)) > threshold;
      });
      var low = Math.min.apply(null, values) - 10;
      var high = Math.max.apply(null, values) + 10;
      var circles = values.map(function (value, index) {
        var x = 55 + ((value - low) / (high - low)) * 535;
        var y = 80 + (index % 8) * 24;
        return '<circle class="' + (flagged[index] ? "chart-danger" : "chart-primary") +
          '" cx="' + x + '" cy="' + y + '" r="' + (flagged[index] ? 6 : 4) + '" opacity="0.82"></circle>';
      }).join("");
      var robustMean = mean(values.filter(function (_, index) { return !flagged[index]; }));
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() + circles +
            '<text class="chart-label" x="60" y="312">Rojo: marcado por el criterio seleccionado</text>',
            "Gráfico de puntos con observaciones marcadas como extremas"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Marcados", flagged.filter(Boolean).length) +
          metric("Media", format(center, 1)) +
          metric("Mediana", format(median(values), 1)) +
          metric("Media sin marcados", format(robustMean, 1)) +
        "</div>" +
        '<p class="sim-explanation">El umbral cambia la etiqueta estadística, no la naturaleza del caso. Verificá unidades, proceso y consecuencias antes de excluir.</p>';
    }
    listen(render);
    render();
  }

  function skewness(values) {
    var center = mean(values);
    var sd = standardDeviation(values) || 1;
    return mean(values.map(function (value) { return Math.pow((value - center) / sd, 3); }));
  }

  function simulation04() {
    var controls =
      select("transform", "Transformación", [["none", "Original"], ["log", "Logaritmo"], ["standard", "Estandarización"], ["minmax", "Min-max"]]) +
      range("source-skew", "Asimetría original", 0, 25, 14, 1, "") +
      range("future-shift", "Cambio futuro", 0, 80, 35, 5, "") +
      checkbox("fit-all", "Ajustar también con futuro", false);
    var stage = base("Transformación, escala y leakage", controls);

    function render() {
      var kind = root.querySelector("#transform").value;
      var sourceSkew = Number(root.querySelector("#source-skew").value) / 10;
      var futureShift = Number(root.querySelector("#future-shift").value);
      var fitAll = root.querySelector("#fit-all").checked;
      var random = mulberry32(404);
      var train = Array.from({ length: 55 }, function () {
        var z = normal(random);
        return Math.max(1, 40 + 8 * z + Math.max(0, z) * sourceSkew * 12);
      });
      var future = Array.from({ length: 20 }, function () {
        var z = normal(random);
        return Math.max(1, 40 + futureShift + 8 * z + Math.max(0, z) * sourceSkew * 12);
      });
      var fitValues = fitAll ? train.concat(future) : train;
      var center = mean(fitValues);
      var sd = standardDeviation(fitValues) || 1;
      var minimum = Math.min.apply(null, fitValues);
      var maximum = Math.max.apply(null, fitValues);
      function transform(value) {
        if (kind === "log") return Math.log1p(value);
        if (kind === "standard") return (value - center) / sd;
        if (kind === "minmax") return (value - minimum) / (maximum - minimum || 1);
        return value;
      }
      var transformed = train.map(transform);
      var allX = train.concat(future);
      var allY = train.map(transform).concat(future.map(transform));
      var minX = Math.min.apply(null, allX);
      var maxX = Math.max.apply(null, allX);
      var minY = Math.min.apply(null, allY);
      var maxY = Math.max.apply(null, allY);
      var circles = allX.map(function (value, index) {
        var x = 55 + ((value - minX) / (maxX - minX || 1)) * 535;
        var y = 280 - ((allY[index] - minY) / (maxY - minY || 1)) * 245;
        return '<circle class="' + (index < train.length ? "chart-primary" : "chart-accent") +
          '" cx="' + x + '" cy="' + y + '" r="4" opacity="0.72"></circle>';
      }).join("");
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() + circles +
            '<text class="chart-label" x="60" y="312">Verde: entrenamiento · ámbar: período futuro</text>',
            "Relación entre valores originales y transformados"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Asimetría antes", format(skewness(train), 2)) +
          metric("Asimetría después", format(skewness(transformed), 2)) +
          metric("Rango después", format(Math.max.apply(null, transformed) - Math.min.apply(null, transformed), 2)) +
          metric("Riesgo de leakage", fitAll ? "Alto" : "Controlado") +
        "</div>" +
        '<p class="sim-explanation">' +
          (fitAll
            ? "El transformador conoce la distribución futura. La escala parece más cómoda, pero la evaluación queda contaminada."
            : "Los parámetros se aprenden con entrenamiento y se aplican sin mirar el período futuro.") +
        "</p>";
    }
    listen(render);
    render();
  }

  function fitLine(xs, ys) {
    var mx = mean(xs);
    var my = mean(ys);
    var numerator = 0;
    var denominator = 0;
    xs.forEach(function (x, index) {
      numerator += (x - mx) * (ys[index] - my);
      denominator += Math.pow(x - mx, 2);
    });
    var slope = numerator / (denominator || 1);
    return { slope: slope, intercept: my - slope * mx };
  }

  function simulation05() {
    var controls =
      range("true-slope", "Pendiente real", -30, 80, 42, 2, "") +
      range("reg-noise", "Ruido", 0, 45, 16, 1, "") +
      range("reg-outlier", "Influencia extrema", 0, 120, 0, 10, "");
    var stage = base("Ajuste lineal y error", controls);

    function render() {
      var trueSlope = Number(root.querySelector("#true-slope").value) / 10;
      var noise = Number(root.querySelector("#reg-noise").value);
      var outlier = Number(root.querySelector("#reg-outlier").value);
      var random = mulberry32(505);
      var xs = Array.from({ length: 38 }, function (_, index) { return index / 2; });
      var ys = xs.map(function (x) { return 35 + trueSlope * x + normal(random) * noise; });
      if (outlier > 0) ys[ys.length - 1] += outlier;
      var model = fitLine(xs, ys);
      var predictions = xs.map(function (x) { return model.intercept + model.slope * x; });
      var errors = ys.map(function (value, index) { return value - predictions[index]; });
      var mae = mean(errors.map(Math.abs));
      var rmse = Math.sqrt(mean(errors.map(function (error) { return error * error; })));
      var r2 = Math.pow(correlation(xs, ys), 2);
      var minY = Math.min.apply(null, ys.concat(predictions));
      var maxY = Math.max.apply(null, ys.concat(predictions));
      function px(x) { return 55 + (x / 19) * 535; }
      function py(y) { return 280 - ((y - minY) / (maxY - minY || 1)) * 245; }
      var circles = xs.map(function (x, index) {
        return '<circle class="chart-primary" cx="' + px(x) + '" cy="' + py(ys[index]) +
          '" r="4.5" opacity="0.76"></circle>';
      }).join("");
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() + circles +
            '<line class="chart-secondary" stroke-width="3" x1="' + px(0) + '" y1="' + py(model.intercept) +
              '" x2="' + px(19) + '" y2="' + py(model.intercept + model.slope * 19) + '"></line>',
            "Diagrama de dispersión con recta de regresión ajustada"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Pendiente estimada", format(model.slope, 2)) +
          metric("MAE", format(mae, 1)) +
          metric("RMSE", format(rmse, 1)) +
          metric("R cuadrado", format(r2, 2)) +
        "</div>" +
        '<p class="sim-explanation">Ruido y observaciones influyentes cambian coeficientes y métricas. RMSE reacciona más que MAE ante errores grandes.</p>';
    }
    listen(render);
    render();
  }

  function simulation06() {
    var controls =
      range("folds", "Cantidad de folds", 3, 10, 5, 1, "") +
      select("cv-strategy", "Estrategia", [["random", "K-Fold aleatorio"], ["group", "Por clientes"], ["time", "Origen temporal"]]) +
      checkbox("cv-shuffle", "Mezclar observaciones", true);
    var stage = base("Particiones y riesgo de contaminación", controls);

    function render() {
      var folds = Number(root.querySelector("#folds").value);
      var strategy = root.querySelector("#cv-strategy").value;
      var shuffle = root.querySelector("#cv-shuffle").checked;
      var rows = "";
      var width = 520 / 30;
      for (var fold = 0; fold < folds; fold += 1) {
        for (var index = 0; index < 30; index += 1) {
          var validation;
          if (strategy === "time") {
            var boundary = Math.floor(((fold + 1) / (folds + 1)) * 30);
            validation = index >= boundary && index < boundary + Math.max(2, Math.floor(30 / (folds + 2)));
          } else {
            validation = (index + (shuffle ? fold * 3 : 0)) % folds === fold;
          }
          var isFutureExcluded = strategy === "time" &&
            index > Math.floor(((fold + 1) / (folds + 1)) * 30) + Math.floor(30 / (folds + 2));
          var fill = isFutureExcluded ? "#c9dce3" : (validation ? palette[1] : palette[0]);
          rows += '<rect x="' + (70 + index * width) + '" y="' + (32 + fold * (245 / folds)) +
            '" width="' + Math.max(3, width - 2) + '" height="' + Math.max(12, 190 / folds) +
            '" rx="2" fill="' + fill + '" opacity="' + (isFutureExcluded ? "0.35" : "0.78") + '"></rect>';
        }
        rows += '<text class="chart-label" x="18" y="' + (46 + fold * (245 / folds)) + '">Fold ' + (fold + 1) + "</text>";
      }
      var risk = (strategy === "time" && shuffle) || (strategy === "group" && shuffle)
        ? "Alto"
        : strategy === "random"
          ? "Depende"
          : "Controlado";
      var trainShare = strategy === "time" ? 50 : Math.round((folds - 1) / folds * 100);
      var uncertainty = 1 / Math.sqrt(folds) * (strategy === "time" ? 1.35 : 1);
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            rows +
            '<rect x="70" y="292" width="18" height="10" fill="' + palette[0] + '"></rect>' +
            '<text class="chart-label" x="94" y="301">Entrenamiento</text>' +
            '<rect x="190" y="292" width="18" height="10" fill="' + palette[1] + '"></rect>' +
            '<text class="chart-label" x="214" y="301">Validación</text>',
            "Esquema de particiones de entrenamiento y validación"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Entrenamiento medio", trainShare + "%") +
          metric("Veces evaluado", strategy === "time" ? "Variable" : "1") +
          metric("Variación esperada", format(uncertainty, 2)) +
          metric("Leakage", risk) +
        "</div>" +
        '<p class="sim-explanation">' +
          (strategy === "random"
            ? "K-Fold aleatorio supone observaciones intercambiables. Revisá si tiempo o entidades repetidas rompen ese supuesto."
            : strategy === "group"
              ? "Los clientes deben permanecer completos en un solo lado. Mezclar filas vuelve a compartir identidad."
              : "El origen temporal entrena con pasado y evalúa más adelante. Mezclar destruiría esa imitación del uso real.") +
        "</p>";
    }
    listen(render);
    render();
  }

  function simulation07() {
    var controls =
      range("ts-trend", "Tendencia mensual", -10, 30, 8, 1, "") +
      range("ts-season", "Estacionalidad", 0, 45, 24, 1, "") +
      range("ts-noise", "Ruido", 0, 25, 7, 1, "") +
      range("ts-horizon", "Horizonte", 3, 12, 6, 1, " meses");
    var stage = base("Serie sintética y backtesting", controls);

    function render() {
      var trend = Number(root.querySelector("#ts-trend").value) / 10;
      var season = Number(root.querySelector("#ts-season").value);
      var noise = Number(root.querySelector("#ts-noise").value);
      var horizon = Number(root.querySelector("#ts-horizon").value);
      var random = mulberry32(707);
      var length = 60 + horizon;
      var actual = Array.from({ length: length }, function (_, t) {
        return 100 + trend * t + season * Math.sin(2 * Math.PI * t / 12) + normal(random) * noise;
      });
      var origin = 60;
      var naive = Array.from({ length: horizon }, function () { return actual[origin - 1]; });
      var seasonal = Array.from({ length: horizon }, function (_, index) { return actual[origin + index - 12]; });
      var actualFuture = actual.slice(origin);
      var maeNaive = mean(actualFuture.map(function (value, index) { return Math.abs(value - naive[index]); }));
      var maeSeasonal = mean(actualFuture.map(function (value, index) { return Math.abs(value - seasonal[index]); }));
      var minY = Math.min.apply(null, actual.concat(naive, seasonal));
      var maxY = Math.max.apply(null, actual.concat(naive, seasonal));
      function px(index) { return 55 + (index / (length - 1)) * 535; }
      function py(value) { return 280 - ((value - minY) / (maxY - minY || 1)) * 245; }
      var historyPoints = actual.slice(0, origin).map(function (value, index) { return [px(index), py(value)]; });
      var futurePoints = actualFuture.map(function (value, index) { return [px(origin + index), py(value)]; });
      var naivePoints = naive.map(function (value, index) { return [px(origin + index), py(value)]; });
      var seasonalPoints = seasonal.map(function (value, index) { return [px(origin + index), py(value)]; });
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() +
            polyline(historyPoints, "chart-primary") +
            polyline(futurePoints, "chart-primary", 'stroke-dasharray="4 3"') +
            polyline(naivePoints, "chart-danger") +
            polyline(seasonalPoints, "chart-secondary") +
            '<line class="chart-accent" stroke-width="2" x1="' + px(origin) + '" y1="20" x2="' + px(origin) + '" y2="285"></line>' +
            '<text class="chart-label" x="60" y="312">Verde: real · rojo: naive · azul: estacional · ámbar: origen</text>',
            "Serie real y pronósticos naive y estacional"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("MAE naive", format(maeNaive, 1)) +
          metric("MAE estacional", format(maeSeasonal, 1)) +
          metric("Mejor baseline", maeSeasonal < maeNaive ? "Estacional" : "Último valor") +
          metric("Horizonte", horizon + " meses") +
        "</div>" +
        '<p class="sim-explanation">La estacionalidad favorece repetir el ciclo previo; una tendencia fuerte castiga ese baseline. Evaluá varios orígenes antes de elegir.</p>';
    }
    listen(render);
    render();
  }

  function classificationData(prevalence) {
    var random = mulberry32(808);
    return Array.from({ length: 400 }, function () {
      var actual = random() < prevalence ? 1 : 0;
      var score = clamp((actual ? 0.64 : 0.30) + normal(random) * 0.19, 0.01, 0.99);
      return { actual: actual, score: score };
    });
  }

  function confusion(rows, threshold) {
    var result = { tp: 0, fp: 0, tn: 0, fn: 0 };
    rows.forEach(function (row) {
      var predicted = row.score >= threshold ? 1 : 0;
      if (row.actual && predicted) result.tp += 1;
      else if (!row.actual && predicted) result.fp += 1;
      else if (!row.actual && !predicted) result.tn += 1;
      else result.fn += 1;
    });
    return result;
  }

  function simulation08() {
    var controls =
      range("class-threshold", "Umbral", 10, 90, 50, 5, "%") +
      range("prevalence", "Prevalencia", 5, 60, 20, 5, "%") +
      range("cost-fn", "Costo falso negativo", 1, 20, 10, 1, "") +
      range("cost-fp", "Costo falso positivo", 1, 10, 3, 1, "");
    var stage = base("Matriz de confusión y utilidad", controls);

    function render() {
      var threshold = Number(root.querySelector("#class-threshold").value) / 100;
      var prevalence = Number(root.querySelector("#prevalence").value) / 100;
      var costFn = Number(root.querySelector("#cost-fn").value);
      var costFp = Number(root.querySelector("#cost-fp").value);
      var values = confusion(classificationData(prevalence), threshold);
      var precision = values.tp / (values.tp + values.fp || 1);
      var recall = values.tp / (values.tp + values.fn || 1);
      var utility = values.tp * 6 - values.fp * costFp - values.fn * costFn;
      stage.innerHTML =
        '<div class="chart-panel"><div class="confusion-grid" aria-label="Matriz de confusión">' +
          '<div class="confusion-cell good"><strong>' + values.tp + '</strong><span>Verdaderos positivos</span></div>' +
          '<div class="confusion-cell bad"><strong>' + values.fp + '</strong><span>Falsos positivos</span></div>' +
          '<div class="confusion-cell bad"><strong>' + values.fn + '</strong><span>Falsos negativos</span></div>' +
          '<div class="confusion-cell good"><strong>' + values.tn + '</strong><span>Verdaderos negativos</span></div>' +
        "</div></div>" +
        '<div class="metric-grid">' +
          metric("Precision", format(precision * 100, 1) + "%") +
          metric("Recall", format(recall * 100, 1) + "%") +
          metric("Seleccionados", values.tp + values.fp) +
          metric("Utilidad", format(utility, 0)) +
        "</div>" +
        '<p class="sim-explanation">Subir el umbral suele aumentar precision y reducir recall. La utilidad depende de prevalencia, costos y capacidad, no de un corte universal.</p>';
    }
    listen(render);
    render();
  }

  function simulation09() {
    var controls =
      range("tree-depth", "Profundidad", 1, 10, 4, 1, "") +
      range("tree-count", "Árboles en el bosque", 1, 201, 101, 20, "") +
      range("tree-noise", "Ruido", 0, 50, 20, 5, "%");
    var stage = base("Complejidad, bosque y estabilidad", controls);

    function render() {
      var depth = Number(root.querySelector("#tree-depth").value);
      var count = Number(root.querySelector("#tree-count").value);
      var noise = Number(root.querySelector("#tree-noise").value) / 100;
      var random = mulberry32(909);
      var cells = "";
      var correct = 0;
      var total = 18 * 12;
      for (var row = 0; row < 12; row += 1) {
        for (var column = 0; column < 18; column += 1) {
          var x = (column + 0.5) / 18;
          var y = (row + 0.5) / 12;
          var actual = (x - 0.5) * (x - 0.5) + (y - 0.5) * (y - 0.5) < 0.12;
          var granularity = Math.max(2, depth + 1);
          var bx = Math.floor(x * granularity) / granularity + 0.5 / granularity;
          var by = Math.floor(y * granularity) / granularity + 0.5 / granularity;
          var predicted = (bx - 0.5) * (bx - 0.5) + (by - 0.5) * (by - 0.5) < 0.12;
          var forestNoise = noise / Math.sqrt(Math.max(1, count));
          if (random() < forestNoise + Math.max(0, depth - 7) * 0.015) predicted = !predicted;
          if (predicted === actual) correct += 1;
          cells += '<rect x="' + (55 + column * 29) + '" y="' + (25 + row * 21) +
            '" width="27" height="19" rx="2" fill="' + (predicted ? palette[0] : palette[1]) +
            '" opacity="0.74"></rect>';
        }
      }
      var trainAccuracy = clamp(0.63 + depth * 0.045 + (1 - noise) * 0.08, 0, 0.995);
      var validationAccuracy = correct / total;
      var stability = 1 - noise / Math.sqrt(Math.max(1, count)) - 0.02 * Math.max(0, depth - 7);
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            cells +
            '<text class="chart-label" x="60" y="302">Frontera didáctica: la granularidad crece con profundidad</text>',
            "Cuadrícula de frontera de decisión de un ensemble didáctico"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Exactitud train", format(trainAccuracy * 100, 1) + "%") +
          metric("Exactitud validación", format(validationAccuracy * 100, 1) + "%") +
          metric("Brecha", format((trainAccuracy - validationAccuracy) * 100, 1) + " pp") +
          metric("Estabilidad", format(clamp(stability, 0, 1) * 100, 1) + "%") +
        "</div>" +
        '<p class="sim-explanation">La profundidad aumenta capacidad y brecha potencial; más árboles estabilizan el voto, pero no corrigen un diseño de validación defectuoso.</p>';
    }
    listen(render);
    render();
  }

  function kmeans(points, k, iterations) {
    var centroids = points.slice(0, k).map(function (point) { return point.slice(); });
    var labels = Array(points.length).fill(0);
    for (var iteration = 0; iteration < iterations; iteration += 1) {
      labels = points.map(function (point) {
        var best = 0;
        var bestDistance = Infinity;
        centroids.forEach(function (centroid, index) {
          var distance = Math.pow(point[0] - centroid[0], 2) + Math.pow(point[1] - centroid[1], 2);
          if (distance < bestDistance) {
            bestDistance = distance;
            best = index;
          }
        });
        return best;
      });
      centroids = centroids.map(function (centroid, index) {
        var group = points.filter(function (_, pointIndex) { return labels[pointIndex] === index; });
        return group.length
          ? [mean(group.map(function (point) { return point[0]; })), mean(group.map(function (point) { return point[1]; }))]
          : centroid;
      });
    }
    var inertia = points.reduce(function (total, point, index) {
      var centroid = centroids[labels[index]];
      return total + Math.pow(point[0] - centroid[0], 2) + Math.pow(point[1] - centroid[1], 2);
    }, 0);
    return { centroids: centroids, labels: labels, inertia: inertia };
  }

  function simulation10() {
    var controls =
      range("cluster-k", "Cantidad K", 2, 6, 3, 1, "") +
      range("cluster-iterations", "Iteraciones", 1, 15, 6, 1, "") +
      range("cluster-scale", "Escala de X", 1, 8, 1, 1, "x");
    var stage = base("K-Means y representación", controls);

    function render() {
      var k = Number(root.querySelector("#cluster-k").value);
      var iterations = Number(root.querySelector("#cluster-iterations").value);
      var scale = Number(root.querySelector("#cluster-scale").value);
      var random = mulberry32(1010);
      var centers = [[0.23, 0.28], [0.72, 0.30], [0.50, 0.73]];
      var points = [];
      centers.forEach(function (center) {
        for (var index = 0; index < 36; index += 1) {
          points.push([
            clamp(center[0] + normal(random) * 0.07, 0.03, 0.97) * scale,
            clamp(center[1] + normal(random) * 0.08, 0.03, 0.97)
          ]);
        }
      });
      var result = kmeans(points, k, iterations);
      var maxX = scale;
      var circles = points.map(function (point, index) {
        var x = 55 + point[0] / maxX * 535;
        var y = 280 - point[1] * 245;
        return '<circle cx="' + x + '" cy="' + y + '" r="4" fill="' +
          palette[result.labels[index] % palette.length] + '" opacity="0.72"></circle>';
      }).join("");
      var centroids = result.centroids.map(function (point, index) {
        var x = 55 + point[0] / maxX * 535;
        var y = 280 - point[1] * 245;
        return '<circle cx="' + x + '" cy="' + y + '" r="10" fill="none" stroke="' +
          palette[index % palette.length] + '" stroke-width="4"></circle>';
      }).join("");
      var compactness = 1 / (1 + result.inertia / points.length);
      var actionability = k === 3 ? 0.9 : k === 2 || k === 4 ? 0.72 : 0.52;
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(axes() + circles + centroids, "Puntos agrupados y centroides de K-Means", "cluster-canvas") +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Inercia", format(result.inertia, 1)) +
          metric("Compacidad", format(compactness * 100, 1) + "%") +
          metric("Iteraciones", iterations) +
          metric("Utilidad simulada", format(actionability * 100, 0) + "%") +
        "</div>" +
        '<p class="sim-explanation">Cambiar la escala de una variable modifica las distancias y puede redefinir los grupos. K se valida con estabilidad, perfiles y acción, no solo con inercia.</p>';
    }
    listen(render);
    render();
  }

  function activation(kind, value) {
    if (kind === "tanh") return Math.tanh(value);
    if (kind === "relu") return Math.max(0, value);
    return 1 / (1 + Math.exp(-value));
  }

  function simulation11() {
    var controls =
      range("weight-1", "Peso x1", -50, 50, 15, 1, "") +
      range("weight-2", "Peso x2", -50, 50, 15, 1, "") +
      range("bias", "Sesgo", -50, 50, -20, 1, "") +
      select("activation", "Activación", [["sigmoid", "Sigmoide"], ["tanh", "Tanh"], ["relu", "ReLU"]]);
    var stage = base("Neurona, activación y frontera", controls);

    function render() {
      var w1 = Number(root.querySelector("#weight-1").value) / 10;
      var w2 = Number(root.querySelector("#weight-2").value) / 10;
      var bias = Number(root.querySelector("#bias").value) / 10;
      var kind = root.querySelector("#activation").value;
      var cells = "";
      for (var row = 0; row < 20; row += 1) {
        for (var column = 0; column < 30; column += 1) {
          var x1 = column / 29;
          var x2 = 1 - row / 19;
          var output = activation(kind, w1 * x1 + w2 * x2 + bias);
          var normalized = kind === "tanh" ? (output + 1) / 2 : clamp(output, 0, 1);
          cells += '<rect x="' + (55 + column * 18) + '" y="' + (25 + row * 13) +
            '" width="18" height="13" fill="' + (normalized >= 0.5 ? palette[0] : palette[1]) +
            '" opacity="' + (0.22 + Math.abs(normalized - 0.5) * 1.25) + '"></rect>';
        }
      }
      var truth = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]];
      var correct = 0;
      var tableRows = truth.map(function (row) {
        var output = activation(kind, w1 * row[0] + w2 * row[1] + bias);
        var normalized = kind === "tanh" ? (output + 1) / 2 : clamp(output, 0, 1);
        var predicted = normalized >= 0.5 ? 1 : 0;
        if (predicted === row[2]) correct += 1;
        return "<div><span>" + row[0] + "</span><span>" + row[1] + "</span><span>" +
          format(normalized, 2) + "</span><span>" + predicted + "</span></div>";
      }).join("");
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            cells +
            '<text class="chart-label" x="60" y="310">Azul: salida baja · verde: salida alta</text>',
            "Frontera de decisión de una neurona",
            "neural-canvas"
          ) +
        "</div>" +
        '<div class="truth-table" aria-label="Tabla de verdad objetivo AND">' +
          '<div><span>x1</span><span>x2</span><span>Salida</span><span>Clase</span></div>' + tableRows +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Exactitud AND", correct + " / 4") +
          metric("Peso x1", format(w1, 1)) +
          metric("Peso x2", format(w2, 1)) +
          metric("Sesgo", format(bias, 1)) +
        "</div>" +
        '<p class="sim-explanation">Los pesos inclinan la frontera y el sesgo la desplaza. La activación transforma la combinación, pero una sola neurona sigue teniendo una frontera lineal.</p>';
    }
    listen(render);
    render();
  }

  function simulation12() {
    var controls =
      range("profit-a", "Margen producto A", 10, 80, 40, 5, "") +
      range("profit-b", "Margen producto B", 10, 80, 30, 5, "") +
      range("capacity-machine", "Horas de máquina", 40, 160, 100, 10, "") +
      range("capacity-material", "Materia prima", 40, 160, 80, 10, "");
    var stage = base("Región factible y solución", controls);

    function render() {
      var profitA = Number(root.querySelector("#profit-a").value);
      var profitB = Number(root.querySelector("#profit-b").value);
      var machine = Number(root.querySelector("#capacity-machine").value);
      var material = Number(root.querySelector("#capacity-material").value);
      var maxAxis = 90;
      var best = { a: 0, b: 0, value: 0 };
      var feasible = [];
      for (var a = 0; a <= maxAxis; a += 2) {
        for (var b = 0; b <= maxAxis; b += 2) {
          if (2 * a + b <= machine && a + 2 * b <= material) {
            feasible.push([a, b]);
            var value = profitA * a + profitB * b;
            if (value > best.value) best = { a: a, b: b, value: value };
          }
        }
      }
      function px(value) { return 55 + value / maxAxis * 535; }
      function py(value) { return 280 - value / maxAxis * 245; }
      var points = feasible.map(function (point) {
        return '<circle cx="' + px(point[0]) + '" cy="' + py(point[1]) +
          '" r="2.2" fill="' + palette[0] + '" opacity="0.32"></circle>';
      }).join("");
      var machineSlack = machine - (2 * best.a + best.b);
      var materialSlack = material - (best.a + 2 * best.b);
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            axes() + points +
            '<circle class="chart-accent" cx="' + px(best.a) + '" cy="' + py(best.b) + '" r="9"></circle>' +
            '<text class="chart-label" x="' + (px(best.a) + 12) + '" y="' + (py(best.b) - 8) + '">Óptimo</text>' +
            '<text class="chart-label" x="60" y="312">Eje X: producto A · eje Y: producto B</text>',
            "Región factible y punto de mayor beneficio",
            "lp-canvas"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Producto A", best.a) +
          metric("Producto B", best.b) +
          metric("Beneficio", format(best.value, 0)) +
          metric("Holguras", machineSlack + " / " + materialSlack) +
        "</div>" +
        '<p class="sim-explanation">El óptimo surge del objetivo y las restricciones. Cambiar un margen puede mover la mezcla; ampliar un recurso solo aporta si su restricción es vinculante.</p>';
    }
    listen(render);
    render();
  }

  function groupData(group) {
    var random = mulberry32(group === "A" ? 1313 : 1414);
    var prevalence = group === "A" ? 0.30 : 0.46;
    return Array.from({ length: 300 }, function () {
      var actual = random() < prevalence ? 1 : 0;
      var score = clamp((actual ? 0.63 : 0.31) + normal(random) * (group === "A" ? 0.18 : 0.23), 0.01, 0.99);
      return { actual: actual, score: score };
    });
  }

  function groupMetrics(rows, threshold) {
    var values = confusion(rows, threshold);
    return {
      selection: (values.tp + values.fp) / rows.length,
      fnr: values.fn / (values.fn + values.tp || 1),
      fpr: values.fp / (values.fp + values.tn || 1),
      precision: values.tp / (values.tp + values.fp || 1),
      utility: values.tp * 6 - values.fp * 2 - values.fn * 8
    };
  }

  function simulation13() {
    var controls =
      range("threshold-a", "Umbral grupo A", 10, 90, 50, 5, "%") +
      range("threshold-b", "Umbral grupo B", 10, 90, 50, 5, "%") +
      select("fair-focus", "Criterio a observar", [["selection", "Tasa de selección"], ["fnr", "Falsos negativos"], ["precision", "Precision"]]);
    var stage = base("Desempeño por grupos", controls);

    function render() {
      var thresholdA = Number(root.querySelector("#threshold-a").value) / 100;
      var thresholdB = Number(root.querySelector("#threshold-b").value) / 100;
      var focus = root.querySelector("#fair-focus").value;
      var a = groupMetrics(groupData("A"), thresholdA);
      var b = groupMetrics(groupData("B"), thresholdB);
      var rows = [
        ["Selección", a.selection, b.selection],
        ["Falsos negativos", a.fnr, b.fnr],
        ["Precision", a.precision, b.precision]
      ];
      var bars = rows.map(function (row, index) {
        var y = 50 + index * 85;
        return (
          '<text class="chart-label" x="55" y="' + (y - 9) + '">' + row[0] + '</text>' +
          '<rect x="55" y="' + y + '" width="' + (row[1] * 500) + '" height="20" rx="4" fill="' + palette[0] + '"></rect>' +
          '<rect x="55" y="' + (y + 25) + '" width="' + (row[2] * 500) + '" height="20" rx="4" fill="' + palette[1] + '"></rect>'
        );
      }).join("");
      var gap = Math.abs(a[focus] - b[focus]);
      stage.innerHTML =
        '<div class="chart-panel">' +
          svg(
            bars +
            '<rect x="460" y="286" width="16" height="10" fill="' + palette[0] + '"></rect><text class="chart-label" x="482" y="295">Grupo A</text>' +
            '<rect x="540" y="286" width="16" height="10" fill="' + palette[1] + '"></rect><text class="chart-label" x="562" y="295">Grupo B</text>',
            "Comparación de métricas de decisión para dos grupos"
          ) +
        "</div>" +
        '<div class="metric-grid">' +
          metric("Brecha seleccionada", format(gap * 100, 1) + " pp") +
          metric("FNR grupo A", format(a.fnr * 100, 1) + "%") +
          metric("FNR grupo B", format(b.fnr * 100, 1) + "%") +
          metric("Utilidad total", format(a.utility + b.utility, 0)) +
        "</div>" +
        '<p class="sim-explanation">Igualar una métrica puede separar otra cuando cambian tasas base y distribuciones. El criterio debe justificarse con daño, norma y operación.</p>';
    }
    listen(render);
    render();
  }

  function simulation14() {
    var controls =
      range("cases", "Casos por período", 100, 2000, 800, 100, "") +
      range("capstone-recall", "Recall del modelo", 20, 95, 70, 5, "%") +
      range("adoption", "Adopción de la acción", 10, 100, 65, 5, "%") +
      range("benefit", "Beneficio por acierto", 10, 150, 70, 5, "") +
      range("action-cost", "Costo por acción", 1, 40, 12, 1, "");
    var stage = base("Valor esperado y punto de equilibrio", controls);
    var milestoneKey = "datos-decisiones-capstone-milestones";

    function readMilestones() {
      try {
        return JSON.parse(localStorage.getItem(milestoneKey) || "[false,false,false,false]");
      } catch (error) {
        return [false, false, false, false];
      }
    }

    function render() {
      var cases = Number(root.querySelector("#cases").value);
      var recall = Number(root.querySelector("#capstone-recall").value) / 100;
      var adoption = Number(root.querySelector("#adoption").value) / 100;
      var benefit = Number(root.querySelector("#benefit").value);
      var actionCost = Number(root.querySelector("#action-cost").value);
      var prevalence = 0.22;
      var precision = clamp(0.35 + recall * 0.42, 0, 0.9);
      var truePositives = cases * prevalence * recall;
      var selected = truePositives / precision;
      var gross = truePositives * adoption * benefit;
      var cost = selected * actionCost;
      var net = gross - cost;
      var baselineNet = cases * prevalence * 0.35 * adoption * benefit -
        (cases * 0.28) * actionCost;
      var breakEven = selected > 0 ? cost / (truePositives * adoption || 1) : 0;
      var maxBar = Math.max(Math.abs(net), Math.abs(baselineNet), 1);
      var milestones = readMilestones();
      var milestoneLabels = ["Encuadre", "Evidencia", "Alternativas", "Defensa"];
      var milestoneHtml = milestoneLabels.map(function (label, index) {
        return '<label class="milestone-item"><input type="checkbox" data-milestone="' + index + '"' +
          (milestones[index] ? " checked" : "") + '><span>' + (index + 1) + "</span>" + label + "</label>";
      }).join("");
      var chart =
        '<text class="chart-label" x="55" y="75">Baseline</text>' +
        '<rect x="150" y="52" width="' + (Math.abs(baselineNet) / maxBar * 400) + '" height="32" rx="5" fill="' +
          (baselineNet >= 0 ? palette[1] : "#b42318") + '"></rect>' +
        '<text class="chart-label" x="55" y="155">Modelo</text>' +
        '<rect x="150" y="132" width="' + (Math.abs(net) / maxBar * 400) + '" height="32" rx="5" fill="' +
          (net >= 0 ? palette[0] : "#b42318") + '"></rect>' +
        '<text class="chart-label" x="55" y="232">Hitos del proyecto</text>' +
        '<foreignObject x="55" y="245" width="530" height="70"><div xmlns="http://www.w3.org/1999/xhtml" class="milestone-list">' +
          milestoneHtml + "</div></foreignObject>";
      stage.innerHTML =
        '<div class="chart-panel">' + svg(chart, "Comparación de valor y control de hitos") + "</div>" +
        '<div class="metric-grid">' +
          metric("Valor neto", format(net, 0)) +
          metric("Mejora vs baseline", format(net - baselineNet, 0)) +
          metric("Acciones", format(selected, 0)) +
          metric("Beneficio de equilibrio", format(breakEven, 1)) +
        "</div>" +
        '<p class="sim-explanation">El desempeño técnico crea valor solo cuando la acción se adopta, el beneficio supera el costo y la capacidad alcanza. Los hitos sostienen la trazabilidad.</p>';
      stage.querySelectorAll("[data-milestone]").forEach(function (input) {
        input.addEventListener("change", function () {
          var state = readMilestones();
          state[Number(input.dataset.milestone)] = input.checked;
          try {
            localStorage.setItem(milestoneKey, JSON.stringify(state));
          } catch (error) {
            return;
          }
        });
      });
    }
    listen(render);
    render();
  }

  var simulations = {
    "00": simulation00,
    "01": simulation01,
    "02": simulation02,
    "03": simulation03,
    "04": simulation04,
    "05": simulation05,
    "06": simulation06,
    "07": simulation07,
    "08": simulation08,
    "09": simulation09,
    "10": simulation10,
    "11": simulation11,
    "12": simulation12,
    "13": simulation13,
    "14": simulation14
  };

  function enhanceDecisionLab() {
    var storageKey = "datos-decisiones-lab-" + moduleId;
    var scenarios = { A: null, B: null };
    var panel = document.createElement("section");
    panel.className = "decision-lab";
    panel.setAttribute("aria-labelledby", "decision-lab-title");
    panel.innerHTML =
      '<div class="decision-lab-heading">' +
        '<div><span class="sim-badge">Bitácora de decisión</span>' +
        '<h2 id="decision-lab-title">Comparar antes de recomendar</h2>' +
        '<p data-lab-challenge></p></div>' +
        '<div class="scenario-actions">' +
          '<button class="button secondary" type="button" data-save-scenario="A">Guardar escenario A</button>' +
          '<button class="button secondary" type="button" data-save-scenario="B">Guardar escenario B</button>' +
        '</div>' +
      '</div>' +
      '<div class="scenario-comparison" data-scenario-comparison>' +
        '<p>Guardá dos configuraciones para comparar controles y resultados.</p>' +
      '</div>' +
      '<div class="decision-notes-grid">' +
        '<label><span>Hipótesis previa</span><textarea rows="3" data-note="hypothesis" placeholder="Si cambio…, entonces espero… porque…"></textarea></label>' +
        '<label><span>Evidencia observada</span><textarea rows="3" data-note="evidence" placeholder="Qué cambió, cuánto y en qué dirección"></textarea></label>' +
        '<label><span>Recomendación y límite</span><textarea rows="3" data-note="recommendation" placeholder="Acción, población, condición y principal límite"></textarea></label>' +
      '</div>' +
      '<div class="decision-lab-footer">' +
        '<div class="button-row">' +
          '<button class="button primary" type="button" data-save-lab>Guardar bitácora</button>' +
          '<button class="button tertiary" type="button" data-export-lab>Exportar evidencia</button>' +
          '<button class="button tertiary" type="button" data-reset-lab>Reiniciar</button>' +
        '</div>' +
        '<p role="status" aria-live="polite" data-lab-status></p>' +
      '</div>';
    panel.querySelector("[data-lab-challenge]").textContent = root.dataset.challenge ||
      "Compará alternativas y registrá qué evidencia sostiene la decisión.";
    root.insertAdjacentElement("afterend", panel);

    function controlsSnapshot() {
      return Array.from(root.querySelectorAll("input, select")).reduce(function (acc, control) {
        var label = root.querySelector('label[for="' + control.id + '"] span') ||
          root.querySelector('label[for="' + control.id + '"]');
        var key = label ? label.textContent.trim() : control.id;
        acc[key] = control.type === "checkbox" ? (control.checked ? "Sí" : "No") :
          control.value + (control.dataset.suffix || "");
        return acc;
      }, {});
    }

    function metricsSnapshot() {
      return Array.from(root.querySelectorAll(".metric-card")).reduce(function (acc, card) {
        var label = card.querySelector("span");
        var value = card.querySelector("strong");
        if (label && value) acc[label.textContent.trim()] = value.textContent.trim();
        return acc;
      }, {});
    }

    function snapshot() {
      return {
        capturedAt: new Date().toISOString(),
        controls: controlsSnapshot(),
        metrics: metricsSnapshot()
      };
    }

    function renderComparison() {
      var target = panel.querySelector("[data-scenario-comparison]");
      target.innerHTML = "";
      if (!scenarios.A && !scenarios.B) {
        target.innerHTML = "<p>Guardá dos configuraciones para comparar controles y resultados.</p>";
        return;
      }
      var keys = [];
      ["controls", "metrics"].forEach(function (group) {
        ["A", "B"].forEach(function (name) {
          if (!scenarios[name]) return;
          Object.keys(scenarios[name][group]).forEach(function (key) {
            var composite = group + "::" + key;
            if (keys.indexOf(composite) === -1) keys.push(composite);
          });
        });
      });
      var table = document.createElement("table");
      table.className = "scenario-table";
      table.innerHTML = "<caption>Comparación de escenarios guardados</caption><thead><tr><th>Indicador</th><th>Escenario A</th><th>Escenario B</th></tr></thead>";
      var body = document.createElement("tbody");
      keys.forEach(function (composite) {
        var parts = composite.split("::");
        var group = parts[0];
        var key = parts.slice(1).join("::");
        var row = document.createElement("tr");
        [key, scenarios.A && scenarios.A[group][key] || "—", scenarios.B && scenarios.B[group][key] || "—"].forEach(function (value, index) {
          var cell = document.createElement(index === 0 ? "th" : "td");
          if (index === 0) cell.setAttribute("scope", "row");
          cell.textContent = value;
          row.appendChild(cell);
        });
        body.appendChild(row);
      });
      table.appendChild(body);
      target.appendChild(table);
    }

    function notesSnapshot() {
      return Array.from(panel.querySelectorAll("[data-note]")).reduce(function (acc, field) {
        acc[field.dataset.note] = field.value.trim();
        return acc;
      }, {});
    }

    function record() {
      return {
        module: moduleId,
        challenge: root.dataset.challenge,
        notes: notesSnapshot(),
        scenarios: scenarios
      };
    }

    function setStatus(message) {
      panel.querySelector("[data-lab-status]").textContent = message;
    }

    try {
      var saved = JSON.parse(localStorage.getItem(storageKey) || "null");
      if (saved) {
        scenarios = saved.scenarios || scenarios;
        Object.keys(saved.notes || {}).forEach(function (key) {
          var field = panel.querySelector('[data-note="' + key + '"]');
          if (field) field.value = saved.notes[key];
        });
        renderComparison();
      }
    } catch (error) {
      setStatus("La bitácora local no estaba disponible; podés trabajar sin guardado persistente.");
    }

    panel.querySelectorAll("[data-save-scenario]").forEach(function (button) {
      button.addEventListener("click", function () {
        scenarios[button.dataset.saveScenario] = snapshot();
        renderComparison();
        setStatus("Escenario " + button.dataset.saveScenario + " guardado.");
      });
    });
    panel.querySelector("[data-save-lab]").addEventListener("click", function () {
      try {
        localStorage.setItem(storageKey, JSON.stringify(record()));
        setStatus("Bitácora guardada en este navegador.");
      } catch (error) {
        setStatus("No fue posible guardar localmente; exportá la evidencia.");
      }
    });
    panel.querySelector("[data-export-lab]").addEventListener("click", function () {
      var blob = new Blob([JSON.stringify(record(), null, 2)], { type: "application/json" });
      var url = URL.createObjectURL(blob);
      var link = document.createElement("a");
      link.href = url;
      link.download = "modulo-" + moduleId + "-evidencia.json";
      link.click();
      URL.revokeObjectURL(url);
      setStatus("Evidencia exportada.");
    });
    panel.querySelector("[data-reset-lab]").addEventListener("click", function () {
      scenarios = { A: null, B: null };
      panel.querySelectorAll("[data-note]").forEach(function (field) { field.value = ""; });
      try { localStorage.removeItem(storageKey); } catch (error) { /* sin persistencia */ }
      renderComparison();
      setStatus("Bitácora reiniciada.");
    });
  }

  if (simulations[moduleId]) {
    simulations[moduleId]();
    enhanceDecisionLab();
  } else {
    root.innerHTML = '<p class="alert">No se encontró la simulación solicitada.</p>';
  }
})();

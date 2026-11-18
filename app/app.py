from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pleiades</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; overflow: hidden; background: #05030f; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
  body::before { content: ""; position: fixed; inset: -20%; background: linear-gradient(120deg, #1b0b4d, #0b3a6b, #5b0f6e, #0a5a5a, #1b0b4d); background-size: 400% 400%; animation: drift 24s ease infinite; opacity: .85; }
  @keyframes drift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
  canvas { position: fixed; inset: 0; width: 100%; height: 100%; }
  .stage { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; }
  .zoomable { transform: scale(var(--z, 1)); transition: transform .2s ease-out; text-align: center; padding: 0 24px; }
  h1 { font-size: clamp(1.6rem, 4.5vw, 3.4rem); font-weight: 800; line-height: 1.25; background: linear-gradient(90deg, #ff6ec7, #ffd86e, #6effc7, #6ec8ff, #c86eff, #ff6ec7); background-size: 300% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; animation: shine 6s linear infinite; filter: drop-shadow(0 0 18px rgba(255, 255, 255, .25)); }
  @keyframes shine { to { background-position: 300% 0; } }
  .controls { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-radius: 999px; background: rgba(255, 255, 255, .1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, .25); z-index: 5; }
  button { width: 44px; height: 44px; border: 0; border-radius: 50%; font-size: 1.4rem; font-weight: 700; color: #fff; cursor: pointer; background: linear-gradient(135deg, #ff6ec7, #6ec8ff); transition: transform .15s; }
  button:hover { transform: scale(1.12); }
  button:active { transform: scale(.94); }
  #level { min-width: 64px; text-align: center; color: #fff; font-weight: 700; font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div class="stage"><div class="zoomable" id="zoomable"><h1>hello from Pleiades! GitOps is live! from VardhanYash373 :3 v2</h1></div></div>
<div class="controls">
  <button id="out" aria-label="Zoom out">&minus;</button>
  <span id="level">100%</span>
  <button id="in" aria-label="Zoom in">+</button>
  <button id="reset" aria-label="Reset zoom">&#8634;</button>
</div>
<script>
(function () {
  var MIN = 0.4, MAX = 3, STEP = 0.1;
  var z = 1;
  var zoomable = document.getElementById("zoomable");
  var level = document.getElementById("level");
  var canvas = document.getElementById("sky");
  var ctx = canvas.getContext("2d");
  var w = 0, h = 0, dpr = window.devicePixelRatio || 1;

  function setZoom(v) {
    z = Math.min(MAX, Math.max(MIN, Math.round(v * 100) / 100));
    zoomable.style.setProperty("--z", z);
    level.textContent = Math.round(z * 100) + "%";
  }

  document.getElementById("in").addEventListener("click", function () { setZoom(z + STEP); });
  document.getElementById("out").addEventListener("click", function () { setZoom(z - STEP); });
  document.getElementById("reset").addEventListener("click", function () { setZoom(1); });
  window.addEventListener("keydown", function (e) {
    if (e.key === "+" || e.key === "=") setZoom(z + STEP);
    else if (e.key === "-" || e.key === "_") setZoom(z - STEP);
    else if (e.key === "0") setZoom(1);
  });
  window.addEventListener("wheel", function (e) {
    e.preventDefault();
    setZoom(z + (e.deltaY < 0 ? STEP : -STEP));
  }, { passive: false });

  function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener("resize", resize);
  resize();

  var field = [];
  for (var i = 0; i < 320; i++) {
    field.push({
      x: Math.random() * 2 - 0.5,
      y: Math.random() * 2 - 0.5,
      r: Math.random() * 1.4 + 0.3,
      p: Math.random() * 6.28,
      s: Math.random() * 1.5 + 0.5
    });
  }

  var sisters = [
    { x: -0.30, y: -0.28, r: 7, c: "#9fd0ff" },
    { x: -0.17, y: -0.40, r: 8, c: "#ffffff" },
    { x: -0.03, y: -0.31, r: 9, c: "#b6c8ff" },
    { x: 0.10, y: -0.42, r: 6, c: "#ffd6f2" },
    { x: 0.22, y: -0.28, r: 8, c: "#9ff5ff" },
    { x: 0.31, y: -0.38, r: 6, c: "#d4b8ff" },
    { x: 0.05, y: -0.20, r: 7, c: "#c9ffe3" }
  ];

  function glow(x, y, r, color, alpha) {
    var g = ctx.createRadialGradient(x, y, 0, x, y, r * 5);
    g.addColorStop(0, color);
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.globalAlpha = alpha;
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, r * 5, 0, 6.2832);
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    var cx = w / 2, cy = h / 2, u = Math.min(w, h);
    var zs = 1 + (z - 1) * 0.35;
    for (var i = 0; i < field.length; i++) {
      var f = field[i];
      var px = cx + (f.x - 0.5) * w * zs;
      var py = cy + (f.y - 0.5) * h * zs;
      ctx.globalAlpha = 0.4 + 0.6 * Math.abs(Math.sin(t / 1000 * f.s + f.p));
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(px, py, f.r * zs, 0, 6.2832);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    for (var j = 0; j < sisters.length; j++) {
      var s = sisters[j];
      var sx = cx + s.x * u * z;
      var sy = cy + s.y * u * z;
      var rr = s.r * z * (1 + 0.15 * Math.sin(t / 700 + j));
      glow(sx, sy, rr, s.c, 0.55);
      ctx.fillStyle = s.c;
      ctx.beginPath();
      ctx.arc(sx, sy, rr, 0, 6.2832);
      ctx.fill();
    }
    requestAnimationFrame(frame);
  }

  setZoom(1);
  requestAnimationFrame(frame);
})();
</script>
</body>
</html>"""


@app.route('/')
def home():
    return PAGE


@app.route('/health')
def health():
    return {"status": "ok"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

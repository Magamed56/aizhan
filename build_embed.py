# -*- coding: utf-8 -*-
"""Собрать встраиваемый скрипт prank-embed.js из index.html.
Весь пранк кладётся в один .js: он создаёт iframe (srcdoc) и запускает страницу внутри —
изолированно от чужого проекта, но в том же origin, поэтому камера и звук работают.
Запуск: python build_embed.py"""
import base64, pathlib

HERE = pathlib.Path(__file__).parent
html = (HERE / "index.html").read_text(encoding="utf-8")
b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")

js = '''/*! Айжан-пранк — встраиваемый виджет. Добавьте на любую страницу:
      <script src="prank-embed.js"></script>
   Имя (по желанию):
      <script src="prank-embed.js" data-name="Динара"></script>
   Открыть не сразу, а по действию: <script src="prank-embed.js" data-auto="off"></script>
   и потом вызвать  window.AizhanPrank.open()  (например, по клику кнопки).
   Всё работает офлайн; камера/звук — только по действию пользователя. */
(function () {
  var B64 = "__B64__";
  function decode(b) { var bin = atob(b), bytes = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i); return new TextDecoder("utf-8").decode(bytes); }
  var script = document.currentScript, name = (script && script.dataset && script.dataset.name) || "", auto = !(script && script.dataset && script.dataset.auto === "off");
  var frame = null;
  function open(customName) {
    if (frame) return frame;
    var html = decode(B64), who = (customName || name || "").toString();
    if (who) html = html.replace("<script>", "<scr" + "ipt>window.PRANK_NAME=" + JSON.stringify(who) + ";</scr" + "ipt>\\n<script>");
    frame = document.createElement("iframe");
    frame.setAttribute("allow", "camera; microphone; autoplay; fullscreen");
    frame.setAttribute("title", "Сюрприз");
    frame.style.cssText = "position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483647;background:#120a22";
    frame.srcdoc = html;
    (document.body || document.documentElement).appendChild(frame);
    return frame;
  }
  function close() { if (frame) { frame.remove(); frame = null; } }
  window.AizhanPrank = { open: open, close: close };
  if (auto) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { open(); }); else open(); }
})();
'''.replace("__B64__", b64)

(HERE / "prank-embed.js").write_text(js, encoding="utf-8")
print("prank-embed.js собран:", (HERE / "prank-embed.js").stat().st_size, "байт (HTML", len(html), "→ base64", len(b64), ")")

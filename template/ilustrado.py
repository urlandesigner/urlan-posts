"""Template oficial "Ilustrado": Texto escuro + uma mini interface (mockup) em cada slide.

Uso: python3 template/ilustrado.py <pasta-do-post>
post.json: {"style": "ilustrado",
            "slides": [{"text": "...", "sub": "...", "mockup": "mockups/timer.html", "mockup_top": 640}],
            "closing": {"lines": ["Linha 1", "Linha 2"]},
            "cover_override": {...}}
Cada "mockup" é um trecho de HTML na própria pasta do post (só o bloco da interface).
O texto fica sempre no topo, o mockup abaixo, com o aviso "Exemplo ilustrativo".
slide-01.png é a capa da série, renderizada à parte. Referência: 2026-11-black-friday-truques/.
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render as R  # noqa: E402

CARD = "background:#FFFFFF;color:#15131A;border-radius:28px;font-family:'Inter',sans-serif;box-shadow:0 30px 80px rgba(0,0,0,.45)"
NOTE = '<div style="margin-top:22px;text-align:center;font-family:\'Inter\',sans-serif;font-size:24px;color:#6E6A77">Exemplo ilustrativo</div>'


def page(folder, s):
    html = R.text_slide(dict(s, pos="top")).rstrip()
    ui = ""
    if s.get("mockup"):
        inner = (folder / s["mockup"]).read_text()
        ui = (f'<div class="ui" style="position:absolute;left:96px;right:96px;top:{s.get("mockup_top", 640)}px">'
              f'<div style="{CARD};padding:40px 44px">{inner}</div>{NOTE}</div>')
    return html[: html.rfind("</div>")] + ui + "</div>"


def main(folder):
    folder = pathlib.Path(folder).resolve()
    p = json.loads((folder / "post.json").read_text())
    pages = [page(folder, s) for s in p["slides"]] + [R.closing_oficial(p)]
    head = (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{R.font_faces()}{R.BASE_CSS}"
            f"*{{font-family:'Google Sans Flex',sans-serif !important}} .ui,.ui *{{font-family:'Inter',sans-serif !important}}</style></head><body>")
    tmp = folder / "_ilustrado.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": R.W, "height": R.H})
        for n, body in enumerate(pages, 2):
            tmp.write_text(head + body + "</body></html>")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(folder / f"slide-{n:02d}.png"))
        b.close()
    tmp.unlink()
    print(f"{len(pages)} slides em {folder}")


if __name__ == "__main__":
    main(sys.argv[1])

"""Slides do padrão "Duplas de cores" (Figma: Redes sociais, nó 37789:29132).

Uso: python3 template/combos.py <pasta>   (lê <pasta>/post.json, gera combo-NN.png e fechamento)
post.json: {"pairs":[{"dark":["PLUM","#3B0F4C"],"light":["LILAC MIST","#EADCF5"]}, ...],
            "closing":{"lines":["Salve para","usar no seu","próximo","projeto"]}}
"""
import json, sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright

TPL = Path(__file__).parent
F = TPL / "fonts"
e = html.escape

FONTS = f"""
@font-face{{font-family:'DM Sans';font-weight:500;src:url('{(F/'dm-sans-latin-500-normal.woff2').as_uri()}')}}
@font-face{{font-family:'DM Sans';font-weight:700;src:url('{(F/'dm-sans-latin-700-normal.woff2').as_uri()}')}}
@font-face{{font-family:'DM Sans';font-weight:800;src:url('{(F/'dm-sans-latin-800-normal.woff2').as_uri()}')}}
@font-face{{font-family:'DM Sans';font-weight:900;src:url('{(F/'dm-sans-latin-900-normal.woff2').as_uri()}')}}
@font-face{{font-family:'DM Sans';font-weight:900;src:url('{(F/'dm-sans-latin-ext-900-normal.woff2').as_uri()}');unicode-range:U+0100-02AF}}
@font-face{{font-family:'DM Sans';font-weight:500;src:url('{(F/'dm-sans-latin-ext-500-normal.woff2').as_uri()}');unicode-range:U+0100-02AF}}
@font-face{{font-family:'DM Sans';font-weight:800;src:url('{(F/'dm-sans-latin-ext-800-normal.woff2').as_uri()}');unicode-range:U+0100-02AF}}
@font-face{{font-family:'DM Sans';font-weight:700;src:url('{(F/'dm-sans-latin-ext-700-normal.woff2').as_uri()}');unicode-range:U+0100-02AF}}
html,body{{margin:0;background:transparent}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:'DM Sans',sans-serif}}
"""

ARROW = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


PAD, GAP = 10, 10                      # padding da div externa e espaço entre as duas cores
CARD_H = (1350 - 2 * PAD - GAP) // 2   # 660


def card(name, hexv, bg, fg, top, hex_above, extra=""):
    label = f'<div style="font-weight:700;font-size:22px;letter-spacing:.5px">HEX: {e(hexv.upper())}</div>'
    title = f'<div style="font-weight:800;font-size:92px;line-height:1;letter-spacing:-1.5px;text-transform:uppercase;margin:{"14px 0 0" if hex_above else "0 0 14px"}">{e(name)}</div>'
    inner = (label + title) if hex_above else (title + label)
    return f'''<div style="position:absolute;left:{PAD}px;right:{PAD}px;top:{top}px;height:{CARD_H}px;border-radius:44px;background:{bg};color:{fg}">
  <div style="position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center">{inner}</div>{extra}</div>'''


def combo(pair, gap_bg):
    (dn, dh), (ln, lh) = pair["dark"], pair["light"]
    tags = f'''<div style="position:absolute;top:70px;left:64px;right:64px;display:flex;justify-content:space-between;font-weight:500;font-size:32px;color:{lh}">
      <span>#inspiration</span><span>#colors</span></div>'''
    foot = f'''<div style="position:absolute;left:64px;right:58px;bottom:58px;display:flex;justify-content:space-between;align-items:center;font-weight:500;font-size:32px;color:{dh}">
      <span>@urlan.design</span><span style="width:52px;height:52px;border-radius:50%;background:{dh}22;display:flex;align-items:center;justify-content:center">{ARROW.format(c=dh)}</span></div>'''
    return f'''<div class="s" style="background:transparent">
  {card(dn, dh, dh, lh, PAD, True, tags)}
  {card(ln, lh, lh, dh, PAD + CARD_H + GAP, False, foot)}
</div>'''


def closing(p):  # fechamento oficial, mesmo código do render.py
    sys.path.insert(0, str(TPL))
    import render as R
    return R.closing_oficial(p)


def main(folder):
    folder = Path(folder).resolve()
    p = json.loads((folder / "post.json").read_text())
    pages = [combo(pr, p.get("gap", "#15131A")) for pr in p["pairs"]] + [closing(p)]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate(pages, start=2):
            tmp = folder / "_tmp.html"
            tmp.write_text(f"<html><head><meta charset='utf-8'><style>{FONTS}</style></head><body>{body}</body></html>")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            # slides de cor saem com fundo transparente (padrão do Figma); o fechamento é opaco
            pg.screenshot(path=str(folder / f"slide-{i:02d}.png"), omit_background=True)
        b.close()
    (folder / "_tmp.html").unlink(missing_ok=True)
    print(f"{len(pages)} slides em {folder}")


if __name__ == "__main__":
    main(sys.argv[1])

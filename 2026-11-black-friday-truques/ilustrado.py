"""Black Friday no estilo texto escuro, com uma mini interface ilustrativa em cada slide.

Uso: python3 2026-11-black-friday-truques/ilustrado.py
Gera slide-02..slide-07 nesta pasta (slide-01 é a capa da série).
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "template"))
import render as R  # noqa: E402

CARD = "background:#FFFFFF;color:#15131A;border-radius:28px;font-family:'Inter',sans-serif;box-shadow:0 30px 80px rgba(0,0,0,.45)"
RED = "#E5383B"
NOTE = '<div style="margin-top:22px;text-align:center;font-family:\'Inter\',sans-serif;font-size:24px;color:#6E6A77">Exemplo ilustrativo</div>'


def box(inner, top):
    return f'<div class="ui" style="position:absolute;left:96px;right:96px;top:{top}px">{inner}{NOTE}</div>'


def ill_timer():
    def clock(t, hot):
        cells = "".join(
            f'<span style="display:inline-flex;align-items:center;justify-content:center;width:92px;height:96px;border-radius:16px;'
            f'background:{RED if hot else "#15131A"};color:#fff;font-weight:500;font-size:52px;font-variant-numeric:tabular-nums">{c}</span>'
            + ('<span style="font-size:44px;font-weight:500;margin:0 8px;color:#15131A">:</span>' if i < 2 else "")
            for i, c in enumerate(t.split(":")))
        return f'<div style="display:flex;align-items:center;justify-content:center">{cells}</div>'
    return f"""<div style="{CARD};padding:40px 44px">
  <div style="font-size:30px;font-weight:500;color:#6E6A77;text-align:center">A oferta termina em</div>
  <div style="margin-top:22px">{clock("00:00:01", True)}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:16px;margin:22px 0;color:{RED};font-size:28px;font-weight:500">
    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="{RED}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>
    um segundo depois</div>
  {clock("23:59:59", False)}
</div>"""


def ill_scarcity():
    return f"""<div style="{CARD};padding:36px;display:flex;gap:36px;align-items:center">
  <div style="flex:none;width:250px;height:250px;border-radius:20px;background:#EEEBF3;display:flex;align-items:center;justify-content:center">
    <svg width="130" height="130" viewBox="0 0 24 24" fill="none" stroke="#8E8999" stroke-width="1.4" stroke-linecap="round"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2.5" y="13" width="4.5" height="7" rx="2"/><rect x="17" y="13" width="4.5" height="7" rx="2"/></svg></div>
  <div style="flex:1">
    <div style="font-size:34px;font-weight:500">Fone sem fio</div>
    <div style="font-size:52px;font-weight:500;margin-top:8px">R$ 199</div>
    <div style="display:inline-block;margin-top:20px;padding:12px 20px;border-radius:12px;background:#FDECEC;color:{RED};font-size:28px;font-weight:500">Restam só 2 unidades!</div>
    <div style="margin-top:16px;font-size:26px;color:#6E6A77">12 pessoas vendo agora</div>
  </div>
</div>"""


def ill_preselect():
    def row(label, price, checked, hi=False):
        mark = (f'<span style="flex:none;width:46px;height:46px;border-radius:10px;background:#7120D1;display:flex;align-items:center;justify-content:center">'
                f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg></span>') if checked else ""
        bg = "background:#FBF6E9;" if hi else ""
        return (f'<div style="display:flex;align-items:center;gap:22px;padding:22px 26px;border-radius:16px;{bg}font-size:32px">'
                f'{mark}<span style="flex:1">{label}</span><span style="font-variant-numeric:tabular-nums">{price}</span></div>')
    return f"""<div style="{CARD};padding:30px 28px">
  <div style="font-size:30px;font-weight:500;color:#6E6A77;padding:0 26px 10px">Seu carrinho</div>
  {row("Fone sem fio", "R$ 199,00", False)}
  {row("Garantia estendida", "R$ 39,90", True, True)}
  {row("Seguro contra roubo", "R$ 24,90", True, True)}
  <div style="display:flex;justify-content:space-between;padding:22px 26px 6px;border-top:2px solid #EEEBF3;margin-top:8px;font-size:36px;font-weight:500"><span>Total</span><span>R$ 263,80</span></div>
</div>"""


def ill_hidden():
    def r(a, b, strong=False, red=False):
        c = RED if red else "#15131A"
        w = "500" if strong else "400"
        return f'<div style="display:flex;justify-content:space-between;font-size:30px;font-weight:{w};color:{c};padding:10px 0"><span>{a}</span><span>{b}</span></div>'
    return f"""<div style="display:flex;gap:28px;align-items:stretch">
  <div style="{CARD};flex:1;padding:32px">
    <div style="font-size:26px;color:#6E6A77">No anúncio</div>
    <div style="font-size:72px;font-weight:500;margin-top:14px">R$ 199</div>
    <div style="font-size:26px;color:#6E6A77;margin-top:8px">Fone sem fio</div>
  </div>
  <div style="{CARD};flex:1.25;padding:32px">
    <div style="font-size:26px;color:#6E6A77;margin-bottom:8px">No pagamento</div>
    {r("Produto", "R$ 199,00")}
    {r("Frete", "R$ 34,90", red=True)}
    {r("Taxa de serviço", "R$ 17,90", red=True)}
    <div style="border-top:2px solid #EEEBF3;margin-top:8px"></div>
    {r("Total", "R$ 251,80", strong=True)}
  </div>
</div>"""


def ill_shame():
    return f"""<div style="{CARD};padding:40px 44px;text-align:center">
  <div style="font-size:42px;font-weight:500">Ganhe 10% de desconto</div>
  <div style="margin-top:24px;height:84px;border-radius:14px;border:2px solid #DDD9E4;display:flex;align-items:center;padding:0 24px;font-size:28px;color:#8E8999">Seu e-mail</div>
  <div style="margin-top:20px;height:88px;border-radius:14px;background:#7120D1;color:#fff;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:500">Quero meu desconto</div>
  <div style="margin-top:26px;font-size:28px;color:#6E6A77;text-decoration:underline">Não, prefiro pagar mais caro</div>
</div>"""


ILL = [ill_timer, ill_scarcity, ill_preselect, ill_hidden, ill_shame]


def main():
    p = json.loads((HERE / "post.json").read_text())
    slides = p["slides"]
    pages = []
    for i, s in enumerate(slides):
        s = dict(s, pos="top")
        html = R.text_slide(s)
        top = s.get("ill_top", 640)
        html = html.rstrip()
        html = html[: html.rfind("</div>")] + box(ILL[i](), top) + "</div>"
        pages.append(html)
    pages.append(R.text_closing(p))
    head = (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{R.font_faces()}{R.BASE_CSS}"
            f"*{{font-family:'Google Sans Flex',sans-serif !important}} .ui,.ui *{{font-family:'Inter',sans-serif !important}}</style></head><body>")
    tmp = HERE / "_ilustrado.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": R.W, "height": R.H})
        for n, body in enumerate(pages, 2):
            tmp.write_text(head + body + "</body></html>")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(HERE / f"slide-{n:02d}.png"))
        b.close()
    tmp.unlink()
    print(len(pages), "slides")


if __name__ == "__main__":
    main()

"""Renderiza um carrossel do @urlan.design a partir de um post.json.

Uso: python3 template/render.py <pasta-do-post>
A pasta precisa ter post.json; os PNGs saem nela como slide-01.png, slide-02.png...

Formato do post.json:
{
  "tag": "IA NO DESIGN",
  "cover":   {"title": "...", "subtitle": "..."},
  "slides":  [{"title": "...", "body": "...", "takeaway": "..."}],
  "closing": {"title": "...", "body": "..."}
}
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

TPL = pathlib.Path(__file__).resolve().parent
W, H = 1080, 1350

PURPLE = "#7120D1"
VIOLET = "#A255FD"
INK = "#15131A"
MUTED = "#6E6A77"
LIGHT_BG = "#FAFAFA"


def font_faces():
    css = []
    latin = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
    ext = "U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
    for fam, slug, weights in (("DM Sans", "dm-sans", (500, 700)), ("Inter", "inter", (400, 500))):
        for w in weights:
            for sub, rng in (("latin", latin), ("latin-ext", ext)):
                f = TPL / "fonts" / f"{slug}-{sub}-{w}-normal.woff2"
                css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('{f.as_uri()}') format('woff2');unicode-range:{rng};}}")
    return "".join(css)


BASE_CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden}}
.s{{position:relative;width:{W}px;height:{H}px;padding:0 96px;font-family:'Inter',sans-serif}}
.pill{{position:absolute;top:98px;left:96px;display:inline-flex;align-items:center;gap:14px;height:66px;padding:0 30px;border-radius:999px;
  font-family:'DM Sans',sans-serif;font-weight:700;font-size:24px;letter-spacing:.5px;text-transform:uppercase}}
.pill i{{width:11px;height:11px;border-radius:50%;background:currentColor;display:block}}
.h{{font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:-2px}}
.rule{{width:96px;height:7px;border-radius:4px}}
.foot{{position:absolute;left:96px;right:96px;bottom:108px;display:flex;justify-content:space-between;align-items:center;
  font-family:'DM Sans',sans-serif;font-weight:500;font-size:33px}}
.arrow{{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
"""


def arrow_svg(color):
    return (f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            f'<path d="M5 12h14M13 6l6 6-6 6" stroke="{color}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def e(t):
    return html.escape(t or "")


def cover(p, folder):
    c = p["cover"]
    img = c.get("image")
    bg = PURPLE
    if img:
        # Capa ilustrada: a imagem ocupa a capa inteira (sangrada na parte de baixo) e o fundo
        # assume a cor do topo da imagem, com degradê para esconder a emenda.
        path = folder / img
        src = path.as_uri()
        from PIL import Image
        im = Image.open(path).convert("RGB")
        top = im.crop((0, 0, im.width, max(1, im.height // 40))).resize((1, 1)).getpixel((0, 0))
        bg = "#%02x%02x%02x" % top
        w = 1120  # um pouco além da largura da capa, para a cena sangrar nas laterais
        img_h = round(w * im.height / im.width)
        lift = 150  # a cena termina acima do rodapé, que fica livre para o @ e a seta
        text_block = f"""
  <img src="{src}" alt="" style="position:absolute;left:{(1080 - w) // 2}px;width:{w}px;bottom:{lift}px;height:{img_h}px">
  <div style="position:absolute;left:0;right:0;bottom:{lift + img_h - 200}px;height:210px;background:linear-gradient({bg},rgba(0,0,0,0))"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:{lift + 120}px;background:linear-gradient(rgba(0,0,0,0),{bg} 45%)"></div>
  <div style="position:absolute;top:220px;left:96px;right:110px">
    <h1 class="h" style="font-size:96px;line-height:1.04">{e(c['title'])}</h1>
    <div class="rule" style="background:#B794F6;margin:40px 0 34px"></div>
    <p style="font-size:36px;line-height:1.4;color:#EADDFF;max-width:820px">{e(c.get('subtitle'))}</p>
  </div>"""
    else:
        text_block = f"""
  <div style="position:absolute;top:330px;left:96px;right:110px">
    <h1 class="h" style="font-size:120px;line-height:1.04">{e(c['title'])}</h1>
    <div class="rule" style="background:#B794F6;margin:52px 0 44px"></div>
    <p style="font-size:38px;line-height:1.4;color:#EADDFF;max-width:780px">{e(c.get('subtitle'))}</p>
  </div>"""
    return f"""
<div class="s" style="background:{bg};color:#fff;overflow:hidden">{text_block}
  <div class="pill" style="background:rgba(255,255,255,.18);border:2px solid rgba(255,255,255,.22);color:#fff"><i></i>{e(p['tag'])}</div>
  <div class="foot" style="color:#fff"><span>@urlan.design</span>
    <span class="arrow" style="background:#fff">{arrow_svg(PURPLE)}</span></div>
</div>"""


def content(p, i, s):
    take = s.get("takeaway")
    take_html = (f'<div style="position:absolute;left:96px;right:96px;top:1010px;display:flex;align-items:center;gap:24px;font-size:29px;color:{INK}">'
                 f'<span style="flex:none">{arrow_svg(VIOLET).replace("24", "34", 2)}</span><span>{e(take)}</span></div>') if take else ""
    return f"""
<div class="s" style="background:{LIGHT_BG};color:{INK}">
  <div class="pill" style="background:#F1E5FF;color:{VIOLET}"><i></i>{e(p['tag'])}</div>
  <div style="position:absolute;top:290px;left:96px;right:110px">
    <div class="h" style="font-size:190px;line-height:1;letter-spacing:-6px;color:{VIOLET}">{i:02d}</div>
    <h2 class="h" style="font-size:66px;line-height:1.1;margin-top:26px;letter-spacing:-1.5px">{e(s['title'])}</h2>
    <p style="font-size:36px;line-height:1.45;color:{MUTED};margin-top:30px">{e(s['body'])}</p>
  </div>
  {take_html}
  <div class="foot" style="color:{MUTED}"><span>@urlan.design</span>
    <span class="arrow" style="background:{VIOLET}">{arrow_svg('#fff')}</span></div>
</div>"""


def closing(p):
    c = p["closing"]
    avatar = (TPL / "assets" / "avatar.png").as_uri()
    return f"""
<div class="s" style="background:{PURPLE};color:#fff">
  <div class="pill" style="background:#F3E8FF;color:{VIOLET}"><i></i>Pra fechar</div>
  <div style="position:absolute;top:370px;left:96px;right:110px">
    <h2 class="h" style="font-size:116px;line-height:1.04">{e(c['title'])}</h2>
    <div class="rule" style="background:#B794F6;margin:48px 0 44px"></div>
    <p style="font-size:38px;line-height:1.4;color:#EADDFF;max-width:760px">{e(c.get('body'))}</p>
  </div>
  <div style="position:absolute;left:90px;right:90px;bottom:96px;height:196px;border-radius:26px;background:rgba(255,255,255,.08);
       border:2px solid rgba(255,255,255,.14);display:flex;align-items:center;padding:0 36px;gap:38px">
    <img src="{avatar}" alt="" style="width:140px;height:140px;border-radius:50%;object-fit:cover;flex:none">
    <div style="flex:1;font-family:'DM Sans',sans-serif;font-weight:500;font-size:38px;line-height:1.3;color:#EADDFF">@urlan.design<br>AI Product Designer</div>
    <span style="flex:none;background:#fff;color:{PURPLE};font-family:'DM Sans',sans-serif;font-weight:700;font-size:36px;
       height:90px;padding:0 46px;border-radius:999px;display:flex;align-items:center">Seguir</span>
  </div>
</div>"""


def main(folder):
    folder = pathlib.Path(folder).resolve()
    p = json.loads((folder / "post.json").read_text())
    pages = [cover(p, folder)] + [content(p, i, s) for i, s in enumerate(p["slides"], 1)] + [closing(p)]
    head = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{font_faces()}{BASE_CSS}</style></head><body>"
    tmp = folder / "_render.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for n, body in enumerate(pages, 1):
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

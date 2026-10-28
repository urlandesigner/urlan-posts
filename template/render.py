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
    for w in (400, 500):
        for sub, rng in (("latin", latin), ("latin-ext", ext)):
            f = TPL / "fonts" / f"google-sans-code-{sub}-{w}-normal.woff2"
            if f.exists():
                css.append(f"@font-face{{font-family:'Google Sans Code';font-weight:{w};src:url('{f.as_uri()}') format('woff2');unicode-range:{rng};}}")
    # Google Sans Flex: fonte variável (peso 1 a 1000), usada quando o post pede "font": "Google Sans Flex".
    for sub, rng in (("latin", latin), ("latin-ext", ext)):
        f = TPL / "fonts" / f"google-sans-flex-{sub}-full-normal.woff2"
        if f.exists():
            css.append(f"@font-face{{font-family:'Google Sans Flex';font-weight:1 1000;font-stretch:25% 151%;src:url('{f.as_uri()}') format('woff2');unicode-range:{rng};}}")
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
        if im.height / im.width > 1.1:
            # Foto vertical: ocupa a capa inteira, com sombra no topo (título) e na base (rodapé).
            text_block = f"""
  <img src="{src}" alt="" style="position:absolute;left:0;top:{c.get('image_top', 270)}px;width:1080px;height:{round(1080 * im.height / im.width)}px">
  <div style="position:absolute;left:0;right:0;top:0;height:{c.get('image_top', 270) + 380}px;background:linear-gradient({bg} {c.get('image_top', 270)}px,rgba(22,5,56,.5) 85%,rgba(22,5,56,0))"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(rgba(22,5,56,0),rgba(22,5,56,.8))"></div>
  <div style="position:absolute;top:220px;left:96px;right:110px">
    <h1 class="h" style="font-size:96px;line-height:1.04">{e(c['title'])}</h1>
    <div class="rule" style="background:#B794F6;margin:40px 0 34px"></div>
    <p style="font-size:36px;line-height:1.4;color:#EADDFF;max-width:820px">{e(c.get('subtitle'))}</p>
  </div>"""
            return f"""
<div class="s" style="background:{bg};color:#fff;overflow:hidden">{text_block}
  <div class="pill" style="background:rgba(255,255,255,.18);border:2px solid rgba(255,255,255,.22);color:#fff"><i></i>{e(p['tag'])}</div>
  <div class="foot" style="color:#fff"><span>@urlan.design</span>
    <span class="arrow" style="background:#fff">{arrow_svg(PURPLE)}</span></div>
</div>"""
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


# ---------- Estilo "texto": só tipografia em fundo escuro ----------
# post.json: {"style": "texto", "slides": [{"text": "...", "sub": "...", "pos": "top|middle|bottom"}],
#             "closing": {"title": "...", "body": "..."}}
# Uma palavra ou trecho entre **asteriscos** fica destacado em lilás.
DARK = "#15131A"
DARK_MUTED = "#8E8999"  # contraste ~5.7:1 sobre o fundo escuro


def rich(t):
    import re
    return re.sub(r"\*\*(.+?)\*\*", rf'<span style="color:{VIOLET}">\1</span>', e(t))


def text_slide(s, last=False):
    pos = s.get("pos", "middle")
    place = {"top": "top:180px", "middle": "top:50%;transform:translateY(-55%)", "bottom": "bottom:230px"}[pos]
    align = "right" if s.get("align") == "right" else "left"
    sub = (f'<p style="margin-top:40px;font-family:\'DM Sans\',sans-serif;font-weight:500;font-size:56px;line-height:1.12;'
           f'letter-spacing:0;color:{DARK_MUTED}">{rich(s["sub"])}</p>') if s.get("sub") else ""
    return f"""
<div class="s" style="background:{DARK};color:#fff">
  <div style="position:absolute;left:96px;right:96px;{place};text-align:{align}">
    <p class="h" style="font-size:{132 if s.get('size') == 'xl' else 88}px;line-height:1.04;letter-spacing:{-4 if s.get('size') == 'xl' else -2.5}px">{rich(s['text'])}</p>{sub}
  </div>
  <div class="foot" style="color:{DARK_MUTED}"><span>@urlan.design</span>
    <span class="arrow" style="background:{VIOLET}">{arrow_svg('#fff')}</span></div>
</div>"""


def text_closing(p):
    c = p["closing"]
    hd = TPL / "assets" / "avatar-hd.webp"
    avatar = (hd if hd.exists() else TPL / "assets" / "avatar.png").as_uri()
    return f"""
<div class="s" style="background:{DARK};color:#fff">
  <div style="position:absolute;top:300px;left:96px;right:96px">
    <h2 class="h" style="font-size:100px;line-height:1.06">{rich(c['title'])}</h2>
    <p style="margin-top:40px;font-size:40px;line-height:1.4;color:{DARK_MUTED};max-width:820px">{rich(c.get('body'))}</p>
  </div>
  <div style="position:absolute;left:90px;right:90px;bottom:96px;height:196px;border-radius:26px;background:rgba(255,255,255,.05);
       border:2px solid rgba(255,255,255,.1);display:flex;align-items:center;padding:0 36px;gap:38px">
    <img src="{avatar}" alt="" style="width:140px;height:140px;border-radius:50%;object-fit:cover;flex:none">
    <div style="flex:1;font-family:'DM Sans',sans-serif;font-weight:500;font-size:38px;line-height:1.3;color:#EADDFF">@urlan.design<br>AI Product Designer</div>
    <span style="flex:none;background:{VIOLET};color:#fff;font-family:'DM Sans',sans-serif;font-weight:700;font-size:36px;
       height:90px;padding:0 46px;border-radius:999px;display:flex;align-items:center">Seguir</span>
  </div>
</div>"""


# ---------- Estilo "editorial": capa com foto de produto + itens limpos (listas, repos, ferramentas) ----------
# post.json: {"style": "editorial", "cover": {"lines": ["4 REPOS", "**BOMBANDO**"], "tag": "(OUTUBRO 2026)",
#   "subtitle": "...", "image": "cover-image.png", "top_right": "...", "foot_right": "..."},
#   "items": [{"name": "...", "ref": "owner/repo", "stat": "89 mil estrelas", "what": "...", "why": "..."}],
#   "closing": {"lines": [...], "body": "..."}}
ED_BG = "#F3F0F8"
ED_INK = "#15131A"
ED_MONO_MUTED = "#5E5A68"  # 6.0:1 sobre ED_BG

MONO = "font-family:'Google Sans Code',monospace"
CONDENSED = "font-family:'Google Sans Flex',sans-serif;font-weight:900;font-stretch:72%;text-transform:uppercase"


def rich_ed(t):
    import re
    return re.sub(r"\*\*(.+?)\*\*", rf'<span style="color:{PURPLE}">\1</span>', e(t))


def ed_arrow(color=ED_INK):
    return (f'<svg width="96" height="24" viewBox="0 0 96 24" fill="none" aria-hidden="true"><path d="M2 12h90M80 3l11 9-11 9" '
            f'stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def ed_frame(inner, foot_left="@URLAN.DESIGN", foot_right="", top_right="", bg=ED_BG, extra="", footer=True):
    foot = (f'''<div style="position:absolute;left:96px;right:96px;bottom:84px;border-top:2px solid rgba(21,19,26,.55);padding-top:22px;display:flex;justify-content:space-between;align-items:flex-start;{MONO};font-size:22px;letter-spacing:2px;line-height:1.5">
    <span>{e(foot_left)}</span><span style="text-align:right;white-space:pre-line">{e(foot_right)}</span></div>''') if footer else ""
    return f"""
<div class="s" style="background:{bg};color:{ED_INK};overflow:hidden;padding:0">{extra}
  <div style="position:absolute;top:84px;left:96px;right:96px;display:flex;justify-content:space-between;{MONO};font-weight:500;font-size:26px;letter-spacing:2px">
    <span style="font-family:'Google Sans Flex',sans-serif;font-weight:500;font-size:30px;letter-spacing:0">@urlan.design</span><span>{e(top_right)}</span></div>
  {inner}
  {foot}
</div>"""


def ed_cover(p, folder):
    c = p["cover"]
    bg = ED_BG
    bg_img = ""
    if c.get("image"):
        # Foto de produto ocupando a parte de baixo da capa. O fundo da capa assume a cor do topo da
        # foto e um degradê esconde as bordas, para o objeto parecer "solto" na capa inteira.
        from PIL import Image
        path = folder / c["image"]
        im = Image.open(path).convert("RGB")
        bg = "#%02x%02x%02x" % im.crop((0, 0, im.width, max(1, im.height // 30))).resize((1, 1)).getpixel((0, 0))
        left_c = "#%02x%02x%02x" % im.crop((0, 0, max(1, im.width // 30), im.height // 2)).resize((1, 1)).getpixel((0, 0))
        w = c.get("image_width", 1180)
        top = c.get("image_top", 290)
        left = c.get("image_left", 0)
        h = round(w * im.height / im.width)
        bg_img = f"""
  <img src="{path.as_uri()}" alt="" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px">
  <div style="position:absolute;left:0;right:0;top:{top - 2}px;height:260px;background:linear-gradient({bg},rgba(0,0,0,0))"></div>
"""
    lines = "".join(f'<div><span class="ln">{rich_ed(l)}</span></div>' for l in c["lines"])
    inner = f"""
  <div style="position:absolute;top:170px;left:90px;right:60px">
    <div class="fit-lines" style="{CONDENSED};font-size:{c.get('size', 200)}px;line-height:.9;letter-spacing:-2px;white-space:nowrap">{lines}</div>
    <div style="{MONO};font-size:40px;margin-top:22px">{e(c.get('tag'))}</div>
  </div>
  <div style="position:absolute;left:96px;top:{c.get('sub_top', 760)}px;width:{c.get('sub_width', 340)}px;{MONO};font-size:24px;line-height:1.55;letter-spacing:2px;text-transform:uppercase">{e(c.get('subtitle'))}
    <div style="margin-top:30px">{ed_arrow()}</div></div>"""
    return ed_frame(inner, foot_left=p_foot.get("left", ""), foot_right=c.get("foot_right", ""), top_right=c.get("top_right", ""), bg=bg, extra=bg_img)


def ed_item(i, it, total):
    star = ('<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6-4.9-4.6 6.6-.8z" '
            f'fill="{PURPLE}"/></svg>')
    block = lambda label, txt: (f'<div style="margin-top:56px"><div style="{MONO};font-size:24px;letter-spacing:3px;color:{ED_MONO_MUTED}">{label}</div>'
                                f'<p style="margin-top:14px;font-family:\'Google Sans Flex\',sans-serif;font-weight:500;font-size:44px;line-height:1.25">{rich_ed(txt)}</p></div>')
    inner = f"""
  <div style="position:absolute;top:220px;left:96px;right:96px">
    <div style="{MONO};font-size:34px;color:{PURPLE};font-weight:500">{i:02d}</div>
    <div class="fit" style="{CONDENSED};font-size:150px;line-height:.92;margin-top:14px;letter-spacing:-1px;white-space:nowrap">{e(it['name'])}</div>
    <div style="display:flex;align-items:center;gap:18px;margin-top:30px;{MONO};font-size:28px">
      <span>{e(it['ref'])}</span><span style="opacity:.4">·</span>{star}<span>{e(it['stat'])}</span></div>
    <div style="height:2px;background:rgba(21,19,26,.15);margin-top:44px"></div>
    {block(p_foot.get('label_what', 'O QUE FAZ'), it['what'])}
    {block(p_foot.get('label_why', 'POR QUE IMPORTA'), it['why'])}
  </div>"""
    return ed_frame(inner, foot_left=p_foot.get("left", ""), foot_right=p_foot.get("right", ""), top_right=p_foot.get("top_right", ""))


def ed_closing(p):
    c = p["closing"]
    hd = TPL / "assets" / "avatar-hd.webp"
    avatar = (hd if hd.exists() else TPL / "assets" / "avatar.png").as_uri()
    lines = "".join(f'<div><span class="ln">{rich_ed(l)}</span></div>' for l in c["lines"])
    inner = f"""
  <div style="position:absolute;top:260px;left:90px;right:60px">
    <div class="fit-lines" style="{CONDENSED};font-size:170px;line-height:.9;letter-spacing:-2px;white-space:nowrap">{lines}</div>
    <p style="margin-top:44px;{MONO};font-size:28px;line-height:1.55;letter-spacing:2px;text-transform:uppercase;max-width:760px">{e(c.get('body'))}</p>
  </div>
  <div style="position:absolute;left:90px;right:90px;bottom:96px;height:180px;border-radius:24px;background:#FFFFFF;
       border:2px solid rgba(21,19,26,.08);display:flex;align-items:center;padding:0 32px;gap:32px">
    <img src="{avatar}" alt="" style="width:120px;height:120px;border-radius:50%;object-fit:cover;flex:none">
    <div style="flex:1;font-family:'Google Sans Flex',sans-serif;font-weight:500;font-size:36px;line-height:1.3">@urlan.design<br><span style="color:{ED_MONO_MUTED}">AI Product Designer</span></div>
    <span style="flex:none;background:{PURPLE};color:#fff;font-family:'Google Sans Flex',sans-serif;font-weight:700;font-size:34px;
       height:84px;padding:0 44px;border-radius:999px;display:flex;align-items:center">Seguir</span>
  </div>"""
    return ed_frame(inner, top_right=p_foot.get("top_right", ""), footer=False)


p_foot = {}

# Reduz o tamanho da fonte de títulos marcados até caberem na largura disponível (888 px).
FIT_JS = """() => {
  // Reduz a fonte até a linha mais larga caber na largura do próprio bloco.
  for (const el of document.querySelectorAll('.fit, .fit-lines')) {
    const limit = el.clientWidth;
    const spans = el.classList.contains('fit-lines') ? [...el.querySelectorAll('.ln')] : [];
    const widest = () => spans.length ? Math.max(...spans.map(s => s.offsetWidth)) : el.scrollWidth;
    let size = parseFloat(getComputedStyle(el).fontSize);
    while (widest() > limit && size > 40) { size -= 2; el.style.fontSize = size + 'px'; }
  }
}"""


def main(folder):
    folder = pathlib.Path(folder).resolve()
    p = json.loads((folder / "post.json").read_text())
    if p.get("style") == "texto":
        pages = [text_slide(s) for s in p["slides"]] + [text_closing(p)]
    elif p.get("style") == "editorial":
        p_foot.update(p.get("footer", {}))
        items = p["items"]
        pages = [ed_cover(p, folder)] + [ed_item(i, it, len(items)) for i, it in enumerate(items, 1)] + [ed_closing(p)]
    else:
        pages = [cover(p, folder)] + [content(p, i, s) for i, s in enumerate(p["slides"], 1)] + [closing(p)]
    override = ""
    if p.get("style") == "texto" and not p.get("font"):
        p["font"] = "Google Sans Flex"  # padrão visual do post só de texto (aprovado em 27/10/2026)
    if p.get("style") == "editorial" and p.get("case") == "sentence":
        override += ".s *{text-transform:none !important}"
    if p.get("font"):
        # Troca a fonte do post inteiro (títulos, textos, @ e card), mantendo tamanhos e layout.
        override = f"*{{font-family:'{p['font']}',sans-serif !important}}"
    head = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{font_faces()}{BASE_CSS}{override}</style></head><body>"
    tmp = folder / "_render.html"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        if p.get("style") == "editorial" and p.get("case") == "sentence":
            pages = [pg_.replace("font-weight:900;font-stretch:72%", "font-weight:700;font-stretch:100%").replace("line-height:.9;letter-spacing:-2px", "line-height:1.02;letter-spacing:-3px").replace("line-height:.92;margin-top:14px;letter-spacing:-1px", "line-height:1;margin-top:14px;letter-spacing:-3px").replace("letter-spacing:2px", "letter-spacing:0").replace("letter-spacing:3px", "letter-spacing:0") for pg_ in pages]
        for n, body in enumerate(pages, 1):
            tmp.write_text(head + body + "</body></html>")
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.evaluate(FIT_JS)
            pg.screenshot(path=str(folder / f"slide-{n:02d}.png"))
        b.close()
    tmp.unlink()
    print(f"{len(pages)} slides em {folder}")


if __name__ == "__main__":
    main(sys.argv[1])

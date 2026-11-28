"""Carrossel em vídeo: cada slide é uma cena oficial animada (plugin theme-examples, Apache 2.0) com texto mínimo.
Uso: python3 video/make.py  (de dentro da pasta do post). Gera video/slide-NN.mp4 e video/still-NN.png."""
import pathlib, subprocess, shutil, json
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; POST = HERE.parent; TPL = POST.parent / 'template'
FONTS = f"""@font-face{{font-family:GSF;src:url('{(TPL/'fonts'/'google-sans-flex-latin-full-normal.woff2').as_uri()}');font-weight:1 1000}}
@font-face{{font-family:GSC;src:url('{(TPL/'fonts'/'google-sans-code-latin-500-normal.woff2').as_uri()}')}}
@font-face{{font-family:Caveat;src:url('{(POST.parent/'testes-capa'/'serie'/'caveat-latin-700-normal.woff2').as_uri()}');font-weight:700}}"""
FPS, DUR = 30, 5.0
SLIDES = [
 dict(scene='night-reef', name='Night Reef', align='xMaxYMax', speed=4, cover=True),
 dict(scene='honu-lagoon', name='Honu Lagoon', align='xMaxYMid', speed=4, title='O fundo do app agora pode ser uma <em>cena animada.</em>', window=True),
 dict(scene='koi-mosaic', name='Koi Mosaic', align='xMaxYMid', speed=12, title='Instala com <em>um comando.</em>', code='/plugin install theme-examples@claude-plugins-official'),
 dict(scene='departure-board', name='Departure Board', align='xMaxYMid', speed=20, title='São <em>38 cenas</em> pra escolher.', code='/custom-theme list'),
 dict(scene='halftone-dawn', name='Halftone Dawn', align='xMaxYMax', speed=6, title='Ou pede um tema com as <em>cores da sua marca.</em>', code='Cria um tema com o roxo #7120D1 e o lilás #A255FD'),
 dict(scene='paper-garden', name='Paper Garden', align='xMinYMax', speed=4, title='Hoje no app desktop, em <em>sessão local.</em> Nuvem vem em breve.'),
]
CSS = """*{margin:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden;background:#0E0C12}
.st{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:GSF}
.sc svg{position:absolute;inset:0;width:1080px;height:1350px;display:block}
.shade{position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(#0E0C12ee,#0E0C12aa 55%,#0E0C1200)}
.t{position:absolute;left:84px;right:84px;top:150px;color:#fff;font-weight:800;font-size:96px;line-height:1.0;letter-spacing:-3px}
.t em{font-style:normal;color:#C9A8FF}
.code{position:absolute;left:84px;right:84px;top:470px;padding:22px 26px;border-radius:20px;background:rgba(14,12,18,.82);border:2px solid rgba(255,255,255,.18);color:#fff;font-family:GSC;font-size:30px;line-height:1.35;word-break:break-word}
.foot{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#fff;font-weight:500;text-shadow:0 2px 12px #0009}
.foot span{background:rgba(14,12,18,.72);padding:8px 16px;border-radius:999px}.foot span:last-child{font-size:22px}
.win{position:absolute;left:130px;right:130px;top:560px;height:600px;border-radius:30px;border:2px solid rgba(255,255,255,.5);box-shadow:0 30px 90px #0006;overflow:hidden}
.win .bar{height:54px;background:rgba(255,255,255,.35);backdrop-filter:blur(10px);display:flex;gap:12px;align-items:center;padding:0 22px}
.win .bar i{width:16px;height:16px;border-radius:50%;background:#0005}
.pn{position:absolute;padding:20px 24px;border-radius:18px;background:rgba(255,255,255,.55);backdrop-filter:blur(14px);font-size:28px;color:#15131A;font-weight:500}
.mid{position:absolute;left:0;right:0;top:50%;transform:translateY(-60%);text-align:center;color:#fff}
.mid .s{font-family:Caveat;font-weight:700;font-size:86px;color:#7FE3D6}
.mid .tt{font-weight:800;font-size:200px;line-height:.9;letter-spacing:-6px;margin:18px 0 22px;text-shadow:0 6px 40px #0006}"""
def page(sl):
    svg = (POST/'cenas'/'svg'/f"svg-{sl['scene']}.svg").read_text()
    if sl.get('cover'):
        body = f"""<div class="mid"><div class="s">Temas no Claude Code</div><div class="tt">Com a sua<br>marca</div><div class="s">38 cenas animadas</div></div>"""
        shade = '<div class="shade" style="height:1350px;background:linear-gradient(#0E0C12cc,#0E0C1266 60%,#0E0C1200)"></div>'
    else:
        body = f'<div class="t">{sl["title"]}</div>' + (f'<div class="code">{sl["code"]}</div>' if sl.get('code') else '')
        shade = '<div class="shade"></div>'
        if sl.get('window'):
            body += '<div class="win"><div class="bar"><i></i><i></i><i></i></div><div class="pn" style="left:30px;top:90px">Cria uma tela de login</div><div class="pn" style="right:30px;bottom:30px">Pronto. Vou abrir o arquivo.</div></div>'
    foot = f'<div class="foot"><span>@urlan.design</span><span>Cena {sl["name"]} · plugin oficial da Anthropic</span></div>'
    return f"<html><head><meta charset='utf-8'><style>{FONTS}{CSS}</style></head><body><div class='st'><div class='sc'>{svg}</div>{shade}{body}{foot}</div></body></html>"
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
    for i, sl in enumerate(SLIDES, 1):
        tmp = HERE/'_p.html'; tmp.write_text(page(sl)); pg.goto(tmp.as_uri()); pg.evaluate('document.fonts.ready')
        pg.evaluate(f"document.querySelector('.sc svg').setAttribute('preserveAspectRatio','{sl['align']} slice')")
        pg.wait_for_timeout(300)
        fr = HERE/f'_f{i}'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
        for n in range(int(FPS*DUR)):
            t = n/FPS*1000*sl['speed']
            pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}})")
            pg.screenshot(path=str(fr/f'{n:04d}.png'))
        shutil.copy(fr/'0000.png', HERE/f'still-{i:02d}.png')
        subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(fr/'%04d.png'),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(HERE/f'slide-{i:02d}.mp4')],check=True)
        shutil.rmtree(fr); print('ok', i)
    b.close(); (HERE/'_p.html').unlink()

import sys, asyncio, os
from playwright.async_api import async_playwright
W = os.path.dirname(os.path.abspath(__file__))
FPS = 30
PAGE = os.environ.get('PAGE', 'index.html')
PFX = os.environ.get('PFX', 'still')
OUT = os.environ.get('OUT', 'frames')
RAF = 'new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))'

async def main(mode, args):
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + W + '/' + PAGE)
        await pg.wait_for_function('window.ready===true')
        if mode == 'stills':
            for t in [float(x) for x in args]:
                await pg.evaluate(f'seek({t})'); await pg.evaluate(RAF)
                await pg.screenshot(path=f'{W}/{PFX}_{t:.1f}.png')
        else:
            os.makedirs(f'{W}/{OUT}', exist_ok=True)
            for f in range(int(args[0]), int(args[1])):
                await pg.evaluate(f'seek({f/FPS})'); await pg.evaluate(RAF)
                await pg.screenshot(path=f'{W}/{OUT}/f_{f:05d}.png')
        await br.close()

asyncio.run(main(sys.argv[1], sys.argv[2:]))

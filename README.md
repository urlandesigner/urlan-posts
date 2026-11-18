# urlan-posts

Carrosséis e Reels do Instagram @urlan.design, produzidos com assistência de IA e agendados somente pela mLabs.

- `template/`: modelo visual (capa, conteúdo e fechamento) com as fontes e o avatar.
- `AAAA-MM-tema/`: uma pasta por post, com `post.json` (texto, legenda, fontes e link do post) e os slides em PNG.
- `REGRAS.md`: regras de texto, visual e publicação que todo post segue.
- `AGENTS.md`: contexto operacional e limites para os agentes.
- `STATUS.md`: estado atual de publicações, agendamentos e pendências.

## Preparação local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Para gerar os slides de um post:

```bash
source .venv/bin/activate
python3 template/render.py 2026-10-rea
```

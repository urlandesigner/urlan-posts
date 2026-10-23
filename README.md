# urlan-posts

Carrosséis do Instagram @urlan.design, gerados pelo Claude e agendados no Metricool.

- `template/`: modelo visual (capa, conteúdo e fechamento) com as fontes e o avatar.
- `AAAA-MM-tema/`: uma pasta por post, com `post.json` (texto, legenda, fontes e link do post) e os slides em PNG.
- `REGRAS.md`: regras de texto, visual e publicação que todo post segue.

Para gerar os slides de um post: `python3 template/render.py 2026-10-rea`

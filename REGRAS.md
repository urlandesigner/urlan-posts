# Regras dos carrosséis @urlan.design

Regras fixas para todo carrossel gerado neste repositório. Valem junto com o documento de marca do projeto Instagram (`CONTEXTO_marca_urlan_design_resumido.md`). Se houver conflito, este arquivo vale para produção e publicação; o documento de marca vale para posicionamento e tom.

## Estrutura do post

- 1 capa + 4 a 6 slides de conteúdo + 1 fechamento. Máximo de 10 imagens.
- Capa: selo do pilar (ex.: "IA NO DESIGN"), título que é o hook, subtítulo de uma frase.
- Conteúdo: número grande (o item, não a página), título, texto curto e uma frase-resumo com seta.
- Fechamento: selo "PRA FECHAR", título com a CTA, uma frase de apoio e o card de perfil com "Seguir".
- A CTA segue o objetivo do post: alcance pede comentar, salvar ou compartilhar. Link na bio só em post de cliente.

## Texto dos slides

- Título do slide: de 2 a 5 palavras, de preferência como pergunta ("Funciona mesmo?").
- Texto do slide: de 12 a 20 palavras, no máximo 3 linhas.
- Frase-resumo: até 7 palavras, em minúscula, sem ponto final. Não pode repetir o texto do slide.
- Cada frase diz literalmente o que a coisa faz ou o que aconteceu. Nada de metáfora, frase de efeito ou ideia que o leitor precise adivinhar.
- Tom coloquial e profissional: "pra" e "tá" são permitidos. Sem gíria forçada, sem emojis, sem travessões.
- Proibido: "a leitura que fica é", "a direção é clara", "não é sobre X, é sobre Y", trios de substantivos abstratos ("fluxo, contexto e acabamento"), "no fim do dia", "game changer".
- Nada de números, resultados ou casos inventados. Todo fato vem de fonte pesquisada, e as fontes ficam no `post.json` (campo `sources`).

## Legenda

- Entre 40 e 90 palavras, sem contar hashtags.
- Abre com uma frase literal sobre o assunto, nunca com uma metáfora.
- Não repete os slides: explica o contexto em linguagem simples e diz por que importa pra quem desenha produto.
- Termina com a mesma CTA do fechamento.
- 4 ou 5 hashtags, no fim.

## Revisão antes de publicar

Antes de subir qualquer imagem, reler o texto com estas perguntas e corrigir o que falhar:

1. Alguém que não conhece o assunto entende cada frase na primeira leitura?
2. Alguma frase é metáfora, slogan ou abstração? Trocar por uma descrição literal.
3. Algum slide passa de 20 palavras? Cortar.
4. A frase-resumo só repete o texto? Reescrever.
5. A legenda repete os slides? Reescrever por outro ângulo.
6. Algum número ou fato está sem fonte? Remover ou buscar a fonte.

## Visual

- O template é `template/render.py`. Ele reproduz o padrão do Figma "Redes sociais" (frame "Roxa"): capa roxa, conteúdo claro, fechamento roxo com card de perfil.
- Tokens: roxo `#7120D1`, lilás `#A255FD`, texto `#15131A`, texto secundário `#6E6A77`, fundo claro `#FAFAFA`.
- Fontes: DM Sans (títulos, selo, @) e Inter (texto corrido), arquivos em `template/fonts/`.
- Formato 1080 × 1350 px, margem lateral de 96 px.
- Não mexer no layout por post. Mudança de visual se faz no template e vale para todos.
- **Post só de texto** (`"style": "texto"` no `post.json`): fundo #15131A, fonte **Google Sans Flex** (padrão desse estilo), frase principal em negrito com uma palavra em lilás (`**palavra**`), frase de apoio em peso médio e cinza #8E8999, texto alternando entre topo, meio e base, card de perfil com a foto em alta (`template/assets/avatar-hd.webp`) no fechamento. Usar para posts de opinião. Referência aprovada: `2026-10-cliente-sistema-gsf/`.
- Estilo único por enquanto: todos os posts usam este padrão (capa roxa flat). Os outros estilos de capa do documento de marca (aurora escura, citação, foto) não estão em uso até o Urlan liberar.

## Publicação

1. Criar a pasta `AAAA-MM-tema/` com o `post.json` e gerar os slides: `python3 template/render.py AAAA-MM-tema`.
2. Conferir a folha de contato dos slides antes de subir.
3. Fazer commit e push. Nos links das imagens, usar o hash do commit, não `main`: `https://raw.githubusercontent.com/urlandesigner/urlan-posts/<commit>/<pasta>/slide-01.png`. Com `main`, o GitHub pode servir uma versão antiga em cache.
4. Criar o post no Metricool (marca `urlan.design`, rede Instagram, tipo POST), com texto alternativo em cada imagem e `isAiGenerated: false`.
5. Modo padrão: rascunho. Só publicar direto quando isso estiver combinado.
6. Depois do horário marcado, conferir no Metricool se o status mudou para "Published" e guardar o link do post no `post.json` (campo `instagramUrl`). Um carrossel pode levar até 5 minutos para processar.

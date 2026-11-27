# Regras dos carrosséis @urlan.design

Regras fixas para todo carrossel gerado neste repositório. Valem junto com o documento de marca do projeto Instagram (`CONTEXTO_marca_urlan_design_resumido.md`). Se houver conflito, este arquivo vale para produção e publicação; o documento de marca vale para posicionamento e tom.

## Templates oficiais (decisão de 27/11/2026)

Todo post novo usa um destes quatro templates, escolhido pelo tipo de post. Exemplos aprovados em `templates-oficiais/`.

| Tipo de post | Template | `style` no post.json | Como gerar |
|---|---|---|---|
| Explicativo: pesquisa, novidade, erro, como fazer, opinião, história | **Texto escuro** | `texto` | `python3 template/render.py <pasta>` |
| Explicativo que precisa mostrar uma interface (golpe, padrão de tela, antes e depois) | **Ilustrado** | `ilustrado` | `python3 template/ilustrado.py <pasta>` |
| Lista de recursos: repositórios, ferramentas, sites | **Editorial** | `editorial` | `python3 template/render.py <pasta>` |
| Paleta de cores | **Combos** | `combos` | `python3 template/combos.py <pasta>` |

- **Capa:** sempre a capa "série" (seção "Capas: referência fixa"), em `slide-01.png`, com `cover_override` no post.json.
- **Fechamento:** um só para todos os templates, o do Combos: fundo escuro com brilho roxo, ícone de salvar, título grande e card de perfil, tudo em Google Sans Flex 800 (decisão de 27/11/2026, pra acompanhar o peso dos slides de conteúdo). No post.json: `"closing": {"lines": ["Você já caiu", "nesse **erro**?"]}`. O fechamento não tem texto de apoio; o complemento da CTA vai na legenda.
- **Aposentados:** Padrão roxo, Padrão claro e Alternado. Ficam só para refazer posts antigos (`"legado": true` no post.json). O `render.py` recusa esses estilos em post novo.
- Mudança de template, fechamento ou capa se faz no código do template e vale para todos. Não criar estilo novo por post.

### Texto escuro e Ilustrado: regras do texto

- Uma ideia por slide, de 5 a 7 slides de conteúdo.
- `text`: frase principal, de 4 a 10 palavras, com uma palavra ou trecho em `**lilás**`.
- `sub`: frase de apoio, até 16 palavras, no máximo 3 linhas.
- `pos`: alternar entre `top`, `middle` e `bottom`. O primeiro slide pode usar `"size": "xl"`.
- No Ilustrado, o texto fica no topo e o mockup (HTML na pasta do post, campo `mockup`) logo abaixo, com o aviso "Exemplo ilustrativo".

## Estrutura do post

- 1 capa + 4 a 7 slides de conteúdo + 1 fechamento. Máximo de 10 imagens.
- Capa: selo do pilar (ex.: "IA NO DESIGN"), título que é o hook, subtítulo de uma frase.
- Conteúdo: segue o template escolhido (tabela acima).
- Fechamento: o fechamento oficial, com a CTA no título e o card de perfil com "Seguir".
- A CTA segue o objetivo do post: alcance pede comentar, salvar ou compartilhar. Link na bio só em post de cliente.

## Texto dos slides

(As medidas abaixo valem para os templates aposentados e para o Editorial. Texto escuro e Ilustrado seguem as regras da seção deles.)

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

- Os templates oficiais estão na seção "Templates oficiais". O padrão roxo do Figma "Redes sociais" (frame "Roxa") está aposentado desde 27/11/2026.
- Tokens: roxo `#7120D1`, lilás `#A255FD`, texto `#15131A`, texto secundário `#6E6A77`, fundo claro `#FAFAFA`.
- Fontes: DM Sans (títulos, selo, @) e Inter (texto corrido), arquivos em `template/fonts/`.
- Formato 1080 × 1350 px, margem lateral de 96 px.
- Não mexer no layout por post. Mudança de visual se faz no template e vale para todos.
- **Post só de texto** (`"style": "texto"` no `post.json`): fundo #15131A, fonte **Google Sans Flex** (padrão desse estilo), frase principal em negrito com uma palavra em lilás (`**palavra**`), frase de apoio em peso médio e cinza #8E8999, texto alternando entre topo, meio e base, card de perfil com a foto em alta (`template/assets/avatar-hd.webp`) no fechamento. Usar para posts de opinião. Referência aprovada: `2026-10-cliente-sistema-gsf/`.
- **Post editorial** (`"style": "editorial"`): para listas de repositórios, ferramentas ou recursos. Capa com foto de produto (gerada no Higgsfield) sangrando a capa, título em Google Sans Flex peso 900 e largura 72% em maiúsculas com a palavra de destaque em roxo #7120D1; itens limpos (número, nome, referência, uma estatística e duas frases: "O que faz" e "Por que importa"), sem prints. Textos pequenos e técnicos em **Google Sans Code**. Referência aprovada: `2026-10-repos-em-alta/`. Texto com só a primeira letra maiúscula (`"case": "sentence"` no `post.json`), não em caixa alta.
- **Imagem de capa (Higgsfield):** modelo padrão Nano Banana Pro (`nano_banana_pro`, 2k, 3:4, cerca de 2 créditos), gerado do zero sem imagem de referência, com a metade de cima do fundo vazia pro título. Uma geração por capa; segunda só se a primeira não servir. Z Image só pra rascunho barato. Baixar o resultado direto com `curl` do `result_url` (domínio `d8j0ntlcm91z4.cloudfront.net` liberado em 28/10/2026); o Chrome só como plano B.
- **Fontes da marca:** DM Sans + Inter (template roxo), Google Sans Flex (posts de texto e editorial) e Google Sans Code (só textos técnicos pequenos do editorial). Não introduzir outra família sem aprovação.
- **Assinatura @urlan.design** sempre em fonte sem serifa da marca (Google Sans Flex ou DM Sans), nunca em fonte de código.
- Os outros estilos de capa do documento de marca (aurora escura, citação, foto) não estão em uso até o Urlan liberar.

## Publicação

1. Criar a pasta `AAAA-MM-tema/` com o `post.json` e gerar os slides: `python3 template/render.py AAAA-MM-tema`.
2. Conferir a folha de contato dos slides antes de subir.
3. Fazer commit e push. Nos links das imagens, usar o hash do commit, não `main`: `https://raw.githubusercontent.com/urlandesigner/urlan-posts/<commit>/<pasta>/slide-01.png`. Com `main`, o GitHub pode servir uma versão antiga em cache.
4. Enviar as mídias e criar o post na mLabs para o perfil `ext_ODYyMzk3MA.7exPeI4iUtJyY-cNYfOl0u`, com texto alternativo quando suportado.
5. Modo padrão: rascunho. Só publicar direto quando isso estiver combinado.
6. Depois do horário marcado, conferir na mLabs se o status mudou para publicado e guardar o link no `post.json` (campo `instagramUrl`). Um carrossel pode levar alguns minutos para processar.

## Capas: referência fixa

- **Toda capa nova usa como referência o Instagram @craftwork.design** (https://www.instagram.com/craftwork.design/), adaptado à marca. Salvo em 05/11/2026.
- Padrão: estilo "série". Fundo gerado no Nano Banana Pro (diferente a cada post, roxo/lilás, centro calmo), título centralizado em 3 camadas (manuscrita Caveat / tema em Google Sans Flex 800 / manuscrita), uma cor de destaque puxada do fundo, sem textos nos cantos (decisão de 16/11/2026): só "Deslize pra ver" com seta, em 56 px, no rodapé.
- Template da capa: `testes-capa/serie/capa.tpl.html`. Exemplos aprovados: `capa-repos`, `capa-cd`, `capa1` (color combos), `capa-dia-design-3d`.
- **Posição do título: igual em todas as capas da série.** Bloco do título (`.mid`) em `top:50%` com `translateY(-54%)`, título em 210px. Não usar `style` inline para subir, descer ou reduzir o título. Se o texto não couber, encurtar o texto, não mover o bloco. Motivo: no feed as capas aparecem lado a lado, e uma capa com o título mais alto parece desalinhada (feedback do Urlan em 12/11/2026, capa "Apps no Claude" estava em 40% e 190px).
- Antes de agendar uma capa nova, comparar lado a lado com a capa anterior da série (mesma altura do título, mesmo tamanho).
- Posts de opinião e explicativos usam o Texto escuro (ver "Templates oficiais").
- Fundo gerado não pode vir com borda de papel/moldura; se vier, gerar de novo em vez de cortar (cortar perde qualidade).

## Stories

- Um story por post (1080 × 1920): fundo da capa desfocado, selo "POST NOVO", capa num card, uma frase que só descreve o assunto. Sem chamadas tipo "corre no feed".
- Agendar na mLabs em modo lembrete quando o adesivo de link precisar ser incluído manualmente pelo app. Mandar o link do post pro Urlan na hora.

## Horário

Posts do feed saem sempre às 10h (America/Sao_Paulo), um por dia útil. Stories às 18h do mesmo dia, em modo lembrete.

## Reels: som
- Sem efeitos sonoros de transicao (parecem bug). Usar trilha instrumental continua do inicio ao fim, com fade in/out.
- Trilha gerada no Higgsfield (elevenlabs_music_v2_5, ~4 creditos por 30 s, force_instrumental). O Magnific tem limite diario gratis.
- Gancho nos primeiros 3 s falando com o publico geral, nunca como resposta a uma pessoa.
- Imagens ilustrativas devem ter aviso no video; so afirmar visual da ferramenta se confirmado na fonte.

## Agendamento

A partir de 15/11/2026 o agendamento é feito somente pelo mLabs (perfil ext_ODYyMzk3MA.7exPeI4iUtJyY-cNYfOl0u). Não usar Flux nem Metricool. Fluxo: upload_media com URL raw do GitHub (hash do commit), create_post com status scheduled.

## Reels: música (decisão de 15/11/2026)

Não gerar trilha no Higgsfield nem embutir música no MP4. O Reel sai sem trilha e o áudio é adicionado pelo próprio Instagram, via mLabs: search_instagram_audio para achar a faixa e audioConfigurations no create_post (somente instagram_reels, máximo 1). Sem efeitos sonoros de transição.

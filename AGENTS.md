# Operação do Instagram @urlan.design

Este repositório produz e agenda conteúdo para o Instagram de Urlan Dipré, AI Product Designer, sob a marca UD Labs.

## Antes de trabalhar

- Ler `REGRAS.md` e o `post.json` da pasta envolvida.
- Consultar `STATUS.md` para o estado operacional mais recente.
- Responder e escrever os conteúdos em pt-BR, com tom direto, coloquial e profissional.
- Não usar travessão nem emoji nos textos do Instagram.

## Conteúdo e fontes

- O posicionamento é IA aplicada a design de produto.
- Todo fato deve ser verificado em fonte oficial e registrado em `sources` no `post.json`.
- Não inventar números, resultados, prazos ou alegações como “feito em 10 minutos”.
- Produzir rascunho primeiro quando a pauta for nova.
- Posts sobre repositórios usam obrigatoriamente o estilo editorial definido em `REGRAS.md`, com o nome de cada repositório em destaque.
- Posts de história contínua podem usar o estilo escuro de texto, uma ideia por slide, conforme o post Claude Meetings.

## Produção

- Carrosséis ficam em uma pasta por post, com `post.json` e slides PNG.
- Gerar slides com `python3 template/render.py <pasta>`.
- Conferir visualmente todos os slides e a folha de contato antes de subir ou agendar.
- Imagens pagas usam Higgsfield. Uma geração por capa; perguntar antes de nova geração ou gasto em lote.
- Vídeos são feitos em HTML/HyperFrames, com inspeção de frames antes do render final.
- Reels saem sem trilha embutida. Quando aplicável, escolher música do Instagram pela mLabs.

## GitHub e mídia

- Repositório: `urlandesigner/urlan-posts`.
- Fazer commit e push antes de enviar mídia à mLabs.
- URLs raw devem usar o hash completo do commit, nunca `main`.
- Não sobrescrever nem descartar alterações do usuário.

## mLabs

- O agendamento é feito somente pela mLabs. Não usar Instagram nativo, Metricool ou Flux.
- Servidor MCP oficial: `https://mcp.mlabs.io/mcp`.
- Perfil mLabs do Instagram: `ext_ODYyMzk3MA.7exPeI4iUtJyY-cNYfOl0u`.
- Fuso: `America/Sao_Paulo`.
- Fluxo: `upload_media`, depois `create_post` ou `update_post`.
- `create_post` é idempotente por 24 horas. Para recriar, usar um `requestId` novo.
- Modo padrão para conteúdo novo: rascunho.
- Não publicar nem agendar sem pedido explícito do usuário.
- Perguntar antes de apagar qualquer agendamento.
- Só apagar da mLabs depois de confirmar que o post está seguro em outro lugar.
- Depois do horário, verificar o status na mLabs e registrar a URL pública no `post.json`.

## Prioridade das regras

Em caso de conflito, as regras de segurança e publicação deste arquivo prevalecem. Para layout, copy e estrutura dos posts, `REGRAS.md` prevalece.

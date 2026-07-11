# Projeto — Loja Irene Moreira (sistema híbrido de atendimento)

> Documento vivo de brainstorm. Início: 2026-06-18. Pasta: C:\projeto irene moreira

## DNA da marca (Instagram @irenemoreira)

- **Nome:** Irene Moreira — loja **MULTIMARCAS** de moda feminina.
- **Local:** Av. dos Pioneiros, 430 — Paulínia/SP (13140-798).
- **Horário:** Seg–Sex 10h–19h | Sáb 10h–16h.
- **Presença digital:** Instagram @irenemoreira — **23,8 mil seguidores**, 6.293 posts; WhatsApp de compras ativo.
- **Estética:** sofisticada/elegante; identidade **dourado + preto**, monograma "M", logo circular premium.
- **Produto:** moda feminina — vestidos, looks de coquetel/festa/social, peças elegantes.
- **Highlights:** Clientes, Vestidos, Clientes, Coquetel, Inauguração → muito conteúdo de **clientes reais vestindo** (prova social).
- **Tradição:** loja com **40 anos**.

## O atendimento HOJE (modelo de negócio)

- Venda **relacional**: cada **vendedora** cuida de uma carteira de **clientes fiéis e antigas**.
- A vendedora **já conhece o gosto e o tamanho** de cada cliente.
- Chegam **roupas novas toda semana**.
- O "empurrão" de novidade hoje é manual (WhatsApp, foto da peça).
- Cada vendedora tem **~30 a 100 clientes VIP** fidelizadas, que **consomem tudo que é novidade**.

> **Objetivo nº1 do sistema:** a cliente **se ver com a peça no próprio corpo** (gatilho de desejo).
> Caimento/tamanho a vendedora já resolve — o sistema é **visualização que gera desejo**, não prova de medida.

## A IDEIA do Paulo — transcrição do áudio (59s, limpa)

> "A loja é uma multimarcas que representa várias roupas e coleções. Temos clientes
> muito antigas — cada vendedora tem um número X de clientes específicas, com fidelidade.
> Já conhece gosto, já conhece tamanho, então fica mais fácil o atendimento. O que eu
> imagino? Cadastrar todas as roupas novas que chegam (toda semana) através de foto; e a
> vendedora tem a foto da cliente já cadastrada, às vezes de corpo inteiro. O que a
> vendedora faz? Já veste a roupa nova nessa cliente [pela IA] e encaminha pra cliente ver
> se gosta. Existe alguma coisa assim? Você tem ideia? Como podemos fazer? Que tipo de
> sistema? O que funciona, o que não funciona, o que tem de mais novo no mundo?"

**Fluxo imaginado:**
1. Roupa nova chega → **foto da peça** (catálogo da semana).
2. Cada cliente tem uma **foto base cadastrada** (de preferência corpo inteiro).
3. Vendedora escolhe a peça → **IA "veste" a peça na foto da cliente** (provador virtual).
4. Vendedora **envia pra cliente** (WhatsApp): "olha o que chegou, já te imaginei nele".
5. Cliente responde se gostou → fecha venda / separa peça.

→ Conceito: **clienteling personalizado com IA de provador virtual (Virtual Try-On)**.
→ Híbrido digital+presencial: mantém o relacionamento da vendedora e turbina com IA + alcance digital.

## Referências

- 3 prints do anúncio **MAXIIMAGE** (IA): "clona qualquer imagem e adiciona movimentos";
  "você escolhe o lugar, a roupa e a pose dela". = exemplo da tecnologia desejada (VTON + imagem→vídeo).
- Histórico do Paulo: **ComfyUI croqui→render** rodando na **RTX 3070** (SD1.5 + ControlNet) → base técnica já existe.

## Perguntas do Paulo (a responder)

- Isso existe? O que há de mais novo? → **Sim** — Virtual Try-On por difusão (fronteira de "moda + IA").
- Como fazer? Que sistema? O que funciona / não funciona? → em definição (próxima etapa: 2–3 caminhos).

## Princípios, riscos e o que faz/quebra (estratégia)

**Estrela do Norte:** humano (vendedora) no centro, IA no braço pesado.
Produto real = a cliente **se sentir vista**; a imagem é só o veículo.
- A inteligência está no **MATCH** (qual peça → qual VIP), não no render.
- É **ferramenta da vendedora**, não app self-service da cliente.
- Ativo real = **perfil/twin de cada VIP** (corpo, tamanhos por marca, estilo,
  histórico, **ocasiões/calendário** ← o que muda o jogo: moda VIP é movida a evento).

**Onde vira ENFEITE e morre:** espelho AR ao vivo; botão self-service sem curadoria;
automação que vira spam (mata o relacionamento); imagem uncanny (dano de marca premium);
cadastro que vira cemitério de dados; querer fazer tudo de uma vez.

**O que faz ou quebra (não foi falado):**
- Foto padronizada das peças (intake semanal) — o esqueleto sem glamour.
- Captura da foto-base da cliente **com consentimento** (vira momento de relacionamento).
- Motor de **match** (começa na cabeça da vendedora, IA sugere depois).
- Ligação com **estoque/tamanho** (não vestir peça esgotada no tamanho dela).
- **Pré-geração em lote (madrugada)** — velocidade é tudo; espera de 2 min = abandono.
- **LGPD / consentimento** (perk premium se bem feito).
- **Medição:** enviado → aberto → respondeu → provou → comprou.

**Como construir (faseado):**
1. **Piloto:** 1 vendedora, ~20 VIPs, 10 peças da semana, pré-gerado no ComfyUI/RTX 3070,
   ela revisa e envia no WhatsApp → medir venda. (semanas)
2. **App da vendedora:** novidades + perfis + gerar/revisar/enviar em 1 toque.
3. **Match inteligente + calendário de ocasiões + estoque.**
4. **Vídeo nas peças-herói + camada de apresentação com a cara da marca** (editorial Irene Moreira).

## Mecânica de engajamento — "O Provador da Semana" (swipe/match)

Trazer o gatilho do "match" (apps de namoro) como instrumento de venda — SEM cafonice.
- **Inverte o Tinder:** cada carta já é curada pra ela (zero lixo, match-rate alto); o "match" = **ela se vendo na peça**.
- **Ritual semanal:** quinta 18h, "suas 5 escolhidas" (antecipação + curiosidade + completar 5/5).
- **Ações:** Amei / Quero provar / Depois (1 toque). "Amei" **pinga a vendedora na hora** (fecha com humano + escassez "1 no seu tamanho").
- **Compartilhar look** (marca discreta) → cliente vira embaixadora nos Stories = prova social/marketing orgânico.
- **Anti-cafona:** estética editorial dourado/preto + serifa; curadoria zero-lixo; privado (sem ranking/pontos); assinatura humana; pouco e bom; copy "Essa é sua." no lugar de "It's a Match!".
- **Verdade honesta:** o swipe é o LAÇO, não a fundação — amplifica a curadoria (boa ou ruim).
- **Gatilhos:** ritual/antecipação · curiosidade · exclusividade · escassez · prova social · endowment.

## CONCEITO PRINCIPAL — "MIRA" (Desejo guiado por curadoria)

Evolução de "Provador da Semana / Alvo do Desejo / Desejo Guiado" → nome de marca **MIRA**.
- **Promessa:** "a gente não te mostra tudo; a gente mira no que pode te acender."
- **Mecânica:** **7 Miras** (poucas peças curadas). Reações: **Acertou / Passou / Mira de novo / Quero provar**.
- **Fechamento:** provador reservado ("o corpo decide") — a venda acontece no provador.
- **1 marca, 3 vozes (tom, não rótulo):** **MIRA Drop** (jovem/TikTok), **MIRA Style** (adulta descolada), **MIRA Privé** (premium/madame).
- **CTA:** "Quero minha Mira". **Frase-mãe:** "A peça certa não convence. Ela atinge."

### Elevação estratégica (Claude)
- **NÃO é campanha — é motor que aprende.** O placar (reação→dado) é o ativo central; cada rodada fica mais certeira (flywheel/moat).
- **Adições:** "mira de novo" que aprende na hora; "DNA de estilo" como presente compartilhável; mira por ocasião (agenda); vendedora co-piloto cujas trocas treinam a IA; **VTON gerado sob demanda** (só nas peças reagidas — economiza GPU).
- **Riscos:** abismo da promessa (começar guiado por humano); spam/fatiga (cadência); voz não escala (cards com copy rascunhada por IA + treino); tier vira rótulo (é tom).

### Plano faseado
1. **Piloto manual-assistido:** 1 vendedora, ~20 VIPs, VTON sob demanda no ComfyUI, placar em planilha, mede acertou→provou→comprou.
2. **App da vendedora (PWA):** montar mira + enviar WhatsApp + placar automático.
3. **Motor:** placar sugere as 7 + mira por ocasião + estoque/tamanho.
4. **Camada premium:** VTON editorial, vídeo, DNA de estilo, Reels.

**Arquitetura:** um motor (curadoria+dados) · uma voz (Drop/Style/Privé) · três canais (WhatsApp, app vendedora, arara física).

## Arquitetura de nomes (recomendação — a confirmar)

- **Marca/produto:** **MIRA** (nome + verbo "mirar"; vira botão/app/hashtag/ritual)
- **Assinatura:** "Desejo guiado por curadoria" (absorve "Desejo Guiado" como tagline)
- **Mecânica:** as **7 Flechas** (verbo: mirar)
- **CTA entrada:** "Guiar meu desejo" / "Quero minha mira"
- **Botões (curtos):** Acertou · Passou · Mira de novo · Me surpreende · Quero provar
- **Fechamento:** Provador reservado
- **Campanha sazonal pontual:** "Alvo do Desejo" (tom mais sensual)
- **Decisão em aberto:** MIRA lidera (recomendação) vs Desejo Guiado lidera — Paulo bate o martelo.

## Pré-filtro do condicional → protege o GIRO (pilar de ROI)

Insight do Paulo: a loja usa muita **sacola de condicional** (peça física vai pra casa da cliente provar). Problema: trava o giro (peça fora da loja = ninguém compra), devolução/logística, tempo da vendedora com chute.

**MIRA = pré-filtro:** o condicional acontece primeiro no DIGITAL. Só o que a cliente marca "Acertou em mim" vira peça física. Sacola encolhe de "10 chutes" → "3 quase-certezas".
- Menos peça saindo = **giro protegido** (capital gira mais rápido).
- Sacola só de vencedores = **+conversão, −devolução**.
- Vendedora não perde tempo com chute.

**Funil:** mira digital (grátis/infinita) → "Acertou" → físico só dos certeiros (provador OU condicional) → venda.

**Fulfillment pós-"Acertou em mim":** (a) Provador reservado (loja) · (b) Provar em casa (condicional enxuto).

**Métrica de ouro do piloto:** peças/condicional, % devolução, dias de giro — ANTES vs DEPOIS da MIRA. É a prova de ROI pro caixa.

## Apresentação (entregue 2026-06-18)

- Deck A4 de 12 páginas: `apresentacao_desejo_guiado.html` + `Desejo_Guiado.pdf`. Inclui capa editorial, problema, conceito, nomes, fluxo, **tecnologia explicada p/ leigos**, **página de prova (antes→depois da IA)**, "por que é possível", giro/condicional, **página do app (alvo + 4 botões)**, encanto, fechamento.
- **Link público (PDF):** https://is.gd/on1YOS · tinyurl.com/2y4m7zda · QR em `conceitos/qr_apresentacao.png`.
- Headline: "Essa é sua" (cafona) → trocado por "Vi você nessa" (sutil). Paulo curtiu muito a tela do alvo+botões.
- Plano do Paulo: apresentar o conceito primeiro, depois voltar pra desenvolver com mais pontaria.

## MVP — A BASE: "Estúdio da vendedora" (esquema + áudio do Paulo, 2026-06-18)

Construir PRIMEIRO a ferramenta da vendedora (a base), antes do app da cliente. (áudio: `transcricao_audio_2.txt`, 130s; + imagem esquemática)

1. **Arara digital (estoque virtual):** digitalizar as roupas em fotos, por tipo (top, calça/jeans, blusa, vestido, saia).
2. **Seleção tipo "fotos do iPhone":** vendedora navega e marca no quadradinho ("quero essa"); selecionados vão pra uma pasta = looks a montar.
3. **Mesa de montagem (o coração):** 2 quadrados de arrastar — [foto da cliente] + [roupa selecionada] — e BOTÕES DE OCASIÃO/ESTILO embaixo (festa, dia a dia, casual, trabalho, praia, academia). Apertar "Festa" → a IA gera a cliente com aquela roupa **+ PRODUÇÃO COMPLETA da ocasião: maquiagem, cabelo e clima de festa** (stylist + maquiador + fotógrafo num botão). **É o pulo do gato.** "Praia" = outro clima/produção, etc.
4. **Resultado:** a vendedora **salva a imagem** e envia direto pra cliente (botão Enviar no WhatsApp).

**Regra de ouro:** simples e prático — vendedora só seleciona + arrasta (cliente + roupa + estilo); o sistema faz o resto.

**Arquitetura = 2 sistemas conectados:**
- 🎨 **Sistema 1 — Estúdio da vendedora:** gera o look produzido (este quadro) → salva → envia.
- 📱 **Sistema 2 — App da cliente:** recebe e reage.
- **A ponte:** a imagem produzida chega na cliente como **card interativo** (imagem + botões) — nunca "solta". Os botões = *quer ou não*:
  - ♥ **Acertou em mim** = amei, é isso (sim emocional)
  - **Mira de novo** = quase, me mostra outra
  - **Me surpreenda** = quero algo diferente
  - **Provador reservado** = QUERO, separa pra mim (= venda)
- Construir o Sistema 1 PRIMEIRO (a base). → 1º alvo de build do piloto.

## NÍVEL 2 — Clube de Venda (post promocional automático) — Paulo 2026-06-18

Dor: clubes de venda postam peças promocionais com **foto de cabide** (pouca produção) → não desperta desejo (ex: jaqueta cropped laranja CARMIM, calça wide laranja, jeans metalizado).
Ideia: IA veste a peça promo numa **influencer digital** + campo onde a vendedora digita **valores e condições** → sai PRONTO pra postar no clube. Máximo de automação, rápido, sem preguiça.

**Adições (Claude):**
- **Modelos da casa:** 2-3 influencers IA consistentes (Soul treinado) = identidade/marca no clube.
- **Pipeline auto:** peça entra na arara → post já gerado (modelo+cenário+legenda) → fila "pronto pra postar".
- **Preço = selo inteligente** (dourado/preto com "M") + valores-padrão; **legenda escrita pela IA**.
- **Modo lote** (10 peças → 10 posts); formatos 9:16/1:1; voz pro preço.
- Mesmo motor (estoque digital + VTON + selos): **Sist.1** look cliente · **Sist.2** card cliente · **Sist.3** post clube.

UX sem preguiça: tudo pré-preenchido, 1 tela + 1 botão (peça → preço → Gerar → Postar), pré-gerado.

## Fluxo unificado (touch-first) + automação dos clubes — Paulo 2026-06-18

**PRINCÍPIO Nº1:** simples ao ponto de fazer **COM O DEDO** (touch, tablet no balcão). Mesas em sequência ("subir de mesa").
- **Mesa 1 (cliente / Desejo Guiado):** ~20 peças no quadro → arrasta blusa+calça → seleciona cliente → aperta estilo (dia a dia/festa/trabalho) → IA gera com o mood → sobe pra próxima mesa (Sist.2 com os botões) → envia / marca condicional. Cliente se vê produzida pra a ocasião.
- **Mesa 2 (clube de venda):** seleção do estoque → escolhe a influencer ("meninas da Irene") → arrasta as roupas → digita condições de oferta → aperta o mood → sobe a foto pro clube.

**Automação das postagens (é possível? SIM, com nuance por canal):**
- **Telegram** → 100% automático (Bot API oficial).
- **Instagram** (feed/stories/reels) → sim, API oficial de publicação (agenda/posta sozinho).
- **WhatsApp GRUPOS** → API oficial NÃO posta em grupo (é 1:1); automação não-oficial **arrisca BANIR o número**. Seguro = post pronto + **1 toque** pra compartilhar (ou Canal/lista de transmissão oficial).
- Recomendação: "pronto + 1 toque" (seguro, universal) + automação total onde é permitido (Telegram/Insta).

## As duas equações + princípio "simples × sofisticado" — Paulo 2026-06-18

**PRINCÍPIO:** Sistema 1 (interface) = **SIMPLES**. O **SOFISTICADO é a FOTO GERADA** — tem que ser condizente com o estilo dos botões. (toda a inteligência fica escondida atrás do botão).

- **Equação 1 (cliente):** `Cliente + Roupa + Estilo` → Resultado → Sistema 2 (Desejo Guiado, botões de reação). Preserva o ROSTO da cliente.
- **Equação 2 (clube):** `Meninas Irene + Roupa + Estilo + Descrição(promoção)` → automático → Clube de Venda → Resposta → Venda. Usa MODELOS FIXAS.

**CRUX técnico:** cada botão de estilo = uma **"receita" curada de geração** (mood, luz, cenário, maquiagem, pose). Ex: Festa = make marcada + luz dramática + cenário noturno; Trabalho = make clean + luz natural + sóbrio; Praia = luz solar + externo. A vendedora aperta 1 botão; por trás, um pipeline art-directed garante que o resultado condiz com a ocasião. **É onde concentramos a sofisticação.**

## Concorrência + risco + sequência (pesquisa 2026 — ver `pesquisa_concorrencia_2026.md`)

- **Mercado = 3 silos que ninguém juntou:** gerador de modelo (Botika/ZMO), provador consumidor (Doppl, **Doris-BR**), estilista por mood (StyTrix). Ninguém faz produção-por-ocasião + cliente real + venda.
- **Clienteling (Endear/Tulip/BSPK) = IA de TEXTO**, não gera imagem. Clube BR = grupo Zap manual.
- **WHITE SPACE confirmado:** laço relationship-native (vendedora → try-on por ocasião → WhatsApp → botões → condicional). Greenfield no Brasil. **Conceito inédito.**
- **Divergência-chave (o moat):** mercado TIRA a vendedora (autoatendimento); nós AMPLIFICAMOS ela.
- **RISCO Nº1 (matador):** glam demais → conversão sobe mas DEVOLUÇÃO sobe mais rápido + queima a credibilidade da vendedora (devolução EUA 2025 ~15,8%; caimento 50% + "não era o que esperava" 42%).
  - **Fix:** 2 modos — "Desejo" (glam, isca) + "Espelho honesto" (realista, decisão); provador/condicional físico = verdade.
- **SEQUÊNCIA:** validar laço à mão → Sistema 1+2 (moat) → Clube → postagem automática POR ÚLTIMO. (bate com instinto do Paulo: S1 primeiro.)
- **Buy vs build:** ComfyUI + API = motor. Diferencial = fluxo+dado+vendedora. Montar, não reconstruir.

## Estoque digital inteligente (cadastro automático) — Paulo 2026-06-18 (registrar p/ depois)

Requisito: cadastrar roupas SEM preguiça / sem estrutura pesada/lenta. A IA remove a fricção.
- **Padrão de foto** (cabide/fundo neutro, enquadramento) → reconhecimento confiável + boa base p/ geração.
- **Auto-reconhecimento + organização:** sobe 100 fotos → IA classifica cada uma (tipo saia/blusa/calça/vestido; cor; estampa; manga; comprimento) → auto-organiza na arara digital. (vision/multimodal — viável e leve, sem PIM enterprise.)
- **Filtros p/ a vendedora:** tipo · cor · **tamanho** · marca · preço · **tempo parado (giro)**. Visual sai da foto; tamanho/preço/estoque vêm do ERP/PDV ou cadastro rápido/etiqueta.
- **Busca em linguagem natural:** "saias laranja paradas há +30 dias" (anti-preguiça, sem menu).
- **Loop:** "tempo parado" vira gatilho → sistema sugere a peça pro Clube/promo (Sist.3). Estoque encalhado = oportunidade automática.
- Princípio: dinâmico, intuitivo, rápido. (Reforça a pergunta aberta: existe ERP/PDV p/ tamanho/preço/qtd?)

## Protótipo Sistema 1 + aprendizados (2026-06-18)

- **Protótipo "Estúdio da vendedora" FEITO e funcionando:** `estudio/estudio.html` — 21 peças (8 categorias + filtro), 6 modelos (idades/corpos reais), 6 ocasiões, gera resultado (5 combos pré-gerados), botões Enviar WhatsApp / Provador reservado. Touch-first. Roda em `http://localhost:8765/estudio/estudio.html` (LAN p/ tablet). Assets: `estudio/modelos|estoque|resultados`.
- **Aprendizado técnico (viés de corpo):** a IA puxa forte pra MAGRO — "manequim 50" não basta. O que funcionou: **MEDIDAS REAIS em cm** (BR 50 ≈ busto 112 / cintura 100 / quadril 120) + "NÃO magra" + features (rosto cheio, braços/barriga/quadril cheios). Guardar pras "modelos da casa". No **Sistema 1, a foto REAL da cliente elimina o viés** (mais um motivo pra usar a foto dela).

## PROTÓTIPO COMPLETO — app navegável (2026-06-18) ✅

App de 5 telas em `C:\projeto irene moreira\estudio\` (abrir `index.html`):
- **index.html** — Home/dashboard touch-first (entrada, 4 módulos).
- **estudio.html** — Sistema 1: 8 modelos + 27 peças (com filtro/categorias incl. Conjunto) + 6 ocasiões + 11 resultados prontos + limpar/novo look + clientes conectadas (lê localStorage `mira_clientes`).
- **cadastro.html** — Estoque: foto + tipo + tamanho + coleção + tempo parado + filtros (localStorage `mira_cadastros`).
- **cadastro_cliente.html** — Clientes: foto + nome + tamanho + ocasiões (localStorage `mira_clientes`) → aparecem no Estúdio.
- **clube.html** — Sistema 2: peça + modelo + estilo + **preço → selo dourado** → post pronto + postar/salvar.
- **Navegação unificada** (Início · Estúdio · Estoque · Clientes · Clube) em todas. Dark+gold, Fraunces, touch-first.
- **Imagens otimizadas** (jpg ~850px; 184MB→4,6MB) → carregam rápido. Script `_convert.py`.

**Aprendizados:** viés de corpo magro (resolver com MEDIDAS cm + foto real); biquíni-no-corpo bate filtro NSFW (usar saída de praia / foto real); loira clara em fundo claro lava (usar pele dourada + fundo médio + contraste). Resultado preserva corpo plus-size com "do not slim" + foto-referência.

**Abrir pra demo:** 2 cliques em `index.html` (file://, sem servidor) ou LAN `http://192.168.15.57:8765/estudio/index.html`.

**v2 (2026-06-18, QA completo):** estoque trocado por ALTO PADRÃO multimarca (gala paetê/vinho, cocktail renda, slip seda, maxi tropical, alfaiataria, macacão, midi, conjunto fitness, athleisure, kaftan, vestido praia, maiô) — categorias Academia/Praia/Casual; genérico removido. **Toggle Irenetes/Minhas clientes** no Estúdio. **Botão "?" com passo a passo em todas as telas.** QA: 5 telas testadas (gerar, selo, cadastros, toggle, filtros) — tudo OK. Modelo loira refeita (estava lavada). Filtro NSFW bloqueia biquíni-no-corpo (usar maiô/kaftan/foto real).

## Decisões tomadas

- **Conceito de marca:** MIRA — Desejo guiado por curadoria. *(a confirmar)*
- **Abordagem de build:** piloto manual-assistido primeiro, software depois. *(a confirmar)*
- **Direção visual (confirmada 2026-06-18):** key visual cinematográfico "conceito 2" — dark + Mira Gold #C7A34A + ambiente bordô #7A1E2B, manchete "Essa é sua" embaixo, retículo de mira dourado, foto editorial como palco. Render em `conceitos/mira_conceito_2.png`.
- **Botões oficiais (Paulo):** Acertou em mim · Mira de novo · Me surpreenda · **Provador reservado** (CTA de conversão, destaque bordô).

## Camada mágica / EUREKA (embasada — ver `pesquisa_eureka_2026.md`)

Conceito unificador: **Gêmea de Estilo** — parar de esconder o algoritmo; mostrar, deixar a cliente moldar, devolver como identidade. Personalização = relacionamento + identidade compartilhável + ativo que compõe.

6 momentos mágicos (todos viáveis hoje):
1. **Vídeo dela, não de modelo** — stills local (CatVTON+PuLID, RTX 3070) + vídeo em nuvem sob demanda (Doppl/Kling).
2. **DNA de Estilo vivo e visível** — ela vê/corrige o perfil; "mira de novo" aprende na hora (Stitch Fix Latent Style + PinnerSage).
3. **Receita das 7** = 4 certeiras + 2 calibradas + 1 carta selvagem (calibração + Thompson sampling = anti-staleness).
4. **Radar de ocasião + "em quem mirar hoje"** — proativo, score por recência (estilo Mytheresa).
5. **MIRA Wrapped** — cartão/filme de estilo compartilhável (viral + status).
6. **Espelho honesto + Cofre** — confiança/LGPD como luxo (consentimento granular + direito de imagem).

Anti-"tiozão": aprende e mostra; vídeo+editorial; compartilhável + humano-assinado; sem NFT/metaverso; IA rotulada; nunca afina o corpo; sem disparo em massa.
Arquitetura de compute: **híbrida** (3070 = stills/identidade/privacidade · nuvem = vídeo HD/editorial).

## Pergunta aberta p/ blueprint

- Já existe sistema com estoque/catálogo + cadastro de clientes (ERP/PDV/planilha) ou é greenfield?

## Abordagens consideradas

(a detalhar na próxima etapa, com mockups)

---

## v3 — Classificação de estilo + clientes de teste (2026-06-19)

**Classificação de estilo (a inteligência da curadoria) = 2 eixos cruzados:**
- **OCASIÃO (pra onde ela vai)** — ~10: Dia a dia · Trabalho · Jantar/Date · Festa · Gala/Madrinha · Brunch/Almoço · Praia/Resort · Academia · Viagem · (Maternidade). No protótipo hoje: 6 (Dia a dia/Trabalho/Festa/Casual/Praia/Academia). Faltam: Jantar, Gala, Brunch, Viagem.
- **ESTILO/PERSONALIDADE (o jeito dela)** — 7: Clássico · Romântico · Sensual · Minimalista · Dramático/Statement · Boho/Natural · Esportivo. Ainda NÃO existe no fluxo; é o que falta pra IA acertar (festa de "clássica" ≠ festa de "dramática"). Já adicionado como tag nas clientes-demo.

**Gaps mapeados:** acessórios (bolsa/sapato/joia) no look; estilo da cliente no cadastro; cápsula/multi-look (3–5 looks de uma vez). **Pode ficar extraordinário:** resultado por ocasião → por ocasião×estilo×corpo real; cadastro → DNA de estilo que aprende. **O que ninguém viu:** o GUARDA-ROUPA da cliente (sistema sabe o que ela já comprou → sugere o que completa, não repete) + cápsula inteligente por agenda.

**Clientes aleatórias de teste (6, em `clientes/cliente_1..6.jpg`):** Marina (M·Clássico), Patrícia (G·Sensual), Cláudia (GG·Romântico), Vera (M·Minimalista), Taís (P·Esportivo), Neusa (GG·Clássico) — idades/corpos/tons variados, "cara de cliente real" (não modelo). Seed `CLIENTES_DEMO` em `estudio.html` + `cadastro_cliente.html` (sempre aparecem, somam às cadastradas em localStorage).

**5 looks VTON de cliente prontos** (provador real, não placeholder): `RESULTS['demo_0|Festa']`=Marina+cocktail renda, `demo_1|Trabalho`=Patrícia+alfaiataria, `demo_2|Festa`=Cláudia(plus)+gala paetê, `demo_3|Festa`=Vera+gala vinho, `demo_4|Academia`=Taís+athleisure. Corpo plus da Cláudia preservado (não afina).

**Roteiro coerente do demo (cliente + a peça que combina + ocasião):** Marina+Cocktail de renda+Festa · Patrícia+Alfaiataria+Trabalho · Cláudia+Vestido gala paetê+Festa · Vera+Vestido gala vinho+Festa · Taís+Conjunto fitness+Academia. (Se escolher outra peça, o protótipo mostra o look pronto da ocasião; no sistema real gera com a peça exata.)

**Técnico:** VTON = `generate_image` nano_banana_pro, `medias:[{value:JOB_ID,role:"image"}]` — `value` é o **job_id** de uma geração anterior (NÃO url; url dá erro de validação). 1ª referência = pessoa, 2ª = peça. Preview serve a RAIZ do projeto → app em `/estudio/estudio.html` (não `/estudio.html`). Evals do preview caem após navegação (flaky) — confirmar arquivos com `curl` é autoritativo.

---

## v4 — Estúdio reconstruído: Mesa de Separação (2026-06-19)

Rebuild completo da tela Estúdio (Sistema 1) no fluxo da loja física, ideia do Paulo. Backup do antigo em `estudio_v1_backup.html`. Brainstorming skill aplicado: desenho apresentado (mockup `show_widget` + prosa) → Paulo aprovou ("confio, decide você") → construído e verificado.

**Fluxo:** barra de sessão (vendedora + busca cliente) → **1·Estoque** (com categoria Acessórios) → **2·Mesa de separação** (pessoa: toggle Irenetes/Clientes + looks separados + acessórios separados) → **3·Palco em camadas** (veste a pessoa: look + acessórios empilham como chips) → Ocasião → Gerar → **Bandeja multi-look** → Enviar → Desejo Guiado / Clube.

**Decisões travadas (Paulo: "decide você"):** palco em camadas (1 janela, não 3 separadas); **toque** (não arrasto) pra constância no touch; finder = `<select>` de 10 vendedoras (sticky `mira_vendedora`) + busca de cliente; **registro = bandeja salva por `mira_sessao_<vend>_<pessoaKey>`** (sai e volta, está lá). Acessórios: 4 product shots em `estoque/acc_*.jpg` (bolsa/scarpin/brinco/óculos). Geração ainda keyed por `pessoa|ocasião` (acessório/look não mudam o resultado pré-pronto — limitação do protótipo, no real a IA usa as peças exatas). QA preview OK: 10 vendedoras, 18 peças, categoria Acessórios, mesa→palco (2 chips vestindo), sessão Maria→Cláudia, gerar→res_festa_claudia, bandeja 3, envio liberado.

**Próximos (não construídos ainda):** mesa por-cliente (hoje é global); cápsula (gerar 3–5 da mesa de uma vez); "combinar" (sugerir acessório que casa com o look); VTON real com acessório+look juntos na geração; eixo estilo/personalidade (7) entrando no gerar.

---

## v5 — Numeração brasileira + trava de tamanho (2026-06-19)

**Numeração 34–54 (manequim) com medidas reais (cm, busto/cintura/quadril — padrão da casa, ajustável):**
34=80/64/88 (PP) · 36=84/68/92 (P) · 38=88/72/96 (P-M) · 40=92/76/100 (M) · 42=96/80/104 (M-G) · 44=100/84/108 (G) · 46=104/88/112 (G-GG) · 48=108/92/116 (GG) · 50=112/100/120 (XGG) · 52=116/106/124 · 54=120/112/128 (EG).

**Implementado:** ESTOQUE: cada peça tem `tam` (array de manequins); acessórios `tam:null`. Tile e mesa mostram "Tam X–Y". Cliente tem `manequim` (demo: Marina40/Patrícia44/Cláudia48/Vera40/Taís38/Neusa48); mapa letra→nº `LETTER2NUM={PP:36,P:38,M:40,G:44,GG:48,XGG:50}`. **Trava de fit:** ao escolher cliente, peça sem o manequim dela fica apagada + selo "fora do tam." e o clique é BLOQUEADO (não monta look que não serve); chip "só serve na [nome]" filtra só o que cabe. Irenetes sem restrição (modelam qualquer tamanho). Cadastro mercadoria: tamanhos numéricos + filtros em camadas (busca + tipo + coleção + tamanho) + padrão de foto. Cadastro cliente: manequim numérico 34–54.

**Bug corrigido:** busca do estoque e busca de cliente dividiam `S.busca` → separados em `buscaEst`/`buscaCli`.

**Arquitetura multi-vendedora (resposta ao "open claw"):** NÃO precisa conta de IA por vendedora. 1 sistema central (servidor + 1 acesso ao motor de IA) e cada vendedora só faz login dela; as 10 dividem o mesmo motor, o sistema separa o trabalho por vendedora+cliente. Sem 10 chaves de IA.

**Padrão de foto da peça:** peça sozinha, fundo branco/claro, de frente, inteira no quadro, boa luz, foto em pé (retrato 3:4). Quanto mais limpa, melhor a IA veste.

**TESTE DO CABIDE (2026-06-19, em `estudio/testes/compare.html`):** gerei foto "de loja" (vestido esmeralda no cabide+arara) e mandei o VTON (nano_banana_pro) vestir a Helena. **Resultado: a IA vestiu certo, cabide e fundo sumiram, sem alucinação** (quadro 2). PORÉM a remoção de fundo genérica (`remove_background`/rembg) **deixou o cabide** — ela isola o objeto inteiro (peça+cabide), não só o tecido. → Pipeline correto: foto → **segmentação da PEÇA** (cloth segmentation, não rembg) **OU** confiar no VTON (já ignora o cabide quando instruído) → vendedora aprova (gerar de novo em 1 clique). Padrão de captura (peça deitada/fundo claro) derruba na origem. Conclusão: cabide não trava o projeto.

---

## v6 — Cápsula + Combinar + Limpeza no upload (2026-06-19)

- **Cápsula:** botão "✦ Gerar cápsula (a mesa toda)" no palco → pega os looks da mesa que SERVEM na pessoa (até 5), gera 1 por look (ocasião inferida da categoria via `catToOcc`) direto na bandeja. Verificado.
- **Combinar:** no palco, ao escolher um look, sugere o acessório que casa (`suggestAcc` por categoria: Festa→bolsa/brinco, Terninho→scarpin, Casual→óculos…); botão "💡 combina com + [acessório]" adiciona ao palco+mesa. Avança pro próximo acessório quando um já está vestido. Verificado.
- **Limpeza no upload** (cadastro mercadoria): após subir a foto, passo visível "🪄 limpeza automática (remove cabide+fundo)". É a UX do passo; a segmentação real roda no backend (provada no teste do cabide). Honesto: o protótipo mostra ONDE acontece, não fake o recorte.
- **Fotos REAIS do Paulo** (Carmim/Irene Moreira: pantacourt laranja, jeans metalizado, jaqueta cropped laranja) = padrão real de cadastro (peça no cabide branco da marca, parede de espelhinhos da loja, foto de celular, peça grande/de frente/luz boa). Fundo de espelhos é consistente → afinar limpeza 1x serve pra todas. Anexos de chat NÃO caem no disco (busca confirmou) → pra testar no real, usar `media_upload_widget` (Paulo sobe os arquivos).

**TESTE NA PEÇA REAL (2026-06-19, `estudio/testes/compare2.html`):** Paulo subiu 3 fotos reais via widget (pantacourt laranja=6ba66f52, jeans metalizado=002a8538, +1). Rodei VTON: Valentina (bfdfae0d) + pantacourt real → **resultado impecável**: mesma peça (corte wide-leg, cor, recorte no joelho), cabide+parede de espelhos removidos, qualidade de catálogo. **Pipeline provado em mercadoria real.** Mais exemplos reais do Paulo: flat-lay na mesa de vidro com VÁRIAS peças + etiquetas + chão da loja (mais difícil que cabide). **Decisão de padrão de captura:** cadastro = SEMPRE 1 peça no cabide da marca na parede de espelhos (consistente, vertical, sem ambiguidade — provado); flat-lay multi-peça serve pro Clube/IG, não pro cadastro; regra de ouro 1 foto=1 peça. Bônus: etiquetas nítidas (John John 38, Carmim) → futuro OCR lê marca+tamanho no cadastro. Mockup da tela do celular (captura→monta→envia) entregue via show_widget; "Enviar" agora usa Web Share (`navigator.share`) → abre WhatsApp com as imagens no celular, fallback wa.me.

---

## v7 — 2º teste real + app de celular + OCR (2026-06-19)

- **2º teste em peça real:** jeans metalizado Carmim (002a8538) → Helena (8ee9f3ec) VTON → brilho prateado preservado, sem cabide, qualidade catálogo (`testes/real_jeans_result.jpg`). 2 de 2 acertos em mercadoria real (pantacourt + jeans).
- **App de celular `estudio/celular.html`:** single-column mobile (max 460px), header + link "TV/PC", sessão (select vendedora), strip horizontal de pessoas (toggle clientes/irenetes), botão **"📷 Fotografar peça nova"** (`input capture=environment` → abre câmera → vira tile selecionável no estoque), grid com chips + trava de tamanho (fora do tam.), ocasião, Gerar, **Enviar no WhatsApp** (Web Share), bandeja, novo look. Reusa os mesmos dados/RESULTS. Verificado.
- **OCR de etiqueta** (cadastro mercadoria): Tesseract.js via jsdelivr (carregou OK no preview). Botão "🔎 Ler etiqueta" roda OCR na foto → acha marca (lista de marcas BR) + tamanho (regex 34–54) → preenche campo **Marca** (novo) + toggla o tamanho. Fallback honesto se offline/não nítido. É OCR REAL (não simulado), mas precisão depende de foto perto da etiqueta; produção usaria cloud vision (crop+OCR) pra instantâneo. Marca aparece no card do estoque.

- **Cliente REAL no app (ciclo fechado, 2026-06-19):** Paulo subiu foto real (irene.jpg, ed90110c) → VTON na pantacourt real (6ba66f52) → resultado fiel (rosto/corpo dela, peça idêntica). Carregada no app: cliente "Irene" (demo_6, mnq 42) em `clientes/cliente_irene.jpg` + peça `real_pantacourt` (foto real de cadastro, `estoque/real_pantacourt.jpg`) + `RESULTS['demo_6|Dia a dia'/'Casual']='resultados/res_diaadia_irene.jpg'` nos DOIS apps (celular+estudio). No `celular.html`: toca Irene → Pantacourt laranja → Dia a dia → Gerar → ela produzida + "Enviar no WhatsApp". **Cenário "foto da cliente + look real → imagem final no celular" provado de ponta a ponta.** Pro demo ao vivo: "mágica preparada" (pré-gerar clientes VIP reais antes da reunião). LGPD: foto de cliente = dado sensível, pedir ok.

**DECK SENDABLE (2026-06-19):** `apresentacao_sistema.html` + `.pdf` (10 págs A4, ~866KB, dark+gold) na raiz do projeto — gerado via Chrome headless `--print-to-pdf` da URL localhost (imagens via http resolvem). Páginas: capa · problema · 3 sistemas · storyboard 6 passos · prova peças reais (pantacourt+jeans) · cliente real Irene (antes/depois) · cabide · por dentro (mesa/tamanho/cápsula/app) · o que falta+plano 3 fases+custo · fecho. Embeds reais de `estudio/testes/`, `resultados/`, `clientes/`. Pra reabrir/converter PDF→img, pdftoppm NÃO está instalado (verificar via HTML no preview). Arquitetura real (resposta "o que precisamos"): 4 camadas — celular/TV (temos) → nuvem/Supabase (falta) → motor IA limpeza+VTON (falta ligar: nuvem ou RTX 3070) → WhatsApp (Web Share já, Business API depois). Plano 3 fases: piloto (1 vend, semanas) → loja toda (10, WhatsApp oficial, motor de gosto) → escala (GPU local, guarda-roupa). **Versão impressão (fundo branco, economiza tinta):** `apresentacao_sistema_print.html` + `.pdf` (mesmo conteúdo, paleta clara: bg branco, texto #1A1714, dourado vira bronze #A8842C/#8A6A17 pra ler no papel). DARK (`apresentacao_sistema.pdf`) = enviar digital; BRANCO (`apresentacao_sistema_print.pdf`) = imprimir. **+2 páginas (2026-06-19):** "Como a foto vai e volta" (fluxo celular→sistema→celular, captura→entra direto→opera→volta, mesmo app, sem e-mail/WhatsApp Web) + "O alvo. E um só toque." (recria o card da cliente/Sistema 2 com a mira/brackets + headline "Vi você nessa." + as 4 TECLAS: ♥ Acertou em mim / Mira de novo / Me surpreenda / Provador reservado, com explicação de cada). Decks agora 12 págs; numeração de rodapé escondida via `.foot span:last-child{display:none}` (evita renumerar). PDF branco regenerado como `apresentacao_sistema_impressao.pdf` (o `_print.pdf` ficou travado/aberto — substituir).

**CERTIFICAÇÃO DO APP CELULAR (2026-06-19):** `celular.html` testado etapa a etapa, 0 erros no console. ✓ E1 captura (input câmera `capture=environment`) · ✓ E2 cliente real carregada (Irene) · ✓ E3 gera look (peça/cliente carregada → imagem real `res_diaadia_irene`; peça NOVA fotografada → "Em produção…" honesto, não mostra look trocado) · ✓ E4 volta (tela + bandeja) · ✓ E5 envia (Web Share/wa.me). Ajuste de honestidade no `ger.onclick`: `temNova=S.pecas.some(f=>f.startsWith('capt_'))` força placeholder. **Único gap real = geração AO VIVO de peça nova fotografada precisa da nuvem** (Supabase + API VTON). Pra piloto HOJE, 2 caminhos 100% reais: (a) pré-carregar looks de clientes VIP reais antes; (b) concierge (foto nova → eu gero → entra no app).

**UPGRADE PADRÃO REVISTA + EFEITO UAU (2026-06-19):** (1) **Sistema de prompts editoriais** em `prompts_editoriais.md` — template [IDENTIDADE]+[PEÇA]+[CENA por ocasião]+[BELEZA/POSE por estilo]+[QUALIDADE 85mm/bokeh/color grade/magazine], trava corpo real, tira cabide, 2K pros heróis. (2) **Looks-herói regerados em 2K editorial:** Irene (pantacourt, golden hour rua/café, lens flare) `43c56b90` e Cláudia (gala c/ lustres, plus preservado) `4f96c976` → substituíram `resultados/res_diaadia_irene.jpg` + `res_festa_claudia.jpg` (app + deck usam, upgrade automático). Diferença gritante vs estúdio liso. (3) **Reveal premium** no `ger.onclick` (celular) e `gerar.onclick` (estudio): shimmer "✨ produzindo o look…" 1.3s → revela com animação + legenda "Vi você nessa." (CSS `@keyframes rev/shine`, `.reveal .vcap`). Efeito UAU pra vendedora e cliente. Verificado nos dois.

**FIDELIDADE DE ROSTO + ANTI-CARIMBO (2026-06-19):** Paulo (crítico): a cliente TEM que se reconhecer (rosto = identidade; se errar, sente-se enganada). Teste: Irene (real) gerada em 3 cenas (rua golden hour, jardim botânico, galeria de arte) com trava forte de rosto — comparado à foto real, **é claramente a mesma mulher** (mesmo corte/traços/idade; var. galeria pegou o sorriso). Likeness BOA com nano_banana, mas não pixel-perfect. **Pra garantir 100% (doc em `prompts_editoriais.md` seção 0):** InstantID/PuLID/IP-Adapter-FaceID + face-swap (ReActor)+restore (GFPGAN/CodeFormer) + **PORTÃO de similaridade facial** (cosine embedding ≥ limiar, senão regenera sozinho) = acertividade automática + humano confirma. **Anti-carimbo:** `prompts_editoriais.md` seção 4 agora é POOL de 4-6 cenas por ocasião, rotacionado a cada geração → editorial diário, nunca engessado. Comparativo visual em `estudio/testes/var_fidelidade.html` (rosto real → 3 cenas).

**SISTEMA REAL — servidor-ponte (2026-06-19):** Paulo escolheu "nuvem agora + ComfyUI em paralelo" pra testar na loja. Máquina: ComfyUI instalado (`C:\comfyui\...portable_nvidia`, desligado, hoje SD1.5/croqui), RTX 3070 8GB (apertado p/ VTON), IP local **192.168.15.57**, Python 3.14. Construído: **`server.py`** (stdlib, sem deps) — serve `estudio/` na rede (0.0.0.0:8770) + `POST /generate` que monta o prompt editorial (pools anti-carimbo + trava de rosto) e chama **fal.ai** (`fal-ai/nano-banana/edit`, data-uri, sync) → devolve o look. Verificado: serve app (200), /generate responde (sem `FAL_KEY` → erro claro). **App em modo ao vivo** (`celular.html`): demo pré-pronto = reveal instantâneo; peça nova/captura = `fetch('/generate')` → showLook() ou msg honesta se offline/sem chave. Zoom (toque/pinça 5x) nos dois apps. Guia em `SETUP_sistema_real.md`. **Falta (do Paulo):** chave fal.ai (5 min) → `$env:FAL_KEY=...; python server.py` → celular na Wi-Fi abre `http://192.168.15.57:8770/estudio/celular.html`. Possível ajustar `FAL_MODEL` no 1º teste. ComfyUI local = próximo (workflow JSON + nós CatVTON/IDM-VTON+ReActor/InstantID; trocar engine no server.py).

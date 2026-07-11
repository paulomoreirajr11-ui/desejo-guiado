# MIRA — Pesquisa profunda + Eureka (2025–2026)

> Síntese de 5 frentes de pesquisa (com fontes) feita em 2026-06-18.
> Objetivo: embasar a camada "mágica/extraordinária" do MIRA.

---

## Frente 1 — Fronteira moda + IA (provador/VTON/vídeo)

- **Roda na sua RTX 3070 (8GB):** CatVTON faz try-on fotorrealista 1024×768 em <8GB. Identidade do rosto real preservada com PuLID/InstantID (ComfyUI/FLUX). [CatVTON](https://github.com/Zheng-Chong/CatVTON) · [PuLID vs InstantID](https://apatero.com/blog/instantid-vs-pulid-vs-faceid-ultimate-face-swap-comparison-2025)
- **Vídeo no 3070 é limitado** (Wan 2.2 5B ~480p, ~150s p/ 5s) → HD/realista = nuvem. [Wan 2.2](https://stable-diffusion-art.com/wan-2-2-image-to-video/)
- **Novo 2025/26:** FLUX VTO — até 4 peças em camada, <4s (sensação interativa) [BFL](https://bfl.ai/blog/flux-vto-virtual-try-on-at-catalog-scale); Google **Doppl** — vídeo da própria pessoa se movendo (TIME Best Inventions 2025) [PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2025/google-launches-virtual-try-on-app-featuring-ai-generated-videos/); **Kling Kolors 2.1** caimento físico, 360° [MagicHour](https://magichour.ai/blog/kling-kolors-21-for-ai-virtual-try-on); **Nano Banana Pro (Gemini 3)** consistência de personagem + aceita HEX da marca [Google](https://blog.google/innovation-and-ai/products/nano-banana-pro/).
- **Espaço em branco:** vídeo da cliente real (não modelo) em escala de clienteling; editorial travado na marca; restyle de 1 clipe em 4 cenários (Runway Aleph).
- **Mágica:** lookbook vivo "suas 7 da semana" (stills local → reel em nuvem); editorial MIRA (ela é a capa); restyle 1-toque na loja (<4s).

## Frente 2 — Clienteling & personalização de luxo

- **Tese EIP:** top ~3% das clientes = ~40% das vendas; personal shopper dedicada; WhatsApp como canal padrão; early access + trunk shows. [in.Parallel/WWD](https://in-parallel.co.uk/research_article/net-a-porter/)
- **WhatsApp >> e-mail:** 95%+ abertura, 7–14x ROI; até 80% retenção em "salões" conduzidos por consultora. [hellomerx](https://www.hellomerx.com/blog/use-cases-whatsapp-clienteling-software-for-luxury-retail-66f76)
- **Ferramenta = "caderno preto digital"** (Tulip+Salesfloor 2025, Endear, BSPK). [Endear](https://endearhq.com/blog/best-clienteling-software)
- **Novo:** IA acha VIP antes de gastar (Mytheresa pondera últimas 3 semanas) [Glossy](https://www.glossy.co/fashion/luxury/luxury-briefing-mytheresa-is-using-ai-to-find-future-vips/); copilotos de vendedor (Zegna X +75% gasto; Endear escreve no tom da cliente) [Endear AI](https://endearhq.com/blog/putting-the-ai-in-retail-clienteling); McKinsey: IA prepara, humano cria desejo.
- **Espaço em branco:** inteligência de styling **multimarca** + guarda-roupa que a cliente já tem; curadoria por **ocasião individual**; preservar **uma voz humana**.
- **Mágica:** "O Edit, assinado pela sua vendedora"; "radar de ocasião"; score de desejo por recência ("em quem mirar hoje").

## Frente 3 — Modelos de gosto (taste AI)

- **Latent Style (Stitch Fix):** cliente e item no mesmo espaço; like/dislike atualiza o vetor ao vivo. [Stitch Fix](https://multithreaded.stitchfix.com/blog/2018/06/28/latent-style/)
- **PinnerSage (Pinterest):** multi-faceta — ela ama minimalismo E festa sem virar média. [arXiv](https://arxiv.org/abs/2007.03634)
- **Cold-start meta-learning** (MAML); backbone de embeddings **Marqo-FashionSigLIP** (bate FashionCLIP). [marqo](https://github.com/marqo-ai/marqo-FashionCLIP)
- **Novo:** recomendadores agênticos (GPT-4o Thought→Action→Critic; entende negação "sem listras"; memória de rejeições; modela Corpo–Item) [arXiv 2508.02342](https://arxiv.org/html/2508.02342v1); VLM-estilista multi-rodada (FashionM3).
- **Espaço em branco:** aprendizado **visível** (mostrar/corrigir o perfil); **calibração** (manter 70/30, não colapsar no óbvio) [survey](https://arxiv.org/html/2507.02643v1); **exploração** (Thompson/bandits p/ serendipidade) — anti-bolha.
- **Build (cold-start real):** vetor latente + update online; warm-start por onboarding 60s (escolher 5 de 20 arquétipos); slate semanal = 4 exploit + 2 calibradas + 1 explore. Stack: Marqo-FashionSigLIP → FAISS → vetor por cliente (MAML) → facetas (PinnerSage) → bandit calibrado → GPT-4o p/ razão+negação+"cartão de gosto" visível.

## Frente 4 — Social commerce viral & tendências

- **Funciona hoje:** micro-drops semanais + waitlist (SKIMS domingo); live shopping 3–4x conversão; GRWM de fundadora/estilista + UGC; **Brasil = WhatsApp + Instagram + PIX no chat** (vestuário = ~31% do social commerce, US$15,6B em 2025). [Mordor](https://www.mordorintelligence.com/industry-reports/brazil-social-commerce-market)
- **Novo:** artefatos identitários estilo **"Spotify Wrapped"** (feitos pra print/Stories) [Modern Retail](https://www.modernretail.co/marketing/why-spotify-wrapped-esque-year-in-review-posts-took-over-q4-brand-marketing/); feeds de try-on com IA; acesso "members-only" como perk.
- **Datado/cringe (EVITAR):** NFT/metaverso (Nike vendeu RTFKT dez/2025) [Hypebeast](https://hypebeast.com/2026/1/nike-quietly-sold-rtfkt-december-2025); IA **não rotulada** (56% Gen Z confia em quem promete conteúdo humano); personalização genérica de massa.
- **Mágica:** "Meu Drop de Domingo" (drop semanal + PIX + early access VIP); "MIRA Wrapped"; loop autêntico de "compartilhe seu look" premiado com status (não desconto).

## Frente 5 — Ética do "deepfake do bem" + WhatsApp/RCS

- **LGPD:** foto de rosto/corpo = **dado sensível/biométrico** → consentimento específico e destacado, granular por finalidade. [LGPD Art. 11](https://lgpd-brazil.info/chapter_02/article_11)
- **Direito de imagem é requisito SEPARADO** (Código Civil Art. 20; STJ Súmula 403 presume dano em uso comercial não autorizado). Consentimento LGPD não basta. [Jusbrasil](https://www.jusbrasil.com.br/artigos/deepfakes-e-responsabilidade-penal-e-civil-por-que-voce-precisa-saber-o-que-assina-compartilha-ou-publica/5394861409)
- **Limitar finalidade/retenção:** apagar fonte ~1h, geradas ~24h (ou prazo declarado); revogação fácil. **Rotular saída IA**; **não treinar** modelo na foto dela (Lei 15.123/2025). [Photta](https://www.photta.app/business/guides/gdpr-compliant-virtual-try-on)
- **Premium, não creepy:** convite presencial pela vendedora; ela vê o que é guardado; proporções reais, sem afinar corpo; botão "não pareço eu" (refazer).
- **WhatsApp:** botões (≤3), listas (≤10), **carrossel de produtos (≤30)** com botão "provar" por card, **WhatsApp Flows** (formulário multi-tela — ideal p/ consentimento + preferências). Janela de 24h; outreach iniciado pela loja exige **template de Marketing pago** + opt-in. [Meta Flows](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows) · [Meta Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)
- **RCS:** ainda não é primário no Brasil (WhatsApp domina) → WhatsApp agora, RCS como canal 2º em 2026.
- **Mágica:** "Cofre MIRA" (painel de consentimento, apagar/pausar 1 toque); "garantia do espelho honesto"; duplo consentimento (imagem + LGPD), privado por padrão. *(validar com advogado de privacidade antes do lançamento.)*

---

## EUREKA — a síntese

**Pare de esconder o algoritmo.** A MIRA mostra, deixa a cliente moldar e devolve como identidade.
A personalização vira, ao mesmo tempo: **relacionamento + identidade compartilhável + ativo que compõe.**

Conceito unificador: **a Gêmea de Estilo** — retrato vivo de gosto+corpo, pilotado por cliente + vendedora.

6 momentos mágicos (todos viáveis hoje):
1. **Vídeo dela, não de modelo** (stills local 3070 + vídeo em nuvem sob demanda).
2. **DNA de Estilo vivo e visível** (ela vê e corrige; "mira de novo" aprende na hora).
3. **Receita das 7** = 4 certeiras + 2 calibradas + 1 carta selvagem (anti-staleness).
4. **Radar de ocasião + "em quem mirar hoje"** (proativo, recência).
5. **MIRA Wrapped** (cartão/filme de estilo compartilhável = viral + status).
6. **Espelho honesto + Cofre** (confiança/LGPD como luxo).

Anti-"tiozão": aprende e mostra; é vídeo+editorial; é compartilhável e humano-assinado; foge de NFT/metaverso; IA sempre rotulada; nunca afina o corpo; nunca dispara em massa.

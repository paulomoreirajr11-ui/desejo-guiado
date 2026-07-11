# Prompts editoriais — Desejo Guiado (padrão revista)

Sistema de prompts pra geração final (VTON: foto da pessoa + foto da peça → look produzido).
Objetivo: imagem **de revista**, que encanta a cliente e mantém a peça e o corpo reais.
Monte sempre assim: **[IDENTIDADE] + [PEÇA] + [CENA da ocasião] + [BELEZA/POSE do estilo] + [QUALIDADE]**.

---

## 0) FIDELIDADE DO ROSTO — o mais importante (a cliente tem que se RECONHECER)
Se o rosto não for fiel, o efeito se inverte: ela se sente enganada. O rosto é a identidade — é onde a gente se reconhece. Inteligência focada nisso (no sistema real):
1. **Referência boa:** 1 foto de rosto nítida, de frente, bem iluminada (a melhor disponível). Lixo entra = lixo sai.
2. **Módulo de identidade facial:** InstantID / PuLID / IP-Adapter-FaceID — condiciona a geração na "impressão digital" do rosto (embedding facial), não só na imagem de exemplo.
3. **Passo final de rosto:** face-swap (ReActor) + restauração (GFPGAN/CodeFormer) — cola o rosto EXATO dela, nítido, sobre o corpo/cena gerados.
4. **PORTÃO de similaridade (o pulo do gato):** o sistema MEDE a semelhança facial (cosine do embedding) entre a foto original e o resultado; só libera se ≥ limiar (ex. 0,75). Se não passar, **regenera sozinho** até bater. Acertividade automática.
5. **Humano no fim:** a vendedora confere e tem "gerar de novo" em 1 toque se não ficou ela.

## 1) Bloco IDENTIDADE (sempre — trava ROSTO + corpo real, anti-viés magro)
> Use the FIRST reference image as the EXACT same person — her FACE must be IDENTICAL to the reference (same facial features, bone structure, eyes, nose, mouth, smile and expression lines), same hair, skin tone and age; she must be instantly recognizable as the very same woman. Do NOT beautify, do NOT rejuvenate, do NOT slim or alter her face or body. Preserve her REAL body shape and proportions. Flattering and dignified.

Plus-size, reforçar: `keep her real plus-size curves, flattering and confident`.

## 2) Bloco PEÇA (sempre — fidelidade + tira cabide)
> Dress her in the [PEÇA: cor + corte + tecido + detalhes] from the SECOND reference image — reproduce the garment faithfully. Take ONLY the garment; completely remove any hanger, clips and background. [se acessório: + add the {acessório} as a styled layer.]

## 3) Bloco QUALIDADE (sempre, no fim)
> Full-length fashion editorial, shot on an 85mm lens, shallow depth of field, refined color grade, magazine-cover quality, aspirational and elegant, tack-sharp focus, photorealistic, entire body from head to feet in frame, beautifully exposed. No text, no logos, no hanger.

---

## 4) POOL de CENAS por OCASIÃO (sorteia 1 cena diferente a cada geração — ANTI-CARIMBO)
Nunca repetir a mesma cena em looks seguidos da mesma cliente. O sistema rotaciona o pool → parece editorial diário, nunca engessado. Variar também enquadramento (corpo inteiro / 3-4) e pose.
- **Dia a dia / Casual:** rua arborizada golden hour · terraço de café chique · jardim botânico/parque · galeria de arte minimalista · livraria-café aconchegante · calçadão à beira-mar.
- **Trabalho:** arquitetura minimalista clara · calçada urbana chique de dia · lobby/escritório de design · escadaria de concreto + vidro · rooftop corporativo.
- **Jantar / Date:** restaurante intimista à noite · rooftop ao entardecer · bar de hotel elegante · ruela charmosa com luzes quentes.
- **Festa:** salão com bokeh dourado · pista com luzes quentes · varanda de festa à noite · jardim iluminado.
- **Gala / Madrinha:** salão com lustres · escadaria clássica · hall de teatro/ópera · jardim formal à noite.
- **Praia / Resort:** praia de mar turquesa · deck/piscina de resort · calçadão tropical · varanda com vista-mar.
- **Academia:** estúdio fitness claro · academia moderna · estúdio de pilates/yoga · parque pra corrida de manhã.
- **Viagem:** ruela europeia · terraço com vista cênica · café de viagem charmoso · mirante no pôr do sol.

(English, no prompt: street at golden hour / café terrace / botanical garden / minimalist art gallery / cozy bookstore-café / seaside promenade — etc., conforme a ocasião.)

## 5) BELEZA + POSE por ESTILO (a personalidade dela)
- **Clássico:** polished natural makeup, sleek elegant hair, poised graceful posture.
- **Romântico:** soft glowy makeup, loose waves, gentle delicate pose.
- **Sensual:** defined elegant makeup, sleek hair, confident alluring (tasteful) pose.
- **Minimalista:** clean fresh makeup, effortless hair, calm refined stance.
- **Dramático / Statement:** bold refined makeup, structured hair, strong editorial pose.
- **Boho / Natural:** sun-kissed natural makeup, undone hair, relaxed free pose.
- **Esportivo:** dewy fresh makeup, sporty ponytail, dynamic confident posture.

---

## 6) Exemplo montado (Festa · plus · Clássico)
> Editorial fashion photograph for a luxury Brazilian boutique. Use the FIRST reference image as the EXACT person — preserve her exact face, hair, skin and age (~45) and her REAL plus-size body; do NOT slim her down, keep her curves, flattering and dignified. Dress her in the emerald-green hand-beaded sequined floor-length gown from the SECOND reference — reproduce faithfully; take ONLY the gown, remove any hanger/background. Scene: a grand evening gala with blurred warm golden chandelier bokeh, candlelit luxe ambiance. Glamorous tasteful makeup, sleek elegant updo, statement earrings, poised graceful pose. Full-length fashion editorial, 85mm lens, shallow depth of field, warm key + soft rim light, rich color grade, magazine-cover quality, tack-sharp, photorealistic, head to feet in frame, beautifully exposed. No text, no logos, no hanger.

## 7) Regras de ouro
1. Corpo e rosto reais SEMPRE travados (a cliente tem que se reconhecer).
2. Peça fiel — cor/corte/detalhe; tirar cabide e fundo.
3. Cena pela ocasião; pose/beleza pelo estilo dela.
4. 85mm + pouca profundidade + luz suave = cara de revista.
5. Corpo inteiro no quadro, bem exposto, sem texto/logo.
6. Gerar em 2K pros looks-herói (apresentação/Clube); 1K serve pro dia a dia (mais barato/rápido).

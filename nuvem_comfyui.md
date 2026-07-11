# ComfyUI na nuvem — arquitetura de excelência

Decisão (2026-06-19): rodar o ComfyUI **na nuvem**, na potência que entrega o resultado de revista que queremos. Hardware físico (comprar GPU) decidimos **depois**, com a demanda real medida.

## Por que nuvem (e não o 3070 agora)
- 3070 = 8 GB → **não** roda os modelos de ponta (Flux, alta-res, VTON + rosto juntos).
- Nuvem = GPU grande (24–80 GB) → modelos top + 2K/4K + upscale + sem fila → revista de verdade.
- Liga só quando usa → custo controlado no piloto.

## Onde rodar (recomendação)
| Etapa | Plataforma | Por quê |
|---|---|---|
| **Montar + afinar** o workflow | **RunPod** — pod com **A100 40 GB** (ou L40 48 GB), ComfyUI interativo | controle total pra construir/ajustar a receita; API padrão do ComfyUI |
| **Produção** (piloto/loja) | **ComfyDeploy** ou **fal serverless ComfyUI** | vira API gerenciada, paga por imagem, escala sozinho, zero manutenção |
Caminho: afina no RunPod → publica o workflow no serverless pra rodar no dia a dia.

## A RECEITA de excelência (workflow)
1. **Base Flux.1 [dev]** (Fill/Kontext) — realismo de revista *(precisa 24 GB+ → por isso nuvem)*.
2. **Vestir:** peça + pessoa → look (Flux Fill/Redux + IP-Adapter, ou IDM-VTON/CatVTON).
3. **Rosto (fidelidade):** **InstantID/PuLID** trava a identidade + **CodeFormer** restaura o rosto nítido.
4. **Cena/ocasião:** prompts editoriais (pools anti-carimbo de `prompts_editoriais.md`).
5. **Upscale final 2x** → tecido nítido no zoom.
6. **Portão de similaridade facial** → mede a semelhança; regenera se não bater. *(a inteligência)*
→ Saída **2K+, padrão revista, rosto fiel**.

## Como conecta (já está 80% pronto)
- O `server.py` já é a ponte (celular → servidor → motor → volta). 
- A API do ComfyUI é **padrão** (`POST /prompt` → `/history` → `/view`) — rode onde rodar.
- Liga a GPU da nuvem → ComfyUI numa URL → eu aponto o `server.py` (`COMFY_URL`) pra ela. **App e fluxo idênticos.**

## Quem faz o quê
- **Você:** cria a conta (RunPod) + sobe ComfyUI (template pronto, ~10 min) + escolhe a GPU.
- **Eu:** entrego o **workflow** (Flux + rosto + upscale + portão), **ligo no `server.py`**, **afino** a fidelidade e as cenas; testamos na loja.
- **Enquanto monta:** sigo gerando no padrão de excelência (já provado — pantacourt/Cláudia/Irene) pro piloto/concierge.

## Custo (ordem de grandeza)
- RunPod A100: ~US$ 1–2/h **só ligado** (no piloto, liga nas sessões).
- Serverless (ComfyDeploy/fal-comfy): centavos por imagem, escala sozinho.
- Hardware local depois: GPU 24 GB (4090/3090) ~R$ 12–20k **se** o volume justificar.

## Ordem
1. Subir o pod RunPod + ComfyUI (eu te guio passo a passo).
2. Eu monto/importo o workflow de excelência + ligo no `server.py`.
3. Afinar rosto + cenas → teste na loja.
4. Publicar no serverless pra produção.
5. Medir demanda → decidir máquina física.

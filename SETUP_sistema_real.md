# Desejo Guiado — rodar o sistema REAL (teste na loja)

Fluxo: **celular tira foto → servidor-ponte (este PC) → nuvem gera o look → volta no celular → envia no WhatsApp com as teclas / Clube.**
O software já está pronto (`server.py` + app em modo ao vivo). Falta só **ligar o motor de geração** (sua chave de nuvem). Em paralelo, montamos o ComfyUI local.

---

## A. Ligar AGORA (nuvem — testar hoje)

**1. Pegar uma chave de IA (5 min)**
- Crie conta em **fal.ai** → menu API Keys → gere uma chave (`FAL_KEY`). (Custo baixo, centavos por imagem.)
- *(Alternativa: Replicate — me avise que eu adapto o `server.py`.)*

**2. Rodar o servidor (neste PC)** — no PowerShell, na pasta do projeto:
```
$env:FAL_KEY="cole_sua_chave_aqui"
python server.py
```
Vai aparecer: `Motor nuvem (fal.ai): OK ✓` e a URL do celular.

**3. Liberar a porta** — se o Windows perguntar, clique **Permitir acesso** (Python na rede privada). Porta: 8770.

**4. No CELULAR (mesma Wi-Fi da loja)** abra:
```
http://192.168.15.57:8770/estudio/celular.html
```
*(Se o IP do PC mudar, rode `ipconfig` e use o novo IPv4.)*

**5. O teste de verdade:**
- Escolhe a **cliente** (ou Irenete) → **📷 Fotografar peça** (entra no estoque) → toca a peça → escolhe a **ocasião** → **Gerar look** → a nuvem devolve a imagem de revista → **Enviar no WhatsApp** (com as teclas) ou **Clube**.
- Os looks-demo (clientes carregadas) aparecem na hora; **peça nova fotografada** gera na nuvem.

> ⚠️ No 1º teste com a chave, pode ser preciso ajustar o nome do modelo (`$env:FAL_MODEL="..."`) — me chama que a gente acerta em 2 minutos.

---

## B. Modo concierge (HOJE, sem chave nenhuma)
Enquanto a chave não está configurada: a vendedora fotografa, **me manda a foto** (peça + cliente), eu gero (revista, rosto fiel) e devolvo em ~30s pra entrar no app. Real, zero setup.

---

## C. ComfyUI local (em paralelo — privacidade, custo zero/imagem)
Seu RTX 3070 (8 GB) roda VTON com modelo SD1.5 + rosto (apertado, mas dá pra still). Passo a passo (eu te guio):
1. Ligar o ComfyUI (`C:\comfyui\ComfyUI_windows_portable_nvidia\run_nvidia_gpu.bat`).
2. Instalar nós (ComfyUI-Manager): **CatVTON** ou **IDM-VTON** (vestir) + **ReActor**/**InstantID** (rosto) + **GFPGAN/CodeFormer** (restaurar rosto).
3. Baixar os modelos (alguns GB — pelo Manager; com proxy use as fontes confiáveis).
4. Eu entrego o **workflow JSON** (com a trava de rosto + portão de similaridade) e troco o `server.py` de `fal` pra `comfyui` (mesma URL, mesmo app).

---

## Segurança / LGPD
- Login por vendedora (a fazer no sistema real).
- Foto da cliente com consentimento (1 "ok" no WhatsApp basta no piloto).
- ComfyUI local = a foto nunca sai da loja (ideal pra dados sensíveis).

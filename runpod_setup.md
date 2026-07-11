# RunPod — subir o ComfyUI na nuvem (passo a passo)

Objetivo: uma GPU forte na nuvem rodando ComfyUI, com uma URL que o nosso `server.py` chama.
Tempo: ~15 min. No fim, você me manda **a URL do ComfyUI** e eu ligo tudo.

---

## 1. Criar conta e colocar crédito
1. Acesse **runpod.io** → **Sign Up** (Google/e-mail).
2. Menu **Billing** → **Add Credit** → coloque ~**US$ 10** (dá pra muitas horas de teste; só gasta quando o pod está ligado).

## 2. Criar o Pod (a máquina)
1. Menu esquerdo **Pods** → botão **Deploy** (ou **+ Deploy**).
2. **GPU** — escolha:
   - **RTX 4090 (24 GB)** → mais barato, roda Flux. *(comece por essa)*
   - ou **A40 (48 GB)** → folga total pra Flux + rosto + upscale.
3. Em **Pod Template**, clique em **Change Template** e procure **"ComfyUI"** → escolha um template de ComfyUI (ex.: *ai-dock / ComfyUI*, ou um oficial "ComfyUI"). *(É o que já vem com o ComfyUI pronto.)*
4. **Disco:**
   - **Container Disk:** ~20 GB
   - **Volume Disk:** **60–100 GB** (os modelos são grandes; o volume guarda eles entre sessões)
5. **Expose HTTP Ports:** confirme que tem **8188** (porta padrão do ComfyUI). Se o template usar outra (8888/3000), anote.
6. Clique **Deploy On-Demand**.

## 3. Abrir o ComfyUI
1. Espere o pod ficar **Running** (uns minutos — baixa a imagem na 1ª vez).
2. No card do pod → **Connect** → clique no **HTTP Service [Port 8188]** (abre algo tipo `https://xxxxx-8188.proxy.runpod.net`).
3. Abriu a tela do **ComfyUI**? ✅ A máquina está no ar.

## 4. (se o template não tiver) ComfyUI-Manager
- Se não tiver o botão **Manager** no ComfyUI, me avisa que te passo 2 comandos pra instalar (via **Connect → Web Terminal**).
- O **Manager** é o que instala os nós (InstantID, IDM-VTON…) e baixa os modelos — faremos juntos no próximo passo.

## 5. Me manda
- **A URL** do ComfyUI (`https://...-8188.proxy.runpod.net`).
- Confirma que a tela do ComfyUI abriu.
→ Eu **ligo no `server.py`** (`COMFY_URL`) + te entrego o **workflow de excelência** (Flux + rosto + upscale + portão de similaridade) pra importar.

---

### Dicas
- **Desligue o pod** quando não estiver usando (botão **Stop**) — só paga ligado. O **Volume** guarda os modelos pra próxima.
- Travou em algum passo? Tira um **print** e me manda (subo o quadro de upload) que eu te destravo na hora.
- Custo: RTX 4090 ~US$ 0,4–0,7/h · A40 ~US$ 0,4–0,8/h (varia) — só enquanto ligado.

# -*- coding: utf-8 -*-
"""
Servidor-ponte do Desejo Guiado.
- Serve o app (estudio/) pro celular na mesma Wi-Fi.
- POST /generate : recebe pessoa + peca (base64 data-uri OU caminho local) + ocasiao + estilo
                   -> monta o prompt editorial -> chama a nuvem (fal.ai) -> devolve o look.

Rodar:
    set FAL_KEY=sua_chave_fal        (Windows CMD)   |   $env:FAL_KEY="..."  (PowerShell)
    python server.py
Depois, no CELULAR (mesma Wi-Fi):  http://192.168.15.57:8770/estudio/celular.html
(Sem FAL_KEY o app funciona em modo demo/concierge; a geracao ao vivo pede a chave.)
"""
import os, sys, json, base64, random, socket, datetime, uuid, threading, urllib.request, urllib.parse, urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8770"))
FAL_KEY = os.environ.get("FAL_KEY", "").strip()
if not FAL_KEY:
    try:
        with open(os.path.join(ROOT, "fal_key.txt"), "r", encoding="utf-8") as _f:
            FAL_KEY = _f.read().strip()
    except Exception:
        pass
# modelo de edicao estilo "nano-banana" (pessoa + peca -> vestida). Troque via FAL_MODEL se quiser.
FAL_MODEL = os.environ.get("FAL_MODEL", "fal-ai/nano-banana/edit")

# ---- Clube de venda (feed compartilhado entre celular e TV) ----
CLUBE_FILE = os.path.join(ROOT, "clube_posts.json")
def load_clube():
    if SB_ON:
        try:
            rows = sb_req("GET", "clube", "select=*&order=ts.asc") or []
            return [{"img": r.get("img"), "marca": r.get("marca"), "desc": r.get("descricao"),
                "de": r.get("de"), "por": r.get("por"), "cond": r.get("cond"), "occ": r.get("occ"),
                "pecas": r.get("pecas"), "nome": r.get("nome"), "vend": r.get("vend")} for r in rows]
        except Exception:
            pass
    try:
        with open(CLUBE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
def save_clube(posts):
    try:
        with open(CLUBE_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False)
    except Exception:
        pass

# ---- Mesa Geral (estoque compartilhado entre todas as vendedoras) ----
def _ptam(t):
    try:
        return json.loads(t) if t else None
    except Exception:
        return None
def load_pecas(vend=""):
    """Lista SEM a foto (só a URL). Com centenas de peças, mandar base64 travaria o celular.
    sku: share_=Achado da Semana | estq_=estoque da loja (todas veem) | priv_=só da vendedora dona.
    Peça privada só sai pra dona (vend). Sem vend (painel do admin) = tudo."""
    if SB_ON:
        try:
            rows = sb_req("GET", "pecas", "select=sku,cat,nome,tam,preco,vend&order=ts.desc") or []
            out = []
            for r in rows:
                sku = str(r.get("sku") or "")
                priv = sku.startswith("priv_")
                if priv and vend and (r.get("vend") or "") != vend:
                    continue
                out.append({"f": sku, "cap": "/peca/" + sku + ".jpg", "cat": r.get("cat"),
                            "nome": r.get("nome"), "tam": _ptam(r.get("tam")), "preco": r.get("preco"),
                            "vend": r.get("vend"), "priv": 1 if priv else 0})
            return out
        except Exception:
            pass
    return []

_PECA_IMG = {}          # sku -> data-uri (cache em memória; a foto de uma peça nunca muda)
def peca_img(sku):
    if not sku:
        return ""
    if sku in _PECA_IMG:
        return _PECA_IMG[sku]
    img = ""
    if SB_ON:
        try:
            rows = sb_req("GET", "pecas", "sku=eq." + urllib.parse.quote(str(sku)) + "&select=img") or []
            img = (rows[0].get("img") if rows else "") or ""
        except Exception:
            img = ""
    if img:
        _PECA_IMG[sku] = img
    return img

# ---- Registro de uso por vendedora (painel do admin) ----
USO_FILE = os.path.join(ROOT, "uso_log.json")
def load_uso():
    if SB_ON:
        try:
            return sb_req("GET", "uso", "select=*&order=ts.desc&limit=3000") or []
        except Exception:
            pass
    try:
        with open(USO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
def log_uso(entry):
    if SB_ON:
        try:
            sb_req("POST", "uso", body={"vend": entry.get("vend"), "cliente": entry.get("cliente"),
                "pecas": entry.get("pecas"), "ocasiao": entry.get("ocasiao"), "fundo": entry.get("fundo"), "ts": entry.get("ts")})
            return
        except Exception:
            pass
    try:
        log = []
        try:
            with open(USO_FILE, "r", encoding="utf-8") as f:
                log = json.load(f)
        except Exception:
            log = []
        log.append(entry); log = log[-3000:]
        with open(USO_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False)
    except Exception:
        pass

# ---- Reservas no provador ----
RESERVA_FILE = os.path.join(ROOT, "reservas.json")
def load_reservas():
    if SB_ON:
        try:
            return sb_req("GET", "reservas", "select=*&order=ts.desc") or []
        except Exception:
            pass
    try:
        with open(RESERVA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
def add_reserva(r):
    if SB_ON:
        try:
            sb_req("POST", "reservas", body={"vend": r.get("vend"), "cliente": r.get("cliente"),
                "pecas": r.get("pecas"), "preco": r.get("preco"), "img": r.get("img"), "ts": r.get("ts")})
            return
        except Exception:
            pass
    try:
        rs = []
        try:
            with open(RESERVA_FILE, "r", encoding="utf-8") as f:
                rs = json.load(f)
        except Exception:
            rs = []
        rs.append(r); rs = rs[-2000:]
        with open(RESERVA_FILE, "w", encoding="utf-8") as f:
            json.dump(rs, f, ensure_ascii=False)
    except Exception:
        pass

# ---- Looks compartilhados + reacoes (as "teclas") ----
LOOKS_FILE = os.path.join(ROOT, "looks.json")
def load_looks():
    if SB_ON:
        try:
            rows = sb_req("GET", "looks", "select=*&order=ts.desc&limit=4000") or []
            return {r["id"]: {"img": r.get("img"), "cliente": r.get("cliente"), "vend": r.get("vend"),
                "pecas": r.get("pecas"), "occ": r.get("occ"), "reacao": r.get("reacao") or "",
                "reacao_ts": r.get("reacao_ts"), "ts": r.get("ts")} for r in rows if r.get("id")}
        except Exception:
            pass
    try:
        with open(LOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
def save_looks(d):
    try:
        with open(LOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
    except Exception:
        pass

# ---- Trava por aparelho (device-lock das vendedoras) ----
CLAIMS_FILE = os.path.join(ROOT, "claims.json")
def load_claims():
    if SB_ON:
        try:
            rows = sb_req("GET", "claims", "select=*") or []
            return {r["vend"]: {"device": r.get("device"), "ts": r.get("ts")} for r in rows if r.get("vend")}
        except Exception:
            pass
    try:
        with open(CLAIMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
def save_claims(d):
    try:
        with open(CLAIMS_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
    except Exception:
        pass

# ---- Supabase (banco de dados persistente) ----
SB_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SB_KEY = os.environ.get("SUPABASE_KEY", "")
SB_ON = bool(SB_URL and SB_KEY)
def sb_req(method, table, params="", body=None, prefer="return=representation"):
    if not SB_ON:
        return None
    url = SB_URL + "/rest/v1/" + table + (("?" + params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    headers = {"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY, "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt.strip() else []

# ---- Placar de esforço (agrega uso + looks + fichas por vendedora) ----
def load_fichas_all():
    if SB_ON:
        try:
            return sb_req("GET", "fichas", "select=vend,cliente,ts") or []
        except Exception:
            pass
    return []

def _placar_cutoff(periodo):
    now = datetime.datetime.now()
    if periodo == "hoje":
        d = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif periodo == "semana":
        d = now - datetime.timedelta(days=7)
    elif periodo == "sempre":
        return ""
    else:
        d = now - datetime.timedelta(days=30)
    return d.isoformat(timespec="seconds")

def _gen_cliente(nome):
    n = (nome or "").strip().lower()
    return (not n) or n in ("oi", "oi!", "cliente") or n.startswith("foto") or n.startswith("cliente")

def build_placar(periodo="mes"):
    cutoff = _placar_cutoff(periodo)
    uso = load_uso() or []
    looks = load_looks() or {}
    fichas = load_fichas_all() or []
    reservas = load_reservas() or []
    gerados, atendidas, enviados, respostas, fichas_ct, reservas_ct = {}, {}, {}, {}, {}, {}
    # sumidas reativadas: historico completo por (vend, cliente), gap >= 30 dias
    hist = {}
    for e in uso:
        c = (e.get("cliente") or "").strip()
        if not _gen_cliente(c):
            hist.setdefault((e.get("vend") or "", c), []).append(e.get("ts") or "")
    reativadas = {}
    for (v, c), tss in hist.items():
        tss = sorted(t for t in tss if t)
        for i in range(1, len(tss)):
            try:
                gap = (datetime.datetime.fromisoformat(tss[i]) - datetime.datetime.fromisoformat(tss[i - 1])).days
            except Exception:
                continue
            if gap >= 30 and tss[i] >= cutoff:
                reativadas[v] = reativadas.get(v, 0) + 1
    for e in uso:
        if (e.get("ts") or "") < cutoff:
            continue
        v = e.get("vend") or ""
        gerados[v] = gerados.get(v, 0) + 1
        c = (e.get("cliente") or "").strip()
        if not _gen_cliente(c):
            atendidas.setdefault(v, set()).add(c)
    for l in looks.values():
        if (l.get("ts") or "") >= cutoff:
            v = l.get("vend") or ""
            enviados[v] = enviados.get(v, 0) + 1
        if (l.get("reacao") or "") == "Acertou em mim" and (l.get("reacao_ts") or l.get("ts") or "") >= cutoff:
            v = l.get("vend") or ""
            respostas[v] = respostas.get(v, 0) + 1
    for f in fichas:
        if (f.get("ts") or "") >= cutoff:
            v = f.get("vend") or ""
            fichas_ct[v] = fichas_ct.get(v, 0) + 1
    for r in reservas:
        if (r.get("ts") or "") >= cutoff:
            v = r.get("vend") or ""
            reservas_ct[v] = reservas_ct.get(v, 0) + 1
    vends = set(list(gerados) + list(enviados) + list(fichas_ct) + list(respostas)
                + list(reservas_ct) + list(reativadas) + list(atendidas))
    vends.discard("")
    rows = [{"vend": v, "fichas": fichas_ct.get(v, 0), "gerados": gerados.get(v, 0),
             "atendidas": len(atendidas.get(v, set())), "enviados": enviados.get(v, 0),
             "respostas": respostas.get(v, 0), "reservas": reservas_ct.get(v, 0),
             "reativadas": reativadas.get(v, 0)} for v in vends]
    rows.sort(key=lambda r: (-r["enviados"], -r["gerados"], -r["fichas"]))
    return rows

# ---- Meta do mês (o admin define; a vendedora vê o progresso) ----
META_FILE = os.path.join(ROOT, "metas.json")
def _mes_atual():
    return datetime.datetime.now().strftime("%Y-%m")
def load_meta(mes):
    if SB_ON:
        try:
            rows = sb_req("GET", "metas", "mes=eq." + urllib.parse.quote(mes) + "&select=*") or []
            return rows[0] if rows else {}
        except Exception:
            pass
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return (json.load(f) or {}).get(mes, {})
    except Exception:
        return {}
def _mint(v):
    try:
        s = str(v).strip()
        return int(s) if s not in ("", "None") else None
    except Exception:
        return None
def save_meta(mes, body):
    row = {"mes": mes, "fichas": _mint(body.get("fichas")), "looks": _mint(body.get("looks")),
           "enviados": _mint(body.get("enviados")), "reativadas": _mint(body.get("reativadas")),
           "atualizado": datetime.datetime.now().isoformat(timespec="seconds")}
    if SB_ON:
        try:
            sb_req("POST", "metas", body=row, prefer="resolution=merge-duplicates")
            return row
        except Exception:
            pass
    try:
        d = {}
        try:
            with open(META_FILE, "r", encoding="utf-8") as f:
                d = json.load(f) or {}
        except Exception:
            d = {}
        d[mes] = row
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
    except Exception:
        pass
    return row

# ---- POOL de cenas por ocasiao (25 cada, 9 estilos; rotaciona automatico -> anti-carimbo) ----
POOLS = {
 "Festa Dia": [
   "a bright garden brunch party with white florals and warm sunlight",
   "a sunny rooftop daytime party with skyline views",
   "a chic poolside day party with palms and turquoise water",
   "an elegant outdoor lunch party under a pergola, dappled sunlight",
   "a refined garden tea party with pastel flowers in daylight",
   "a bright beach club daytime celebration with white cabanas",
   "a sunlit courtyard party with hanging greenery",
   "a vineyard daytime celebration with long tables and sunshine",
   "a colorful garden party with soft bunting and bright midday light",
   "a marina daytime party on a white yacht deck",
   "an outdoor terrace brunch celebration with balloons and sun",
   "a botanical garden party with lush greenery and soft daylight",
   "a rooftop garden daytime soiree with a bright skyline",
   "a charming backyard celebration in warm afternoon sun",
   "a lakeside daytime party on a wooden deck",
   "a bright gallery daytime reception with white walls",
   "an elegant hotel garden party at midday",
   "a sunny orchard party with blossoming trees",
   "a chic rooftop pool party in bright afternoon light",
   "a daytime garden gala with a white marquee and sunlight",
   "a chic seaside terrace daytime party with ocean breeze",
   "a sunlit park celebration with picnic elegance",
   "a bright greenhouse party with glass walls and daylight",
   "a countryside estate lawn party in golden afternoon light",
   "a vibrant tropical garden daytime party with bright blooms"],
 "Festa Noite": [
   "a lively party with warm golden bokeh lights",
   "an elegant venue with crystal chandelier bokeh",
   "a night-time rooftop terrace with warm string lights and a city skyline",
   "a glamorous ballroom with soft golden lighting",
   "an upscale garden party at dusk with delicate fairy lights",
   "an opulent staircase bathed in golden chandelier light",
   "a rooftop cocktail bar at night with city-light bokeh",
   "a grand theater foyer in red and gold tones",
   "an elegant garden gala under a lit pergola at night",
   "a luxe rooftop party with champagne-gold bokeh",
   "an intimate jazz club with warm amber stage lights",
   "a marble ballroom with tall floral arrangements at night",
   "a glamorous yacht deck at night with distant city lights",
   "an art gallery soiree with soft spotlights and warm bokeh",
   "a dazzling chandelier hall with golden reflections",
   "a rooftop celebration with sparkling string lights at night",
   "an elegant masquerade ballroom in deep jewel tones",
   "a luxe lounge with a warm amber glow",
   "a candlelit palace terrace at night",
   "a glamorous red-carpet entrance with warm bokeh",
   "an opulent dinner gala with golden table settings",
   "a rooftop champagne terrace under fairy lights",
   "a vintage-glamour cocktail bar with velvet booths",
   "a festive winter gala with twinkling lights",
   "a chic lounge club with a warm golden glow at night"],
 "Casamento Dia": [
   "an elegant garden wedding venue with white florals in daylight",
   "a sunlit vineyard wedding terrace at golden hour",
   "a romantic garden gazebo draped in white flowers, soft daylight",
   "a sunlit countryside estate lawn with elegant white wedding decor",
   "a refined coastal wedding terrace overlooking the sea by day",
   "a classic European church entrance with stone arches in daylight",
   "a manor-house garden with rose arches at golden hour",
   "a blooming glass orangery with soft diffused daylight",
   "a romantic vineyard ceremony aisle at golden hour",
   "a luxurious garden reception with white draped tables in daylight",
   "a coastal cliffside wedding terrace by day",
   "a charming countryside barn wedding in soft afternoon light",
   "a lush conservatory wedding with greenery and blooms in daylight",
   "a palace garden with fountains and white florals in sunlight",
   "a beachside wedding arch on white sand at midday",
   "a sunlit lavender field wedding setting",
   "an elegant garden marquee wedding with daylight streaming in",
   "a romantic orchard wedding with blossoming trees by day",
   "a refined lakeside wedding lawn in soft morning light",
   "a Tuscan countryside wedding terrace at golden hour",
   "a botanical garden wedding aisle with lush daylight",
   "a chic rooftop garden wedding in bright daytime",
   "a charming village chapel courtyard in warm daylight",
   "an elegant estate veranda wedding with sunlight and florals",
   "a sunny seaside wedding deck with white drapery"],
 "Casamento Noite": [
   "an opulent ballroom set for a wedding, warm chandelier light",
   "a candlelit wedding reception with lush floral centerpieces",
   "a grand staircase decorated with white florals, soft evening light",
   "a lakeside wedding pavilion at dusk with warm lights",
   "an upscale hotel ballroom foyer with crystal chandeliers at night",
   "an elegant marquee wedding with draped fabric and fairy lights",
   "a candlelit wedding terrace at dusk overlooking the sea",
   "a grand ballroom with a floral arch and chandeliers at night",
   "an intimate candlelit chapel with floral arrangements",
   "a rooftop wedding terrace overlooking the city at dusk",
   "a romantic garden reception under string lights at night",
   "an elegant cathedral interior with warm evening light",
   "a luxurious vineyard wedding terrace at twilight with lanterns",
   "a candlelit courtyard wedding with climbing vines",
   "a glamorous hotel ballroom wedding with golden light",
   "a charming barn wedding glowing with fairy lights at night",
   "a coastal wedding terrace at sunset with warm reflections",
   "a palace ballroom wedding with chandeliers and candlelight",
   "a romantic rooftop wedding under twinkling lights",
   "an elegant tented reception with warm hanging lanterns",
   "a candlelit lakeside wedding pavilion at night",
   "a grand garden gala wedding with golden uplighting",
   "a refined ballroom wedding with tall candelabras",
   "an intimate winery cellar wedding with warm candlelight",
   "a starlit garden wedding with fairy lights and florals"],
 "Dia a dia": [
   "a sunlit upscale tree-lined street at golden hour, warm backlight, creamy bokeh",
   "a chic sidewalk cafe terrace in the morning, soft natural daylight",
   "a lush botanical garden path, dappled sunlight through the leaves",
   "a bright airy minimalist loft with tall windows, soft daylight",
   "a charming cobblestone old-town street, warm late-afternoon light",
   "a quiet luxury boutique interior with soft warm lighting",
   "a sunlit Parisian-style balcony with potted flowers",
   "a refined marble staircase with warm daylight",
   "a leafy boulevard with creamy bokeh at golden hour",
   "a bright art gallery with soft diffused light",
   "an elegant tree-shaded plaza with a stone fountain, warm light",
   "a sunlit flower shop with blooms by the entrance, soft daylight",
   "a refined cafe interior with marble tables and warm light",
   "a bright loft with natural light and indoor greenery",
   "a quiet upscale residential street with ivy walls at golden hour",
   "a sunlit cobblestone square with a coffee kiosk, morning light",
   "a leafy university campus path with old stone buildings",
   "a bright farmers market with flower stalls, soft daylight",
   "a charming bakery storefront with warm window light",
   "a tree-lined canal walk with gentle reflections",
   "a sunny rooftop cafe with potted herbs",
   "a quiet museum garden courtyard, soft light",
   "a pastel-colored townhouse street at golden hour",
   "a bright modern library reading room with tall windows",
   "a sunlit plaza with a vintage carousel in the distance"],
 "Casual": [
   "a charming city street at golden hour, relaxed elegant vibe",
   "a cozy bookstore-cafe with warm window light",
   "a breezy seaside promenade, airy bright light",
   "a rooftop terrace with green plants and soft sunlight",
   "a sunny park lawn lined with trees, gentle daylight",
   "a lively open-air market street, warm afternoon light",
   "a minimalist concept store, bright and airy",
   "a wooden lakeside pier at golden hour",
   "a leafy courtyard cafe with warm string lights",
   "a sunny rooftop garden overlooking the city",
   "a sunny vineyard terrace with rolling hills behind",
   "a relaxed beachside cafe with rattan chairs, warm light",
   "a cobblestone piazza with a gelato cart in afternoon sun",
   "a leafy riverside walkway with dappled light",
   "a cozy artisan coffee roastery with warm wood tones",
   "a relaxed harbor boardwalk with sailboats, bright light",
   "a sunny rooftop bar in the afternoon with city views",
   "a bohemian street with murals and string lights",
   "a cozy garden brunch spot with wicker chairs",
   "a sunlit orchard path with fruit trees",
   "a vibrant flower market lane, warm tones",
   "a beachside palm grove at golden hour",
   "a charming bookshop alley with warm lamps",
   "a riverside picnic lawn with soft afternoon light",
   "a trendy concept cafe with greenery and natural light"],
 "Trabalho": [
   "a sophisticated minimalist architectural lobby, clean daylight",
   "a chic urban sidewalk beside glass buildings, bright directional light",
   "a modern design office with warm wood and glass, soft light",
   "an elegant hotel lobby with marble and brass accents, refined light",
   "a bright contemporary co-working space with large windows, crisp daylight",
   "a sleek glass conference lounge, soft daylight",
   "an upscale rooftop business lounge at midday",
   "a refined library study with warm wood shelves",
   "a contemporary museum atrium, clean bright light",
   "a boutique hotel reception with brass and stone",
   "a minimalist rooftop terrace of a glass tower at midday",
   "an elegant executive lounge with leather and brass details",
   "a bright architectural courtyard with clean modern lines",
   "a sophisticated art-deco lobby with polished marble floors",
   "a modern boardroom with floor-to-ceiling city views",
   "a sleek glass skybridge with city views, crisp light",
   "an elegant law-firm library with dark wood and brass",
   "a minimalist white gallery-like office, bright light",
   "a rooftop executive terrace at golden hour",
   "a modern atrium with indoor trees and skylights",
   "a refined hotel business lounge with marble",
   "a contemporary tech campus courtyard, clean light",
   "a polished corporate lobby with a grand reception desk",
   "a bright open-plan studio with designer furniture",
   "a sophisticated rooftop meeting lounge at midday"],
 "Festa": [
   "a lively party with warm golden bokeh lights",
   "an elegant venue with crystal chandelier bokeh",
   "a night-time rooftop terrace with warm string lights and a city skyline",
   "a glamorous ballroom with soft golden lighting",
   "an upscale garden party at dusk with delicate fairy lights",
   "an opulent staircase bathed in golden chandelier light",
   "a candlelit fine-dining restaurant, warm glow",
   "a rooftop cocktail bar at night with city-light bokeh",
   "a grand theater foyer in red and gold tones",
   "an elegant garden gala under a lit pergola at night",
   "a luxe rooftop party with champagne-gold bokeh",
   "an intimate jazz club with warm amber stage lights",
   "a marble ballroom with tall floral arrangements at night",
   "a glamorous yacht deck at night with distant city lights",
   "an art gallery soiree with soft spotlights and warm bokeh",
   "a dazzling chandelier hall with golden reflections",
   "a rooftop celebration with sparkling string lights at night",
   "an elegant masquerade ballroom in deep jewel tones",
   "a luxe lounge with a warm amber glow",
   "a candlelit palace terrace at night",
   "a glamorous red-carpet entrance with bokeh",
   "an opulent dinner gala with golden table settings",
   "a rooftop champagne terrace under fairy lights",
   "a vintage-glamour cocktail bar with velvet booths",
   "a festive winter gala with twinkling lights"],
 "Praia": [
   "a luminous beach with turquoise sea and white sand, bright airy light",
   "a stylish resort pool deck, sunny with soft palm shadows",
   "a wooden beach boardwalk at golden hour",
   "a tropical seaside terrace overlooking the ocean",
   "a sandy dune with sea grass, soft warm afternoon light",
   "a white-sand cove with turquoise water, bright midday sun",
   "a chic beach club with cabanas and palms",
   "a coastal cliff path overlooking the sea at golden hour",
   "a wooden overwater deck in bright tropical light",
   "a sunset beach with a warm pink sky",
   "a Mediterranean seaside village with whitewashed walls",
   "a luxury beach resort lounge with billowing white curtains",
   "a turquoise lagoon with a wooden jetty in bright sun",
   "a palm-lined coastal road at golden hour",
   "a chic infinity pool overlooking the ocean at midday",
   "a secluded white-sand beach with clear turquoise water",
   "a luxury yacht deck on a calm blue sea",
   "a tropical beach bar with a thatched roof and palms",
   "a rocky cove with crystal water at midday",
   "a beachfront boardwalk at sunset with warm tones",
   "a palm-shaded hammock spot by the shore",
   "a sunny marina with white boats and blue water",
   "an overwater bungalow deck in a turquoise lagoon",
   "a golden-sand dune with sea oats at golden hour",
   "a chic poolside cabana overlooking the sea"],
 "Academia": [
   "a bright modern fitness studio, crisp even daylight",
   "a clean pilates studio with large windows, soft light",
   "a minimalist yoga studio with wood floor and plants, calm light",
   "an outdoor park workout spot at sunrise, fresh light",
   "a sleek gym with natural light and mirrors, clean modern look",
   "a rooftop yoga deck at sunrise, fresh light",
   "a boutique gym with warm wood and green plants",
   "a reformer pilates studio with large bright windows",
   "an outdoor park running track on a fresh morning",
   "a modern wellness studio with soft natural light",
   "a bright spin studio with sleek modern bikes and ambient light",
   "an open-air rooftop gym deck at sunrise over the skyline",
   "a serene beachfront yoga platform at dawn",
   "a modern running track in a green park at soft morning light",
   "a minimalist home gym with warm wood and large windows",
   "a sleek rooftop fitness terrace at sunrise",
   "a bright boxing studio with modern equipment",
   "a calm outdoor yoga deck surrounded by greenery",
   "a modern functional-training box with natural light",
   "a riverside running path on a fresh morning",
   "a minimalist stretching studio with wood floors",
   "a sunny park calisthenics area at dawn",
   "a clean reformer pilates room with soft light",
   "a mountain-view gym terrace in morning light",
   "a bright dance studio with mirrored walls"],
 "Casamento": [
   "an elegant garden wedding venue with white florals and string lights",
   "a grand stone chapel courtyard with soft daylight",
   "a luxurious vineyard wedding terrace at golden hour",
   "a romantic garden gazebo draped in white flowers",
   "an opulent ballroom set for a wedding, warm chandelier light",
   "a sunlit countryside estate lawn with elegant white wedding decor",
   "a refined coastal wedding terrace overlooking the sea at sunset",
   "a classic European church entrance with stone arches, warm light",
   "an elegant marquee wedding with draped fabric and fairy lights",
   "a manor-house garden with rose arches at golden hour",
   "a candlelit wedding reception with lush floral centerpieces",
   "a grand staircase decorated with white florals, soft light",
   "a lakeside wedding pavilion at dusk with warm lights",
   "an upscale hotel ballroom foyer with crystal chandeliers",
   "a blooming glass orangery with soft diffused daylight",
   "an elegant cathedral interior with soft light through stained glass",
   "a romantic vineyard ceremony aisle at golden hour",
   "a luxurious garden reception with white draped tables",
   "a grand ballroom with a floral arch and chandeliers",
   "a coastal cliffside wedding terrace at sunset",
   "a charming countryside barn wedding with fairy lights",
   "a lush conservatory wedding with greenery and blooms",
   "a palace garden with fountains and white florals",
   "an intimate candlelit chapel with floral arrangements",
   "a rooftop wedding terrace overlooking the city at dusk"],
 "Viagem": [
   "a charming European cobblestone alley lined with cafes, warm light",
   "a scenic Amalfi-style coastal cliff with deep-blue sea behind",
   "a luxury hotel lobby with vintage travel trunks, refined light",
   "a sunlit Mediterranean piazza with a central fountain",
   "a chic airport lounge with floor-to-ceiling windows",
   "a romantic Parisian boulevard at golden hour",
   "a vintage train platform with warm directional light",
   "a Santorini-style whitewashed terrace overlooking the sea",
   "a Tuscan countryside road lined with cypress trees",
   "a colorful old-town market street in warm tones",
   "a luxury resort garden path with tall palms in bright light",
   "a historic grand plaza with elegant architecture at golden hour",
   "a seaside boardwalk of a glamorous coastal town at sunset",
   "a rooftop terrace overlooking an iconic city skyline",
   "a charming canal-side street with little bridges, soft daylight",
   "a sunlit Greek-island staircase with bougainvillea",
   "a grand European avenue with landmark architecture, golden hour",
   "a colorful old-town tram street at golden hour",
   "a Venetian-style canal with gondolas, warm light",
   "a Moroccan riad courtyard with mosaic tiles",
   "a luxury safari lodge terrace at golden hour",
   "a snowy alpine village street with warm lights",
   "a tropical resort infinity pool overlooking the jungle",
   "a historic sunlit piazza at sunset",
   "a scenic coastal cliff road with a vintage vibe"],
 "Jantar": [
   "an intimate candlelit fine-dining restaurant, warm glow",
   "a romantic rooftop restaurant with city lights at night",
   "a cozy wine bar with warm amber lighting",
   "an elegant terrace restaurant with hanging lights at dusk",
   "a chic hotel bar with moody warm lighting",
   "a candlelit garden dinner with delicate fairy lights",
   "a sophisticated speakeasy with deep warm tones",
   "a waterfront restaurant terrace at sunset with warm reflections",
   "an upscale Italian trattoria with warm intimate light",
   "a romantic balcony dinner overlooking the city at night",
   "a refined cocktail lounge with velvet and gold accents",
   "a candlelit courtyard restaurant with climbing vines",
   "a moody supper club with warm amber stage glow",
   "an elegant private dining room with soft candlelight",
   "a stylish rooftop lounge at blue hour with warm bokeh",
   "an elegant rooftop restaurant with skyline and candlelight",
   "a romantic seaside terrace dinner at sunset",
   "a cozy fireplace lounge with warm amber light",
   "a chic bistro at night with warm glowing windows",
   "a candlelit wine cellar with rustic charm",
   "a sophisticated jazz lounge in deep blue and gold",
   "an intimate garden terrace with hanging lanterns",
   "a luxury hotel rooftop bar at blue hour",
   "a candlelit private chef's table, warm glow",
   "a moody cocktail speakeasy with leather and brass"],
}
_scene_idx = {}
def pick_cena(ocasiao):
    pool = POOLS.get(ocasiao, POOLS["Dia a dia"])
    if ocasiao not in _scene_idx:
        _scene_idx[ocasiao] = random.randint(0, len(pool) - 1)
    else:
        _scene_idx[ocasiao] = (_scene_idx[ocasiao] + 1) % len(pool)
    return pool[_scene_idx[ocasiao]]

BEAUTY = {
 "Festa Dia": "fresh natural daytime makeup with a soft glow and an elegant hairstyle that suits the dress",
 "Festa Noite": "soft elegant evening makeup and a refined hairstyle that suits the dress",
 "Casamento Dia": "elegant fresh makeup with a luminous daytime complexion and softly styled hair",
 "Casamento Noite": "elegant evening makeup with a warm glow and softly styled elegant hair",
 "Festa": "soft minimal makeup and an elegant hairstyle that simply suits the dress",
 "Trabalho": "polished natural makeup and a neat, sophisticated hairstyle",
 "Dia a dia": "fresh natural everyday makeup and soft, natural hair",
 "Casual": "light fresh makeup and relaxed natural hair",
 "Praia": "sun-kissed glowing skin with minimal beachy makeup and natural beach waves",
 "Academia": "a fresh, dewy clean look and a sporty sleek ponytail",
 "Casamento": "elegant refined makeup with a luminous complexion and softly styled elegant hair",
 "Viagem": "fresh radiant makeup with a healthy glow and effortless natural hair",
 "Jantar": "soft glamorous evening makeup with a warm glow and elegant loose waves",
}
LAYER_BASE  = ("camis","blus","regata","body","cropp","t-shirt","tshirt","top ","chemise","vestido","gola alta")
LAYER_MID   = ("colete","macac","macaqu","jardineira","salopete","suspens","avental")
LAYER_OUTER = ("casaco","blazer","jaqueta","cardig","sobretudo","trench","palet","kimono","poncho","parka","capa ")

def _layer_of(nome):
    n = " " + (nome or "").lower() + " "
    for k in LAYER_OUTER:
        if k in n: return 3
    for k in LAYER_MID:
        if k in n: return 2
    for k in LAYER_BASE:
        if k in n: return 1
    return 0

def layering_hint(nomes):
    """Descobre a ordem das camadas pelos nomes das peças: base por baixo, meio, externa por cima."""
    tag = [(_layer_of(n), n) for n in nomes]
    tag = sorted([t for t in tag if t[0] > 0], key=lambda x: x[0])
    if len(tag) < 2:
        return ""
    base  = [n for (l, n) in tag if l == 1]
    mid   = [n for (l, n) in tag if l == 2]
    outer = [n for (l, n) in tag if l == 3]
    parts = []
    if base:  parts.append("the " + " and ".join(base) + " worn UNDERNEATH as the base layer (closest to the body)")
    if mid:   parts.append("the " + " and ".join(mid) + " layered ON TOP of the base")
    if outer: parts.append("the " + " and ".join(outer) + " worn OVER everything as the outermost layer")
    if len(parts) < 2:
        return ""
    return (" LAYERING ORDER (very important — keep this exact order): " + ", then ".join(parts) +
            ". The base layer stays underneath with its sleeves, collar or hem visible coming out from beneath the piece on top; "
            "never swap this order and never hide the base layer.")

def build_prompt(ocasiao, estilo, pecas="", fundo="cena"):
    pose = {"Clássico":"poised graceful posture","Romântico":"soft delicate pose","Sensual":"confident tasteful pose",
            "Minimalista":"calm refined stance","Dramático":"strong editorial pose","Esportivo":"dynamic confident posture"}.get(estilo, "confident elegant pose")
    beauty = BEAUTY.get(ocasiao, "polished natural makeup and styled hair")
    if isinstance(pecas, (list, tuple)):
        nomes = [str(x) for x in pecas if x]
        peca = (" The complete look includes: " + ", ".join(nomes) + ".") if nomes else ""
        peca += layering_hint(nomes)
    else:
        peca = (" The garment is a " + pecas + ".") if pecas else ""
    if fundo == "estudio":
        cena = ("in a professional photography studio against a seamless infinite light-grey backdrop, "
                "clean even softbox studio lighting, no props and no scenery")
    else:
        cena = pick_cena(ocasiao)
    return ("A realistic, elegant fashion photograph of a REAL woman wearing a REAL outfit — a virtual try-on for a real "
            "boutique. The woman and the clothes are REAL products and must be reproduced EXACTLY as in the reference images; "
            "ONLY the background scene and her pose may change for the occasion — NEVER the woman and NEVER the garment. "
            "THE GARMENTS ARE THE PRODUCT BEING SOLD, so this is the most important rule. Reproduce each piece from the "
            "OTHER reference images (every image after the first) EXACTLY and unchanged: the SAME silhouette, the SAME "
            "neckline, the SAME straps and sleeves, the SAME length, the SAME fabric and colors, and the EXACT same print, "
            "flowers, embroidery, lace, beading or appliqué in the SAME place and SAME size as the reference. Do NOT "
            "redesign, restyle or 'upgrade' the garment to match the occasion or a magazine look. Specifically: do NOT turn "
            "a localized floral appliqué into an all-over floral print; do NOT change a spaghetti-strap dress into a "
            "one-shoulder, halter, sleeved or lace dress; do NOT add, remove or move straps, sleeves, flowers or details; "
            "do NOT replace a complex artwork/fresco print with a different print. The customer must receive the IDENTICAL "
            "piece shown. Include EVERY piece shown — top, bottom or dress, footwear and accessories — styled into one "
            "harmonious look; take ONLY the garments and remove any hanger, clips and background." + peca +
            " The occasion only sets the BACKGROUND scene and her hair and makeup — it must NEVER change the cut, neckline, "
            "straps, sleeves, length or design of the dress. Even for a party, gala, wedding or night event, keep the EXACT "
            "same store garment; do NOT make it more formal, strapless, one-shoulder, longer or a gala gown. "
            "The woman is the person in the FIRST reference image and her FACE must be IDENTICAL to that reference "
            "(same facial features, bone structure, eyes, nose, mouth, smile and expression), with the SAME hair COLOR, the "
            "SAME hair LENGTH, the same skin tone and the same AGE. If she wears glasses in the reference, KEEP the glasses. "
            "She must remain INSTANTLY recognizable as that exact same real woman. Do NOT beautify, rejuvenate, slim her, "
            "change her hair color or hair length, remove her glasses, or turn her into a young fashion model. "
            "Hair and makeup: " + beauty + " — you may arrange the hair to suit the occasion, but ALWAYS keep its real color and real length. "
            # --- CORPO FIEL: nem mais gorda, nem mais magra (a IA estava ENGORDANDO a cliente) ---
            "HER BODY: reproduce her REAL body EXACTLY as it is in the FIRST reference image — the same height, the same "
            "weight, the same silhouette and the same proportions (shoulders, bust, waist, hips, arms, legs). She is a real "
            "customer, not a fashion model. Do NOT make her heavier, wider, thicker, rounder or bulkier than she really is; "
            "and do NOT slim, stretch, tone or idealize her either. Her body must be TRUE. NEVER copy the body of the model "
            "who appears in the garment reference photos — those images are there ONLY to show the clothes. If her legs or "
            "hips are not visible in the reference, infer them conservatively from her visible proportions instead of "
            "inventing a fuller body. "
            # --- CAIMENTO: vestido justo tem que abraçar o corpo real, sem inventar volume ---
            "HOW THE CLOTHES SIT ON HER: a fitted or body-hugging garment must follow her real silhouette smoothly and fall "
            "naturally with gravity — the fabric skims the body. Do NOT add padding, bulk, thickness or extra volume under or "
            "around the garment; do NOT bunch, crease or wrinkle the fabric in a way that adds width at the waist, stomach or "
            "hips; do NOT stretch it as if the size were too small. It must look like the garment FITS her, in her own size. "
            "Background scene (only the setting around her — does NOT change her outfit): " + cena + ". " + pose + ". "
            # --- FOTOGRAFIA QUE VALORIZA SEM MENTIR (pose 3/4 + luz lateral + lente longa) ---
            "Photographed exactly like the boutique's own lookbook: she stands in a natural three-quarter turn — body angled "
            "about 30-45 degrees from the camera, weight on the back leg, front leg slightly crossed in front, shoulders "
            "relaxed and slightly angled, spine long, neck long, chin slightly forward and a touch down. Camera at chest "
            "height and perfectly level: NEVER shot from below, NEVER a wide-angle or selfie perspective (those distort and "
            "widen the body). 85-105mm portrait lens, no lens distortion. Directional key light from about 45 degrees to one "
            "side, sculpting a soft shadow down the far side of her body, plus a subtle rim light separating her from the "
            "background — the light must DEFINE her waistline honestly instead of flattening and widening her; avoid flat "
            "frontal lighting. Full-length vertical framing with the entire body from head to shoes in frame, shoes visible, "
            "generous headroom. Refined natural color grade with rich elegant tones, shallow depth of field, tack-sharp "
            "focus, natural photorealistic skin texture, magazine-quality finish. Every bit of the flattery must come ONLY "
            "from the pose, the lighting, the lens and the scene — NEVER from changing her body or her clothes. "
            "No text, no logos, no hanger.")

def to_uri(v):
    """data-uri ou http(s) passa direto; caminho local vira data-uri."""
    if not v: return v
    if v.startswith("/peca/"):
        sku = v[len("/peca/"):]
        if sku.endswith(".jpg"): sku = sku[:-4]
        return peca_img(sku) or v
    if v.startswith("data:") or v.startswith("http"): return v
    p = os.path.join(ROOT, v.replace("/", os.sep))
    if os.path.exists(p):
        ext = os.path.splitext(p)[1].lower().lstrip(".") or "jpeg"
        if ext == "jpg": ext = "jpeg"
        with open(p, "rb") as f:
            return "data:image/%s;base64,%s" % (ext, base64.b64encode(f.read()).decode())
    return v

def fal_generate(prompt, image_uris):
    body = json.dumps({"prompt": prompt, "image_urls": image_uris, "num_images": 1}).encode()
    req = urllib.request.Request("https://fal.run/" + FAL_MODEL, data=body,
        headers={"Authorization": "Key " + FAL_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode())
    imgs = data.get("images") or data.get("image") or []
    if isinstance(imgs, dict): imgs = [imgs]
    if imgs and isinstance(imgs[0], dict): return imgs[0].get("url")
    return data.get("url")

def fal_faceswap(look_url, face_uri):
    """Cola o rosto REAL (face_uri) sobre o look gerado (look_url). Garante a identidade."""
    body = json.dumps({"base_image_url": look_url, "swap_image_url": face_uri}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/face-swap", data=body,
        headers={"Authorization": "Key " + FAL_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    img = d.get("image")
    if isinstance(img, dict): return img.get("url")
    imgs = d.get("images")
    if isinstance(imgs, list) and imgs and isinstance(imgs[0], dict): return imgs[0].get("url")
    return d.get("url")

# ---- Geração do look (usada pelo /generate síncrono E pela fila /gerar) ----
def gerar_look_img(body):
    """Gera o look na nuvem (fal) + faceswap. Retorna (url, erro)."""
    if not FAL_KEY:
        return None, "Sem FAL_KEY no servidor."
    garments = body.get("garments")
    if not garments:
        g = body.get("garment", "")
        garments = [g] if g else []
    prompt = build_prompt(body.get("ocasiao", "Dia a dia"), body.get("estilo", ""), body.get("pecas", body.get("peca", "")), body.get("fundo", "cena"))
    if body.get("prompt_override"):
        prompt = body.get("prompt_override")
    uris = [to_uri(body.get("person", ""))] + [to_uri(g) for g in garments if g]
    url = fal_generate(prompt, uris)
    if not url:
        return None, "a nuvem nao devolveu imagem"
    if body.get("faceswap"):
        face = to_uri(body.get("person", ""))
        if body.get("reforco"):
            for _try in range(3):
                try:
                    _sw = fal_faceswap(url, face)
                    if _sw:
                        url = _sw; break
                except Exception:
                    pass
        else:
            try:
                _sw = fal_faceswap(url, face)
                if _sw: url = _sw
            except Exception:
                pass
    try:
        log_uso({"vend": body.get("vend", ""), "cliente": body.get("cliente", ""),
                 "pecas": body.get("pecas", ""), "ocasiao": body.get("ocasiao", ""),
                 "fundo": body.get("fundo", "cena"),
                 "ts": datetime.datetime.now().isoformat(timespec="seconds")})
    except Exception:
        pass
    return url, None

# ---- Fila de geração (roda no fundo, sobrevive a fechar/trocar de app) ----
_GEN_SEM = threading.Semaphore(8)   # no máximo 8 gerações simultâneas no servidor (protege a nuvem)
def _fila_worker(job_id, body):
    with _GEN_SEM:
        try:
            url, err = gerar_look_img(body)
        except Exception as e:
            url, err = None, str(e)
    try:
        if url:
            sb_req("PATCH", "fila_looks", "id=eq." + urllib.parse.quote(job_id), body={"status": "pronto", "image": url})
        else:
            sb_req("PATCH", "fila_looks", "id=eq." + urllib.parse.quote(job_id), body={"status": "erro", "erro": (err or "falhou")[:280]})
    except Exception:
        pass

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
    def end_headers(self):
        pth = self.path.split("?")[0]
        seg = pth.rsplit("/", 1)[-1]
        if pth.endswith(".html") or pth.endswith("/") or "." not in seg:
            self.send_header("Cache-Control", "no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()
    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_GET(self):
        p = self.path.split("?")[0]
        if p.startswith("/peca/"):
            sku = p[len("/peca/"):]
            if sku.endswith(".jpg"): sku = sku[:-4]
            uri = peca_img(sku)
            if not uri or "base64," not in uri:
                self.send_response(404); self.end_headers(); return
            try:
                head, b64 = uri.split("base64,", 1)
                raw = base64.b64decode(b64)
            except Exception:
                self.send_response(404); self.end_headers(); return
            ctype = "image/jpeg"
            if head.startswith("data:") and ";" in head:
                ctype = head[5:].split(";", 1)[0] or "image/jpeg"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
            self.end_headers()
            self.wfile.write(raw)
            return
        if p == "/clube":
            return self._json(200, {"posts": load_clube()})
        if p == "/uso":
            return self._json(200, {"log": load_uso()})
        if p == "/pecas":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            return self._json(200, {"pecas": load_pecas((q.get("vend") or [""])[0])})
        if p == "/reserva":
            return self._json(200, {"reservas": load_reservas()})
        if p == "/look":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            lid = (q.get("id") or [""])[0]
            ids = (q.get("ids") or [""])[0]
            if ids:
                wanted = [x for x in ids.split(",") if x][:300]
                out = {}
                if SB_ON and wanted:
                    try:
                        rows = sb_req("GET", "looks", "id=in.(" + ",".join(wanted) + ")&select=id,reacao") or []
                        for r in rows:
                            out[r["id"]] = r.get("reacao") or ""
                    except Exception:
                        pass
                else:
                    looks = load_looks()
                    for w in wanted:
                        if w in looks:
                            out[w] = looks[w].get("reacao") or ""
                return self._json(200, {"reacoes": out})
            looks = load_looks()
            if lid:
                return self._json(200, looks.get(lid) or {"error": "not_found"})
            return self._json(200, {"looks": looks})
        if p == "/claim":
            return self._json(200, {"claims": load_claims()})
        if p == "/sbstatus":
            out = {"sb_on": SB_ON}
            if SB_ON:
                try:
                    out["amostra"] = sb_req("GET", "claims", "select=vend&limit=1")
                    out["ok"] = True
                except Exception as e:
                    out["ok"] = False
                    out["error"] = str(e)
            return self._json(200, out)
        if p == "/version":
            return self._json(200, {"version": "2026-07-14_corpo-fiel", "ok": True})
        if p == "/placar":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            periodo = (q.get("periodo") or ["mes"])[0]
            vend = (q.get("vend") or [""])[0]
            try:
                rows = build_placar(periodo)
            except Exception as e:
                return self._json(200, {"periodo": periodo, "placar": [], "error": str(e)})
            if vend:
                mine = next((r for r in rows if r["vend"] == vend), {"vend": vend, "fichas": 0, "gerados": 0, "atendidas": 0, "enviados": 0, "respostas": 0, "reservas": 0, "reativadas": 0})
                pos = next((i + 1 for i, r in enumerate(rows) if r["vend"] == vend), None)
                return self._json(200, {"periodo": periodo, "eu": mine, "posicao": pos, "total": len(rows)})
            return self._json(200, {"periodo": periodo, "placar": rows})
        if p == "/meta":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            mes = (q.get("mes") or [_mes_atual()])[0]
            return self._json(200, {"mes": mes, "meta": load_meta(mes)})
        if p == "/ficha":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            vend = (q.get("vend") or [""])[0]
            out = []
            if SB_ON:
                try:
                    params = "select=vend,cliente,foto,manequim,sapato,telefone,aniversario,notas,ocasioes,estilo,cores,arquetipo,vip,ult_compra,status&order=cliente.asc"
                    if vend:
                        params = "vend=eq." + urllib.parse.quote(vend) + "&" + params
                    out = sb_req("GET", "fichas", params) or []
                except Exception as e:
                    return self._json(200, {"fichas": [], "error": str(e)})
            return self._json(200, {"fichas": out})
        if p == "/fila":
            q = urllib.parse.parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            vend = (q.get("vend") or [""])[0]
            out = []
            if SB_ON and vend:
                # varre 'gerando' velho (>4min) e marca erro (caso o servidor tenha reiniciado no meio)
                try:
                    cutoff = (datetime.datetime.now() - datetime.timedelta(minutes=4)).isoformat(timespec="seconds")
                    sb_req("PATCH", "fila_looks", "vend=eq." + urllib.parse.quote(vend) + "&status=eq.gerando&criado=lt." + urllib.parse.quote(cutoff), body={"status": "erro", "erro": "timeout"})
                except Exception:
                    pass
                try:
                    out = sb_req("GET", "fila_looks", "vend=eq." + urllib.parse.quote(vend) + "&select=id,vend,cliente,person_key,pecas,occ,status,image,erro&order=criado.asc") or []
                except Exception as e:
                    return self._json(200, {"fila": [], "error": str(e)})
            return self._json(200, {"fila": out})
        return super().do_GET()
    def do_POST(self):
        p = self.path.split("?")[0]
        if p == "/clube":
            try:
                n = int(self.headers.get("Content-Length", 0))
                post = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                if SB_ON:
                    try:
                        sb_req("POST", "clube", body={"img": post.get("img"), "marca": post.get("marca"),
                            "descricao": post.get("desc"), "de": post.get("de"), "por": post.get("por"),
                            "cond": post.get("cond"), "occ": post.get("occ"), "pecas": post.get("pecas"),
                            "nome": post.get("nome"), "vend": post.get("vend"),
                            "ts": datetime.datetime.now().isoformat(timespec="seconds")})
                        return self._json(200, {"ok": True})
                    except Exception:
                        pass
                posts = load_clube(); posts.append(post); save_clube(posts)
                return self._json(200, {"ok": True, "count": len(posts)})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/reserva":
            try:
                n = int(self.headers.get("Content-Length", 0))
                r = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                r["ts"] = datetime.datetime.now().isoformat(timespec="seconds")
                add_reserva(r)
                return self._json(200, {"ok": True, "count": len(load_reservas())})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/look":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                lid = uuid.uuid4().hex[:10]
                ts = datetime.datetime.now().isoformat(timespec="seconds")
                if SB_ON:
                    try:
                        sb_req("POST", "looks", body={"id": lid, "img": d.get("img"), "cliente": d.get("cliente"),
                            "vend": d.get("vend"), "pecas": d.get("pecas"), "occ": d.get("occ"), "ts": ts, "reacao": ""})
                        return self._json(200, {"id": lid})
                    except Exception:
                        pass
                looks = load_looks()
                d["ts"] = ts
                d["reacao"] = ""
                looks[lid] = d
                if len(looks) > 4000:
                    for k in list(looks.keys())[:len(looks) - 4000]:
                        looks.pop(k, None)
                save_looks(looks)
                return self._json(200, {"id": lid})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/reacao":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                lid = d.get("id", "")
                if SB_ON and lid:
                    try:
                        sb_req("PATCH", "looks", "id=eq." + lid, body={"reacao": d.get("reacao", ""),
                            "reacao_ts": datetime.datetime.now().isoformat(timespec="seconds")})
                        return self._json(200, {"ok": True})
                    except Exception:
                        pass
                looks = load_looks()
                if lid in looks:
                    looks[lid]["reacao"] = d.get("reacao", "")
                    looks[lid]["reacao_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
                    save_looks(looks)
                return self._json(200, {"ok": True})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/claim":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                vend = (d.get("vend") or "").strip(); dev = (d.get("device") or "").strip()
                if not vend or not dev:
                    return self._json(200, {"ok": False})
                now = datetime.datetime.now().isoformat(timespec="seconds")
                if SB_ON:
                    try:
                        rows = sb_req("GET", "claims", "vend=eq." + urllib.parse.quote(vend) + "&select=*") or []
                        cur = rows[0] if rows else None
                        if not cur or cur.get("device") == dev:
                            sb_req("POST", "claims", body={"vend": vend, "device": dev, "ts": now}, prefer="resolution=merge-duplicates")
                            return self._json(200, {"ok": True})
                        return self._json(200, {"ok": False, "locked": True})
                    except Exception:
                        pass
                claims = load_claims(); cur = claims.get(vend)
                if not cur or cur.get("device") == dev:
                    claims[vend] = {"device": dev, "ts": now}
                    save_claims(claims)
                    return self._json(200, {"ok": True})
                return self._json(200, {"ok": False, "locked": True})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/claim/reset":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                vend = (d.get("vend") or "").strip()
                if SB_ON:
                    try:
                        sb_req("DELETE", "claims", "vend=eq." + urllib.parse.quote(vend))
                        return self._json(200, {"ok": True})
                    except Exception:
                        pass
                claims = load_claims(); claims.pop(vend, None); save_claims(claims)
                return self._json(200, {"ok": True})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/pecas":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                if d.get("del"):
                    _PECA_IMG.pop(str(d.get("del")), None)
                    if SB_ON:
                        try:
                            sb_req("DELETE", "pecas", "sku=eq." + urllib.parse.quote(str(d.get("del"))))
                        except Exception:
                            pass
                    return self._json(200, {"ok": True})
                if not d.get("img") or not d.get("sku"):
                    return self._json(200, {"ok": False, "skip": "sem img/sku"})
                row = {"sku": d.get("sku"), "img": d.get("img"), "cat": d.get("cat"),
                       "nome": d.get("nome"), "tam": json.dumps(d.get("tam")) if d.get("tam") is not None else None,
                       "preco": d.get("preco"), "vend": d.get("vend")}
                if not SB_ON:
                    return self._json(200, {"ok": False, "sb": False})
                try:
                    sb_req("POST", "pecas", body=row)
                    _PECA_IMG[str(d.get("sku"))] = d.get("img")
                    return self._json(200, {"ok": True, "sku": d.get("sku")})
                except Exception as e:
                    return self._json(200, {"ok": False, "error": str(e)})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/meta":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                mes = (d.get("mes") or _mes_atual())
                return self._json(200, {"ok": True, "meta": save_meta(mes, d)})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/ficha":
            try:
                n = int(self.headers.get("Content-Length", 0))
                d = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                vend = (d.get("vend") or "").strip()
                cliente = (d.get("cliente") or "").strip()
                if not cliente:
                    return self._json(200, {"ok": False, "skip": "sem nome"})
                row = {"vend": vend, "cliente": cliente, "ts": datetime.datetime.now().isoformat(timespec="seconds")}
                for _k in ("foto", "manequim", "sapato", "telefone", "aniversario", "notas", "ocasioes", "estilo", "cores", "arquetipo", "vip", "ult_compra", "status"):
                    if _k in d:
                        row[_k] = d.get(_k)
                if not SB_ON:
                    return self._json(200, {"ok": False, "sb": False})
                try:
                    ex = sb_req("GET", "fichas", "vend=eq." + urllib.parse.quote(vend) + "&cliente=eq." + urllib.parse.quote(cliente) + "&select=id")
                    if ex:
                        sb_req("PATCH", "fichas", "id=eq." + str(ex[0]["id"]), body=row)
                    else:
                        sb_req("POST", "fichas", body=row)
                    return self._json(200, {"ok": True})
                except Exception as e:
                    return self._json(200, {"ok": False, "error": str(e)})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/gerar":
            # geração ASSÍNCRONA: aceita na hora, renderiza no fundo, guarda o resultado no banco.
            try:
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                vend = (body.get("vend") or "").strip()
                pecas = body.get("pecas")
                pecas_txt = ", ".join(pecas) if isinstance(pecas, list) else str(pecas or "")
                if not SB_ON:
                    # sem banco -> gera na hora (fallback, comportamento antigo)
                    url, err = gerar_look_img(body)
                    if url:
                        return self._json(200, {"ok": True, "image": url, "async": False})
                    return self._json(502, {"ok": False, "error": err or "falhou"})
                # trava anti-abuso: no máximo 12 pendentes por vendedora
                try:
                    pend = sb_req("GET", "fila_looks", "vend=eq." + urllib.parse.quote(vend) + "&status=eq.gerando&select=id") or []
                    if len(pend) >= 12:
                        return self._json(200, {"ok": False, "full": True})
                except Exception:
                    pass
                job_id = "L" + uuid.uuid4().hex[:16]
                row = {"id": job_id, "vend": vend, "cliente": body.get("cliente", ""),
                       "person_key": body.get("person_key", ""), "pecas": pecas_txt,
                       "occ": body.get("ocasiao", ""), "status": "gerando",
                       "criado": datetime.datetime.now().isoformat(timespec="seconds")}
                try:
                    sb_req("POST", "fila_looks", body=row)
                except Exception as e:
                    return self._json(200, {"ok": False, "error": str(e)})
                threading.Thread(target=_fila_worker, args=(job_id, body), daemon=True).start()
                return self._json(200, {"ok": True, "id": job_id, "async": True})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p == "/fila/limpar":
            try:
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                ids = body.get("ids") or ([body.get("id")] if body.get("id") else [])
                ids = [str(i) for i in ids if i and str(i).replace("_", "").isalnum()]
                if SB_ON and ids:
                    try:
                        sb_req("DELETE", "fila_looks", "id=in.(" + ",".join(ids) + ")")
                    except Exception:
                        pass
                return self._json(200, {"ok": True})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p != "/generate":
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
            url, err = gerar_look_img(body)
            if url:
                return self._json(200, {"image": url})
            return self._json(502, {"error": err or "falhou"})
        except urllib.error.HTTPError as e:
            self._json(502, {"error": "nuvem HTTP %s: %s" % (e.code, e.read().decode()[:300])})
        except Exception as e:
            self._json(500, {"error": str(e)})

def _local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close(); return ip
    except Exception:
        return "SEU-IP-LOCAL"

if __name__ == "__main__":
    ip = _local_ip()
    print("=" * 60)
    print(" DESEJO GUIADO - servidor")
    print("")
    print(" >> No CELULAR (mesma Wi-Fi):")
    print("    http://%s:%d/estudio/celular.html" % (ip, PORT))
    print("")
    print(" >> Na TV/PC:  http://localhost:%d/estudio/estudio.html" % PORT)
    print(" >> Motor nuvem (fal.ai):", "LIGADO" if FAL_KEY else "FALTA A CHAVE (fal_key.txt)")
    print("")
    print(" Deixe esta janela ABERTA. Pra parar: Ctrl+C.")
    print("=" * 60)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

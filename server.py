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
import os, sys, json, base64, random, socket, datetime, urllib.request, urllib.error
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

# ---- Registro de uso por vendedora (painel do admin) ----
USO_FILE = os.path.join(ROOT, "uso_log.json")
def load_uso():
    try:
        with open(USO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
def log_uso(entry):
    try:
        log = load_uso(); log.append(entry); log = log[-3000:]
        with open(USO_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False)
    except Exception:
        pass

# ---- POOL de cenas por ocasiao (5 cada; rotaciona automatico -> anti-carimbo) ----
POOLS = {
 "Dia a dia": [
   "a sunlit upscale tree-lined street at golden hour, warm backlight, creamy bokeh",
   "a chic sidewalk cafe terrace in the morning, soft natural daylight",
   "a lush botanical garden path, dappled sunlight through the leaves",
   "a bright airy minimalist loft with tall windows, soft daylight",
   "a charming cobblestone old-town street, warm late-afternoon light"],
 "Casual": [
   "a charming city street at golden hour, relaxed elegant vibe",
   "a cozy bookstore-cafe with warm window light",
   "a breezy seaside promenade, airy bright light",
   "a rooftop terrace with green plants and soft sunlight",
   "a sunny park lawn lined with trees, gentle daylight"],
 "Trabalho": [
   "a sophisticated minimalist architectural lobby, clean daylight",
   "a chic urban sidewalk beside glass buildings, bright directional light",
   "a modern design office with warm wood and glass, soft light",
   "an elegant hotel lobby with marble and brass accents, refined light",
   "a bright contemporary co-working space with large windows, crisp daylight"],
 "Festa": [
   "a lively party with warm golden bokeh lights",
   "an elegant venue with crystal chandelier bokeh",
   "a night-time rooftop terrace with warm string lights and a city skyline",
   "a glamorous ballroom with soft golden lighting",
   "an upscale garden party at dusk with delicate fairy lights"],
 "Praia": [
   "a luminous beach with turquoise sea and white sand, bright airy light",
   "a stylish resort pool deck, sunny with soft palm shadows",
   "a wooden beach boardwalk at golden hour",
   "a tropical seaside terrace overlooking the ocean",
   "a sandy dune with sea grass, soft warm afternoon light"],
 "Academia": [
   "a bright modern fitness studio, crisp even daylight",
   "a clean pilates studio with large windows, soft light",
   "a minimalist yoga studio with wood floor and plants, calm light",
   "an outdoor park workout spot at sunrise, fresh light",
   "a sleek gym with natural light and mirrors, clean modern look"],
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
 "Festa": "elegant evening glam makeup with defined eyes and luminous skin, and beautifully styled evening hair",
 "Trabalho": "polished natural makeup and a neat, sophisticated hairstyle",
 "Dia a dia": "fresh natural everyday makeup and soft, natural hair",
 "Casual": "light fresh makeup and relaxed natural hair",
 "Praia": "sun-kissed glowing skin with minimal beachy makeup and natural beach waves",
 "Academia": "a fresh, dewy clean look and a sporty sleek ponytail",
}
def build_prompt(ocasiao, estilo, pecas="", fundo="cena"):
    pose = {"Clássico":"poised graceful posture","Romântico":"soft delicate pose","Sensual":"confident tasteful pose",
            "Minimalista":"calm refined stance","Dramático":"strong editorial pose","Esportivo":"dynamic confident posture"}.get(estilo, "confident elegant pose")
    beauty = BEAUTY.get(ocasiao, "polished natural makeup and styled hair")
    if isinstance(pecas, (list, tuple)):
        nomes = [str(x) for x in pecas if x]
        peca = (" The complete look includes: " + ", ".join(nomes) + ".") if nomes else ""
    else:
        peca = (" The garment is a " + pecas + ".") if pecas else ""
    if fundo == "estudio":
        cena = ("in a professional photography studio against a seamless infinite light-grey backdrop, "
                "clean even softbox studio lighting, no props and no scenery")
    else:
        cena = pick_cena(ocasiao)
    return ("Editorial fashion photograph for a luxury boutique. Use the FIRST reference image as the EXACT same person "
            "— her FACE must be IDENTICAL to the reference (same facial features, bone structure, eyes, nose, mouth, "
            "smile and expression), same hair, skin tone and age; she must be instantly recognizable. Do NOT beautify, "
            "rejuvenate, slim or alter her face or body; preserve her REAL body shape and proportions. "
            "Dress her in a COMPLETE, cohesive outfit assembled from ALL the OTHER reference images (every image after "
            "the first): include EVERY piece shown — top, bottom or dress, footwear and accessories — reproducing each "
            "faithfully (color, cut, fabric, details) and styling them into one harmonious look. Take ONLY the garments; "
            "remove any hanger, clips and background." + peca +
            " Hair and makeup: " + beauty + " — keep this styling regardless of the background. "
            "Scene: " + cena + ". " + pose + ". "
            "Full-length fashion editorial, 85mm lens, shallow depth of field, refined color grade, magazine-cover quality, "
            "aspirational and elegant, tack-sharp focus, photorealistic, entire body head to feet in frame, beautifully "
            "exposed. No text, no logos, no hanger.")

def to_uri(v):
    """data-uri ou http(s) passa direto; caminho local vira data-uri."""
    if not v: return v
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

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
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
        if p == "/clube":
            return self._json(200, {"posts": load_clube()})
        if p == "/uso":
            return self._json(200, {"log": load_uso()})
        return super().do_GET()
    def do_POST(self):
        p = self.path.split("?")[0]
        if p == "/clube":
            try:
                n = int(self.headers.get("Content-Length", 0))
                post = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
                posts = load_clube(); posts.append(post); save_clube(posts)
                return self._json(200, {"ok": True, "count": len(posts)})
            except Exception as e:
                return self._json(500, {"error": str(e)})
        if p != "/generate":
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads((self.rfile.read(n) or b"{}").decode("utf-8", "replace"))
            if not FAL_KEY:
                return self._json(400, {"error": "Sem FAL_KEY no servidor. Configure a chave (SETUP) ou use o modo concierge."})
            garments = body.get("garments")
            if not garments:
                g = body.get("garment", "")
                garments = [g] if g else []
            prompt = build_prompt(body.get("ocasiao", "Dia a dia"), body.get("estilo", ""), body.get("pecas", body.get("peca", "")), body.get("fundo", "cena"))
            uris = [to_uri(body.get("person", ""))] + [to_uri(g) for g in garments if g]
            url = fal_generate(prompt, uris)
            if not url: return self._json(502, {"error": "a nuvem nao devolveu imagem"})
            try:
                log_uso({"vend": body.get("vend", ""), "cliente": body.get("cliente", ""),
                         "pecas": body.get("pecas", ""), "ocasiao": body.get("ocasiao", ""),
                         "fundo": body.get("fundo", "cena"),
                         "ts": datetime.datetime.now().isoformat(timespec="seconds")})
            except Exception:
                pass
            self._json(200, {"image": url, "prompt": prompt})
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

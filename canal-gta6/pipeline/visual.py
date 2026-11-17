# -*- coding: utf-8 -*-
"""Gráficos animados originales (estética neón/atardecer) con PIL + numpy."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FPS = 30

F = "/usr/share/fonts/opentype/inter/"
FONT_BLACK = F + "InterDisplay-Black.otf"
FONT_BLACKI = F + "InterDisplay-BlackItalic.otf"
FONT_XB = F + "InterDisplay-ExtraBold.otf"
FONT_SB = F + "Inter-SemiBold.otf"
FONT_MED = F + "Inter-Medium.otf"
FONT_MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"

ROSA = (255, 46, 136)
CIAN = (25, 227, 255)
NARANJA = (255, 170, 60)
AMARILLO = (255, 222, 89)
VERDE = (60, 230, 140)
ROJO = (255, 70, 90)
BLANCO = (255, 255, 255)
GRIS = (200, 190, 220)

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3

def ease_back(x):
    x = min(1.0, max(0.0, x))
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ------------------------------------------------------------------ fondo
def _palmera(d, x, base_y, alto, escala, color):
    # tronco curvo
    pts = []
    curva = random.uniform(-0.25, 0.25) * alto
    for i in range(21):
        t = i / 20
        px = x + curva * math.sin(t * math.pi / 2)
        py = base_y - alto * t
        w = (14 - 8 * t) * escala
        pts.append((px, py, w))
    izq = [(p[0] - p[2], p[1]) for p in pts]
    der = [(p[0] + p[2], p[1]) for p in reversed(pts)]
    d.polygon(izq + der, fill=color)
    cx, cy = pts[-1][0], pts[-1][1]
    # hojas
    for k in range(9):
        ang = math.radians(-180 + k * 22.5 + random.uniform(-8, 8))
        L = random.uniform(130, 190) * escala
        caida = random.uniform(0.35, 0.6)
        hoja_a, hoja_b = [], []
        for i in range(16):
            t = i / 15
            hx = cx + math.cos(ang) * L * t
            hy = cy + math.sin(ang) * L * t + (L * caida) * t * t
            ancho = 16 * escala * math.sin(t * math.pi) + 1
            nx, ny = -math.sin(ang), math.cos(ang)
            hoja_a.append((hx + nx * ancho, hy + ny * ancho))
            hoja_b.append((hx - nx * ancho * 0.3, hy - ny * ancho * 0.3))
        d.polygon(hoja_a + list(reversed(hoja_b)), fill=color)
    d.ellipse([cx - 10 * escala, cy - 8 * escala, cx + 10 * escala, cy + 10 * escala], fill=color)

class Fondo:
    """Cielo + sol a rayas + skyline + palmeras + rejilla animada."""
    def __init__(self, semilla=1, tono=0):
        random.seed(semilla)
        self.horizonte = int(H * 0.62)
        MW = W + 200
        self.MW = MW
        y = np.linspace(0, 1, H)[:, None]
        paletas = [
            [(18, 6, 46), (88, 20, 110), (230, 60, 120), (255, 150, 90)],
            [(6, 10, 40), (40, 20, 110), (180, 40, 150), (255, 120, 110)],
            [(10, 4, 30), (70, 10, 90), (210, 50, 90), (255, 170, 80)],
        ]
        pal = np.array(paletas[tono % 3], np.float32)
        stops = np.array([0, 0.35, 0.52, 0.62])
        cielo = np.zeros((H, MW, 3), np.float32)
        yy = y[:, 0]
        for c in range(3):
            cielo[:, :, c] = np.interp(yy, stops, pal[:, c])[:, None]
        img = Image.fromarray(cielo.clip(0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img, "RGBA")
        # estrellas
        for _ in range(260):
            sx, sy = random.randint(0, MW), random.randint(0, int(H * 0.4))
            a = random.randint(60, 200)
            r = random.choice([1, 1, 1, 2])
            d.ellipse([sx, sy, sx + r, sy + r], fill=(255, 255, 255, a))
        # sol con degradado y rayas
        sol = Image.new("RGBA", (560, 560))
        sa = np.zeros((560, 560, 4), np.uint8)
        yy2, xx2 = np.mgrid[0:560, 0:560]
        dist = np.hypot(xx2 - 280, yy2 - 280)
        dentro = dist < 270
        tt = yy2 / 560
        sa[..., 0] = 255
        sa[..., 1] = (230 - 170 * tt).astype(np.uint8)
        sa[..., 2] = (90 + 60 * tt).astype(np.uint8)
        sa[..., 3] = np.where(dentro, 255, 0)
        for i in range(9):
            y0 = int(300 + i * 30)
            gap = 4 + i * 2
            sa[y0:y0 + gap, :, 3] = 0
        sol = Image.fromarray(sa)
        glow = Image.new("RGBA", (MW, H))
        gd = ImageDraw.Draw(glow)
        sx = MW // 2 - 280
        sy = self.horizonte - 430
        gd.ellipse([sx - 80, sy - 80, sx + 640, sy + 640], fill=(255, 90, 140, 120))
        glow = glow.filter(ImageFilter.GaussianBlur(90))
        img = Image.alpha_composite(img.convert("RGBA"), glow)
        img.alpha_composite(sol, (sx, sy))
        # skyline
        sky = Image.new("RGBA", (MW, H))
        sd = ImageDraw.Draw(sky)
        x = 0
        while x < MW:
            w = random.randint(40, 110)
            h = random.randint(60, 300) if abs(x - MW / 2) > 300 else random.randint(40, 140)
            sd.rectangle([x, self.horizonte - h, x + w, self.horizonte], fill=(30, 8, 50, 255))
            # ventanas
            for wy in range(self.horizonte - h + 10, self.horizonte - 6, 14):
                for wx in range(x + 6, x + w - 6, 12):
                    if random.random() < 0.18:
                        sd.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 200, 120, random.randint(90, 200)))
            x += w + random.randint(0, 14)
        img.alpha_composite(sky)
        self.cielo = img.convert("RGB")
        # suelo
        suelo = np.zeros((H - self.horizonte, MW, 3), np.float32)
        g = np.linspace(0, 1, H - self.horizonte)[:, None]
        suelo[..., 0] = (40 - 30 * g)
        suelo[..., 1] = (6 + 0 * g)
        suelo[..., 2] = (60 - 30 * g)
        self.suelo = suelo.astype(np.uint8)
        # palmeras (capa delantera)
        pal = Image.new("RGBA", (MW, H))
        pd = ImageDraw.Draw(pal)
        for (px, alto, esc) in [(90, 640, 1.5), (260, 520, 1.2), (MW - 140, 680, 1.6), (MW - 330, 480, 1.1)]:
            _palmera(pd, px, H + 20, alto, esc, (12, 2, 22, 255))
        self.palmeras = pal
        # viñeta + scanlines
        vy, vx = np.mgrid[0:H, 0:W]
        v = 1 - 0.55 * (((vx - W / 2) / (W / 2)) ** 2 + ((vy - H / 2) / (H / 2)) ** 2) ** 1.4
        v = v.clip(0.35, 1)
        scan = np.where(vy % 4 == 0, 0.93, 1.0)
        self.mult = (v * scan).astype(np.float32)[..., None]

    def frame(self, t):
        ox = int(100 + 70 * math.sin(t * 0.07))
        base = np.asarray(self.cielo)[:, ox:ox + W].copy()
        # rejilla en perspectiva
        hz = self.horizonte
        suelo = self.suelo[:, ox:ox + W].copy()
        img = Image.fromarray(base)
        img.paste(Image.fromarray(suelo), (0, hz))
        d = ImageDraw.Draw(img, "RGBA")
        cx = W / 2 - (ox - 100) * 0.3
        for i in range(-24, 25):
            x_bottom = cx + i * 170
            d.line([(cx + i * 6, hz), (x_bottom, H)], fill=(255, 60, 200, 150), width=2)
        off = (t * 0.6) % 1.0
        for k in range(14):
            z = (k + 1 - off)
            yline = hz + (H - hz) * (1 / max(0.3, 14 - z)) * 1.0
            yline = hz + (H - hz) * ((z / 14) ** 2.2)
            a = int(60 + 160 * (z / 14))
            d.line([(0, yline), (W, yline)], fill=(255, 60, 200, a), width=2)
        d.line([(0, hz), (W, hz)], fill=(255, 150, 220, 220), width=3)
        # palmeras con paralaje
        px = int(100 + 110 * math.sin(t * 0.07))
        img.paste(self.palmeras.crop((px, 0, px + W, H)), (0, 0), self.palmeras.crop((px, 0, px + W, H)))
        return img

    def post(self, img):
        a = np.asarray(img, np.float32) * self.mult
        return a.clip(0, 255).astype(np.uint8)

# ------------------------------------------------------------------ texto
def texto_glow(txt, fnt, color=BLANCO, glow=ROSA, stroke=0, stroke_color=(20, 0, 40), radio=14, espaciado=0):
    lineas = txt.split("\n")
    asc, desc = fnt.getmetrics()
    lh = asc + desc + espaciado
    ws = [fnt.getbbox(l, stroke_width=stroke)[2] for l in lineas]
    pad = radio * 3
    w = max(ws) + pad * 2
    h = lh * len(lineas) + pad * 2
    capa = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(capa)
    for i, l in enumerate(lineas):
        d.text((pad + (max(ws) - ws[i]) // 2, pad + i * lh), l, font=fnt, fill=color,
               stroke_width=stroke, stroke_fill=stroke_color)
    if glow is None:
        return capa
    g = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(g)
    for i, l in enumerate(lineas):
        gd.text((pad + (max(ws) - ws[i]) // 2, pad + i * lh), l, font=fnt, fill=glow + (255,), stroke_width=stroke + 4)
    g = g.filter(ImageFilter.GaussianBlur(radio))
    out = Image.alpha_composite(g, g)
    out = Image.alpha_composite(out, capa)
    return out

def texto_simple(txt, fnt, color=BLANCO, anchor_w=None):
    bb = fnt.getbbox(txt)
    asc, desc = fnt.getmetrics()
    capa = Image.new("RGBA", (bb[2] + 4, asc + desc + 4))
    ImageDraw.Draw(capa).text((0, 0), txt, font=fnt, fill=color)
    return capa

def panel(w, h, radio=28, color=(20, 6, 40, 200), borde=ROSA, grosor=3):
    p = Image.new("RGBA", (w + 60, h + 60))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], radio, fill=borde + (160,))
    p = p.filter(ImageFilter.GaussianBlur(16))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], radio, fill=color, outline=borde + (255,), width=grosor)
    return p

def badge(estado):
    col = {"SÍ": VERDE, "NO": ROJO, "?": AMARILLO}[estado]
    txt = {"SÍ": "SÍ", "NO": "NO", "?": "SIN CONFIRMAR"}[estado]
    f = font(FONT_BLACK, 34)
    w = f.getbbox(txt)[2] + 44
    b = Image.new("RGBA", (w, 58))
    d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, w - 1, 57], 29, fill=col + (255,))
    d.text((22, 8), txt, font=f, fill=(20, 6, 30))
    return b

# ------------------------------------------------------------------ elementos
class El:
    """Elemento animado: imagen + posición + momento de aparición."""
    def __init__(self, img, x, y, t0, anim="up", dur=0.45):
        self.img, self.x, self.y, self.t0, self.anim, self.dur = img, x, y, t0, anim, dur
        self._alpha_cache = {}

    def draw(self, canvas, t, salida):
        if t < self.t0:
            return
        p = ease((t - self.t0) / self.dur)
        a = p * salida
        if a <= 0.01:
            return
        img = self.img
        x, y = self.x, self.y
        if self.anim == "up":
            y += int((1 - p) * 60)
        elif self.anim == "left":
            x -= int((1 - p) * 120)
        elif self.anim == "pop":
            s = 0.6 + 0.4 * ease_back(min(1, (t - self.t0) / self.dur))
            if abs(s - 1) > 0.01:
                nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
                img = img.resize((nw, nh), Image.BILINEAR)
                x += (self.img.width - nw) // 2
                y += (self.img.height - nh) // 2
        if a < 0.99:
            q = round(a, 2)
            key = (q, img.size)
            if key not in self._alpha_cache or self.anim == "pop":
                al = img.getchannel("A").point(lambda v: int(v * q))
                im2 = img.copy(); im2.putalpha(al)
                if self.anim != "pop":
                    self._alpha_cache[key] = im2
                img = im2
            else:
                img = self._alpha_cache[key]
        canvas.alpha_composite(img, (int(x), int(y)))

def centrado_x(img):
    return (W - img.width) // 2

def construir_escena(esc, tl_esc, canal):
    """Devuelve la lista de elementos de una escena, con tiempos relativos al inicio."""
    t0 = tl_esc["inicio"]
    bt = [b["inicio"] - t0 for b in tl_esc["beats"]]
    lead = esc.get("lead", 1)
    def tb(i):
        return bt[min(i, len(bt) - 1)] if i < len(bt) else bt[-1]
    els = []
    tipo = esc["tipo"]

    def cabecera(txt, y=110, color=CIAN):
        im = texto_glow(txt, font(FONT_BLACKI, 70), glow=color, radio=12)
        els.append(El(im, centrado_x(im), y - 42, 0.0, "left"))

    if tipo == "title":
        k = texto_glow(esc["kicker"], font(FONT_BLACK, 44), color=(20, 6, 30), glow=None)
        kp = Image.new("RGBA", (k.width + 50, k.height + 16))
        ImageDraw.Draw(kp).rounded_rectangle([0, 0, kp.width - 1, kp.height - 1], 12, fill=CIAN + (255,))
        kp.alpha_composite(k, (25, 6))
        els.append(El(kp, centrado_x(kp), 170, 0.0, "pop"))
        ti = texto_glow(esc["title"], font(FONT_BLACKI, 168), glow=ROSA, stroke=3, radio=22, espaciado=-30)
        els.append(El(ti, centrado_x(ti), 250, 0.15, "pop", 0.6))
        su = texto_glow(esc["sub"], font(FONT_SB, 44), color=AMARILLO, glow=(80, 0, 60), radio=8)
        els.append(El(su, centrado_x(su), 250 + ti.height - 30, 0.6, "up"))
    elif tipo == "bignum":
        n = texto_glow(esc["value"], font(FONT_BLACKI, 300 if len(esc["value"]) <= 5 else 210), glow=ROSA, stroke=4, radio=26)
        u = texto_glow(esc["unit"], font(FONT_BLACK, 90), color=CIAN, glow=(0, 80, 140), radio=14) if esc["unit"] else None
        tot = n.width + (u.width - 40 if u else 0)
        x0 = (W - tot) // 2
        y0 = 190
        els.append(El(n, x0, y0, 0.1, "pop", 0.55))
        if u:
            els.append(El(u, x0 + n.width - 60, y0 + n.height - u.height - 70, 0.45, "left"))
        lab = texto_glow(esc["label"], font(FONT_SB, 54), color=BLANCO, glow=(60, 0, 80), radio=10)
        els.append(El(lab, centrado_x(lab), y0 + n.height - 20, tb(1) if len(bt) > 1 else 0.8, "up"))
    elif tipo in ("bullets", "profile"):
        cabecera(esc["heading"])
        items = esc["items"]
        n = len(items)
        size = 58 if n <= 4 else 46
        paso = 112 if n <= 4 else 92
        pw = 1400
        ph = paso * n + 60
        py = 230 + (6 - n) * 18
        pn = panel(pw, ph)
        els.append(El(pn, (W - pn.width) // 2, py - 30, 0.0, "up"))
        for i, it in enumerate(items):
            fila = Image.new("RGBA", (pw - 80, paso))
            d = ImageDraw.Draw(fila)
            d.ellipse([10, paso // 2 - 22, 54, paso // 2 + 22], fill=ROSA + (255,))
            d.text((32, paso // 2), str(i + 1) if tipo == "bullets" else "›", font=font(FONT_BLACK, 30), fill=BLANCO, anchor="mm")
            d.text((84, paso // 2), it, font=font(FONT_XB, size), fill=BLANCO, anchor="lm")
            els.append(El(fila, (W - pw) // 2 + 40, py + 30 + i * paso, tb(lead + i), "left"))
    elif tipo in ("times", "history"):
        cabecera(esc["heading"])
        rows = esc["rows"]
        n = len(rows)
        paso = 104 if n > 4 else 130
        pw, ph = 1500, paso * n + 50
        py = 220 + (6 - n) * 20
        pn = panel(pw, ph, borde=CIAN)
        els.append(El(pn, (W - pn.width) // 2, py - 30, 0.0, "up"))
        for i, (a, b) in enumerate(rows):
            fila = Image.new("RGBA", (pw - 80, paso))
            d = ImageDraw.Draw(fila)
            if i:
                d.line([(0, 2), (pw - 80, 2)], fill=(255, 255, 255, 40), width=2)
            d.text((10, paso // 2), a, font=font(FONT_XB, 54), fill=BLANCO, anchor="lm")
            d.text((pw - 100, paso // 2), b, font=font(FONT_MONO, 44), fill=AMARILLO, anchor="rm")
            els.append(El(fila, (W - pw) // 2 + 40, py + 25 + i * paso, tb(lead + i), "left"))
    elif tipo == "status":
        cabecera(esc["heading"])
        rows = esc["rows"]
        paso = 150
        pw, ph = 1560, paso * len(rows) + 40
        py = 250
        pn = panel(pw, ph, borde=CIAN)
        els.append(El(pn, (W - pn.width) // 2, py - 30, 0.0, "up"))
        for i, (lab, est, nota) in enumerate(rows):
            fila = Image.new("RGBA", (pw - 80, paso))
            d = ImageDraw.Draw(fila)
            if i:
                d.line([(0, 2), (pw - 80, 2)], fill=(255, 255, 255, 40), width=2)
            d.text((10, paso // 2 - (22 if nota else 0)), lab, font=font(FONT_XB, 54), fill=BLANCO, anchor="lm")
            if nota:
                d.text((12, paso // 2 + 36), nota, font=font(FONT_MED, 34), fill=GRIS, anchor="lm")
            bd = badge(est)
            fila.alpha_composite(bd, (pw - 100 - bd.width, paso // 2 - 29))
            els.append(El(fila, (W - pw) // 2 + 40, py + 20 + i * paso, tb(lead + i), "left"))
    elif tipo == "compare":
        cabecera(esc["heading"])
        cw, ch = 760, 620
        for j, col in enumerate(esc["cols"]):
            borde = CIAN if j == 0 else ROSA
            card = panel(cw, ch, borde=borde)
            d = ImageDraw.Draw(card)
            d.text((30 + cw // 2, 120), col["name"], font=font(FONT_BLACKI, 76), fill=borde, anchor="mm")
            d.text((30 + cw // 2, 250), col["price"], font=font(FONT_BLACK, 120), fill=BLANCO, anchor="mm")
            for k, it in enumerate(col["items"]):
                d.text((90, 380 + k * 90), "• " + it, font=font(FONT_SB, 44), fill=BLANCO, anchor="lm")
            x = W // 2 - cw - 50 + j * (cw + 100) - 30
            els.append(El(card, x, 210, tb(lead + j), "up"))
    elif tipo in ("warn", "verdict"):
        cabecera(esc["heading"], color=AMARILLO if tipo == "warn" else VERDE)
        col = AMARILLO if tipo == "warn" else VERDE
        fs = 76
        txt = texto_glow(esc["text"], font(FONT_BLACK, fs), glow=None, espaciado=10)
        while txt.width > 1640 and fs > 40:
            fs -= 4
            txt = texto_glow(esc["text"], font(FONT_BLACK, fs), glow=None, espaciado=10)
        pw, ph = min(1720, max(1300, txt.width + 120)), txt.height + 160
        pn = panel(pw, ph, borde=col)
        d = ImageDraw.Draw(pn)
        icon = "!" if tipo == "warn" else "✓"
        pn.alpha_composite(txt, (30 + (pw - txt.width) // 2, 30 + 100))
        circ = Image.new("RGBA", (130, 130))
        cd = ImageDraw.Draw(circ)
        cd.ellipse([0, 0, 129, 129], fill=col + (255,))
        cd.text((65, 62), icon, font=font(FONT_BLACK if icon == "!" else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90), fill=(20, 6, 30), anchor="mm")
        els.append(El(pn, (W - pn.width) // 2, 290, 0.1, "up"))
        els.append(El(circ, (W - 130) // 2, 240, 0.3, "pop"))
    elif tipo == "regions":
        cabecera(esc["heading"])
        regs = esc["regions"]
        tw, th = 560, 290
        cols = [CIAN, ROSA, VERDE, NARANJA, AMARILLO, (180, 120, 255)]
        for i, (nom, desc) in enumerate(regs):
            c = cols[i % len(cols)]
            tile = panel(tw, th, borde=c)
            d = ImageDraw.Draw(tile)
            d.text((60, 90), f"0{i+1}", font=font(FONT_MONO, 44), fill=c)
            d.text((60, 150), nom, font=font(FONT_BLACKI, 58 if len(nom) < 12 else 50), fill=BLANCO)
            d.text((60, 235), desc, font=font(FONT_MED, 32), fill=GRIS)
            x = (W - 3 * tw - 2 * 40) // 2 + (i % 3) * (tw + 40) - 30
            y = 200 + (i // 3) * (th + 40)
            els.append(El(tile, x, y, tb(lead + i), "pop"))
        nota = texto_glow("Esquema orientativo · no es el mapa oficial", font(FONT_SB, 32), color=GRIS, glow=None)
        els.append(El(nota, centrado_x(nota), 900, 0.3, "up"))
    elif tipo == "cta":
        h1 = texto_glow(esc["heading"], font(FONT_BLACKI, 110), glow=ROSA, stroke=2, radio=20)
        els.append(El(h1, centrado_x(h1), 250, 0.05, "pop", 0.6))
        btn = Image.new("RGBA", (720, 150))
        d = ImageDraw.Draw(btn)
        d.rounded_rectangle([0, 0, 719, 149], 75, fill=(255, 30, 60, 255))
        d.polygon([(70, 45), (70, 105), (120, 75)], fill=BLANCO)
        d.text((400, 74), "SUSCRÍBETE", font=font(FONT_BLACK, 74), fill=BLANCO, anchor="mm")
        els.append(El(btn, centrado_x(btn), 520, 0.5, "pop", 0.5))
        su = texto_glow(esc["sub"], font(FONT_SB, 46), color=AMARILLO, glow=(80, 0, 60), radio=8)
        els.append(El(su, centrado_x(su), 720, 0.9, "up"))
    return els

class Hud:
    def __init__(self, canal):
        self.bug = texto_glow(canal, font(FONT_BLACKI, 40), glow=ROSA, radio=8)
    def draw(self, canvas, t, dur):
        canvas.alpha_composite(self.bug, (30, 14))
        d = ImageDraw.Draw(canvas)
        w = int(W * min(1, t / dur))
        d.rectangle([0, H - 8, W, H], fill=(0, 0, 0, 120))
        d.rectangle([0, H - 8, w, H], fill=ROSA + (255,))

# ------------------------------------------------------------------ miniatura
def miniatura(lineas, canal, semilla, ruta):
    fo = Fondo(semilla, semilla)
    img = fo.frame(3.0).convert("RGBA")
    img = Image.fromarray(fo.post(img.convert("RGB"))).convert("RGBA")
    # oscurecer el centro para que el texto destaque
    sh = Image.new("RGBA", (W, H), (10, 0, 20, 110))
    img.alpha_composite(sh)
    l1 = texto_glow(lineas[0], font(FONT_BLACKI, 200), color=BLANCO, glow=ROSA, stroke=8, radio=26)
    l2 = texto_glow(lineas[1], font(FONT_BLACKI, 200), color=AMARILLO, glow=ROSA, stroke=8, radio=26)
    tag = texto_glow(lineas[2], font(FONT_BLACK, 110), color=(20, 6, 30), glow=None)
    tp = Image.new("RGBA", (tag.width + 40, tag.height))
    ImageDraw.Draw(tp).rounded_rectangle([0, 20, tp.width - 1, tp.height - 20], 20, fill=CIAN + (255,))
    tp.alpha_composite(tag, (20, 0))
    for im in (l1, l2):
        if im.width > W - 60:
            r = (W - 60) / im.width
            im2 = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
            if im is l1: l1 = im2
            else: l2 = im2
    img.alpha_composite(l1, (centrado_x(l1), 70))
    img.alpha_composite(l2, (centrado_x(l2), 70 + l1.height - 120))
    tp = tp.rotate(-4, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(tp, (W - tp.width - 60, H - tp.height - 50))
    img.alpha_composite(texto_glow(canal, font(FONT_BLACKI, 48), glow=ROSA, radio=8), (40, H - 120))
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(ruta, quality=92)

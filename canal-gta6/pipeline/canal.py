# -*- coding: utf-8 -*-
"""Banner (2560x1440) y avatar (800x800) del canal."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import visual as V, guiones as G

out = os.path.join(os.path.dirname(__file__), "..", "salida", "00-canal")
os.makedirs(out, exist_ok=True)
fo = V.Fondo(7, 1)
base = Image.fromarray(fo.post(fo.frame(2.0).convert("RGB"))).convert("RGBA")
ban = base.resize((2560, 1440), Image.LANCZOS)
# zona segura de YouTube: 1546x423 centrada
t = V.texto_glow(G.CANAL, V.font(V.FONT_BLACKI, 230), glow=V.ROSA, stroke=6, radio=28)
ban.alpha_composite(t, ((2560 - t.width) // 2, 720 - t.height // 2 - 40))
s = V.texto_glow("Guías de GTA 6 · solo datos confirmados", V.font(V.FONT_SB, 64), color=V.AMARILLO, glow=(80, 0, 60), radio=10)
ban.alpha_composite(s, ((2560 - s.width) // 2, 820))
ban.convert("RGB").save(os.path.join(out, "banner-2560x1440.jpg"), quality=92)
av = base.crop((560, 0, 1640, 1080)).resize((800, 800), Image.LANCZOS)
a = V.texto_glow("N6", V.font(V.FONT_BLACKI, 380), glow=V.ROSA, stroke=8, radio=30)
av.alpha_composite(a, ((800 - a.width) // 2, (800 - a.height) // 2 - 20))
av.convert("RGB").save(os.path.join(out, "avatar-800x800.jpg"), quality=92)
print("ok")

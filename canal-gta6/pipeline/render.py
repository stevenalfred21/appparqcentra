# -*- coding: utf-8 -*-
"""Monta un vídeo completo: voz + música + gráficos animados -> MP4.

Uso: python3 render.py <indice 0-9> [--preview SEGUNDOS]
Necesita KOKORO_DIR con kokoro-v1.0.onnx y voices-v1.0.bin.
"""
import os, sys, json, subprocess, time
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guiones, audio, visual as V

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TMP = os.environ.get("TRABAJO", os.path.join(RAIZ, ".trabajo"))

def srt_tiempo(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def trocea(texto, maxc=84):
    # parte frases largas en subtítulos de 2 líneas como máximo
    palabras, out, cur = texto.split(), [], ""
    for p in palabras:
        if len(cur) + len(p) + 1 > maxc and cur:
            out.append(cur); cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur: out.append(cur)
    return out

def escribe_srt(tl, ruta):
    n, lineas = 1, []
    for e in tl["escenas"]:
        for b in e["beats"]:
            trozos = trocea(b["texto"])
            total = sum(len(x) for x in trozos)
            t = b["inicio"]
            for tr in trozos:
                d = (b["fin"] - b["inicio"]) * len(tr) / total
                lineas += [str(n), f"{srt_tiempo(t)} --> {srt_tiempo(t + d)}", tr, ""]
                n += 1; t += d
    open(ruta, "w", encoding="utf-8").write("\n".join(lineas))

def render(i, preview=None):
    v = guiones.VIDEOS[i]
    slug = v["slug"]
    trab = os.path.join(TMP, slug)
    os.makedirs(trab, exist_ok=True)
    out_dir = os.path.join(RAIZ, "salida", slug)
    os.makedirs(out_dir, exist_ok=True)

    tl = audio.narracion(v, trab)
    dur = tl["duracion"] if not preview else min(preview, tl["duracion"])
    mus = os.path.join(trab, "musica.wav")
    if not os.path.exists(mus):
        audio.musica(tl["duracion"], semilla=i, ruta=mus)

    fondo = V.Fondo(semilla=i + 3, tono=i)
    hud = V.Hud(guiones.CANAL)
    escenas = [(e, tle, V.construir_escena(e, tle, guiones.CANAL)) for e, tle in zip(v["escenas"], tl["escenas"])]

    mp4 = os.path.join(out_dir, f"{slug}.mp4") if not preview else os.path.join(trab, "preview.mp4")
    af = ("[2:a]volume=0.22[m];[1:a]aresample=48000,asplit=2[v1][v2];"
          "[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];"
          "[v1][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{V.W}x{V.H}", "-r", str(V.FPS), "-i", "-",
           "-i", os.path.join(trab, "voz.wav"), "-i", mus,
           "-filter_complex", af, "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart", mp4]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(dur * V.FPS)
    t_ini = time.time()
    for f in range(nframes):
        t = f / V.FPS
        # escena activa
        k = 0
        for j, (_, tle, _) in enumerate(escenas):
            if t >= tle["inicio"] - 0.15:
                k = j
        e, tle, els = escenas[k]
        rel = t - tle["inicio"]
        fin_rel = tle["fin"] - tle["inicio"]
        salida = 1.0 if k == len(escenas) - 1 else V.ease((fin_rel - rel) / 0.3) if rel > fin_rel - 0.3 else 1.0
        img = fondo.frame(t).convert("RGBA")
        # capa oscura para legibilidad
        img.alpha_composite(_sombra())
        for el in els:
            el.draw(img, rel, salida)
        # destello de transición
        if 0 <= rel < 0.22 and k > 0:
            a = int(90 * (1 - rel / 0.22))
            img.alpha_composite(Image.new("RGBA", img.size, (255, 80, 180, a)))
        hud.draw(img, t, tl["duracion"])
        ff.stdin.write(fondo.post(img.convert("RGB")).tobytes())
        if f % 300 == 0:
            el_t = time.time() - t_ini
            print(f"[{slug}] {f}/{nframes} ({(f+1)/max(el_t,1e-3):.1f} fps)", flush=True)
    ff.stdin.close()
    ff.wait()
    if preview:
        return mp4
    escribe_srt(tl, os.path.join(out_dir, f"{slug}.srt"))
    V.miniatura(v["miniatura"], guiones.CANAL, i, os.path.join(out_dir, f"{slug}-miniatura.jpg"))
    meta = (f"TÍTULO:\n{v['titulo']}\n\nDESCRIPCIÓN:\n{v['descripcion']}\n\n"
            f"Vídeo informativo independiente. No afiliado a Rockstar Games ni a Take-Two Interactive. "
            f"Datos revisados el 16 de noviembre de 2026.\n\n#GTA6 #GTAVI\n\n"
            f"ETIQUETAS:\n{', '.join(v['tags'])}\n\nDURACIÓN: {int(tl['duracion']//60)}:{int(tl['duracion']%60):02d}\n")
    open(os.path.join(out_dir, f"{slug}-ficha.txt"), "w", encoding="utf-8").write(meta)
    guion = [f"# {v['titulo']}\n"]
    for e in v["escenas"]:
        guion.append(f"\n## [{e['tipo']}] " + (e.get("title") or e.get("heading") or e.get("value") or "").replace("\n", " "))
        guion += [f"- {b}" for b in e["beats"]]
    open(os.path.join(out_dir, f"{slug}-guion.md"), "w", encoding="utf-8").write("\n".join(guion) + "\n")
    print(f"[{slug}] OK {tl['duracion']:.1f}s en {time.time()-t_ini:.0f}s", flush=True)
    return mp4

_sh = None
def _sombra():
    global _sh
    if _sh is None:
        _sh = Image.new("RGBA", (V.W, V.H), (8, 0, 18, 95))
    return _sh

if __name__ == "__main__":
    idx = int(sys.argv[1])
    pv = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--preview" else None
    render(idx, pv)

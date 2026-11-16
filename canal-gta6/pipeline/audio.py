# -*- coding: utf-8 -*-
"""Voz (Kokoro, offline) y música original generada por código."""
import os, re, json
import numpy as np
import soundfile as sf

SR_MUSIC = 48000
PAUSA_BEAT = 0.30
PAUSA_ESCENA = 0.70

_REEMPLAZOS = [
    (r"\bGTA 6\b", "Ge Te A seis"),
    (r"\bGTA VI\b", "Ge Te A seis"),
    (r"\bGTA plus\b", "Ge Te A plus"),
    (r"\bGTA cinco\b", "Ge Te A cinco"),
    (r"\bGTA cuatro\b", "Ge Te A cuatro"),
    (r"\bGTA Online\b", "Ge Te A Online"),
    (r"\bGTA\b", "Ge Te A"),
    (r"\bPS5 Pro\b", "Pe Ese cinco Pro"),
    (r"\bPS5\b", "Pe Ese cinco"),
    (r"\bTake-Two\b", "Teik Tu"),
    (r"\bXbox\b", "Exbox"),
    (r"\bDigital Foundry\b", "Díyital Faundri"),
    (r"\bBloomberg\b", "Blúmberg"),
    (r"\bJason Schreier\b", "Yeison Shráier"),
    (r"\bJason\b", "Yeison"),
    (r"\bLeonida Keys\b", "Leonida Kis"),
    (r"\bMount Kalaga\b", "Maunt Kalaga"),
    (r"\bGrassrivers\b", "Grasrívers"),
    (r"\bPort Gellhorn\b", "Port Guélhorn"),
    (r"\bVice City\b", "Vais Siti"),
    (r"\bVintage Vice City Pack\b", "Vintach Vais Siti Pak"),
    (r"\bRockstar\b", "Rókstar"),
    (r"\bCal Hampton\b", "Cal Jámpton"),
    (r"\bBoobie Ike\b", "Bubi Aik"),
    (r"\bDre'Quan Priest\b", "Drecuán Prist"),
    (r"\bReal Dimez\b", "Rial Daims"),
    (r"\bBrian Heder\b", "Bráian Héder"),
    (r"\bDuval\b", "Duval"),
    (r"\bStandard\b", "Estándar"),
    (r"\bUltimate\b", "Últimeit"),
    (r"\bonline\b", "onlain"),
    (r"\bOnline\b", "Onlain"),
]

def para_voz(texto):
    t = texto
    # Primero los nombres compuestos más largos
    for pat, rep in sorted(_REEMPLAZOS, key=lambda x: -len(x[0])):
        t = re.sub(pat, rep, t)
    return t

_kokoro = None
def _k():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        d = os.environ["KOKORO_DIR"]
        _kokoro = Kokoro(f"{d}/kokoro-v1.0.onnx", f"{d}/voices-v1.0.bin")
    return _kokoro

def sintetiza(texto, voz="em_alex", velocidad=1.08):
    s, sr = _k().create(para_voz(texto), voice=voz, speed=velocidad, lang="es")
    s = np.asarray(s, dtype=np.float32)
    # recorta silencios extremos
    idx = np.where(np.abs(s) > 0.01)[0]
    if len(idx):
        s = s[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.08 * sr)]
    return s, sr

def narracion(video, carpeta, voz="em_alex"):
    """Genera la voz de un vídeo. Devuelve timeline con tiempos de cada beat."""
    os.makedirs(carpeta, exist_ok=True)
    cache = os.path.join(carpeta, "timeline.json")
    wav = os.path.join(carpeta, "voz.wav")
    if os.path.exists(cache) and os.path.exists(wav):
        return json.load(open(cache))
    trozos, t = [], 0.4
    sr0 = None
    tl = {"escenas": []}
    trozos.append(("sil", 0.4))
    for esc in video["escenas"]:
        e = {"inicio": t, "beats": []}
        for b in esc["beats"]:
            s, sr = sintetiza(b, voz)
            sr0 = sr
            dur = len(s) / sr
            e["beats"].append({"inicio": t, "fin": t + dur, "texto": b})
            trozos.append(("aud", s))
            t += dur
            trozos.append(("sil", PAUSA_BEAT))
            t += PAUSA_BEAT
        trozos.append(("sil", PAUSA_ESCENA))
        t += PAUSA_ESCENA
        e["fin"] = t
        tl["escenas"].append(e)
    tl["duracion"] = t + 0.8
    partes = []
    for k, v in trozos:
        partes.append(np.zeros(int(v * sr0), np.float32) if k == "sil" else v)
    partes.append(np.zeros(int(0.8 * sr0), np.float32))
    audio = np.concatenate(partes)
    # al reconstruir los tiempos con muestras enteras hay deriva mínima; la corregimos
    sf.write(wav, audio, sr0)
    tl["duracion"] = len(audio) / sr0
    json.dump(tl, open(cache, "w"), ensure_ascii=False, indent=1)
    return tl

# ------------------------------------------------------------------ música
def _env(n, a, r, sr):
    e = np.ones(n, np.float32)
    na, nr = int(a * sr), int(r * sr)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def _lp(x, alpha):
    # filtro paso bajo de un polo, dos pasadas
    from scipy.signal import lfilter
    y = lfilter([alpha], [1, alpha - 1], x)
    return lfilter([alpha], [1, alpha - 1], y).astype(np.float32)

def musica(duracion, semilla=0, ruta=None):
    """Bucle synthwave original: Am - F - C - G a 100 bpm."""
    sr = SR_MUSIC
    rng = np.random.default_rng(semilla)
    bpm = 100 + (semilla % 3) * 4
    beat = 60 / bpm
    compas = 4 * beat
    progs = [[57, 53, 48, 55], [50, 53, 48, 55], [57, 52, 53, 55]]
    prog = progs[semilla % len(progs)]
    n = int(duracion * sr) + sr
    out = np.zeros(n, np.float32)
    t_loop = np.arange(int(compas * sr)) / sr

    def hz(m): return 440 * 2 ** ((m - 69) / 12)

    def saw(f, t): return 2 * ((t * f) % 1) - 1

    ncomp = int(np.ceil(duracion / compas)) + 1
    for c in range(ncomp):
        raiz = prog[c % 4]
        st = int(c * compas * sr)
        if st >= n: break
        # pad: triada menor/mayor según acorde
        tercera = 3 if raiz in (57, 50, 52) else 4
        pad = np.zeros_like(t_loop)
        for m in (raiz, raiz + tercera, raiz + 7, raiz + 12):
            for det in (-0.12, 0.12):
                pad += saw(hz(m) * (1 + det / 100), t_loop) * 0.05
        pad *= _env(len(t_loop), 0.4, 0.4, sr)
        # bajo en corcheas
        bajo = np.zeros_like(t_loop)
        for k in range(8):
            a = int(k * beat / 2 * sr); b = int((k + 1) * beat / 2 * sr)
            tt = t_loop[: b - a]
            bajo[a:b] = saw(hz(raiz - 24), tt) * _env(b - a, 0.005, 0.12, sr) * 0.22
        seg = pad + bajo
        e = min(n, st + len(seg))
        out[st:e] += seg[: e - st]
    out = _lp(out, 0.08)
    # batería: bombo y palmada/hat sintetizados
    nb = int(duracion / beat) + 2
    for k in range(nb):
        st = int(k * beat * sr)
        if st >= n: break
        L = int(0.25 * sr)
        tt = np.arange(L) / sr
        kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.55
        e = min(n, st + L); out[st:e] += kick[: e - st]
        if k % 2 == 1:
            Ls = int(0.18 * sr)
            sn = rng.standard_normal(Ls).astype(np.float32) * np.exp(-np.arange(Ls) / sr * 18) * 0.12
            e = min(n, st + Ls); out[st:e] += sn[: e - st]
        hst = st + int(beat / 2 * sr)
        Lh = int(0.04 * sr)
        if hst + Lh < n:
            h = rng.standard_normal(Lh).astype(np.float32)
            h = np.diff(h, prepend=0) * np.exp(-np.arange(Lh) / sr * 90) * 0.05
            out[hst:hst + Lh] += h
    out = out[: int(duracion * sr)]
    fade = int(1.5 * sr)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    out /= max(1e-6, np.abs(out).max()) / 0.8
    st = np.stack([out, np.roll(out, 240)], 1)  # leve ensanchado estéreo
    if ruta: sf.write(ruta, st, sr)
    return st

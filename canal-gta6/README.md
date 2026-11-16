# Canal GTA 6 — 10 vídeos para el lanzamiento (19-nov-2026)

Nombre provisional del canal: **NEÓN SEIS** (se cambia en `pipeline/guiones.py`, variable `CANAL`, y se vuelve a renderizar).

## Qué hay en `salida/`

Cada carpeta es un vídeo listo para subir:

| Archivo | Para qué |
|---|---|
| `NN-slug.mp4` | Vídeo 1080p30, voz + música + gráficos |
| `NN-slug-miniatura.jpg` | Miniatura 1280x720 |
| `NN-slug.srt` | Subtítulos en español (subir en YouTube Studio › Subtítulos) |
| `NN-slug-ficha.txt` | Título, descripción y etiquetas para copiar y pegar |
| `NN-slug-guion.md` | Guion completo por escenas |

`salida/00-canal/` tiene el banner (2560x1440) y el avatar (800x800).

## Los 10 vídeos (orden de búsqueda prevista)

1. ¿A qué hora sale GTA 6? (hora por país)
2. ¿Cuánto pesa? Precarga y espacio
3. Standard vs Ultimate
4. ¿Tiene online?
5. ¿Sale en PC?
6. ¿Está en español?
7. ¿60 FPS? PS5 / PS5 Pro / Xbox
8. El mapa: las 6 regiones de Leonida
9. Jason y Lucía, los protagonistas
10. Todo lo que necesitas saber (resumen)

## Antes de subir (importante)

- **Escucha cada vídeo entero.** La voz es sintética (Kokoro, offline). Los nombres en inglés se pronuncian con una transcripción fonética aproximada; alguno puede sonar raro.
- **Revisa los datos el miércoles por la noche.** Los guiones usan lo publicado hasta el 16-nov-2026. Los que más pueden cambiar: 04 (online), 05 (PC) y 07 (FPS). Si algo cambia, edita el beat en `guiones.py` y vuelve a renderizar ese vídeo.
- Los vídeos 01, 02 y 03 rinden más **antes** del lanzamiento (la gente busca la hora y el peso antes de jugar). Si puedes, súbelos martes o miércoles.
- Todo el material visual y la música son originales (generados por código). No se usa ningún tráiler, logo ni arte de Rockstar.

## Volver a renderizar

```bash
pip install kokoro-onnx soundfile scipy pillow numpy
# modelos: kokoro-v1.0.onnx y voices-v1.0.bin (release model-files-v1.0 de thewh1teagle/kokoro-onnx en GitHub)
export KOKORO_DIR=/ruta/a/modelos TRABAJO=/tmp/trabajo
python3 pipeline/render.py 0     # vídeo 1 (índices 0-9)
python3 pipeline/canal.py        # banner y avatar
```

Si cambias el texto de un vídeo, borra `$TRABAJO/<slug>/` para que se regenere la voz.

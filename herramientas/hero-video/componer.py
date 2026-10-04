#!/usr/bin/env python3
"""Compone el video del hero de abdominoplastiapad.com desde el clip original de Higgsfield.

    python3 herramientas/hero-video/componer.py [video-original.mp4] [--salida CARPETA]

Escribe hero-torso-claro.mp4|jpg y hero-torso-oscuro.mp4|jpg (por defecto en la raíz del
proyecto). Necesita numpy, opencv, Pillow, rembg (modelo u2net) y ~/bin/ffmpeg.

Qué hace, en orden:
  1. Estima la placa del fondo (el fondo sin torso ni seda) y aplana la iluminación.
  2. Arma el bucle: la seda repite su vaivén cada 130 cuadros; se funden 16 para cerrar.
  3. Versión clara: fondo BLANCO puro. La página la mezcla con `mix-blend-mode: multiply`.
  4. Versión oscura: recompone la seda sobre fondo oscuro y deja el fondo en NEGRO puro.
     La página la mezcla con `screen`. No se generó otro video: sale del mismo clip.
  5. Recorta a 4:5, escala a 960x1200, codifica H.264 y saca la imagen fija (primer cuadro).

Los números de abajo (bucle, encuadre, zonas) son de ESTE clip: 1244x1664, 241 cuadros.
Con otro clip hay que volver a medirlos.

También se importa desde intro.py (la Venus de entrada), que usa `leer`, `preparar`,
`final` y `codificar` para que el empalme con el bucle sea exacto.
"""
import os, subprocess, time, argparse
import numpy as np, cv2
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN_POR_DEFECTO = os.path.join(RAIZ, "material/hero-higgsfield/hf_20261004_031751_torso-seda.mp4")
FFMPEG = os.path.expanduser("~/bin/ffmpeg")

# ── Parámetros de este clip ──────────────────────────────────────────────────
INICIO, FIN, FUNDIDO = 71, 201, 16          # bucle [71,201): 130 cuadros = 5,42 s
X0, Y0, CW, CH = 266, 284, 978, 1222        # encuadre 4:5 sobre el original
OW, OH = 960, 1200                          # tamaño final
CREMA = np.array([250, 248, 244], np.float32)       # --cream claro  #FAF8F4
CREMA_OSC = np.array([27, 31, 29], np.float32)      # --cream oscuro #1B1F1D
YESO_OSC = np.array([240, 237, 230], np.float32) / 255   # el yeso, en oscuro, al tono de --ink
CRF = 22

t0 = time.time()
def paso(msg): print(f"[{time.time()-t0:5.1f}s] {msg}", flush=True)
ker = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*r+1, 2*r+1))

# ── 1. Cuadros ───────────────────────────────────────────────────────────────
def leer(origen=ORIGEN_POR_DEFECTO):
    cap = cv2.VideoCapture(origen); cuadros = []
    while True:
        ok, f = cap.read()
        if not ok: break
        cuadros.append(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    F = np.stack(cuadros); del cuadros
    assert F.shape[:3] == (241, 1664, 1244), f"clip distinto al esperado: {F.shape[0]} cuadros de {F.shape[2]}x{F.shape[1]}"
    paso(f"{F.shape[0]} cuadros de {F.shape[2]}x{F.shape[1]}")
    return F

def preparar(F):
    """Mide el clip (máscaras, placa del fondo, sólido) y devuelve componer(k)."""
    N, H, W, _ = F.shape
    # ── 2. Máscaras del objeto (rembg) y mapa de movimiento ──────────────────
    from rembg import remove, new_session
    ses = new_session("u2net")
    mascara = lambda k: np.asarray(remove(Image.fromarray(np.ascontiguousarray(F[k])), session=ses, only_mask=True), np.float32) / 255
    union = np.stack([mascara(k) for k in (0, 60, 120, 180, 240)]).max(0)          # yeso + seda en 5 poses
    comun = np.stack([mascara(k) for k in range(55, 201, 6)]).min(0)               # lo que nunca se mueve
    gris = np.stack([cv2.resize(cv2.cvtColor(np.ascontiguousarray(F[k]), cv2.COLOR_RGB2GRAY), (W//4, H//4), interpolation=cv2.INTER_AREA) for k in range(N)]).astype(np.float32)
    mov = cv2.resize(gris.std(0), (W, H), interpolation=cv2.INTER_LINEAR); del gris
    paso("máscaras listas")

    # ── 3. Placa del fondo ───────────────────────────────────────────────────
    Bp = np.empty((H, W, 3), np.float32); k85 = int(N * 0.85)                      # la seda solo oscurece:
    for c in range(3): Bp[..., c] = np.partition(np.ascontiguousarray(F[..., c]), k85, axis=0)[k85]   # percentil alto = fondo
    nucleo = cv2.dilate((union > 0.05).astype(np.uint8), ker(14))
    lejos = cv2.dilate(((union > 0.05) | (mov > 2.5)).astype(np.uint8), ker(28))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); xn = xx / W * 2 - 1; yn = yy / H * 2 - 1
    terminos = [xn**i * yn**j for i in range(5) for j in range(5 - i)]             # polinomio de orden 4
    A = np.stack([t[::6, ::6][lejos[::6, ::6] == 0] for t in terminos], 1); Bs = np.empty_like(Bp)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, Bp[::6, ::6, c][lejos[::6, ::6] == 0], rcond=None)
        Bs[..., c] = sum(cf * t for cf, t in zip(coef, terminos))
    res = Bp - Bs
    valido = ((np.abs(res).max(2) < 22) & (nucleo == 0)).astype(np.float32)        # 22: entra la sombra del piso
    num = cv2.GaussianBlur(res * valido[..., None], (0, 0), 28); den = cv2.GaussianBlur(valido, (0, 0), 28)[..., None]
    relleno = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0) * np.clip(den / 0.25, 0, 1)
    B = cv2.GaussianBlur(np.where(valido[..., None] > 0, Bp, Bs + relleno), (0, 0), 1.2)
    G = (CREMA / B).astype(np.float32)                                              # ganancia que aplana el fondo
    paso("placa del fondo lista")

    # ── 4. Sólido: el fragmento (yeso + envoltura), sin la lengua de la cola ─
    sol = (comun > 0.5).astype(np.uint8)
    for y in range(1162, H): sol[y, int(788 - 0.33 * (y - 1160)):] = 0
    sol = cv2.erode(sol, ker(2)); _, lab, st, _ = cv2.connectedComponentsWithStats(sol)
    sol = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.float32)
    SOL = cv2.GaussianBlur(sol, (0, 0), 2.0)[..., None]
    SOLZ = cv2.dilate((SOL[..., 0] > 0.02).astype(np.uint8), ker(6)).astype(np.float32)
    # zona del muñón: el extremo de yeso que asoma bajo la seda, abajo a la izquierda. Se retira.
    ZM = np.zeros((H, W), np.float32); ZM[1222:1325, 395:612] = 1; ZM = cv2.GaussianBlur(ZM, (0, 0), 5.0)
    LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
    # color de la seda densa, para estimar su transparencia
    ff = np.clip(F[100].astype(np.float32) * G, 0, 255)
    S0 = np.percentile(ff[(union > 0.5) & (sol < 0.5) & ((CREMA - ff).max(2) > 40)], 4, axis=0).astype(np.float32)

    def componer(k):
        """Devuelve el cuadro k en sus dos versiones: (claro sobre blanco, oscuro sobre negro)."""
        ff = np.clip(F[k].astype(np.float32) * G, 0, 255)                           # campo plano: fondo = CREMA
        lum = cv2.GaussianBlur(ff @ LUM, (0, 0), 1.2)
        queda = 1 - ZM * (1 - np.clip((222 - lum) / 17, 0, 1))                      # fuera el muñón
        ff = CREMA + queda[..., None] * (ff - CREMA); solk = SOL * queda[..., None]
        d = cv2.GaussianBlur(np.abs(ff - CREMA).max(2), (0, 0), 1.6)
        w = np.clip((d - 1.6) / 3.2, 0, 1); w = w * w * (3 - 2 * w)                 # 0 = fondo, 1 = objeto
        fuerte = cv2.dilate((d > 12).astype(np.uint8), ker(7)).astype(np.float32)   # solo cuenta lo pegado a
        zona = cv2.GaussianBlur(np.maximum(fuerte, SOLZ * (queda > 0.5)), (0, 0), 3.0)   # seda o yeso de verdad
        w = (w * np.clip(zona * 1.6, 0, 1))[..., None]
        claro = CREMA + w * (ff - CREMA)
        claro = np.where(SOLZ[..., None] > 0, claro, np.minimum(claro, CREMA))      # fuera del yeso nada brilla más que el papel
        fm = np.minimum(ff, CREMA)
        a = np.clip(((CREMA - fm) / (CREMA - S0)).max(2), 0, 1)[..., None]          # opacidad de la seda
        recomp = CREMA_OSC + w * (fm - (1 - a) * (CREMA - CREMA_OSC) - CREMA_OSC)   # la seda sobre fondo oscuro
        oscuro = solk * (ff * YESO_OSC) + (1 - solk) * recomp
        # A «espacio de mezcla»: claro/CREMA -> blanco puro de fondo; (oscuro-OSC)/(1-OSC) -> negro puro.
        return np.clip(claro * (255 / CREMA), 0, 255), np.clip((oscuro - CREMA_OSC) * (255 / (255 - CREMA_OSC)), 0, 255)
    componer.S0, componer.SOL = S0, SOL          # intro.py usa la misma seda densa y el mismo sólido
    return componer

final = lambda im: cv2.resize(im[Y0:Y0+CH, X0:X0+CW], (OW, OH), interpolation=cv2.INTER_AREA)

# ── 5. Codificar ─────────────────────────────────────────────────────────────
def codificar(arr, destino, crf=CRF, gop=None):
    tmp = destino + ".tmp.mp4"; gop = gop or len(arr); h, w = arr.shape[1:3]
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
           "-c:v", "libx264", "-preset", "veryslow", "-crf", str(crf), "-profile:v", "high", "-level", "4.0",
           "-g", str(gop), "-movflags", "+faststart", "-an", "-map_metadata", "-1", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); p.stdin.write(np.ascontiguousarray(arr).tobytes()); p.stdin.close(); assert p.wait() == 0
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-c", "copy",      # etiqueta BT.709 completa
                    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
                    "-movflags", "+faststart", "-map_metadata", "-1", destino], check=True)
    os.remove(tmp); return os.path.getsize(destino)

def main():
    ap = argparse.ArgumentParser(description="Compone el video del hero desde el clip de Higgsfield.")
    ap.add_argument("origen", nargs="?", default=ORIGEN_POR_DEFECTO)
    ap.add_argument("--salida", default=RAIZ, help="carpeta de destino (por defecto, la raíz del proyecto)")
    a_ = ap.parse_args()
    componer = preparar(leer(a_.origen))

    L = FIN - INICIO; claro = np.empty((L, OH, OW, 3), np.uint8); oscuro = np.empty_like(claro)
    for i in range(L):
        cl, osc = componer(INICIO + i); j = i - (L - FUNDIDO)
        if j >= 0:                                                              # fundido hacia el cuadro previo al inicio
            t = (j + 1) / (FUNDIDO + 1); t = t * t * (3 - 2 * t); cl2, os2 = componer(INICIO - FUNDIDO + j)
            cl = (1 - t) * cl + t * cl2; osc = (1 - t) * osc + t * os2
        claro[i] = np.rint(final(cl)); oscuro[i] = np.rint(final(osc))
    paso(f"bucle compuesto: {L} cuadros ({L/24:.2f} s)")

    os.makedirs(a_.salida, exist_ok=True)
    for tema, arr, sub in (("claro", claro, 0), ("oscuro", oscuro, 2)):
        kb = codificar(arr, os.path.join(a_.salida, f"hero-torso-{tema}.mp4")) / 1024
        jpg = os.path.join(a_.salida, f"hero-torso-{tema}.jpg")
        Image.fromarray(np.ascontiguousarray(arr[0])).save(jpg, "JPEG", quality=80, optimize=True, progressive=True, subsampling=sub)
        fondo = tuple(int(x) for x in arr[:, :40, :40].reshape(-1, 3).max(0)), tuple(int(x) for x in arr[:, :40, :40].reshape(-1, 3).min(0))
        paso(f"{tema}: video {kb:.0f} KB · imagen {os.path.getsize(jpg)/1024:.0f} KB · fondo {fondo[0]}..{fondo[1]}")

if __name__ == "__main__":
    main()

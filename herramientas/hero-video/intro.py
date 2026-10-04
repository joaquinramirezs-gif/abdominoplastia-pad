#!/usr/bin/env python3
"""La entrada del hero de abdominoplastiapad.com: la Venus de Milo que se convierte en el torso.

    python3 herramientas/hero-video/intro.py [--salida CARPETA] [--hoja]

Escribe hero-venus-claro.mp4 y hero-venus-oscuro.mp4 (por defecto en la raíz del proyecto).
Con --hoja guarda además una hoja de contacto de cada versión, para revisarla.

Parte de un clip de Kling 3.0 (Higgsfield, 4 oct 2026) hecho de cuadro inicial a cuadro final:
la Venus de yeso con la seda salvia en el pecho → el cuadro 56 del clip del torso. Está en
material/hero-higgsfield/, fuera de git. Necesita lo mismo que componer.py.

La versión oscura no se generó aparte: el filtro de Kling rechazó la Venus sobre negro (el busto
descubierto también lo rechazó, por eso lleva la seda). Sale del mismo clip, como el bucle.

Qué hace, en orden:
  1. Aplana el fondo cuadro a cuadro (su brillo cambia durante el clip), retira la sombra del
     piso y deja el fondo en blanco puro (claro) o negro puro (oscuro), como el bucle: la página
     lo mezcla con multiply/screen.
  2. Oscuro: el cuerpo (máscara de u2net, suavizada en el tiempo) va en yeso claro sobre negro;
     la seda suelta se recompone translúcida. Al final se pasa al sólido fijo de componer.py.
  3. Tiempo: entra desde el fondo y arranca lento, para que la Venus alcance a leerse.
  4. Encuadre: parte abierto, con la Venus entera, y se cierra hasta el del bucle mientras
     ocurre la transformación.
  5. Empalme: los últimos cuadros de Kling se funden con el cuadro 56 del torso tal como lo
     compone componer.py, y siguen los cuadros 57 a 70. El bucle parte en el 71: el corte no se ve.
"""
import os, sys, argparse
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import componer as C
from componer import CREMA, CREMA_OSC, YESO_OSC, OW, OH, RAIZ, paso, ker

suave = lambda t: (lambda u: u * u * (3 - 2 * u))(np.clip(t, 0, 1))

CLIP = "material/hero-higgsfield/hf_20261004_121329_venus-intro.mp4"
EMPALME = 56                     # cuadro del torso que Kling recibió como cuadro final
FUNDE = 8                        # cuadros finales de Kling que se funden hacia ese cuadro
ABIERTO = (0.0, 90.0, 1244.0)    # encuadre inicial: x, y, ancho (alto = ancho · 5/4)
CERRADO = (float(C.X0), float(C.Y0), float(C.CW))
CIERRA = (40, 110)               # el encuadre se cierra entre estos cuadros de Kling
RAMPA, LENTO = 30, 0.35          # los primeros 30 cuadros aceleran de 0,35x a 1x
ENTRA = 14                       # cuadros de entrada desde el fondo
CRF_INTRO = 24
LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
# El muñón: el yeso que asoma bajo la seda, abajo a la izquierda (el bucle ya lo retira).
# Aquí se desvanece entre estos cuadros de Kling, dentro de esta zona del original.
MUNON = (112, 124)
ZMI = np.zeros((1664, 1244), np.float32); ZMI[1210:1450, 370:600] = 1; ZMI = cv2.GaussianBlur(ZMI, (0, 0), 8.0)
# El piso: bajo esta altura del original solo quedan la figura y la seda (la sombra se retira).
PISO = suave((np.arange(1664, dtype=np.float32) - 1370) / 50)
SOLIDO = 25                      # apertura que separa el cuerpo (sólido) de la seda suelta
FIJO = (122, 140)                # en oscuro, entre estos cuadros se pasa al sólido fijo del bucle
PESOS = np.exp(-0.5 * np.arange(-2, 3) ** 2).astype(np.float32); PESOS /= PESOS.sum()

def leer_clip(ruta):
    cap = cv2.VideoCapture(ruta); cuadros = []
    while True:
        ok, f = cap.read()
        if not ok: break
        cuadros.append(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    return np.stack(cuadros)

def tiempos(n_kling):
    """Para cada cuadro de salida, el cuadro (fraccionario) de Kling que le toca."""
    vel = LENTO + (1 - LENTO) * suave(np.arange(RAMPA) / (RAMPA - 1))
    tau = list(np.concatenate([[0], np.cumsum(vel)[:-1]]))
    k = round(tau[-1] + 1)                               # de ahí en adelante, cuadros enteros
    while k <= n_kling - 1: tau.append(float(k)); k += 1
    return tau

def encuadre(tau):
    s = float(suave((tau - CIERRA[0]) / (CIERRA[1] - CIERRA[0])))
    return s, [a + s * (b - a) for a, b in zip(ABIERTO, CERRADO)]

def recortar(im, tau):
    s, (x0, y0, w) = encuadre(tau)
    if s >= 1: return C.final(im)                        # el mismo recorte exacto del bucle
    e = OW / w
    M = np.float32([[e, 0, -x0 * e], [0, e, -y0 * e]])
    return cv2.warpAffine(im, M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

class Aplanado:
    """Cuadros de Kling con el fondo aplanado, en sus dos versiones y en «espacio de mezcla».

    El fondo de cada cuadro = un polinomio suave + lo que queda fuera de la figura (la sombra
    del piso), interpolado hacia adentro. Ambos se suavizan en el tiempo para que no parpadee."""
    def __init__(self, V, comp):
        from rembg import remove, new_session
        self.V, self.S0, self.SOL = V, comp.S0, comp.SOL[..., 0]
        N, H, W, _ = V.shape; self.HW = (H, W)
        ses = new_session("u2net")
        self.M = np.empty((N, H, W), np.uint8)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); xn = xx / W * 2 - 1; yn = yy / H * 2 - 1
        self.T = [xn**i * yn**j for i in range(4) for j in range(4 - i)]    # polinomio de orden 3
        sub = (slice(None, None, 8), slice(None, None, 8)); h4, w4 = H // 4, W // 4
        A = np.stack([t[sub].ravel() for t in self.T], 1)
        T4 = [cv2.resize(t, (w4, h4), interpolation=cv2.INTER_AREA) for t in self.T]
        coefs = np.empty((N, 3, len(self.T)), np.float32)
        fuera4 = np.empty((N, h4, w4), np.float32); f4s = np.empty((N, h4, w4, 3), np.float32)
        for k in range(N):
            self.M[k] = np.asarray(remove(Image.fromarray(np.ascontiguousarray(V[k])), session=ses, only_mask=True))
            fuera_k = cv2.dilate((self.M[k] > 12).astype(np.uint8), ker(30)) == 0
            f4 = cv2.resize(V[k], (w4, h4), interpolation=cv2.INTER_AREA).astype(np.float32)
            verde = (f4[..., 1] - np.maximum(f4[..., 0], f4[..., 2])) > 2                # la seda nunca es fondo
            fuera4[k] = cv2.resize(fuera_k.astype(np.float32), (w4, h4), interpolation=cv2.INTER_AREA) * (~verde)
            f4s[k] = f4
            fuera = fuera_k[sub].ravel(); f = V[k][sub].reshape(-1, 3).astype(np.float32)
            for c in range(3):                           # dos pasadas: la segunda sin lo que no es fondo
                usa = fuera.copy()
                for _ in range(2):
                    with np.errstate(all="ignore"):      # numpy 2.0 + Accelerate avisa en falso en matmul
                        cf, *_ = np.linalg.lstsq(A[usa], f[usa, c], rcond=None)
                        usa = fuera & (np.abs(A @ cf - f[:, c]) < 4)
                coefs[k, c] = cf
        suaviza = lambda a, s: cv2.GaussianBlur(a.reshape(N, -1), (1, 0), sigmaX=0.001, sigmaY=s).reshape(a.shape)
        self.coefs = suaviza(coefs, 2.0)                 # suavizado en el tiempo: el fondo no parpadea
        # lo que el polinomio no explica (la sombra del piso), interpolado bajo la figura
        rel = np.empty_like(f4s)
        for k in range(N):
            P4 = np.stack([sum(cf * t for cf, t in zip(self.coefs[k, c], T4)) for c in range(3)], -1)
            m = fuera4[k] * (fuera4[k] > 0.99)
            num = cv2.GaussianBlur((f4s[k] - P4) * m[..., None], (0, 0), 6); den = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
            rel[k] = np.where(den > 0.02, num / np.maximum(den, 0.02), 0) * np.clip(den / 0.15, 0, 1)
        self.rel = suaviza(rel, 1.5)
        self.cache = {}

    def fondo(self, k):
        P = np.stack([sum(cf * t for cf, t in zip(self.coefs[k, c], self.T)) for c in range(3)], -1)
        return P + cv2.resize(self.rel[k], self.HW[::-1], interpolation=cv2.INTER_LINEAR)

    def mascara(self, k):
        """La máscara de u2net, promediada con sus vecinas: así la cabeza se apaga, no salta."""
        N = len(self.M); j = np.clip(np.arange(k - 2, k + 3), 0, N - 1)
        return sum(p * self.M[i].astype(np.float32) for p, i in zip(PESOS, j)) / 255

    def __call__(self, k):
        if k in self.cache: return self.cache[k]
        f = self.V[k].astype(np.float32); B = self.fondo(k)
        obj = cv2.dilate((self.M[k] > 128).astype(np.uint8), ker(6)).astype(np.float32)
        lum = cv2.GaussianBlur(f @ LUM, (0, 0), 1.2)
        r = float(suave((k - MUNON[0]) / (MUNON[1] - MUNON[0])))                    # el muñón se va de a poco
        # franja del piso: ahí, lo que no es figura ni seda es sombra y se va
        firme = cv2.GaussianBlur(cv2.dilate((self.M[k] > 128).astype(np.uint8), ker(3)).astype(np.float32), (0, 0), 2.0)
        verde = cv2.GaussianBlur(np.clip((f[..., 1] - np.maximum(f[..., 0], f[..., 2]) - 1) / 3, 0, 1), (0, 0), 3.0)
        libre = PISO[:, None] * (1 - firme) * (1 - np.clip(verde * 2, 0, 1))
        ff = np.clip(f * (CREMA / B), 0, 255)                                       # fondo = CREMA
        # el muñón: yeso claro de la zona, o lo que no es seda bajo el borde inferior de la seda
        y0, y1, x0, x1 = 1150, 1460, 370, 600
        filas = np.arange(y0, y1)[:, None]
        borde = np.where(verde[y0:y1, x0:x1] > 0.6, filas, -1).max(0)              # última fila con seda, por columna,
        borde = np.lib.stride_tricks.sliding_window_view(np.pad(borde, 20, mode="edge"), 41).max(1)   # y la más baja de sus vecinas
        bajo = np.zeros_like(lum); bajo[y0:y1, x0:x1] = (filas > borde + 6) & (borde >= 0)
        bajo = cv2.GaussianBlur(bajo, (0, 0), 2.0) * (1 - np.clip(verde * 2, 0, 1))
        yeso = np.maximum(1 - np.clip((222 - lum) / 17, 0, 1), bajo)
        queda = (1 - r * ZMI * yeso) * (1 - libre)                                  # fuera el muñón y la sombra
        ff = CREMA + queda[..., None] * (ff - CREMA)
        d = cv2.GaussianBlur(np.abs(ff - CREMA).max(2), (0, 0), 1.6)
        w = np.clip((d - 1.6) / 3.2, 0, 1); w = w * w * (3 - 2 * w)
        fuerte = cv2.dilate((d > 12).astype(np.uint8), ker(7)).astype(np.float32)
        zona = cv2.GaussianBlur(np.maximum(fuerte, obj), (0, 0), 3.0)
        w = (w * np.clip(zona * 1.6, 0, 1))[..., None]
        claro = CREMA + w * (ff - CREMA)
        claro = np.where(obj[..., None] > 0, claro, np.minimum(claro, CREMA))       # fuera de la figura nada brilla más que el papel
        # oscuro, como en componer.py: el cuerpo en yeso claro, la seda suelta translúcida
        ms = self.mascara(k)
        nucleo = cv2.morphologyEx((ms > 0.5).astype(np.uint8), cv2.MORPH_OPEN, ker(SOLIDO)).astype(np.float32)
        sol = np.minimum(ms, cv2.GaussianBlur(nucleo, (0, 0), 2.0))
        s = float(suave((k - FIJO[0]) / (FIJO[1] - FIJO[0])))                      # el sólido fijo, solo donde ya hay figura
        cerca = cv2.GaussianBlur(cv2.dilate((ms > 0.5).astype(np.uint8), ker(4)).astype(np.float32), (0, 0), 2.0)
        solk = ((1 - s) * sol + s * np.minimum(self.SOL, cerca)) * queda
        fm = np.minimum(ff, CREMA)
        a = np.clip(((CREMA - fm) / (CREMA - self.S0)).max(2), 0, 1)[..., None]     # opacidad de la seda
        recomp = CREMA_OSC + w * (fm - (1 - a) * (CREMA - CREMA_OSC) - CREMA_OSC)
        oscuro = solk[..., None] * (ff * YESO_OSC) + (1 - solk[..., None]) * recomp
        out = (np.clip(claro * (255 / CREMA), 0, 255),
               np.clip((oscuro - CREMA_OSC) * (255 / (255 - CREMA_OSC)), 0, 255))
        self.cache = {k: out, **{j: v for j, v in self.cache.items() if j == k - 1}}
        return out

def armar(comp, hoja=None):
    V = leer_clip(os.path.join(RAIZ, CLIP)); N = len(V)
    paso(f"clip de Kling: {N} cuadros de {V.shape[2]}x{V.shape[1]}")
    P = Aplanado(V, comp); paso("fondos y máscaras medidos")
    fin = [C.final(x) for x in comp(EMPALME)]; fondo = (255.0, 0.0)
    salida = ([], [])
    for n, tau in enumerate(tiempos(N)):
        k0 = int(np.floor(tau)); fr = tau - k0
        par = P(k0) if fr < 1e-6 else [(1 - fr) * a + fr * b for a, b in zip(P(k0), P(min(k0 + 1, N - 1)))]
        for i, im in enumerate(par):
            out = recortar(im, tau)
            if n < ENTRA: out = fondo[i] + float(suave((n + 1) / ENTRA)) * (out - fondo[i])   # entra desde el fondo
            j = tau - (N - 1 - FUNDE)
            if j > 0: t = float(suave(j / FUNDE)); out = (1 - t) * out + t * fin[i]          # hacia el cuadro 56
            salida[i].append(np.rint(out).astype(np.uint8))
    for k in range(EMPALME + 1, C.INICIO):                                                  # 57..70; el bucle parte en el 71
        for i, im in enumerate(comp(k)): salida[i].append(np.rint(C.final(im)).astype(np.uint8))
    arr = [np.stack(s) for s in salida]
    paso(f"{len(arr[0])} cuadros ({len(arr[0])/24:.2f} s)")
    if hoja:
        for tema, a_ in zip(("claro", "oscuro"), arr):
            sel = np.linspace(0, len(a_) - 1, 12).round().astype(int)
            th = [cv2.resize(a_[i], (240, 300), interpolation=cv2.INTER_AREA) for i in sel]
            Image.fromarray(np.vstack([np.hstack(th[:6]), np.hstack(th[6:])])).save(os.path.join(hoja, f"hoja-venus-{tema}.png"))
    return arr

def main():
    ap = argparse.ArgumentParser(description="Compone la entrada del hero: la Venus que se vuelve torso.")
    ap.add_argument("--salida", default=RAIZ, help="carpeta de destino (por defecto, la raíz del proyecto)")
    ap.add_argument("--hoja", action="store_true", help="guarda una hoja de contacto de cada versión")
    a_ = ap.parse_args()
    comp = C.preparar(C.leer())
    os.makedirs(a_.salida, exist_ok=True)
    for tema, arr in zip(("claro", "oscuro"), armar(comp, a_.salida if a_.hoja else None)):
        kb = C.codificar(arr, os.path.join(a_.salida, f"hero-venus-{tema}.mp4"), crf=CRF_INTRO) / 1024
        borde = np.concatenate([arr[:, :24].reshape(-1, 3), arr[:, -24:].reshape(-1, 3)])
        paso(f"{tema}: video {kb:.0f} KB · borde {tuple(int(x) for x in borde.min(0))}..{tuple(int(x) for x in borde.max(0))}")

if __name__ == "__main__":
    main()

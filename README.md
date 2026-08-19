# Abdominoplastia PAD — abdominoplastiapad.com

> 🌐 **Publicado en Vercel: <https://abdominoplastia-pad.vercel.app>** (desde el
> 2026-08-18). Repo: `github.com/joaquinramirezs-gif/abdominoplastia-pad`,
> proyecto Vercel `abdominoplastia-pad` (equipo joaquin20). **No toca el
> dominio real**, que sigue en Wix — mismo esquema paralelo que Leblon y JR.
>
> **Para publicar cambios:** editar las fuentes (`sitio-web.html`,
> `blog.html`, `blog/*.html`), regenerar `publicar/` y hacer push:
> ```bash
> ./publicar.sh && git add -A && git commit -m "..." && git push
> ```

Maqueta nueva del sitio, creada el **2026-08-18** con las líneas de diseño de la
casa (skill `paginas-web`). El sitio real vive en **Wix** (site ID
`d7c99be0-30bf-4d02-8ab6-b4faca5f7119`) y no se puede editar por API — esta
maqueta es la propuesta local, autocontenida, para reemplazarlo o publicarlo
aparte cuando se decida.

| Archivo | Qué es |
|---|---|
| `sitio-web.html` | ⭐ La maqueta vigente. Un solo archivo, se abre con doble clic |
| `blog.html` | El blog: los 4 artículos completos del sitio Wix, en una sola página con índice y anclas |
| `JR-monograma-transparente.png` | Monograma JR (copiado de `dr-joaquin-ramirez/logos/`) |
| `retrato-joaquin-ramirez.jpg` | Retrato del doctor (copiado de `dr-joaquin-ramirez/fotos/`, ya en sRGB) |

## Decisiones

- **Identidad JR** (salvia + dorado sobre crema, tema claro y oscuro): el sitio
  es el embudo del procedimiento del doctor; Leblon aparece solo como el lugar
  de atención.
- **El contacto de este embudo es su propio número**: `+56 9 4457 5535`
  (WhatsApp y teléfono), **no** el de Leblon. Correo:
  `contacto@abdominoplastiapad.com`.
- Todos los CTA abren **WhatsApp con mensaje precargado** («…quiero saber si
  soy candidata a la abdominoplastia con Bono PAD»), según la decisión medida
  de que los formularios no convierten.
- **Valores PAD publicados como información Fonasa** (código 2505950): valor
  total $3.583.580 · copago $1.791.790 · préstamo hasta 85% ($1.523.020) ·
  mínimo día de cirugía $268.769. Con nota de «referenciales, sujetos a
  actualización por Fonasa». No es promoción por precio: es el arancel fijo
  de Fonasa.
- **Sin material de pacientes** (sin antes-después): el consentimiento vigente
  no cubre publicidad.
- **Calculadora de IMC (2026-08-18):** en la sección Candidatas. Campos
  subrayados (peso y estatura; acepta metros con coma o punto, y centímetros),
  resultado grande en peso 200, y veredicto contra el criterio PAD en 4 tramos
  (<25 · 25–27 caso a caso · 27–30 · >30). El botón «Conversemos tu caso» arma
  el enlace de WhatsApp **con el IMC ya escrito en el mensaje**. Siempre con la
  nota «valor referencial: la evaluación presencial lo confirma».
- **Fondo editorial (2026-08-18):** tres recursos, todos dentro del gesto de la
  casa — **folios** (01–05, números de sección enormes en peso 200 al tono de
  las líneas), **hilos de contorno** (pares de curvas de un pixel que cruzan el
  fondo del bono en salvia y del contacto en dorado, eco del trazo del hero) y
  un **filete dorado vertical** que cruza cada borde de sección, cita de la
  barra dorada del monograma JR. Hilos y folios tienen paralaje sutil al hacer
  scroll (±52 px, `requestAnimationFrame`), anulado con
  `prefers-reduced-motion`. Sin sombras, sin degradados.
- **Hero animado (2026-08-18):** contorno de torso femenino en trazo continuo
  SVG —el gesto de la casa— que se dibuja solo al cargar
  (`stroke-dashoffset`), con la línea baja discreta en dorado, flotación suave
  y entrada escalonada del texto. En pantallas angostas la figura pasa a marca
  de agua detrás del texto (`opacity .13`). Todo respeta
  `prefers-reduced-motion` y funciona sin JavaScript (la figura queda dibujada).

## Contenido rescatado del sitio Wix actual (2026-08-18)

Secciones: qué es / criterios de inclusión y exclusión / proceso en 4 pasos /
bio del doctor (U. de los Andes, cirugía general en Hospital Militar, 3 años
Instituto Ivo Pitanguy, **certificado CONACEM en Cirugía Plástica y
Reparadora**, atiende en ES/EN/PT) / preguntas frecuentes / contacto.
Dirección: San Sebastián 2839, of. 211, Las Condes. Redes: Instagram y TikTok
`@abdominoplastiapad`, Facebook (`profile.php?id=61574757542211`) y podcast en
Spotify (`show/3WAZH5wDXqHfwVPTGVhRtO`).

**Lo que la maqueta NO replica (decisión o pendiente):**
- El **formulario de contacto** — fuera a propósito: cero conversión medida;
  todo termina en WhatsApp.
- ~~El blog~~ → **replicado el 2026-08-18 en `blog.html`**: los 4 artículos
  completos (requisitos / recuperación / FAQ / plicaturas), texto íntegro del
  sitio Wix con adaptaciones mínimas (se quitó la mención al formulario de
  contacto; cada artículo cierra en WhatsApp con mensaje propio). Ojo: el
  sitio original tiene cifras que no calzan entre artículos (drenajes 7–12 vs
  7–14 días; reposo 2 vs 3 semanas; faja 6 vs 8–12 semanas) — se mantuvieron
  fieles a cada fuente, pendiente que el doctor unifique.
- Las versiones **`/en/` y `/pt/`**.
- El detalle curricular exhaustivo del doctor (fechas, TOEFL/CELPEBRAS, cursos
  en Columbia y Harvard) — resumido en la tarjeta, no listado.

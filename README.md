# Abdominoplastia PAD — abdominoplastiapad.com

> 🌐 **EN VIVO en <https://www.abdominoplastiapad.com>** desde el **2026-08-19**.
> Repo: `github.com/joaquinramirezs-gif/abdominoplastia-pad`, proyecto Vercel
> `abdominoplastia-pad` (equipo joaquin20). Espejo:
> <https://abdominoplastia-pad.vercel.app>.
>
> **El dominio sigue registrado en Wix** (renovación 25 mar 2030) y Wix sigue
> siendo el **servidor DNS** — solo se cambiaron dos registros para apuntar a
> Vercel. Se hizo así a propósito: mantener la zona en Wix deja **DNSSEC
> válido** y el **correo Google Workspace intacto**.
>
> | Registro | Antes (Wix) | Ahora (Vercel) |
> |---|---|---|
> | `A` @ | 185.230.63.107 / .186 / .171 | **216.198.79.1** |
> | `CNAME` www | cdn1.wixdns.net | **32f71aa8def6956b.vercel-dns-017.com** |
>
> **Para revertir a Wix:** volver a poner los tres registros A y el CNAME de
> arriba. Los MX, SPF, DKIM y DMARC **nunca se tocaron**.
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
| `preguntas-frecuentes.html` | **Página propia del FAQ** (10 preguntas) — es la única con `FAQPage` JSON-LD |
| `privacidad.html` | Política de privacidad (Ley 19.628, con trato especial de datos de salud) |
| `blog.html` | Índice del blog (portada + tarjetas) |
| `blog/*.html` | Los 7 artículos, **una URL por artículo** (decisión SEO 2026-08-18): requisitos-bono-pad, recuperacion-abdominoplastia, plicaturas-abdominales, bono-pad-con-otras-cirugias, programa-guatita-de-delantal-o-bono-pad, guatita-de-delantal-diastasis-o-grasa, prestamo-medico-fonasa-bono-pad |
| `publicar.sh` | Regenera `publicar/` reescribiendo los enlaces relativos a URLs limpias |
| `icon-192.png` | Favicon cuadrado (monograma sobre crema) |
| `JR-monograma-transparente.png` | Monograma JR (copiado de `dr-joaquin-ramirez/logos/`) |
| `retrato-joaquin-ramirez.jpg` | Retrato del doctor (copiado de `dr-joaquin-ramirez/fotos/`, ya en sRGB) |
| `hero-torso-claro.mp4` · `hero-torso-oscuro.mp4` | El video del inicio: bucle de 5,4 s, 960×1200, ~370 KB cada uno. Fondo blanco puro el claro, negro puro el oscuro |
| `hero-torso-claro.jpg` · `hero-torso-oscuro.jpg` | La imagen fija del mismo hero (primer cuadro del bucle): lo que se ve antes del video, sin JavaScript o con «reducir movimiento» |
| `herramientas/hero-video/componer.py` | Recompone los cuatro archivos del hero desde el clip original. Reproduce el resultado publicado bit a bit |
| `material/` | **Fuera de git.** `hero-higgsfield/hf_20261004_031751_torso-seda.mp4`: el clip original de Higgsfield (8 MB) |

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
- **Hero con video (2026-10-04):** un fragmento de torso en yeso blanco,
  envuelto en seda salvia, con una línea dorada fina de cadera a cadera. Es la
  misma idea del hero anterior (contorno en trazo + línea dorada baja), llevada
  a un objeto. Solo se mueve la seda. Reemplazó al contorno SVG que se dibujaba
  solo (2026-08-18), que sigue en el historial de git.
  - **De dónde sale:** imagen en Higgsfield con Nano Banana Pro (más una edición
    para subir la seda hasta la línea dorada) y video con Kling 3.0, 10 s. Costó
    25,5 créditos. Sin pacientes ni piel: es una escultura generada.
  - **Por qué no tiene marco:** el video trae fondo **blanco puro** y la página
    lo mezcla con `mix-blend-mode: multiply`; en tema oscuro, fondo **negro
    puro** con `screen`. Así calza exacto en cualquier navegador. Igualar el
    color de la página dentro del video no sirve: cada decodificador lo corre
    2 o 3 niveles y aparece el rectángulo.
  - **`.hero .wrap{z-index:auto}` es necesario.** La regla general
    `main section>.wrap{z-index:1}` crea un contexto de apilamiento y la mezcla
    deja de ver el fondo del hero: el video aparece como una caja.
  - **La versión oscura no es otro video generado:** sale del mismo clip,
    recomponiendo la seda sobre fondo oscuro. Mismo movimiento en los dos temas.
  - **El bucle:** la seda repite su vaivén cada 130 cuadros; se funden 16 para
    cerrar. La costura es menor que la diferencia entre dos cuadros seguidos.
  - **Carga:** la imagen fija va por `<picture>` según el tema. El video parte
    después del `load`, y solo sin `prefers-reduced-motion` ni ahorro de datos;
    se pausa al salir de pantalla. Sin JavaScript queda la imagen.
  - **En móvil** (≤ 880 px) la figura es una franja de borde a borde sobre el
    título, y **los botones suben sobre el párrafo**: sin eso la franja empujaba
    el llamado a la acción fuera de la primera pantalla.
  - **Pendiente:** se revisó solo en Chromium. Falta verlo en Safari de iPhone.
- **Menú que no desborda (2026-10-04):** entre 921 y ~1320 px de ancho el menú
  se salía y el botón de WhatsApp quedaba fuera de pantalla (notebooks de 1280,
  iPad horizontal). Ahora, en todas las páginas: bajo 1400 px se oculta el
  subtítulo de la marca, bajo 1240 px queda solo el monograma, y los enlaces se
  ocultan bajo 1000 px (antes 920).

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
  contacto; cada artículo cierra en WhatsApp con mensaje propio).
  **2026-08-18: cifras unificadas en todo el sitio** tras la auditoría SEO —
  drenajes **7–12 días**, reposo laboral **2 a 3 semanas según actividad**,
  faja **8–12 semanas**, préstamo **$1.523.021** (para que cuadre con el pie
  de $268.769), posparto «menor de 6 meses con lactancia activa». ⚠️
  **Pendiente que el doctor confirme** estos cuatro criterios clínicos: se
  eligió la variante del propio sitio más coherente, no un juicio médico
  nuevo.

## SEO — artículos publicados

- **2026-09-29:** se publicó `blog/guatita-de-delantal-diastasis-o-grasa` («¿Guatita de delantal, diástasis o grasa? Qué tienes y qué opera el bono PAD»), enlazado desde `/blog`, el bloque «sigue leyendo» de los demás artículos y el `sitemap.xml`.
- **2026-10-04:** se publicó `blog/prestamo-medico-fonasa-bono-pad` («El préstamo médico de Fonasa, paso a paso»), con fuentes ChileAtiende y Fonasa. Estaba programado para el 22 de septiembre, pero esa tarea se abrió y se cerró sin ejecutar nada; se publicó a mano con la fecha real.

## SEO — segunda pasada (2026-08-20)

Correcciones sobre el sitio ya en vivo, tras la auditoría de posicionamiento y
visibilidad en IA:
- **Fechas visibles junto a las cifras** — «Vigencia agosto de 2026» en el
  bloque del bono (con `<time datetime="2026-08">`) y en la nota al pie. Es lo
  que permite a un modelo de lenguaje citar los valores con confianza.
- **Nodo `WebSite`** en el grafo de la portada, con `isPartOf` desde la
  `MedicalWebPage`, más `datePublished`/`dateModified`.
- **`Physician` con `jobTitle` (CONACEM) y `sameAs`**: drjoaquinramirez.cl,
  leblonplasticsurgery.cl, Instagram, TikTok, Facebook y el podcast de Spotify.
  El autor de los artículos y del FAQ también lleva `jobTitle` y `url`.
- **`FAQPage` con fechas y autor**, y etiqueta visible «actualizado agosto 2026».
- **`datePublished` `2026-04` → `2026-04-01`** (ISO 8601 válido) en `blog.html`
  y en `blog/requisitos-bono-pad.html`.
- **`og:image` de `/blog`** apuntaba al espejo `abdominoplastia-pad.vercel.app`
  → corregido al dominio real.
- **Títulos alineados a cómo se busca**: «bono PAD» y «plicatura abdominal» al
  frente; etiquetas de fecha «Actualizado agosto 2026» en el blog y los tres
  artículos (antes decían «Abril 2026», en contradicción con el schema).
- **`trailingSlash: false`** en `vercel.json` — `/blog/x/` daba 200 con el logo
  roto; ahora hace 308 a la URL canónica.
- `sitemap.xml` con `lastmod` 2026-08-20.

**Lo que quedó fuera de esta pasada** (requiere decisión o acción del doctor):
página propia de valores, artículo sobre la Ley Saín / vía pública, nombrar la
clínica donde se opera en el texto visible, citar fuentes oficiales
(fonasa.cl, Ley 21.438, registro CONACEM), enlaces desde drjoaquinramirez.cl y
leblonplasticsurgery.cl, ficha de Google Business Profile, y el alta en Search
Console + la etiqueta GA4.

## SEO (2026-08-18)

Paquete aplicado tras auditoría multi-agente (19 hallazgos corregidos):
- **Canonical al dominio real** en todas las páginas (la copia de Vercel no
  compite contra el Wix; queda lista para la migración).
- Title/description optimizados («Abdominoplastia con Bono PAD Fonasa —
  Guatita de Delantal»), H1 y H2 con las keywords, Open Graph + Twitter.
- **JSON-LD**: MedicalWebPage + SurgicalProcedure + Physician (CONACEM,
  membresías, idiomas) + MedicalClinic + **FAQPage sincronizado palabra a
  palabra con el FAQ visible** + Blog/BlogPosting por artículo.
- **Blog en URLs propias** con canonical, BlogPosting y bloque «sigue
  leyendo» (enlazado interno). `/blog` es índice puro.
- **FAQ consolidado en `/preguntas-frecuentes`** (2026-08-18): había dos FAQ
  compitiendo —el de la portada y el artículo `blog/preguntas-frecuentes-pad`—.
  Se fusionaron en una sola página de 10 preguntas, que es la única que lleva
  `FAQPage` JSON-LD; el artículo del blog se eliminó con **redirect 301** hacia
  ella en `vercel.json`. La portada solo conserva una tarjeta que enlaza ahí.
- **`/privacidad`** enlazada desde el pie de todas las páginas.
- robots.txt + sitemap.xml (6 URLs, dominio real), favicon cuadrado,
  imágenes con width/height + lazy, contenido visible sin JavaScript
  (gating `.js`).
- **Al migrar el dominio**: dar de alta la propiedad en Search Console,
  enviar el sitemap, montar redirecciones 301 desde las URLs viejas de Wix
  (`/que-es-la-abdominoplastia-pad`, `/post/*`, `/en`, `/pt`) y agregar la
  etiqueta GA4/Google Ads. Sin eso no hay ranking que defender.
- Las versiones **`/en/` y `/pt/`**.
- El detalle curricular exhaustivo del doctor (fechas, TOEFL/CELPEBRAS, cursos
  en Columbia y Harvard) — resumido en la tarjeta, no listado.

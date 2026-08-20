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
| `blog/*.html` | Los 3 artículos, **una URL por artículo** (decisión SEO 2026-08-18): requisitos-bono-pad, recuperacion-abdominoplastia, plicaturas-abdominales |
| `publicar.sh` | Regenera `publicar/` reescribiendo los enlaces relativos a URLs limpias |
| `icon-192.png` | Favicon cuadrado (monograma sobre crema) |
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
  contacto; cada artículo cierra en WhatsApp con mensaje propio).
  **2026-08-18: cifras unificadas en todo el sitio** tras la auditoría SEO —
  drenajes **7–12 días**, reposo laboral **2 a 3 semanas según actividad**,
  faja **8–12 semanas**, préstamo **$1.523.021** (para que cuadre con el pie
  de $268.769), posparto «menor de 6 meses con lactancia activa». ⚠️
  **Pendiente que el doctor confirme** estos cuatro criterios clínicos: se
  eligió la variante del propio sitio más coherente, no un juicio médico
  nuevo.

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

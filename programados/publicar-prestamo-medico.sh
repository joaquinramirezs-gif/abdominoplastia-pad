#!/bin/zsh
# Publica el artículo «El préstamo médico de Fonasa, paso a paso», programado
# para el 2026-09-22. Idempotente: si ya está publicado, no hace nada.
# Uso:  ./programados/publicar-prestamo-medico.sh           → publica (commit + push)
#       ./programados/publicar-prestamo-medico.sh --prueba  → ensayo, deja todo como estaba
set -e
cd "$(dirname "$0")/.."
SLUG=prestamo-medico-fonasa-bono-pad
URL="https://www.abdominoplastiapad.com/blog/$SLUG"
PRUEBA=0; [ "$1" = "--prueba" ] && PRUEBA=1

if grep -q "$SLUG" publicar.sh && [ -f "blog/$SLUG.html" ]; then
  echo "Ya está publicado ($URL). Nada que hacer."; exit 0
fi
[ -f "programados/$SLUG.html" ] || { echo "Falta programados/$SLUG.html"; exit 1 }

[ $PRUEBA = 1 ] || git pull -q --ff-only origin HEAD
cp "programados/$SLUG.html" "blog/$SLUG.html"

python3 - "$SLUG" <<'PY'
import io, sys
SLUG = sys.argv[1]
URL = f'https://www.abdominoplastiapad.com/blog/{SLUG}'
TITULO = 'El préstamo médico de Fonasa, paso a paso'
FECHA = '2026-09-22'

def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = t.count(old); assert c == n, f"{path}: esperaba {n}, encontré {c} → {old[:60]!r}"
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8').write(t); print("OK", path)

FAQ = '          <li><a href="../preguntas-frecuentes.html">Preguntas frecuentes sobre el PAD</a></li>\n'
ENL = f'          <li><a href="{SLUG}.html">El préstamo médico de Fonasa, paso a paso</a></li>\n'
for f in ['blog/requisitos-bono-pad.html','blog/recuperacion-abdominoplastia.html',
          'blog/plicaturas-abdominales.html','blog/bono-pad-con-otras-cirugias.html',
          'blog/programa-guatita-de-delantal-o-bono-pad.html']:
    edit(f, [(FAQ, ENL + FAQ, 1)])

edit('blog.html', [
 ('''  {
   "@type": "BlogPosting",
   "headline": "Programa «guatita de delantal» o bono PAD: en qué se diferencian y cuál te conviene",''',
  f'''  {{
   "@type": "BlogPosting",
   "headline": "{TITULO}",
   "url": "{URL}",
   "datePublished": "{FECHA}",
   "dateModified": "{FECHA}",
   "inLanguage": "es-CL",
   "author": {{
    "@type": "Person",
    "name": "Dr. Joaquín Ramírez Sneberger",
    "jobTitle": "Cirujano plástico certificado por CONACEM",
    "url": "https://www.drjoaquinramirez.cl"
   }}
  }},
  {{
   "@type": "BlogPosting",
   "headline": "Programa «guatita de delantal» o bono PAD: en qué se diferencian y cuál te conviene",''', 1),
 ('        <a href="blog/programa-guatita-de-delantal-o-bono-pad.html">',
  f'''        <a href="blog/{SLUG}.html">
          <span class="meta">Septiembre 2026 · 4 min</span>
          <h3>El préstamo médico de Fonasa, paso a paso</h3>
          <p>Quién puede pedirlo, qué exige Fonasa, cómo se pagan las cuotas y
          en qué orden hacer el trámite para que el copago baje a $268.769.</p>
        </a>
        <a href="blog/programa-guatita-de-delantal-o-bono-pad.html">''', 1),
])

edit('publicar.sh', [
 ('  <url><loc>https://www.abdominoplastiapad.com/blog</loc><lastmod>2026-09-15</lastmod>',
  f'  <url><loc>https://www.abdominoplastiapad.com/blog</loc><lastmod>{FECHA}</lastmod>', 1),
 ('  <url><loc>https://www.abdominoplastiapad.com/blog/programa-guatita-de-delantal-o-bono-pad</loc>',
  f'  <url><loc>{URL}</loc><lastmod>{FECHA}</lastmod><priority>0.8</priority></url>\n  <url><loc>https://www.abdominoplastiapad.com/blog/programa-guatita-de-delantal-o-bono-pad</loc>', 1),
])
PY

./publicar.sh
python3 - <<'PY'
import json,re,io,glob
for f in sorted(glob.glob('publicar/*.html')+glob.glob('publicar/blog/*.html')):
    s=io.open(f,encoding='utf-8').read()
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S): json.loads(b)
    malos=[h for h in re.findall(r'href="([^"]+)"',s) if h.endswith('.html')]
    assert not malos,(f,malos)
print("JSON-LD válido y enlaces reescritos en todas las páginas")
PY

if [ $PRUEBA = 1 ]; then
  echo "--- ENSAYO: cambios que se harían ---"; git status --short
  git checkout -q -- . && git clean -fdq blog publicar && ./publicar.sh >/dev/null
  echo "--- ensayo revertido; árbol limpio: $(git status --short | wc -l | tr -d ' ') cambios ---"
  exit 0
fi

git rm -q "programados/$SLUG.html"
git add -A
git commit -q -m "Nuevo artículo: el préstamo médico de Fonasa, paso a paso

Publicacion programada el 2026-09-15 para hoy. Quien puede pedirlo, requisitos
de Fonasa (tramos B-C-D, cotizaciones al dia, codeudores), tope de cuota del
10% del ingreso, forma de pago y el orden del tramite respecto del bono PAD.
Fuentes: ChileAtiende y Fonasa, enlazadas al pie y como citation.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git push -q origin HEAD
echo "PUSH OK — esperando el despliegue"
for i in $(seq 1 12); do
  c=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  if [ "$c" = "200" ]; then echo "EN VIVO: $URL"; exit 0; fi
  perl -e 'select(undef,undef,undef,10)'
done
echo "El push se hizo pero $URL aún no responde 200 (último código: $c). Revisar Vercel."; exit 2

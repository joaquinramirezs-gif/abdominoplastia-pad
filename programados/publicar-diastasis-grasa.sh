#!/bin/zsh
# Publica «¿Guatita de delantal, diástasis o grasa localizada?», programado
# para el 2026-09-29. Idempotente y sin depender del orden con el otro programado.
# Uso:  ./programados/publicar-diastasis-grasa.sh           → publica (commit + push)
#       ./programados/publicar-diastasis-grasa.sh --prueba  → ensayo, deja todo como estaba
set -e
cd "$(dirname "$0")/.."
SLUG=guatita-de-delantal-diastasis-o-grasa
URL="https://www.abdominoplastiapad.com/blog/$SLUG"
PRUEBA=0; [ "$1" = "--prueba" ] && PRUEBA=1

if grep -q "$SLUG" publicar.sh && [ -f "blog/$SLUG.html" ]; then
  echo "Ya está publicado ($URL). Nada que hacer."; exit 0
fi
[ -f "programados/$SLUG.html" ] || { echo "Falta programados/$SLUG.html"; exit 1 }

[ $PRUEBA = 1 ] || git pull -q --ff-only origin HEAD
cp "programados/$SLUG.html" "blog/$SLUG.html"

python3 - "$SLUG" <<'PY'
import io, sys, re, glob, os
SLUG = sys.argv[1]
URL = f'https://www.abdominoplastiapad.com/blog/{SLUG}'
TITULO = '¿Guatita de delantal, diástasis o grasa localizada? Cómo saber qué tienes y qué resuelve el bono PAD'
FECHA = '2026-09-29'

def edit(path, pairs):
    t = io.open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = t.count(old); assert c == n, f"{path}: esperaba {n}, encontré {c} → {old[:60]!r}"
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8').write(t); print("OK", path)

# Si el artículo del préstamo aún no está publicado, no lo enlazamos desde este.
if not os.path.exists('blog/prestamo-medico-fonasa-bono-pad.html'):
    edit(f'blog/{SLUG}.html', [
      ('          <li><a href="prestamo-medico-fonasa-bono-pad.html">El préstamo médico de Fonasa, paso a paso</a></li>\n', '', 1)])
    print("aviso: el préstamo médico no está publicado; se omitió su enlace")

FAQ = '          <li><a href="../preguntas-frecuentes.html">Preguntas frecuentes sobre el PAD</a></li>\n'
ENL = f'          <li><a href="{SLUG}.html">¿Guatita de delantal, diástasis o grasa?</a></li>\n'
for f in sorted(glob.glob('blog/*.html')):
    if f.endswith(f'{SLUG}.html'): continue
    edit(f, [(FAQ, ENL + FAQ, 1)])

edit('blog.html', [
 (' "blogPost": [\n',
  f''' "blogPost": [
  {{
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
''', 1),
 ('      <div class="indice sube" style="--d:.55s">\n',
  f'''      <div class="indice sube" style="--d:.55s">
        <a href="blog/{SLUG}.html">
          <span class="meta">Septiembre 2026 · 4 min</span>
          <h3>¿Guatita de delantal, diástasis o grasa?</h3>
          <p>Tres problemas que se parecen desde afuera, una prueba simple para
          reconocer el tuyo, y cuál de los tres resuelve el bono PAD.</p>
        </a>
''', 1),
])

pm = io.open('publicar.sh', encoding='utf-8').read()
pm, n = re.subn(r'(<loc>https://www\.abdominoplastiapad\.com/blog</loc><lastmod>)[0-9-]+(</lastmod><priority>[0-9.]+</priority></url>\n)',
                lambda m: m.group(1) + FECHA + m.group(2) + f'  <url><loc>{URL}</loc><lastmod>{FECHA}</lastmod><priority>0.8</priority></url>\n', pm)
assert n == 1
io.open('publicar.sh','w',encoding='utf-8').write(pm); print("OK publicar.sh")
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
  git checkout -q -- blog blog.html publicar.sh publicar && git clean -fdq blog publicar && ./publicar.sh >/dev/null
  echo "--- ensayo revertido; árbol limpio: $(git status --short | wc -l | tr -d ' ') cambios ---"
  exit 0
fi

git rm -q "programados/$SLUG.html"
git add -A
git commit -q -m "Nuevo artículo: guatita de delantal, diástasis o grasa localizada

Publicacion programada el 2026-09-15 para hoy. Como reconocer cada uno de
los tres problemas con una prueba simple, cual resuelve la abdominoplastia
PAD (delantal; la plicatura incluida cuando hay diastasis) y cual no
(grasa localizada: lipoaspiracion, fuera del bono). Enlaza a la calculadora
de IMC y a los articulos de plicaturas y cirugias asociadas.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git push -q origin HEAD
echo "PUSH OK — esperando el despliegue"
for i in $(seq 1 12); do
  c=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  if [ "$c" = "200" ]; then echo "EN VIVO: $URL"; exit 0; fi
  perl -e 'select(undef,undef,undef,10)'
done
echo "El push se hizo pero $URL aún no responde 200 (último código: $c). Revisar Vercel."; exit 2

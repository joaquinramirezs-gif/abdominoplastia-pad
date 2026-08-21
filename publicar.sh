#!/bin/zsh
# Regenera publicar/ desde las fuentes. Las fuentes usan enlaces relativos
# (funcionan con doble clic); acá se reescriben a las URLs limpias de Vercel.
cd "$(dirname "$0")"
set -e
rm -rf publicar/blog
mkdir -p publicar/blog

limpia_raiz() {  # páginas de la raíz
  sed 's|href="sitio-web\.html|href="/|g; s|href="blog\.html|href="/blog|g; s|href="preguntas-frecuentes\.html|href="/preguntas-frecuentes|g; s|href="privacidad\.html|href="/privacidad|g; s|href="blog/\([a-z-]*\)\.html|href="/blog/\1|g' "$1"
}
limpia_blog() {  # páginas dentro de blog/
  sed 's|href="\.\./sitio-web\.html|href="/|g; s|href="\.\./blog\.html|href="/blog|g; s|href="\.\./preguntas-frecuentes\.html|href="/preguntas-frecuentes|g; s|href="\.\./privacidad\.html|href="/privacidad|g; s|href="\([a-z][a-z-]*\)\.html|href="/blog/\1|g' "$1"
}

for f in sitio-web.html blog.html preguntas-frecuentes.html privacidad.html; do
  [ "$f" = "sitio-web.html" ] && destino="publicar/index.html" || destino="publicar/${f}"
  limpia_raiz "$f" > "$destino"
done
for f in blog/*.html; do limpia_blog "$f" > "publicar/$f"; done
cp JR-monograma-transparente.png retrato-joaquin-ramirez.jpg icon-192.png publicar/

cat > publicar/robots.txt <<'ROBOTS'
User-agent: *
Allow: /

Sitemap: https://www.abdominoplastiapad.com/sitemap.xml
ROBOTS

cat > publicar/sitemap.xml <<'MAPA'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.abdominoplastiapad.com/</loc><lastmod>2026-08-20</lastmod><priority>1.0</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/preguntas-frecuentes</loc><lastmod>2026-08-20</lastmod><priority>0.9</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/blog</loc><lastmod>2026-08-20</lastmod><priority>0.6</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/blog/bono-pad-con-otras-cirugias</loc><lastmod>2026-08-20</lastmod><priority>0.8</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/blog/requisitos-bono-pad</loc><lastmod>2026-08-20</lastmod><priority>0.8</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/blog/recuperacion-abdominoplastia</loc><lastmod>2026-08-20</lastmod><priority>0.8</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/blog/plicaturas-abdominales</loc><lastmod>2026-08-20</lastmod><priority>0.8</priority></url>
  <url><loc>https://www.abdominoplastiapad.com/privacidad</loc><lastmod>2026-08-20</lastmod><priority>0.3</priority></url>
</urlset>
MAPA

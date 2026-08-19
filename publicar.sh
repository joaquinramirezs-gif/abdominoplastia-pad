#!/bin/zsh
# Regenera publicar/ desde las fuentes. Las fuentes usan enlaces relativos
# (funcionan con doble clic); acá se reescriben a URLs limpias de Vercel.
cd "$(dirname "$0")"
mkdir -p publicar/blog
sed 's|href="sitio-web\.html|href="/|g; s|href="blog\.html|href="/blog|g; s|href="blog/\([a-z-]*\)\.html|href="/blog/\1|g' sitio-web.html > publicar/index.html
sed 's|href="sitio-web\.html|href="/|g; s|href="blog\.html|href="/blog|g; s|href="blog/\([a-z-]*\)\.html|href="/blog/\1|g' blog.html > publicar/blog.html
for f in blog/*.html; do
  sed 's|href="\.\./sitio-web\.html|href="/|g; s|href="\.\./blog\.html|href="/blog|g; s|href="\([a-z][a-z-]*\)\.html|href="/blog/\1|g' "$f" > "publicar/$f"
done
cp JR-monograma-transparente.png retrato-joaquin-ramirez.jpg icon-192.png publicar/

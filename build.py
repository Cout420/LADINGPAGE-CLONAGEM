"""Gera index.html a partir de src/index.html, embutindo as imagens de img/ como data URI.
Os vídeos continuam como arquivos em video/ (pesados demais para embutir)."""
import base64, re, pathlib

root = pathlib.Path(__file__).parent
html = (root / 'src/index.html').read_text()

def embed(m):
    attr, path = m.group(1), m.group(2)
    data = base64.b64encode((root / path).read_bytes()).decode()
    return f'{attr}="data:image/webp;base64,{data}"'

html = re.sub(r'\b(src|poster)="(img/[^"]+\.webp)"', embed, html)
(root / 'index.html').write_text(html)
print(f'index.html: {len(html) // 1024} KB')

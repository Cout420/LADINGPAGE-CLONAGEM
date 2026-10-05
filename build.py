"""Gera a página a partir de src/index.html.

- index.html   → para publicar. Imagens e vídeos como arquivos (img/, video/),
                 com lazy-load abaixo da dobra. Suba index.html + img/ + video/.
- preview.html → arquivo único com tudo embutido, para visualizar sem servidor.
"""
import base64, re, pathlib

root = pathlib.Path(__file__).parent
src = (root / 'src/index.html').read_text()

def b64(path):
    return base64.b64encode((root / path).read_bytes()).decode()

# Publicação: só a imagem do topo carrega na hora; o resto quando chega perto da tela
index = re.sub(r'<img (?![^>]*class="mockup")', '<img loading="lazy" decoding="async" ', src)

# Publicação: <source> WebM (menor no Chrome/Android) com MP4 de reserva (Safari/iPhone)
index = re.sub(r'<video data-video="(\w+)"([^>]*)></video>',
               r'<video\2><source src="video/\1.webm" type="video/webm"><source src="video/\1.mp4" type="video/mp4"></video>', index)
(root / 'index.html').write_text(index)

# Prévia: tudo embutido (imagens em data URI, vídeos em base64 antes do script principal)
src = re.sub(r'\b(src|poster)="(img/[^"]+\.webp)"',
             lambda m: f'{m.group(1)}="data:image/webp;base64,{b64(m.group(2))}"', src)
# vídeos comentados no src não entram na prévia
src = re.sub(r'<!--(?:(?!-->).)*?<video.*?-->', '', src, flags=re.S)
blocos = []
def embute(m):
    nome = m.group(1)
    for ext in ('webm', 'mp4'):
        blocos.append(f'<script type="text/plain" id="v-{nome}-{ext}">{b64(f"video/{nome}.{ext}")}</script>')
    return f'<video data-embed="v-{nome}"'
preview = re.sub(r'<video data-video="(\w+)"', embute, src)
preview = preview.replace('<script>\n// =====', '\n'.join(blocos) + '\n<script>\n// =====', 1)
(root / 'preview.html').write_text(preview)

for f in ('index.html', 'preview.html'):
    print(f, (root / f).stat().st_size // 1024, 'KB')

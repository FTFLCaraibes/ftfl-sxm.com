"""
update_index.py
- Remplace le bloc <style> inline par <link rel="stylesheet" href="/css/styles.css"/>
- Remplace le bloc <script> inline par <script src="/js/scripts.js"></script>
- Remplace toutes les URLs postimg.cc par des chemins locaux /images/

Usage : python update_index.py
"""
import re, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE_DIR, 'index.html')

with open(SOURCE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Supprime <link rel="preconnect" href="https://i.postimg.cc"/>
html = html.replace('  <link rel="preconnect" href="https://i.postimg.cc"/>\n', '')

# 2. Remplace le preload postimg hero image par le chemin local
html = html.replace(
    'href="https://i.postimg.cc/k5gsPtd8/FTFL-WEB-3.webp"',
    'href="/images/FTFL-WEB-3.webp"'
)

# 3. Remplace les URLs OG/Twitter image postimg par l'URL canonique locale
html = html.replace(
    'content="https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    'content="https://www.ftfl-sxm.com/images/Logo%20FTFL.png"'
)

# 4. Remplace les URLs favicon postimg par chemin local
html = html.replace(
    'href="https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    'href="/images/Logo FTFL.png"'
)

# 5. Remplace les URLs postimg dans JSON-LD (logo, image)
html = html.replace(
    '"url": "https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    '"url": "https://www.ftfl-sxm.com/images/Logo%20FTFL.png"'
)
html = html.replace(
    '"image": "https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    '"image": "https://www.ftfl-sxm.com/images/Logo%20FTFL.png"'
)
html = html.replace(
    '"logo": "https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    '"logo": "https://www.ftfl-sxm.com/images/Logo%20FTFL.png"'
)

# 6. Remplace les URLs img src postimg dans le body HTML
html = html.replace(
    'src="https://i.postimg.cc/k50W38Zn/Logo-FTFL.png"',
    'src="/images/Logo FTFL.png"'
)
html = html.replace(
    'src="https://i.postimg.cc/k5gsPtd8/FTFL-WEB-3.webp"',
    'src="/images/FTFL-WEB-3.webp"'
)
html = html.replace(
    'src="https://i.postimg.cc/LXqVnK5R/FTFL-WEB-2.jpg"',
    'src="/images/FTFL-WEB-2.jpg"'
)
html = html.replace(
    'src="https://i.postimg.cc/mZHw4sKy/FTFL-WEB-1.webp"',
    'src="/images/FTFL-WEB-1.webp"'
)

# 7. Remplace le bloc <style>...</style> par <link rel="stylesheet">
html = re.sub(
    r'\n  <style>.*?  </style>',
    '\n  <link rel="stylesheet" href="/css/styles.css"/>',
    html,
    count=1,
    flags=re.DOTALL
)

# 8. Remplace le bloc <script>...</script> (le dernier, avant </body>) par <script src>
html = re.sub(
    r'<script>\n// ── AOS INIT.*?</script>',
    '<script src="/js/scripts.js"></script>',
    html,
    count=1,
    flags=re.DOTALL
)

with open(SOURCE, 'w', encoding='utf-8') as f:
    f.write(html)

print('[OK] index.html mis à jour.')
print('     - Bloc <style> → <link rel="stylesheet" href="/css/styles.css"/>')
print('     - Bloc <script> → <script src="/js/scripts.js"></script>')
print('     - URLs postimg.cc → chemins /images/ locaux')

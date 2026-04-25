"""
generate_lang_pages.py
Génère les pages statiques /en/ /es/ /nl/ /pt/ depuis index.html.
À relancer à chaque fois que index.html est modifié.

Usage : python generate_lang_pages.py
"""
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE  = os.path.join(BASE_DIR, 'index.html')

LANGS = {
    'en': {
        'lang':      'en',
        'og_locale': 'en_US',
        'title':     'FTFL CARAÏBES | Construction Company Saint Martin Island | Earthworks Civil Works SXM',
        'desc':      'FTFL CARAÏBES, your trusted construction company on Saint Martin island (SXM). Earthworks, civil works, exterior works, finishing works and maintenance services on both the French and Dutch sides. Free quote.',
        'canonical': 'https://www.ftfl-sxm.com/en/',
    },
    'es': {
        'lang':      'es',
        'og_locale': 'es_ES',
        'title':     'FTFL CARAÏBES | Empresa de Construcción Saint-Martin | Movimiento de Tierras y Obras SXM',
        'desc':      'FTFL CARAÏBES, su empresa de construcción de referencia en Saint-Martin (SXM). Movimiento de tierras, urbanización y redes, obras exteriores, acabados y multiservicios. Lado francés y holandés. Presupuesto gratuito.',
        'canonical': 'https://www.ftfl-sxm.com/es/',
    },
    'nl': {
        'lang':      'nl',
        'og_locale': 'nl_NL',
        'title':     'FTFL CARAÏBES | Bouwbedrijf Sint Maarten Saint-Martin | Grondwerken en Infrastructuur SXM',
        'desc':      'FTFL CARAÏBES, uw betrouwbare bouwpartner op Sint Maarten / Saint-Martin (SXM). Grondwerken, infrastructuurwerken, buitenaanleg, afbouwwerken en multidiensten aan de Franse en Nederlandse kant. Gratis offerte.',
        'canonical': 'https://www.ftfl-sxm.com/nl/',
    },
    'pt': {
        'lang':      'pt',
        'og_locale': 'pt_PT',
        'title':     'FTFL CARAÏBES | Empresa de Construção Saint-Martin | Terraplenagem Obras SXM',
        'desc':      'FTFL CARAÏBES, a sua empresa de construção de referência em Saint-Martin (SXM). Terraplenagem, infraestruturas e redes, obras exteriores, acabamentos e multisserviços nos lados francês e holandês. Orçamento gratuito.',
        'canonical': 'https://www.ftfl-sxm.com/pt/',
    },
}

def generate(source: str, meta: dict) -> str:
    lang = meta['lang']

    # 1. <html lang="">
    out = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', source, count=1)

    # 2. <title>
    out = re.sub(
        r'<title id="seo-title">[^<]*</title>',
        f'<title id="seo-title">{meta["title"]}</title>',
        out, count=1
    )

    # 3. meta description
    out = re.sub(
        r'(<meta id="seo-desc"\s+name="description"\s+content=")[^"]*(")',
        rf'\g<1>{meta["desc"]}\g<2>',
        out, count=1
    )

    # 4. canonical
    out = re.sub(
        r'(<link id="seo-canonical" rel="canonical" href=")[^"]*(")',
        rf'\g<1>{meta["canonical"]}\g<2>',
        out, count=1
    )

    # 5. og:locale → valeur correcte par langue
    out = out.replace(
        '<meta id="og-locale"   property="og:locale"       content="fr_FR"/>',
        f'<meta id="og-locale"   property="og:locale"       content="{meta["og_locale"]}"/>',
        1
    )

    # 6. JSON-LD @id : préfixer par la langue (ex: /en/#business)
    out = out.replace(
        '"https://www.ftfl-sxm.com/#',
        f'"https://www.ftfl-sxm.com/{lang}/#'
    )

    # 7. Inject window.__LANG juste avant </head>
    inject = f'  <script>window.__LANG = \'{lang}\';</script>\n'
    out = out.replace('</head>', inject + '</head>', 1)

    return out


if __name__ == '__main__':
    with open(SOURCE, 'r', encoding='utf-8') as f:
        source = f.read()

    for lang_code, meta in LANGS.items():
        out_dir = os.path.join(BASE_DIR, lang_code)
        os.makedirs(out_dir, exist_ok=True)

        result = generate(source, meta)

        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)

        print(f'[OK] {lang_code}/index.html  —  {meta["canonical"]}')

    print('\nDone. Pensez à commit + push sur GitHub.')

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

ALL_LOCALES = ['fr_FR', 'en_US', 'es_ES', 'nl_NL', 'pt_PT']

LANGS = {
    'en': {
        'lang':      'en',
        'og_locale': 'en_US',
        'title':     'FTFL CARAÏBES | Construction Company Saint Martin Island | Earthworks Civil Works SXM',
        'desc':      'FTFL CARAÏBES, your trusted construction company on Saint Martin island (SXM). Earthworks, civil works, exterior works, finishing works and maintenance services on both the French and Dutch sides. Free quote.',
        'canonical': 'https://www.ftfl-sxm.com/en/',
        'og_url':    'https://www.ftfl-sxm.com/en/',
        'og_title':  'FTFL CARAÏBES | Construction Company Saint Martin',
        'og_desc':   'One trusted partner for all your construction projects in Saint Martin. Earthworks, civil works, exterior works, finishing works and maintenance services.',
        'tw_title':  'FTFL CARAÏBES | Construction Saint Martin Island',
        'tw_desc':   'One trusted partner for your construction projects in Saint Martin SXM. Earthworks, finishing works and maintenance services.',
    },
    'es': {
        'lang':      'es',
        'og_locale': 'es_ES',
        'title':     'FTFL CARAÏBES | Empresa de Construcción Saint-Martin | Movimiento de Tierras y Obras SXM',
        'desc':      'FTFL CARAÏBES, su empresa de construcción de referencia en Saint-Martin (SXM). Movimiento de tierras, urbanización y redes, obras exteriores, acabados y multiservicios. Lado francés y holandés. Presupuesto gratuito.',
        'canonical': 'https://www.ftfl-sxm.com/es/',
        'og_url':    'https://www.ftfl-sxm.com/es/',
        'og_title':  'FTFL CARAÏBES | Empresa de Construcción Saint-Martin',
        'og_desc':   'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acondicionamiento exterior, acabados y multiservicios.',
        'tw_title':  'FTFL CARAÏBES | Construcción Saint-Martin SXM',
        'tw_desc':   'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acabados y multiservicios.',
    },
    'nl': {
        'lang':      'nl',
        'og_locale': 'nl_NL',
        'title':     'FTFL CARAÏBES | Bouwbedrijf Sint Maarten Saint-Martin | Grondwerken en Infrastructuur SXM',
        'desc':      'FTFL CARAÏBES, uw betrouwbare bouwpartner op Sint Maarten / Saint-Martin (SXM). Grondwerken, infrastructuurwerken, buitenaanleg, afbouwwerken en multidiensten aan de Franse en Nederlandse kant. Gratis offerte.',
        'canonical': 'https://www.ftfl-sxm.com/nl/',
        'og_url':    'https://www.ftfl-sxm.com/nl/',
        'og_title':  'FTFL CARAÏBES | Bouwbedrijf Sint Maarten / Saint-Martin',
        'og_desc':   'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, buitenaanleg, afbouwwerken en multidiensten.',
        'tw_title':  'FTFL CARAÏBES | Bouwbedrijf Sint Maarten SXM',
        'tw_desc':   'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, afbouw en multidiensten.',
    },
    'pt': {
        'lang':      'pt',
        'og_locale': 'pt_PT',
        'title':     'FTFL CARAÏBES | Empresa de Construção Saint-Martin | Terraplenagem Obras SXM',
        'desc':      'FTFL CARAÏBES, a sua empresa de construção de referência em Saint-Martin (SXM). Terraplenagem, infraestruturas e redes, obras exteriores, acabamentos e multisserviços nos lados francês e holandês. Orçamento gratuito.',
        'canonical': 'https://www.ftfl-sxm.com/pt/',
        'og_url':    'https://www.ftfl-sxm.com/pt/',
        'og_title':  'FTFL CARAÏBES | Empresa de Construção Saint-Martin',
        'og_desc':   'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, obras exteriores, acabamentos e multisserviços.',
        'tw_title':  'FTFL CARAÏBES | Construção Saint-Martin SXM',
        'tw_desc':   'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, acabamentos e multisserviços.',
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

    # 6. og:locale:alternate → supprimer la locale courante, ajouter fr_FR
    alternate_locales = [l for l in ALL_LOCALES if l != meta['og_locale']]
    new_alternates = '\n  '.join(
        f'<meta property="og:locale:alternate" content="{loc}"/>'
        for loc in alternate_locales
    )
    out = re.sub(
        r'(<meta property="og:locale:alternate"[^\n]*/>\n?)+',
        new_alternates + '\n  ',
        out, count=1
    )

    # 7. og:url → URL correcte par langue
    out = re.sub(
        r'(<meta property="og:url"\s+content=")[^"]*(")',
        rf'\g<1>{meta["og_url"]}\g<2>',
        out, count=1
    )

    # 8. og:title → traduit par langue
    out = re.sub(
        r'(<meta id="og-title"\s+property="og:title"\s+content=")[^"]*(")',
        rf'\g<1>{meta["og_title"]}\g<2>',
        out, count=1
    )

    # 9. og:description → traduit par langue
    out = re.sub(
        r'(<meta id="og-desc"\s+property="og:description"\s+content=")[^"]*(")',
        rf'\g<1>{meta["og_desc"]}\g<2>',
        out, count=1
    )

    # 10. twitter:title → traduit par langue
    out = re.sub(
        r'(<meta id="tw-title"\s+name="twitter:title"\s+content=")[^"]*(")',
        rf'\g<1>{meta["tw_title"]}\g<2>',
        out, count=1
    )

    # 11. twitter:description → traduit par langue
    out = re.sub(
        r'(<meta id="tw-desc"\s+name="twitter:description"\s+content=")[^"]*(")',
        rf'\g<1>{meta["tw_desc"]}\g<2>',
        out, count=1
    )

    # 12. JSON-LD @id : préfixer par la langue (ex: /en/#business)
    out = out.replace(
        '"https://www.ftfl-sxm.com/#',
        f'"https://www.ftfl-sxm.com/{lang}/#'
    )

    # 13. Liens légaux → version langue
    out = out.replace('href="/mentions-legales/"', f'href="/{lang}/mentions-legales/"', 1)
    out = out.replace('href="/confidentialite/"',  f'href="/{lang}/confidentialite/"',  1)

    # 14. Inject window.__LANG juste avant </head>
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

        print(f'[OK] {lang_code}/index.html  --  {meta["canonical"]}')

    print('\nDone. Pensez a commit + push sur GitHub.')

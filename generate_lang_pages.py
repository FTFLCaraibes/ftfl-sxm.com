"""
generate_lang_pages.py
Génère les pages statiques /en/ /es/ /nl/ /pt/ depuis index.html.
À relancer à chaque fois que index.html est modifié.

Usage : python generate_lang_pages.py
"""
import re
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE  = os.path.join(BASE_DIR, 'index.html')

ALL_LOCALES = ['fr_FR', 'en_US', 'es_ES', 'nl_NL', 'pt_PT']

# Slugs traduits par langue (doit rester synchronisé avec generate_seo_pages.py)
SLUG_TRANSLATIONS = {
    'services':         {'en':'services',       'es':'servicios',           'nl':'diensten',        'pt':'servicos'},
    'approche':         {'en':'approach',        'es':'enfoque',             'nl':'aanpak',          'pt':'abordagem'},
    'valeurs':          {'en':'values',          'es':'valores',             'nl':'waarden',         'pt':'valores'},
    'zone':             {'en':'area',            'es':'zona',                'nl':'werkgebied',      'pt':'zona'},
    'contact':          {'en':'contact',         'es':'contacto',            'nl':'contact',         'pt':'contacto'},
    'mentions-legales': {'en':'legal-notice',    'es':'aviso-legal',         'nl':'juridische-info', 'pt':'mencoes-legais'},
    'confidentialite':  {'en':'privacy-policy',  'es':'politica-privacidad', 'nl':'privacybeleid',   'pt':'politica-privacidade'},
}

LANGS = {
    'en': {
        'lang':      'en',
        'og_locale': 'en_US',
        'title':     'FTFL CARAÏBES – Construction Company Saint Martin / SXM',
        'desc':      'Construction company on Saint Martin / Sint Maarten. Earthworks, civil works, landscaping, finishing. Free quote.',
        'canonical': 'https://www.ftfl-sxm.com/en/',
        'og_url':    'https://www.ftfl-sxm.com/en/',
        'og_title':  'FTFL CARAÏBES | Construction Company Saint Martin',
        'og_desc':   'One trusted partner for all your construction projects in Saint Martin. Earthworks, civil works, exterior works, finishing works and maintenance services.',
        'tw_title':  'FTFL CARAÏBES | Construction Saint Martin Island',
        'tw_desc':   'One trusted partner for your construction projects in Saint Martin SXM. Earthworks, finishing works and maintenance services.',
        'jsonld': {
            'business_desc': 'FTFL CARAÏBES is a versatile construction company based on Saint Martin island, operating on both the French and Dutch sides. Specialising in earthworks, civil works, exterior landscaping, finishing works and maintenance services.',
            'catalog_name': 'FTFL CARAÏBES Construction Services',
            'svc1_name': 'Earthworks & Civil Works',
            'svc1_desc': 'Site clearance, excavation, land levelling, trenching, road works, drainage networks, retaining walls, material transport.',
            'svc2_name': 'Exterior Works',
            'svc2_desc': 'Fencing, gates, terraces, pergolas, swimming pools, landscaping, driveways, car parks, outdoor lighting, rainwater tanks.',
            'svc3_name': 'Finishing & Interior Works',
            'svc3_desc': 'Carpentry, plumbing, tiling, painting, locksmithing, metalwork, interior renovation.',
            'svc4_name': 'Multiservices & Maintenance',
            'svc4_desc': 'Routine maintenance, preventive and curative upkeep, emergency repairs, site clean-up, minor works, service contracts.',
            'fr_side': 'Saint Martin (French side)',
            'payment': 'Cash, Cheque, Bank transfer',
            'website_desc': 'Official website of FTFL CARAÏBES, construction company on Saint Martin island',
            'faq': [
                {'q': 'What types of work does FTFL CARAÏBES carry out in Saint Martin?', 'a': 'FTFL CARAÏBES carries out all types of construction work: earthworks and civil works, exterior landscaping (terraces, pools, fencing), finishing works (plumbing, tiling, painting, carpentry) and multiservices / maintenance. One single point of contact for all your projects.'},
                {'q': 'Does FTFL CARAÏBES operate on the Dutch side (Sint Maarten)?', 'a': 'Yes, FTFL CARAÏBES operates across the entire island of Saint Martin, on both the French and Dutch sides (Sint Maarten). Our team is familiar with both regulatory systems.'},
                {'q': 'How can I get a quote from FTFL CARAÏBES?', 'a': 'You can request a free quote by filling in the contact form on our website ftfl-sxm.com, by calling us on +590 690 43 28 18 or by emailing contact@ftfl-sxm.com. We respond quickly.'},
                {'q': 'Does FTFL CARAÏBES build swimming pools in Saint Martin?', 'a': 'Yes, FTFL CARAÏBES builds swimming pools and basins in Saint Martin, as well as all associated exterior works: pool surrounds, pergolas, terraces, lighting and landscaping.'},
                {'q': "What is FTFL CARAÏBES's service area?", 'a': 'FTFL CARAÏBES operates across the entire island of Saint Martin / Sint Maarten: Orient Bay, Terres Basses, Marigot, Grand Case, Oyster Pond, Anse Marcel, Philipsburg, Simpson Bay, Maho, Cole Bay. Occasional works in Saint-Barthélemy and Anguilla.'},
                {'q': 'Does FTFL CARAÏBES work on the Dutch side of Saint Martin?', 'a': 'Yes, FTFL CARAÏBES operates on both the French and Dutch sides of Saint Martin / Sint Maarten island. Our team is familiar with both regulatory systems and can manage projects anywhere on the island.'},
            ],
            'breadcrumb': ['Home', 'Services', 'Contact'],
        },
    },
    'es': {
        'lang':      'es',
        'og_locale': 'es_ES',
        'title':     'FTFL CARAÏBES – Empresa de Construcción Saint-Martin',
        'desc':      'Empresa de construcción en Saint-Martin / SXM. Movimiento de tierras, urbanización, exteriores, acabados. Presupuesto gratis.',
        'canonical': 'https://www.ftfl-sxm.com/es/',
        'og_url':    'https://www.ftfl-sxm.com/es/',
        'og_title':  'FTFL CARAÏBES | Empresa de Construcción Saint-Martin',
        'og_desc':   'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acondicionamiento exterior, acabados y multiservicios.',
        'tw_title':  'FTFL CARAÏBES | Construcción Saint-Martin SXM',
        'tw_desc':   'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acabados y multiservicios.',
        'jsonld': {
            'business_desc': 'FTFL CARAÏBES es una empresa de construcción versátil establecida en Saint-Martin, que opera en los lados francés y holandés. Especializada en movimiento de tierras, urbanización y redes, obras exteriores, acabados y multiservicios.',
            'catalog_name': 'Servicios de Construcción FTFL CARAÏBES',
            'svc1_name': 'Movimiento de Tierras y Urbanización',
            'svc1_desc': 'Explanación general, desmonte, nivelación, excavaciones, viales y redes, saneamiento, drenaje, muros de contención, transporte de materiales.',
            'svc2_name': 'Obras Exteriores',
            'svc2_desc': 'Vallado, portales, terrazas, pérgolas, piscinas, ajardinamiento, accesos, aparcamientos, iluminación exterior, depósitos de agua pluvial.',
            'svc3_name': 'Obras de Acabado',
            'svc3_desc': 'Carpintería, fontanería, alicatado, pintura, cerrajería, metalistería, renovación de interiores.',
            'svc4_name': 'Multiservicios y Mantenimiento',
            'svc4_desc': 'Mantenimiento rutinario, preventivo y correctivo, reparaciones de emergencia, limpieza de obras, pequeñas reparaciones, contratos de mantenimiento.',
            'fr_side': 'Saint-Martin (parte francesa)',
            'payment': 'Efectivo, Cheque, Transferencia bancaria',
            'website_desc': 'Sitio oficial de FTFL CARAÏBES, empresa de construcción en Saint-Martin',
            'faq': [
                {'q': '¿Qué tipos de trabajos realiza FTFL CARAÏBES en Saint-Martin?', 'a': 'FTFL CARAÏBES realiza todo tipo de trabajos: movimiento de tierras y urbanización, obras exteriores (terrazas, piscinas, vallado), obras de acabado (fontanería, alicatado, pintura, carpintería) y multiservicios / mantenimiento. Un único interlocutor para todos sus proyectos.'},
                {'q': '¿FTFL interviene en el lado holandés (Sint Maarten)?', 'a': 'Sí, FTFL CARAÏBES opera en toda la isla de Saint-Martin, tanto en el lado francés como en el holandés (Sint Maarten). Nuestro equipo domina ambos sistemas normativos.'},
                {'q': '¿Cómo obtener un presupuesto de FTFL CARAÏBES?', 'a': 'Puede solicitar un presupuesto gratuito rellenando el formulario de contacto en ftfl-sxm.com, llamándonos al +590 690 43 28 18 o escribiendo a contact@ftfl-sxm.com. Respondemos con rapidez.'},
                {'q': '¿FTFL CARAÏBES realiza construcción de piscinas en Saint-Martin?', 'a': 'Sí, FTFL CARAÏBES construye piscinas y estanques en Saint-Martin, así como todos los trabajos exteriores asociados: solados de piscina, pérgolas, terrazas, iluminación y paisajismo.'},
                {'q': '¿Cuál es la zona de intervención de FTFL CARAÏBES?', 'a': 'FTFL CARAÏBES opera en toda la isla de Saint-Martin / Sint Maarten: Orient Bay, Terres Basses, Marigot, Grand Case, Oyster Pond, Anse Marcel, Philipsburg, Simpson Bay, Maho, Cole Bay. Intervenciones puntuales en Saint-Barthélemy y Anguilla.'},
                {'q': '¿FTFL CARAÏBES trabaja en el lado holandés de Saint-Martin?', 'a': 'Sí, FTFL CARAÏBES opera en los lados francés y holandés de la isla de Saint-Martin / Sint Maarten. Nuestro equipo domina ambos sistemas normativos y puede gestionar proyectos en cualquier punto de la isla.'},
            ],
            'breadcrumb': ['Inicio', 'Servicios', 'Contacto'],
        },
    },
    'nl': {
        'lang':      'nl',
        'og_locale': 'nl_NL',
        'title':     'FTFL CARAÏBES – Bouwbedrijf Sint Maarten / Saint-Martin',
        'desc':      'Bouwbedrijf op Sint Maarten / Saint-Martin. Grondwerken, infrastructuur, buitenaanleg, afbouw. Gratis offerte.',
        'canonical': 'https://www.ftfl-sxm.com/nl/',
        'og_url':    'https://www.ftfl-sxm.com/nl/',
        'og_title':  'FTFL CARAÏBES | Bouwbedrijf Sint Maarten / Saint-Martin',
        'og_desc':   'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, buitenaanleg, afbouwwerken en multidiensten.',
        'tw_title':  'FTFL CARAÏBES | Bouwbedrijf Sint Maarten SXM',
        'tw_desc':   'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, afbouw en multidiensten.',
        'jsonld': {
            'business_desc': 'FTFL CARAÏBES is een veelzijdig bouwbedrijf gevestigd op Sint Maarten / Saint-Martin, actief aan de Franse en Nederlandse kant. Gespecialiseerd in grondwerken, infrastructuurwerken, buitenaanleg, afbouwwerken en multidiensten.',
            'catalog_name': 'FTFL CARAÏBES Bouwdiensten',
            'svc1_name': 'Grondwerken & Infrastructuur',
            'svc1_desc': 'Grondverzet, ontgraving, nivellering, sleufgraving, wegwerken, rioleringsnetwerken, keermuren, materiaalafvoer.',
            'svc2_name': 'Buitenaanleg',
            'svc2_desc': "Omheiningen, poorten, terrassen, pergola's, zwembaden, landscaping, opritten, parkeerplaatsen, buitenverlichting, regenwateropslagtanks.",
            'svc3_name': 'Afbouwwerken',
            'svc3_desc': 'Schrijnwerk, loodgieterswerk, tegelwerk, schilderwerk, sluitwerk, metaalwerk, binnenrenovatie.',
            'svc4_name': 'Multidiensten & Onderhoud',
            'svc4_desc': 'Regulier onderhoud, preventief en curatief onderhoud, spoedherstellingen, werfopruiming, kleine werken, onderhoudscontracten.',
            'fr_side': 'Saint-Martin (Franse kant)',
            'payment': 'Contant, Cheque, Bankoverschrijving',
            'website_desc': 'Officiële website van FTFL CARAÏBES, bouwbedrijf op Sint Maarten / Saint-Martin',
            'faq': [
                {'q': 'Welke soorten werken voert FTFL CARAÏBES uit op Sint Maarten?', 'a': "FTFL CARAÏBES voert alle soorten bouwwerken uit: grondwerken en infrastructuur, buitenaanleg (terrassen, zwembaden, omheiningen), afbouwwerken (loodgieterswerk, tegelwerk, schilderwerk, schrijnwerk) en multidiensten / onderhoud. Één aanspreekpunt voor al uw projecten."},
                {'q': 'Werkt FTFL CARAÏBES ook aan de Nederlandse kant (Sint Maarten)?', 'a': 'Ja, FTFL CARAÏBES opereert op het gehele eiland Sint Maarten / Saint-Martin, zowel aan de Franse als de Nederlandse kant. Ons team beheerst beide regelgevingssystemen.'},
                {'q': 'Hoe vraag ik een offerte aan bij FTFL CARAÏBES?', 'a': 'U kunt een gratis offerte aanvragen via het contactformulier op ftfl-sxm.com, door ons te bellen op +590 690 43 28 18 of te mailen naar contact@ftfl-sxm.com. Wij reageren snel.'},
                {'q': 'Bouwt FTFL CARAÏBES zwembaden op Sint Maarten?', 'a': "Ja, FTFL CARAÏBES bouwt zwembaden en vijvers op Sint Maarten, evenals alle bijbehorende buitenwerken: zwembadboorden, pergola's, terrassen, verlichting en landscaping."},
                {'q': 'Wat is het werkgebied van FTFL CARAÏBES?', 'a': 'FTFL CARAÏBES opereert op het gehele eiland Sint Maarten / Saint-Martin: Orient Bay, Terres Basses, Marigot, Grand Case, Oyster Pond, Anse Marcel, Philipsburg, Simpson Bay, Maho, Cole Bay. Incidentele werken op Saint-Barthélemy en Anguilla.'},
                {'q': 'Werkt FTFL CARAÏBES aan de Nederlandse kant van Sint Maarten?', 'a': 'Ja, FTFL CARAÏBES opereert aan zowel de Franse als de Nederlandse kant van het eiland Sint Maarten / Saint-Martin. Ons team beheerst beide regelgevingssystemen en kan projecten overal op het eiland beheren.'},
            ],
            'breadcrumb': ['Startpagina', 'Diensten', 'Contact'],
        },
    },
    'pt': {
        'lang':      'pt',
        'og_locale': 'pt_PT',
        'title':     'FTFL CARAÏBES – Construção Saint-Martin / Sint Maarten',
        'desc':      'Empresa de construção em Saint-Martin / SXM. Terraplenagem, infraestruturas, exteriores, acabamentos. Orçamento gratuito.',
        'canonical': 'https://www.ftfl-sxm.com/pt/',
        'og_url':    'https://www.ftfl-sxm.com/pt/',
        'og_title':  'FTFL CARAÏBES | Empresa de Construção Saint-Martin',
        'og_desc':   'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, obras exteriores, acabamentos e multisserviços.',
        'tw_title':  'FTFL CARAÏBES | Construção Saint-Martin SXM',
        'tw_desc':   'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, acabamentos e multisserviços.',
        'jsonld': {
            'business_desc': 'FTFL CARAÏBES é uma empresa de construção versátil estabelecida em Saint-Martin, que opera nos lados francês e holandês. Especializada em terraplenagem, infraestruturas e redes, obras exteriores, acabamentos e multisserviços.',
            'catalog_name': 'Serviços de Construção FTFL CARAÏBES',
            'svc1_name': 'Terraplenagem & Infraestruturas',
            'svc1_desc': 'Terraplenagem geral, escavação, nivelamento, valas, vias e redes, saneamento, drenagem, muros de suporte, transporte de materiais.',
            'svc2_name': 'Obras Exteriores',
            'svc2_desc': 'Vedações, portões, terraços, pérgolas, piscinas, ajardinamento, acessos, estacionamentos, iluminação exterior, reservatórios de água pluvial.',
            'svc3_name': 'Obras de Acabamento',
            'svc3_desc': 'Carpintaria, canalizações, azulejamento, pintura, serralharia, metalurgia, renovação de interiores.',
            'svc4_name': 'Multisserviços e Manutenção',
            'svc4_desc': 'Manutenção de rotina, preventiva e curativa, reparações de emergência, limpeza de obra, pequenos trabalhos, contratos de manutenção.',
            'fr_side': 'Saint-Martin (lado francês)',
            'payment': 'Numerário, Cheque, Transferência bancária',
            'website_desc': 'Site oficial da FTFL CARAÏBES, empresa de construção em Saint-Martin',
            'faq': [
                {'q': 'Que tipos de obras realiza a FTFL CARAÏBES em Saint-Martin?', 'a': 'A FTFL CARAÏBES realiza todos os tipos de obras: terraplenagem e infraestruturas, obras exteriores (terraços, piscinas, vedações), obras de acabamento (canalizações, azulejamento, pintura, carpintaria) e multisserviços / manutenção. Um único ponto de contacto para todos os seus projetos.'},
                {'q': 'A FTFL intervém no lado holandês (Sint Maarten)?', 'a': 'Sim, a FTFL CARAÏBES opera em toda a ilha de Saint-Martin, tanto no lado francês como no holandês (Sint Maarten). A nossa equipa domina ambos os sistemas regulatórios.'},
                {'q': 'Como obter um orçamento da FTFL CARAÏBES?', 'a': 'Pode solicitar um orçamento gratuito preenchendo o formulário de contacto em ftfl-sxm.com, ligando para +590 690 43 28 18 ou escrevendo para contact@ftfl-sxm.com. Respondemos rapidamente.'},
                {'q': 'A FTFL CARAÏBES constrói piscinas em Saint-Martin?', 'a': 'Sim, a FTFL CARAÏBES constrói piscinas e tanques em Saint-Martin, bem como todos os trabalhos exteriores associados: bordas de piscina, pérgolas, terraços, iluminação e paisagismo.'},
                {'q': 'Qual é a zona de intervenção da FTFL CARAÏBES?', 'a': 'A FTFL CARAÏBES opera em toda a ilha de Saint-Martin / Sint Maarten: Orient Bay, Terres Basses, Marigot, Grand Case, Oyster Pond, Anse Marcel, Philipsburg, Simpson Bay, Maho, Cole Bay. Intervenções pontuais em Saint-Barthélemy e Anguilla.'},
                {'q': 'A FTFL CARAÏBES trabalha no lado holandês de Saint-Martin?', 'a': 'Sim, a FTFL CARAÏBES opera nos lados francês e holandês da ilha de Saint-Martin / Sint Maarten. A nossa equipa domina ambos os sistemas regulatórios e pode gerir projetos em qualquer ponto da ilha.'},
            ],
            'breadcrumb': ['Início', 'Serviços', 'Contacto'],
        },
    },
}

def load_translations():
    translations = {}
    for lang in ['fr', 'en', 'es', 'nl', 'pt']:
        path = os.path.join(BASE_DIR, 'i18n', f'{lang}.json')
        with open(path, 'r', encoding='utf-8') as f:
            translations[lang] = json.load(f)
    return translations

TRANSLATIONS = load_translations()


def translate_form_and_modals(html: str, lang: str) -> str:
    t = TRANSLATIONS[lang]
    html = html.replace(
        '<option value="" disabled selected>Sélectionnez un service</option>',
        f'<option value="" disabled selected>{t.get("form.service.placeholder", "Sélectionnez un service")}</option>'
    )
    html = html.replace(
        '<option value="" disabled selected>Partie française ou NL ?</option>',
        f'<option value="" disabled selected>{t.get("form.location.placeholder", "Partie française ou NL ?")}</option>'
    )
    html = html.replace(
        '<option value="" disabled selected>Budget indicatif</option>',
        f'<option value="" disabled selected>{t.get("form.budget.placeholder", "Budget indicatif")}</option>'
    )
    html = html.replace('name="Téléphone"', f'name="{t.get("form.phone.label", "Phone")}"')
    return html


def translate_jsonld(html: str, lang: str, jsonld_meta: dict) -> str:
    """Translate JSON-LD block text fields and update @id prefixes for target language."""
    m = re.search(r'(<script type="application/ld\+json">)\s*(\{.*?\})\s*(</script>)',
                  html, re.DOTALL)
    if not m:
        return html
    try:
        data = json.loads(m.group(2))
    except json.JSONDecodeError:
        return html

    def update_ids(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k == '@id' and isinstance(v, str) and 'ftfl-sxm.com/#' in v:
                    obj[k] = v.replace('ftfl-sxm.com/#', f'ftfl-sxm.com/{lang}/#')
                else:
                    update_ids(v)
        elif isinstance(obj, list):
            for item in obj:
                update_ids(item)

    update_ids(data)

    for node in data.get('@graph', []):
        t = node.get('@type', [])
        if isinstance(t, str):
            t = [t]
        if 'LocalBusiness' in t or 'GeneralContractor' in t:
            node['description'] = jsonld_meta['business_desc']
            cat = node.get('hasOfferCatalog', {})
            cat['name'] = jsonld_meta['catalog_name']
            for i, offer in enumerate(cat.get('itemListElement', []), 1):
                svc = offer.get('itemOffered', {})
                svc['name'] = jsonld_meta[f'svc{i}_name']
                svc['description'] = jsonld_meta[f'svc{i}_desc']
            for place in node.get('areaServed', []):
                if isinstance(place, dict) and 'partie française' in place.get('name', ''):
                    place['name'] = jsonld_meta['fr_side']
            node['paymentAccepted'] = jsonld_meta['payment']
        elif 'WebSite' in t:
            node['description'] = jsonld_meta['website_desc']
        elif 'FAQPage' in t:
            node['mainEntity'] = [
                {'@type': 'Question', 'name': faq['q'],
                 'acceptedAnswer': {'@type': 'Answer', 'text': faq['a']}}
                for faq in jsonld_meta['faq']
            ]
        elif 'BreadcrumbList' in t:
            for item, name in zip(node.get('itemListElement', []), jsonld_meta['breadcrumb']):
                item['name'] = name

    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    indented = serialized.replace('\n', '\n  ')
    replacement = m.group(1) + '\n  ' + indented + '\n  ' + m.group(3)
    return html[:m.start()] + replacement + html[m.end():]


def apply_i18n(html: str, lang_code: str) -> str:
    """Pre-render data-i18n element content with the correct language translation."""
    json_path = os.path.join(BASE_DIR, 'i18n', f'{lang_code}.json')
    if not os.path.exists(json_path):
        return html
    with open(json_path, encoding='utf-8') as f:
        translations = json.load(f)

    open_re = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*\sdata-i18n="([^"]+)"[^>]*>')
    result = []
    pos = 0

    while pos < len(html):
        m = open_re.search(html, pos)
        if m is None:
            result.append(html[pos:])
            break
        tag = m.group(1).lower()
        key = m.group(2)
        open_end = m.end()

        if key not in translations:
            result.append(html[pos:open_end])
            pos = open_end
            continue

        # Stack-based search for the matching closing tag (handles same-tag nesting)
        depth = 1
        search = open_end
        open_pat  = re.compile(rf'<{re.escape(tag)}(?:\s[^>]*)?>',  re.IGNORECASE)
        close_pat = re.compile(rf'</{re.escape(tag)}>', re.IGNORECASE)
        close_m = None

        while depth > 0 and search < len(html):
            om = open_pat.search(html, search)
            cm = close_pat.search(html, search)
            if cm is None:
                break
            if om is not None and om.start() < cm.start():
                depth += 1
                search = om.end()
            else:
                depth -= 1
                if depth == 0:
                    close_m = cm
                else:
                    search = cm.end()

        if close_m is None:
            result.append(html[pos:open_end])
            pos = open_end
            continue

        result.append(html[pos:open_end])   # opening tag (kept as-is with data-i18n attr)
        result.append(translations[key])     # translated inner HTML
        result.append(close_m.group(0))      # closing </tag>
        pos = close_m.end()

    return ''.join(result)


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

    # 6. og:locale:alternate → supprimer TOUTES les anciennes, injecter les bonnes
    # Étape 1 : supprimer toutes les balises og:locale:alternate existantes
    out = re.sub(
        r'\s*<meta\s+property="og:locale:alternate"\s+content="[^"]*"\s*/>',
        '',
        out
    )
    # Étape 2 : reconstituer les 4 balises propres
    alternate_locales = [l for l in ALL_LOCALES if l != meta['og_locale']]
    new_alternates = '\n  '.join(
        f'<meta property="og:locale:alternate" content="{loc}"/>'
        for loc in alternate_locales
    )
    # Étape 3 : les insérer juste après og:locale
    out = re.sub(
        r'(<meta id="og-locale"[^>]*?content="[^"]*"\s*/>)',
        rf'\g<1>\n  {new_alternates}',
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

    # 12. JSON-LD : traduire les champs texte et mettre à jour les @id
    out = translate_jsonld(out, lang, meta['jsonld'])

    # 13. Liens légaux → version langue avec slug traduit
    ml_slug = SLUG_TRANSLATIONS['mentions-legales'][lang]
    cf_slug = SLUG_TRANSLATIONS['confidentialite'][lang]
    out = out.replace('href="/mentions-legales/"', f'href="/{lang}/{ml_slug}/"', 1)
    out = out.replace('href="/confidentialite/"',  f'href="/{lang}/{cf_slug}/"',  1)

    # 14. Section-tag links → version langue avec slug traduit
    for fr_key in ['services', 'approche', 'valeurs', 'zone', 'contact']:
        lang_slug = SLUG_TRANSLATIONS[fr_key][lang]
        out = out.replace(f'href="/{fr_key}/"', f'href="/{lang}/{lang_slug}/"')

    # 14. Inject window.__LANG juste avant </head>
    inject = f'  <script>window.__LANG = \'{lang}\';</script>\n'
    out = out.replace('</head>', inject + '</head>', 1)

    # 15. Pre-render data-i18n elements with translated text (for Googlebot)
    out = apply_i18n(out, lang)

    # 16. Translate form placeholders and phone field name attribute
    out = translate_form_and_modals(out, lang)

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

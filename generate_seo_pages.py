"""
generate_seo_pages.py
Génère 25 pages SEO (5 slugs x 5 langues) + 10 pages légales (2 x 5 langues).
Usage : python generate_seo_pages.py
"""
import os, sys, json, re, datetime
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL  = 'https://www.ftfl-sxm.com'

# ── Configuration langues ─────────────────────────────────────────
LANG_CONFIGS = {
    'fr': {'lang':'fr','prefix':'','home':'/','og_locale':'fr_FR','home_label':'Accueil','flag':'🇫🇷','label':'Français'},
    'en': {'lang':'en','prefix':'/en','home':'/en/','og_locale':'en_US','home_label':'Home','flag':'🇺🇸','label':'English'},
    'es': {'lang':'es','prefix':'/es','home':'/es/','og_locale':'es_ES','home_label':'Inicio','flag':'🇪🇸','label':'Español'},
    'nl': {'lang':'nl','prefix':'/nl','home':'/nl/','og_locale':'nl_NL','home_label':'Startpagina','flag':'🇳🇱','label':'Nederlands'},
    'pt': {'lang':'pt','prefix':'/pt','home':'/pt/','og_locale':'pt_PT','home_label':'Início','flag':'🇵🇹','label':'Português'},
}
ALL_LOCALES = ['fr_FR','en_US','es_ES','nl_NL','pt_PT']
LANG_ORDER  = ['fr','en','es','nl','pt']

# ── Traduction des slugs par langue ──────────────────────────────
SLUG_TRANSLATIONS = {
    'services':          {'fr':'services',        'en':'services',       'es':'servicios',           'nl':'diensten',           'pt':'servicos'},
    'approche':          {'fr':'approche',         'en':'approach',       'es':'enfoque',             'nl':'aanpak',             'pt':'abordagem'},
    'valeurs':           {'fr':'valeurs',          'en':'values',         'es':'valores',             'nl':'waarden',            'pt':'valores'},
    'zone':              {'fr':'zone',             'en':'area',           'es':'zona',                'nl':'werkgebied',         'pt':'zona'},
    'contact':           {'fr':'contact',          'en':'contact',        'es':'contacto',            'nl':'contact',            'pt':'contacto'},
    'mentions-legales':  {'fr':'mentions-legales', 'en':'legal-notice',   'es':'aviso-legal',         'nl':'juridische-info',    'pt':'mencoes-legais'},
    'confidentialite':   {'fr':'confidentialite',  'en':'privacy-policy', 'es':'politica-privacidad', 'nl':'privacybeleid',      'pt':'politica-privacidade'},
}

# ── Slugs des pages SEO ───────────────────────────────────────────
PAGE_SLUGS  = ['services','approche','valeurs','zone','contact']
LEGAL_SLUGS = ['mentions-legales','confidentialite']

# ── Images OG par slug ────────────────────────────────────────────
OG_IMAGES = {
    'services':          f'{BASE_URL}/images/FTFL-WEB-2.jpg',
    'approche':          f'{BASE_URL}/images/FTFL-WEB-3.webp',
    'valeurs':           f'{BASE_URL}/images/FTFL-WEB-3.webp',
    'zone':              f'{BASE_URL}/images/FTFL-WEB-1.webp',
    'contact':           f'{BASE_URL}/images/og-image.jpg',
    'mentions-legales':  f'{BASE_URL}/images/og-image.jpg',
    'confidentialite':   f'{BASE_URL}/images/og-image.jpg',
}

# ── Métadonnées par slug et langue ───────────────────────────────
PAGE_META = {
    'services': {
        'fr': {
            'title':      'Services BTP à Saint-Martin – Terrassement & Second Œuvre',
            'desc':       'Terrassement, VRD, aménagement extérieur, second œuvre et multiservices à Saint-Martin. Devis gratuit.',
            'og_title':   'FTFL CARAÏBES | Services de Construction Saint-Martin',
            'og_desc':    'Terrassement, VRD, aménagement extérieur, second œuvre et multiservices à Saint-Martin. Devis gratuit.',
            'tw_title':   'FTFL CARAÏBES | Services Construction Saint-Martin',
            'tw_desc':    'Terrassement, aménagement extérieur, second œuvre, multiservices SXM.',
            'breadcrumb': 'Services',
        },
        'en': {
            'title':      'Construction Services Saint Martin – Earthworks & Finishing',
            'desc':       'Earthworks, civil works, exterior landscaping, finishing works and maintenance in Saint Martin. Free quote.',
            'og_title':   'FTFL CARAÏBES | Construction Services Saint Martin',
            'og_desc':    'Earthworks, civil works, exterior landscaping, finishing works and maintenance in Saint Martin. Free quote.',
            'tw_title':   'FTFL CARAÏBES | Construction Services Saint Martin',
            'tw_desc':    'Earthworks, landscaping, finishing works and maintenance in Saint Martin SXM.',
            'breadcrumb': 'Services',
        },
        'es': {
            'title':      'Servicios de Construcción Saint-Martin – FTFL CARAÏBES',
            'desc':       'Movimiento de tierras, obras exteriores, acabados y multiservicios en Saint-Martin. Presupuesto gratuito.',
            'og_title':   'FTFL CARAÏBES | Servicios de Construcción Saint-Martin',
            'og_desc':    'Movimiento de tierras, obras exteriores, acabados y multiservicios en Saint-Martin. Presupuesto gratuito.',
            'tw_title':   'FTFL CARAÏBES | Servicios Construcción Saint-Martin',
            'tw_desc':    'Movimiento de tierras, exteriores, acabados y multiservicios en Saint-Martin SXM.',
            'breadcrumb': 'Servicios',
        },
        'nl': {
            'title':      'Bouwdiensten Sint Maarten – Grondwerken & Afbouw',
            'desc':       'Grondwerken, buitenaanleg, afbouwwerken en multidiensten op Sint Maarten / Saint-Martin. Gratis offerte.',
            'og_title':   'FTFL CARAÏBES | Bouwdiensten Sint Maarten / Saint-Martin',
            'og_desc':    'Grondwerken, buitenaanleg, afbouwwerken en multidiensten op Sint Maarten. Gratis offerte.',
            'tw_title':   'FTFL CARAÏBES | Bouwdiensten Sint Maarten',
            'tw_desc':    'Grondwerken, buitenaanleg, afbouw en multidiensten op Sint Maarten SXM.',
            'breadcrumb': 'Diensten',
        },
        'pt': {
            'title':      'Serviços de Construção Saint-Martin – FTFL CARAÏBES',
            'desc':       'Terraplenagem, obras exteriores, acabamentos e multisserviços em Saint-Martin. Orçamento gratuito.',
            'og_title':   'FTFL CARAÏBES | Serviços de Construção Saint-Martin',
            'og_desc':    'Terraplenagem, obras exteriores, acabamentos e multisserviços em Saint-Martin. Orçamento gratuito.',
            'tw_title':   'FTFL CARAÏBES | Serviços Construção Saint-Martin',
            'tw_desc':    'Terraplenagem, exteriores, acabamentos e multisserviços em Saint-Martin SXM.',
            'breadcrumb': 'Serviços',
        },
    },
    'approche': {
        'fr': {
            'title':      'FTFL CARAÏBES | Notre Méthode Construction Saint-Martin',
            'desc':       'Méthode FTFL CARAÏBES : 4 étapes pour vos projets à Saint-Martin — écoute, étude, exécution, livraison. Rigueur et transparence.',
            'og_title':   'FTFL CARAÏBES | Notre Méthode de Travail Saint-Martin',
            'og_desc':    '4 étapes rigoureuses pour vos projets BTP à Saint-Martin : écoute, étude, exécution, livraison.',
            'tw_title':   'FTFL CARAÏBES | Méthode Construction Saint-Martin',
            'tw_desc':    'Écoute, étude, exécution, livraison — méthode FTFL CARAÏBES SXM.',
            'breadcrumb': 'Notre Méthode',
        },
        'en': {
            'title':      'FTFL CARAÏBES | Construction Method Saint Martin',
            'desc':       'The FTFL CARAÏBES method: 4 steps for your projects in Saint Martin — listening, study, execution, delivery.',
            'og_title':   'FTFL CARAÏBES | Our Working Method Saint Martin',
            'og_desc':    '4 rigorous steps to lead your construction projects in Saint Martin: listening, study, execution, delivery.',
            'tw_title':   'FTFL CARAÏBES | Working Method Saint Martin',
            'tw_desc':    'Listening, study, execution, delivery — FTFL CARAÏBES method SXM.',
            'breadcrumb': 'Our Method',
        },
        'es': {
            'title':      'FTFL CARAÏBES | Método de Trabajo Saint-Martin',
            'desc':       'El método FTFL CARAÏBES: 4 etapas clave para sus proyectos de construcción en Saint-Martin — escucha, estudio, ejecución, entrega.',
            'og_title':   'FTFL CARAÏBES | Nuestro Método de Trabajo Saint-Martin',
            'og_desc':    '4 etapas rigurosas para sus proyectos en Saint-Martin: escucha, estudio, ejecución, entrega.',
            'tw_title':   'FTFL CARAÏBES | Método de Trabajo Saint-Martin',
            'tw_desc':    'Escucha, estudio, ejecución, entrega — FTFL CARAÏBES SXM.',
            'breadcrumb': 'Nuestro Método',
        },
        'nl': {
            'title':      'FTFL CARAÏBES | Werkmethode Sint Maarten / Saint-Martin',
            'desc':       'De FTFL CARAÏBES methode: 4 sleutelstappen voor uw bouwprojecten op Sint Maarten — luisteren, studie, uitvoering, oplevering.',
            'og_title':   'FTFL CARAÏBES | Onze Werkmethode Sint Maarten',
            'og_desc':    '4 stappen voor uw bouwprojecten op Sint Maarten: luisteren, studie, uitvoering, oplevering.',
            'tw_title':   'FTFL CARAÏBES | Werkmethode Sint Maarten',
            'tw_desc':    'Luisteren, studie, uitvoering, oplevering — FTFL CARAÏBES SXM.',
            'breadcrumb': 'Onze Methode',
        },
        'pt': {
            'title':      'FTFL CARAÏBES | Método de Trabalho Saint-Martin',
            'desc':       'O método FTFL CARAÏBES: 4 etapas chave para os seus projetos de construção em Saint-Martin — escuta, estudo, execução, entrega.',
            'og_title':   'FTFL CARAÏBES | Nosso Método de Trabalho Saint-Martin',
            'og_desc':    '4 etapas rigorosas para os seus projetos em Saint-Martin: escuta, estudo, execução, entrega.',
            'tw_title':   'FTFL CARAÏBES | Método de Trabalho Saint-Martin',
            'tw_desc':    'Escuta, estudo, execução, entrega — FTFL CARAÏBES SXM.',
            'breadcrumb': 'Nosso Método',
        },
    },
    'valeurs': {
        'fr': {
            'title':      'FTFL CARAÏBES | Nos Valeurs | Construction Saint-Martin',
            'desc':       'Ancrage local, fiabilité, polyvalence et exigence — les 4 piliers de FTFL CARAÏBES à Saint-Martin.',
            'og_title':   'FTFL CARAÏBES | Nos Valeurs',
            'og_desc':    'Ancrage local, fiabilité, polyvalence et exigence — les 4 piliers de FTFL CARAÏBES à Saint-Martin.',
            'tw_title':   'FTFL CARAÏBES | Valeurs Construction Saint-Martin',
            'tw_desc':    'Ancrage local, fiabilité, polyvalence, exigence — FTFL CARAÏBES Saint-Martin.',
            'breadcrumb': 'Nos Valeurs',
        },
        'en': {
            'title':      'FTFL CARAÏBES | Our Values | Construction Company Saint Martin',
            'desc':       'The founding values of FTFL CARAÏBES: local roots, reliability, versatility and excellence. Discover what sets your construction partner apart in Saint Martin.',
            'og_title':   'FTFL CARAÏBES | Our Values',
            'og_desc':    'Local roots, reliability, versatility and excellence — the 4 pillars of FTFL CARAÏBES in Saint Martin.',
            'tw_title':   'FTFL CARAÏBES | Values Construction Saint Martin',
            'tw_desc':    'Local roots, reliability, versatility, excellence — FTFL CARAÏBES Saint Martin.',
            'breadcrumb': 'Our Values',
        },
        'es': {
            'title':      'FTFL CARAÏBES | Nuestros Valores Saint-Martin',
            'desc':       'Arraigo local, fiabilidad, polivalencia y exigencia. Los 4 pilares de FTFL CARAÏBES en Saint-Martin.',
            'og_title':   'FTFL CARAÏBES | Nuestros Valores',
            'og_desc':    'Arraigo local, fiabilidad, polivalencia y exigencia — los 4 pilares de FTFL CARAÏBES en Saint-Martin.',
            'tw_title':   'FTFL CARAÏBES | Valores Construcción Saint-Martin',
            'tw_desc':    'Arraigo local, fiabilidad, polivalencia, exigencia — FTFL CARAÏBES Saint-Martin.',
            'breadcrumb': 'Nuestros Valores',
        },
        'nl': {
            'title':      'FTFL CARAÏBES | Onze Waarden | Bouwbedrijf Sint Maarten Saint-Martin',
            'desc':       'De grondwaarden van FTFL CARAÏBES: lokale verankering, betrouwbaarheid, veelzijdigheid en kwaliteit. Ontdek wat uw bouwpartner op Sint Maarten onderscheidt.',
            'og_title':   'FTFL CARAÏBES | Onze Waarden',
            'og_desc':    'Lokale verankering, betrouwbaarheid, veelzijdigheid en kwaliteit — de 4 pijlers van FTFL CARAÏBES op Sint Maarten.',
            'tw_title':   'FTFL CARAÏBES | Waarden Bouwbedrijf Sint Maarten',
            'tw_desc':    'Lokale verankering, betrouwbaarheid, veelzijdigheid, kwaliteit — FTFL CARAÏBES Sint Maarten.',
            'breadcrumb': 'Onze Waarden',
        },
        'pt': {
            'title':      'FTFL CARAÏBES | Os Nossos Valores Saint-Martin',
            'desc':       'Enraizamento local, fiabilidade, polivalência e exigência. Os 4 pilares da FTFL CARAÏBES em Saint-Martin.',
            'og_title':   'FTFL CARAÏBES | Os Nossos Valores',
            'og_desc':    'Enraizamento local, fiabilidade, polivalência e exigência — os 4 pilares da FTFL CARAÏBES em Saint-Martin.',
            'tw_title':   'FTFL CARAÏBES | Valores Construção Saint-Martin',
            'tw_desc':    'Enraizamento local, fiabilidade, polivalência, exigência — FTFL CARAÏBES Saint-Martin.',
            'breadcrumb': 'Os Nossos Valores',
        },
    },
    'zone': {
        'fr': {
            'title':      "FTFL CARAÏBES | Zone d'Intervention Saint-Martin / SXM",
            'desc':       "Interventions sur toute l'île de Saint-Martin / Sint Maarten. Orient Bay, Marigot, Philipsburg, Grand Case. Côtés français et hollandais.",
            'og_title':   "FTFL CARAÏBES | Zone d'Intervention Saint-Martin",
            'og_desc':    "Interventions sur toute l'île de Saint-Martin / Sint Maarten, côté français et hollandais.",
            'tw_title':   'FTFL CARAÏBES | Zone Intervention SXM',
            'tw_desc':    "Toute l'île Saint-Martin / Sint Maarten, côté français et hollandais.",
            'breadcrumb': "Zone d'Intervention",
        },
        'en': {
            'title':      'FTFL CARAÏBES | Service Area Saint Martin / Sint Maarten',
            'desc':       'Operations across Saint Martin / Sint Maarten island: Orient Bay, Marigot, Philipsburg, Grand Case. French and Dutch sides.',
            'og_title':   'FTFL CARAÏBES | Service Area Saint Martin Sint Maarten',
            'og_desc':    'Operations across the entire island of Saint Martin / Sint Maarten, French and Dutch sides.',
            'tw_title':   'FTFL CARAÏBES | Service Area SXM',
            'tw_desc':    'Entire Saint Martin / Sint Maarten island, French and Dutch sides.',
            'breadcrumb': 'Service Area',
        },
        'es': {
            'title':      'FTFL CARAÏBES | Zona de Intervención Saint-Martin',
            'desc':       'FTFL CARAÏBES opera en toda la isla de Saint-Martin / Sint Maarten: Orient Bay, Marigot, Grand Case, Philipsburg, Simpson Bay y más. Lados francés y holandés.',
            'og_title':   'FTFL CARAÏBES | Zona de Intervención Saint-Martin',
            'og_desc':    'Operaciones en toda la isla de Saint-Martin / Sint Maarten, lados francés y holandés.',
            'tw_title':   'FTFL CARAÏBES | Zona Intervención SXM',
            'tw_desc':    'Toda la isla Saint-Martin / Sint Maarten, lado francés y holandés.',
            'breadcrumb': 'Zona de Intervención',
        },
        'nl': {
            'title':      'FTFL CARAÏBES | Werkgebied Sint Maarten Saint-Martin | Bouw SXM',
            'desc':       'FTFL CARAÏBES opereert op het gehele eiland Sint Maarten / Saint-Martin: Orient Bay, Marigot, Philipsburg, Simpson Bay en meer. Franse en Nederlandse kant.',
            'og_title':   'FTFL CARAÏBES | Werkgebied Sint Maarten / Saint-Martin',
            'og_desc':    'Activiteiten op het gehele eiland Sint Maarten / Saint-Martin, Franse en Nederlandse kant.',
            'tw_title':   'FTFL CARAÏBES | Werkgebied SXM',
            'tw_desc':    'Heel Sint Maarten / Saint-Martin, Franse en Nederlandse kant.',
            'breadcrumb': 'Werkgebied',
        },
        'pt': {
            'title':      'FTFL CARAÏBES | Zona de Intervenção Saint-Martin',
            'desc':       'A FTFL CARAÏBES opera em toda a ilha de Saint-Martin / Sint Maarten: Orient Bay, Marigot, Grand Case, Philipsburg, Simpson Bay e mais. Lados francês e holandês.',
            'og_title':   'FTFL CARAÏBES | Zona de Intervenção Saint-Martin',
            'og_desc':    'Operações em toda a ilha de Saint-Martin / Sint Maarten, lados francês e holandês.',
            'tw_title':   'FTFL CARAÏBES | Zona de Intervenção SXM',
            'tw_desc':    'Toda a ilha Saint-Martin / Sint Maarten, lado francês e holandês.',
            'breadcrumb': 'Zona de Intervenção',
        },
    },
    'contact': {
        'fr': {
            'title':      'FTFL CARAÏBES | Contact & Devis Gratuit Saint-Martin',
            'desc':       'Devis gratuit pour votre projet de construction à Saint-Martin. Réponse sous 24h. Téléphone, WhatsApp et email.',
            'og_title':   'FTFL CARAÏBES | Contact & Devis Gratuit',
            'og_desc':    'Devis gratuit pour votre construction à Saint-Martin. Réponse sous 24h. Téléphone, WhatsApp, email.',
            'tw_title':   'FTFL CARAÏBES | Devis Gratuit Saint-Martin',
            'tw_desc':    'Devis gratuit pour votre construction à Saint-Martin. Réponse sous 24h.',
            'breadcrumb': 'Contact',
        },
        'en': {
            'title':      'FTFL CARAÏBES | Contact & Free Quote Saint Martin',
            'desc':       'Contact FTFL CARAÏBES for your construction project in Saint Martin. Free quote with no commitment. 24h response. Phone, WhatsApp, email and online form.',
            'og_title':   'FTFL CARAÏBES | Contact & Free Quote',
            'og_desc':    'Free quote for your construction in Saint Martin. 24h response. Phone, WhatsApp, email.',
            'tw_title':   'FTFL CARAÏBES | Free Quote Saint Martin',
            'tw_desc':    'Free quote for your construction project in Saint Martin. 24h response.',
            'breadcrumb': 'Contact',
        },
        'es': {
            'title':      'FTFL CARAÏBES | Contacto & Presupuesto Gratuito',
            'desc':       'Presupuesto gratuito para su proyecto en Saint-Martin. Respuesta en 24h. Teléfono, WhatsApp y email.',
            'og_title':   'FTFL CARAÏBES | Contacto & Presupuesto Gratuito',
            'og_desc':    'Presupuesto gratuito para su construcción en Saint-Martin. Respuesta en 24h. Teléfono, WhatsApp, email.',
            'tw_title':   'FTFL CARAÏBES | Presupuesto Gratuito Saint-Martin',
            'tw_desc':    'Presupuesto gratuito para su construcción en Saint-Martin. Respuesta en 24h.',
            'breadcrumb': 'Contacto',
        },
        'nl': {
            'title':      'FTFL CARAÏBES | Contact & Gratis Offerte Sint Maarten',
            'desc':       'Neem contact op met FTFL CARAÏBES voor uw bouwproject op Sint Maarten. Gratis offerte zonder verplichtingen. Antwoord binnen 24u. Telefoon, WhatsApp, e-mail.',
            'og_title':   'FTFL CARAÏBES | Contact & Gratis Offerte',
            'og_desc':    'Gratis offerte voor uw bouw op Sint Maarten. Antwoord binnen 24u. Telefoon, WhatsApp, e-mail.',
            'tw_title':   'FTFL CARAÏBES | Gratis Offerte Sint Maarten',
            'tw_desc':    'Gratis offerte voor uw bouwproject op Sint Maarten. Antwoord binnen 24u.',
            'breadcrumb': 'Contact',
        },
        'pt': {
            'title':      'FTFL CARAÏBES | Contacto & Orçamento Gratuito',
            'desc':       'Orçamento gratuito para o seu projeto em Saint-Martin. Resposta em 24h. Telefone, WhatsApp e email.',
            'og_title':   'FTFL CARAÏBES | Contacto & Orçamento Gratuito',
            'og_desc':    'Orçamento gratuito para a sua construção em Saint-Martin. Resposta em 24h. Telefone, WhatsApp, email.',
            'tw_title':   'FTFL CARAÏBES | Orçamento Gratuito Saint-Martin',
            'tw_desc':    'Orçamento gratuito para a sua construção em Saint-Martin. Resposta em 24h.',
            'breadcrumb': 'Contacto',
        },
    },
}

LEGAL_META = {
    'mentions-legales': {
        'fr': {'title':'FTFL CARAÏBES | Mentions Légales','desc':'Mentions légales de FTFL CARAÏBES, SAS — SIREN 102 641 339 — 34 rue de l\'Escale, Oyster Pond, 97150 Saint-Martin.','breadcrumb':'Mentions Légales'},
        'en': {'title':'FTFL CARAÏBES | Legal Notice','desc':'Legal notice for FTFL CARAÏBES, SAS — SIREN 102 641 339 — 34 rue de l\'Escale, Oyster Pond, 97150 Saint-Martin.','breadcrumb':'Legal Notice'},
        'es': {'title':'FTFL CARAÏBES | Aviso Legal','desc':'Aviso legal de FTFL CARAÏBES, SAS — SIREN 102 641 339 — 34 rue de l\'Escale, Oyster Pond, 97150 Saint-Martin.','breadcrumb':'Aviso Legal'},
        'nl': {'title':'FTFL CARAÏBES | Juridische Informatie','desc':'Juridische informatie van FTFL CARAÏBES, SAS — SIREN 102 641 339 — 34 rue de l\'Escale, Oyster Pond, 97150 Saint-Martin.','breadcrumb':'Juridische Informatie'},
        'pt': {'title':'FTFL CARAÏBES | Menções Legais','desc':'Menções legais da FTFL CARAÏBES, SAS — SIREN 102 641 339 — 34 rue de l\'Escale, Oyster Pond, 97150 Saint-Martin.','breadcrumb':'Menções Legais'},
    },
    'confidentialite': {
        'fr': {'title':'FTFL CARAÏBES | Politique de Confidentialité','desc':'Politique de confidentialité de FTFL CARAÏBES : données collectées, droits RGPD, contact.','breadcrumb':'Politique de Confidentialité'},
        'en': {'title':'FTFL CARAÏBES | Privacy Policy','desc':'Privacy policy for FTFL CARAÏBES: data collected, GDPR rights, contact information.','breadcrumb':'Privacy Policy'},
        'es': {'title':'FTFL CARAÏBES | Política de Privacidad','desc':'Política de privacidad de FTFL CARAÏBES: datos recopilados, derechos RGPD, contacto.','breadcrumb':'Política de Privacidad'},
        'nl': {'title':'FTFL CARAÏBES | Privacybeleid','desc':'Privacybeleid van FTFL CARAÏBES: verzamelde gegevens, AVG-rechten, contactinformatie.','breadcrumb':'Privacybeleid'},
        'pt': {'title':'FTFL CARAÏBES | Política de Privacidade','desc':'Política de privacidade da FTFL CARAÏBES: dados recolhidos, direitos RGPD, contacto.','breadcrumb':'Política de Privacidade'},
    },
}


# ── Constructeurs de blocs ────────────────────────────────────────

def slug_url(lang_code, slug):
    """URL canonique pour un slug dans une langue (slug traduit)."""
    translated = SLUG_TRANSLATIONS[slug][lang_code]
    if lang_code == 'fr':
        return f'{BASE_URL}/{translated}/'
    return f'{BASE_URL}/{lang_code}/{translated}/'

def build_hreflang(slug):
    """Blocs hreflang pour un slug (identiques quelle que soit la langue)."""
    lines = []
    for lk in LANG_ORDER:
        url = slug_url(lk, slug)
        lines.append(f'  <link rel="alternate" hreflang="{lk}" href="{url}"/>')
    fr_slug = SLUG_TRANSLATIONS[slug]['fr']
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/{fr_slug}/"/>')
    return '\n'.join(lines)

def build_head(lc, slug, meta, og_image):
    lang      = lc['lang']
    canonical = slug_url(lang, slug)
    alt_locales = [l for l in ALL_LOCALES if l != lc['og_locale']]
    alternates  = '\n  '.join(f'<meta property="og:locale:alternate" content="{l}"/>' for l in alt_locales)
    window_lang = f'\n  <script>window.__LANG = \'{lang}\';</script>' if lang != 'fr' else ''
    return f"""  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>
  <meta name="author"    content="FTFL CARAÏBES"/>
  <meta name="copyright" content="FTFL CARAÏBES 2025"/>
  <meta name="color-scheme" content="dark light"/>

  <!-- GEO -->
  <meta name="geo.region"    content="FR-MF"/>
  <meta name="geo.placename" content="Saint-Martin, Caraïbes"/>
  <meta name="geo.position"  content="18.0735;-63.0820"/>
  <meta name="ICBM"          content="18.0735, -63.0820"/>

  <!-- HREFLANG -->
{build_hreflang(slug)}

  <!-- SEO -->
  <title id="seo-title">{meta['title']}</title>
  <meta id="seo-desc" name="description" content="{meta['desc']}"/>
  <link id="seo-canonical" rel="canonical" href="{canonical}"/>

  <!-- OPEN GRAPH -->
  <meta id="og-title"  property="og:title"       content="{meta['og_title']}"/>
  <meta id="og-desc"   property="og:description"  content="{meta['og_desc']}"/>
  <meta id="og-locale" property="og:locale"       content="{lc['og_locale']}"/>
  <meta property="og:locale:alternate" content="{alt_locales[0]}"/>
  <meta property="og:locale:alternate" content="{alt_locales[1]}"/>
  <meta property="og:locale:alternate" content="{alt_locales[2]}"/>
  <meta property="og:locale:alternate" content="{alt_locales[3]}"/>
  <meta property="og:type"             content="website"/>
  <meta property="og:url"              content="{canonical}"/>
  <meta property="og:image"            content="{og_image}"/>
  <meta property="og:image:alt"        content="FTFL CARAÏBES"/>
  <meta property="og:site_name"        content="FTFL CARAÏBES"/>

  <!-- TWITTER -->
  <meta name="twitter:card"  content="summary_large_image"/>
  <meta id="tw-title" name="twitter:title"       content="{meta['tw_title']}"/>
  <meta id="tw-desc"  name="twitter:description"  content="{meta['tw_desc']}"/>
  <meta name="twitter:image" content="{og_image}"/>

  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico"/>
  <link rel="icon" type="image/png" sizes="16x16" href="/images/favicons/favicon-16x16.png"/>
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicons/favicon-32x32.png"/>
  <link rel="icon" type="image/png" sizes="48x48" href="/images/favicons/favicon-48x48.png"/>
  <link rel="apple-touch-icon" sizes="180x180" href="/images/favicons/apple-touch-icon.png"/>
  <link rel="manifest" href="/site.webmanifest"/>
  <meta name="theme-color" content="#02602A"/>
  <meta name="msapplication-TileColor" content="#02602A"/>

  <!-- FONTS & CSS -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link rel="dns-prefetch" href="https://unpkg.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="https://unpkg.com/aos@2.3.4/dist/aos.css"/>
  <link rel="stylesheet" href="/css/styles.css"/>{window_lang}"""


def build_breadcrumb_schema(lc, slug, meta, canonical):
    home_url  = f'{BASE_URL}{lc["home"]}'
    return f"""  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"{lc['home_label']}","item":"{home_url}"}},
      {{"@type":"ListItem","position":2,"name":"{meta['breadcrumb']}","item":"{canonical}"}}
    ]
  }}
  </script>"""


def build_navbar(lc, slug):
    lang    = lc['lang']
    home    = lc['home']
    prefix  = lc['prefix']
    _contact_slug = SLUG_TRANSLATIONS['contact'][lang]
    contact_url = f'{prefix}/{_contact_slug}/' if lang != 'fr' else f'/{_contact_slug}/'

    lang_options = ''
    for lk in LANG_ORDER:
        lv = LANG_CONFIGS[lk]
        active = 'active' if lk == lang else ''
        other_slug = SLUG_TRANSLATIONS[slug][lk]
        other_url = f'/{lk}/{other_slug}/' if lk != 'fr' else f'/{other_slug}/'
        lang_options += f'          <a class="lang-option {active}" data-lang="{lk}" href="{other_url}"><span class="lang-flag">{lv["flag"]}</span> {lv["label"]}</a>\n'

    return f"""<!-- PRELOADER -->
<div id="preloader">
  <img class="pl-logo" src="/images/Logo FTFL.png" alt="FTFL CARAÏBES"/>
  <div class="pl-bar"><div class="pl-bar-fill"></div></div>
  <span class="pl-label">Loading</span>
</div>

<!-- SCROLL PROGRESS -->
<div id="scrollProgress"></div>

<!-- CUSTOM CURSOR -->
<div class="cursor-dot" id="cursorDot"></div>
<div class="cursor-ring" id="cursorRing"></div>

<!-- MOBILE NAV -->
<div class="mobile-nav" id="mobileNav">
  <div class="mobile-nav-close" onclick="closeMobileNav()">✕</div>
  <a href="{home}#about"    onclick="closeMobileNav()" data-i18n="nav.about">À propos</a>
  <a href="{home}#services" onclick="closeMobileNav()" data-i18n="nav.services">Services</a>
  <a href="{home}#approach" onclick="closeMobileNav()" data-i18n="nav.approach">Approche</a>
  <a href="{home}#values"   onclick="closeMobileNav()" data-i18n="nav.values">Valeurs</a>
  <a href="{home}#zone"     onclick="closeMobileNav()" data-i18n="nav.zone">Zone</a>
  <a href="{contact_url}"   onclick="closeMobileNav()" data-i18n="nav.cta">Contactez-nous</a>
</div>

<!-- NAVBAR -->
<nav class="navbar" id="navbar">
  <div class="container">
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="{home}" class="navbar-logo">
        <img src="/images/Logo FTFL.png" alt="FTFL CARAÏBES" width="140" height="56"/>
      </a>
      <div class="lang-switcher" id="langSwitcher">
        <div class="lang-btn" onclick="toggleLang()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span id="langCurrent">{lang.upper()}</span>
          <svg class="chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="lang-dropdown" id="langDropdown">
{lang_options}        </div>
      </div>
    </div>
    <ul class="nav-links">
      <li><a href="{home}#about"    data-i18n="nav.about">À propos</a></li>
      <li><a href="{home}#services" data-i18n="nav.services">Services</a></li>
      <li><a href="{home}#approach" data-i18n="nav.approach">Approche</a></li>
      <li><a href="{home}#values"   data-i18n="nav.values">Valeurs</a></li>
      <li><a href="{home}#zone"     data-i18n="nav.zone">Zone</a></li>
    </ul>
    <div class="navbar-cta">
      <a href="{contact_url}" class="btn btn-primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg>
        <span data-i18n="nav.cta">Contactez-nous</span>
      </a>
    </div>
    <div class="burger" onclick="openMobileNav()">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>"""


def build_footer(lc):
    prefix = lc['prefix']
    def p(s):
        ts = SLUG_TRANSLATIONS[s][lc['lang']]
        return f'{prefix}/{ts}/' if lc['lang'] != 'fr' else f'/{ts}/'
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="footer-logo"><img src="/images/Logo FTFL.png" alt="FTFL CARAÏBES"/></div>
        <p data-i18n="ft.desc">Un seul partenaire pour tous vos travaux à Saint-Martin.</p>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.svc">Services</h4>
        <ul>
          <li><a href="{p('services')}" data-i18n="ft.svc1">Terrassement & VRD</a></li>
          <li><a href="{p('services')}" data-i18n="ft.svc2">Aménagement Extérieur</a></li>
          <li><a href="{p('services')}" data-i18n="ft.svc3">Second Œuvre</a></li>
          <li><a href="{p('services')}" data-i18n="ft.svc4">Multiservices</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.co">Entreprise</h4>
        <ul>
          <li><a href="{lc['home']}" data-i18n="ft.about">À propos</a></li>
          <li><a href="{p('valeurs')}" data-i18n="ft.vals">Nos valeurs</a></li>
          <li><a href="{p('approche')}" data-i18n="ft.app">Notre approche</a></li>
          <li><a href="{lc['home']}" data-i18n="ft.team">L'équipe</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.ct">Contact</h4>
        <ul>
          <li><a href="tel:+590690432818">+590 690 43 28 18</a></li>
          <li><a href="https://wa.me/590690432818" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></li>
          <li><a href="https://www.linkedin.com/company/ftfl-cara%C3%AFbes/" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="{p('contact')}" data-i18n="ft.quote">Demander un devis</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span data-i18n="ft.copy">© 2025 FTFL CARAÏBES — Tous droits réservés</span>
      <div class="footer-legal-links">
        <a href="{p('mentions-legales')}" data-i18n="ft.legal1">Mentions légales</a>
        <span aria-hidden="true">·</span>
        <a href="{p('confidentialite')}" data-i18n="ft.legal2">Politique de confidentialité</a>
      </div>
      <span data-i18n="ft.slogan">Saint-Martin · Sint Maarten · Caraïbes 🌴</span>
    </div>
  </div>
</footer>"""


# ── Contenu des sections ──────────────────────────────────────────

def content_services(lc):
    home = lc['home']
    home_label = lc['home_label']
    breadcrumb = PAGE_META['services'][lc['lang']]['breadcrumb']
    _cs = SLUG_TRANSLATIONS['contact'][lc['lang']]
    contact = f'{lc["prefix"]}/{_cs}/' if lc['lang'] != 'fr' else f'/{_cs}/'
    lang = lc['lang']
    T = {
        'fr': {
            'svc1_tag': 'Terrassement &amp; VRD',
            'svc1_box_h': 'Exemples de projets réalisés',
            'svc1_p1': "Avant toute construction, le sol doit être préparé avec rigueur. FTFL CARAÏBES maîtrise l'ensemble des opérations de terrassement propres aux contraintes insulaires de Saint-Martin : sols argileux, pentes prononcées, proximité de la mer, risques cycloniques.",
            'svc1_p2': "Nos équipes interviennent pour la préparation des fondations, le décaissement des volumes nécessaires, le drainage des eaux pluviales et l'aménagement des voiries. Nous prenons également en charge les réseaux d'assainissement, l'enrochement des talus et la gestion des terres excavées.",
            'svc1_tags': '<span class="service-tag">Terrassement général</span><span class="service-tag">Décaissement</span><span class="service-tag">Fouilles &amp; fondations</span><span class="service-tag">Voiries &amp; accès</span><span class="service-tag">Assainissement</span><span class="service-tag">Enrochement &amp; talus</span><span class="service-tag">Drainage pluvial</span><span class="service-tag">Réseaux enterrés</span>',
            'svc1_i1': "Terrassement d'une villa à Orient Bay (1 200 m²) avec création de voie d'accès et pose de citernes",
            'svc1_i2': "Réseaux VRD pour lotissement à Terres Basses : assainissement, eau, électricité",
            'svc1_i3': "Drainage et stabilisation d'un talus à Oyster Pond suite aux pluies cycloniques",
            'svc1_i4': "Création de voiries et parkings pour un complexe hôtelier à Simpson Bay",
            'svc2_tag': 'Aménagement Extérieur',
            'svc2_box_h': 'Réalisations emblématiques',
            'svc2_p1': "L'extérieur est la première impression de votre propriété. FTFL CARAÏBES conçoit et réalise des espaces extérieurs à la hauteur du cadre caribéen : piscines, terrasses, pergolas, jardins paysagers et clôtures, tous conçus pour résister aux vents tropicaux et aux UV intenses de Saint-Martin.",
            'svc2_p2': "Nous intervenons autant pour de petits aménagements que pour des projets d'envergure (complexes hôteliers, lotissements, villas de prestige). Notre connaissance des plantes locales, des matériaux adaptés au climat tropical et des techniques de gestion de l'eau de pluie nous permet de proposer des solutions durables et esthétiques.",
            'svc2_tags': '<span class="service-tag">Piscines &amp; spas</span><span class="service-tag">Terrasses &amp; dallages</span><span class="service-tag">Pergolas &amp; ombrières</span><span class="service-tag">Clôtures &amp; portails</span><span class="service-tag">Jardins paysagers</span><span class="service-tag">Éclairage extérieur</span><span class="service-tag">Citernes &amp; récupération eau</span><span class="service-tag">Allées &amp; parkings</span>',
            'svc2_i1': "Construction d'une piscine à débordement avec terrasse de 200 m² à Terres Basses",
            'svc2_i2': "Aménagement complet d'un jardin tropical avec pergola, clôture et éclairage à Grand Case",
            'svc2_i3': "Pose de portail automatique et clôture sur mesure pour villa sécurisée à Philipsburg",
            'svc2_i4': "Création d'espace BBQ, lounges et abri de voiture à Maho Beach",
            'svc3_tag': 'Second Œuvre',
            'svc3_box_h': 'Ce que nos clients nous confient',
            'svc3_p1': "Le second œuvre regroupe tous les travaux de finition intérieure qui donnent vie à votre bâtiment. FTFL CARAÏBES prend en charge l'ensemble de ces corps d'état, assurant une coordination totale entre artisans et corps de métiers — ce qui vous évite d'avoir à gérer une multitude d'intervenants.",
            'svc3_p2': "Menuiserie, plomberie, électricité, carrelage, peinture, serrurerie : chaque prestation est exécutée par des professionnels formés aux normes locales (DTU, réglementation des deux côtés de l'île). Nous intervenons aussi bien sur des constructions neuves que sur des rénovations de villas existantes.",
            'svc3_tags': '<span class="service-tag">Menuiserie bois &amp; alu</span><span class="service-tag">Plomberie &amp; sanitaires</span><span class="service-tag">Électricité &amp; domotique</span><span class="service-tag">Carrelage &amp; revêtements</span><span class="service-tag">Peinture intérieure/extérieure</span><span class="service-tag">Serrurerie &amp; métallerie</span><span class="service-tag">Isolation thermique</span><span class="service-tag">Rénovation complète</span>',
            'svc3_i1': "Rénovation complète d'une villa de 280 m² à Anse Marcel : plomberie, électricité, carrelage, peinture",
            'svc3_i2': "Installation de menuiseries aluminium anti-cyclone pour un immeuble commercial à Marigot",
            'svc3_i3': "Remise aux normes électriques et plomberie pour une location saisonnière à Simpson Bay",
            'svc3_i4': "Pose de carrelage grand format et douche italienne pour un boutique-hôtel à Dutch Quarter",
            'svc4_tag': 'Multiservices',
            'svc4_box_h': 'Nos contrats de maintenance',
            'svc4_p1': "À Saint-Martin, nombreux sont les propriétaires qui résident à l'étranger une partie de l'année. FTFL CARAÏBES propose une offre de multiservices spécialement pensée pour eux : un interlocuteur unique, disponible, qui surveille, entretient et fait intervenir les bons artisans au bon moment.",
            'svc4_p2': "Nous gérons également les urgences : fuite d'eau, problème électrique, dommages après tempête. Notre réseau de partenaires locaux nous permet d'intervenir rapidement, avec un reporting photo systématique envoyé au propriétaire. Idéal pour les investisseurs, les hôteliers et les expatriés.",
            'svc4_tags': '<span class="service-tag">Maintenance préventive</span><span class="service-tag">Dépannage urgence</span><span class="service-tag">Nettoyage &amp; remise en état</span><span class="service-tag">Petits travaux</span><span class="service-tag">Conciergerie propriété</span><span class="service-tag">Suivi photo à distance</span>',
            'svc4_i1': '<strong style="color:#fff;">Contrat saisonnier</strong> — visite mensuelle, rapport d\'état, petits travaux inclus',
            'svc4_i2': '<strong style="color:#fff;">Préparation cyclonique</strong> — sécurisation des ouvertures, évacuation du mobilier ext.',
            'svc4_i3': '<strong style="color:#fff;">Remise en état post-passage</strong> — intervention rapide après intempéries tropicales',
            'svc4_i4': '<strong style="color:#fff;">Conciergerie travaux</strong> — gestion complète pendant l\'absence des propriétaires',
            'faq_h': 'Questions fréquentes',
            'faq1_q': "Intervenez-vous aussi côté hollandais (Sint Maarten) ?",
            'faq1_a': "Oui, nous intervenons sur toute l'île — partie française (Saint-Martin, collectivité 97150) et partie hollandaise (Sint Maarten). Nos équipes maîtrisent les deux cadres réglementaires et vous simplifient toutes les démarches administratives.",
            'faq2_q': "Quel est le délai pour obtenir un devis ?",
            'faq2_a': "Nous nous engageons à revenir vers vous sous 24h ouvrées après réception de votre demande. Pour les projets complexes nécessitant une visite de terrain, nous fixons un rendez-vous dans les 48h et vous remettons un devis détaillé sous 5 jours.",
            'faq3_q': "Pouvez-vous gérer l'ensemble du chantier, de A à Z ?",
            'faq3_a': "C'est exactement notre valeur ajoutée. FTFL CARAÏBES peut prendre en charge la totalité d'un projet : terrassement, gros œuvre, aménagement extérieur, second œuvre et maintenance. Un seul contrat, un seul interlocuteur, un seul responsable.",
            'faq4_q': "Travaillez-vous avec les propriétaires absents de l'île ?",
            'faq4_a': "Oui, nous avons développé une offre spécifique pour les propriétaires non-résidents : suivi photo quotidien, reporting par WhatsApp ou email, coordination avec les gestionnaires locaux. Vous êtes informé à chaque étape sans avoir à vous déplacer.",
            'cta': "Demander un devis gratuit — Réponse sous 24h",
        },
        'en': {
            'svc1_tag': 'Earthworks &amp; Civil Works',
            'svc1_box_h': 'Project highlights',
            'svc1_p1': "Before any construction begins, the ground must be carefully prepared. FTFL CARAÏBES handles all earthwork operations suited to the island conditions of Saint Martin: clay soils, steep slopes, coastal proximity and hurricane risks.",
            'svc1_p2': "Our teams handle foundation preparation, excavation works, stormwater drainage and road development. We also take care of sanitation networks, slope protection and management of excavated material.",
            'svc1_tags': '<span class="service-tag">General earthworks</span><span class="service-tag">Excavation</span><span class="service-tag">Foundations &amp; trenching</span><span class="service-tag">Roads &amp; access</span><span class="service-tag">Drainage systems</span><span class="service-tag">Retaining walls &amp; slopes</span><span class="service-tag">Stormwater drainage</span><span class="service-tag">Underground networks</span>',
            'svc1_i1': "Earthworks for a villa in Orient Bay (1,200 m²) including access road construction and water tank installation",
            'svc1_i2': "Civil and utility networks for a housing development in Terres Basses: sewage, water, electricity",
            'svc1_i3': "Slope drainage and stabilisation in Oyster Pond following cyclonic rainfall",
            'svc1_i4': "Road and car park construction for a hotel complex in Simpson Bay",
            'svc2_tag': 'Exterior Works',
            'svc2_box_h': 'Landmark achievements',
            'svc2_p1': "The exterior is the first impression your property makes. FTFL CARAÏBES designs and builds outdoor spaces worthy of the Caribbean setting: pools, terraces, pergolas, landscaped gardens and fencing — all engineered to withstand tropical winds and intense UV exposure on Saint Martin.",
            'svc2_p2': "We handle projects of all sizes — from small garden improvements to large-scale developments (hotel complexes, residential estates, prestige villas). Our knowledge of local plants, climate-resistant materials and rainwater management enables us to deliver lasting, beautiful solutions.",
            'svc2_tags': '<span class="service-tag">Pools &amp; spas</span><span class="service-tag">Terraces &amp; paving</span><span class="service-tag">Pergolas &amp; shade structures</span><span class="service-tag">Fencing &amp; gates</span><span class="service-tag">Landscaped gardens</span><span class="service-tag">Outdoor lighting</span><span class="service-tag">Rainwater tanks</span><span class="service-tag">Driveways &amp; parking</span>',
            'svc2_i1': "Infinity pool with 200 m² terrace construction in Terres Basses",
            'svc2_i2': "Full tropical garden landscaping with pergola, fencing and lighting in Grand Case",
            'svc2_i3': "Automated gate and custom fencing installation for a gated villa in Philipsburg",
            'svc2_i4': "BBQ area, lounges and carport creation at Maho Beach",
            'svc3_tag': 'Finishing Works',
            'svc3_box_h': 'What our clients trust us with',
            'svc3_p1': "Finishing works encompass all interior completion trades that bring your building to life. FTFL CARAÏBES manages the entire scope, ensuring complete coordination between trades — so you don't have to deal with a dozen different contractors.",
            'svc3_p2': "Carpentry, plumbing, electrical work, tiling, painting, locksmithing: every trade is carried out by professionals trained to local standards and regulations on both sides of the island. We work on new builds and villa renovations alike.",
            'svc3_tags': '<span class="service-tag">Wood &amp; aluminium joinery</span><span class="service-tag">Plumbing &amp; sanitary ware</span><span class="service-tag">Electrical &amp; home automation</span><span class="service-tag">Tiling &amp; wall finishes</span><span class="service-tag">Interior/exterior painting</span><span class="service-tag">Locksmithing &amp; metalwork</span><span class="service-tag">Thermal insulation</span><span class="service-tag">Full renovation</span>',
            'svc3_i1': "Complete renovation of a 280 m² villa in Anse Marcel: plumbing, electrical, tiling, painting",
            'svc3_i2': "Anti-cyclone aluminium window and door installation for a commercial building in Marigot",
            'svc3_i3': "Electrical and plumbing compliance upgrade for a seasonal rental property in Simpson Bay",
            'svc3_i4': "Large-format tiling and walk-in shower installation for a boutique hotel in Dutch Quarter",
            'svc4_tag': 'Multiservices',
            'svc4_box_h': 'Our maintenance contracts',
            'svc4_p1': "In Saint Martin, many property owners live abroad for part of the year. FTFL CARAÏBES offers a bespoke multiservices package designed specifically for them: a single, available point of contact who monitors, maintains and calls in the right tradespeople at the right time.",
            'svc4_p2': "We also handle emergencies: water leaks, electrical faults, storm damage. Our local partner network enables fast response with systematic photo reporting sent directly to the owner. Ideal for investors, hoteliers and expatriates.",
            'svc4_tags': '<span class="service-tag">Preventive maintenance</span><span class="service-tag">Emergency call-out</span><span class="service-tag">Cleaning &amp; reset</span><span class="service-tag">Minor works</span><span class="service-tag">Property concierge</span><span class="service-tag">Remote photo reporting</span>',
            'svc4_i1': '<strong style="color:#fff;">Seasonal contract</strong> — monthly inspection, condition report, minor works included',
            'svc4_i2': '<strong style="color:#fff;">Hurricane preparation</strong> — securing openings, removing outdoor furniture',
            'svc4_i3': '<strong style="color:#fff;">Post-storm restoration</strong> — rapid response after tropical weather events',
            'svc4_i4': '<strong style="color:#fff;">Works concierge</strong> — full property management while owners are away',
            'faq_h': 'Frequently asked questions',
            'faq1_q': "Do you work on the Dutch side (Sint Maarten) too?",
            'faq1_a': "Yes, we operate across the entire island — on the French side (Saint-Martin, collectivité 97150) and the Dutch side (Sint Maarten). Our teams are fluent in both regulatory frameworks and handle all administrative steps for you.",
            'faq2_q': "How long does it take to receive a quote?",
            'faq2_a': "We commit to getting back to you within 24 business hours of receiving your request. For complex projects requiring a site visit, we arrange an appointment within 48 hours and deliver a detailed quote within 5 working days.",
            'faq3_q': "Can you manage the whole project from start to finish?",
            'faq3_a': "That is exactly our added value. FTFL CARAÏBES can take full responsibility for an entire project: earthworks, structural work, exterior development, finishing works and maintenance. One single contract, one point of contact, one accountable partner.",
            'faq4_q': "Do you work with property owners who are off-island?",
            'faq4_a': "Yes, we have developed a specific service for non-resident owners: daily photo updates, WhatsApp or email reporting, coordination with local property managers. You are kept informed at every stage without needing to travel.",
            'cta': "Request a free quote — Reply within 24h",
        },
        'es': {
            'svc1_tag': 'Movimiento de tierras y redes',
            'svc1_box_h': 'Proyectos destacados',
            'svc1_p1': "Antes de cualquier construcción, el suelo debe ser preparado con rigor. FTFL CARAÏBES domina todas las operaciones de movimiento de tierras adaptadas a las condiciones insulares de Saint-Martin: suelos arcillosos, pendientes pronunciadas, proximidad del mar y riesgos ciclónicos.",
            'svc1_p2': "Nuestros equipos intervienen en la preparación de cimentaciones, la excavación de los volúmenes necesarios, el drenaje de aguas pluviales y la pavimentación de viales. También nos encargamos de las redes de saneamiento, la protección de taludes y la gestión de tierras excavadas.",
            'svc1_tags': '<span class="service-tag">Movimiento de tierras general</span><span class="service-tag">Excavación</span><span class="service-tag">Zanjas y cimentaciones</span><span class="service-tag">Viales y accesos</span><span class="service-tag">Saneamiento</span><span class="service-tag">Escollera y taludes</span><span class="service-tag">Drenaje pluvial</span><span class="service-tag">Redes enterradas</span>',
            'svc1_i1': "Movimiento de tierras para una villa en Orient Bay (1.200 m²) con creación de vía de acceso y colocación de cisternas",
            'svc1_i2': "Redes de urbanización para un conjunto residencial en Terres Basses: saneamiento, agua, electricidad",
            'svc1_i3': "Drenaje y estabilización de un talud en Oyster Pond tras las lluvias ciclónicas",
            'svc1_i4': "Creación de viales y aparcamientos para un complejo hotelero en Simpson Bay",
            'svc2_tag': 'Obras exteriores',
            'svc2_box_h': 'Realizaciones emblemáticas',
            'svc2_p1': "El exterior es la primera impresión que ofrece su propiedad. FTFL CARAÏBES diseña y ejecuta espacios exteriores a la altura del entorno caribeño: piscinas, terrazas, pérgolas, jardines y vallas, todo concebido para resistir los vientos tropicales y la intensa radiación UV de Saint-Martin.",
            'svc2_p2': "Intervenimos tanto en pequeños trabajos de acondicionamiento como en proyectos de gran envergadura (complejos hoteleros, urbanizaciones, villas de lujo). Nuestro conocimiento de las plantas locales, los materiales adaptados al clima tropical y las técnicas de gestión del agua de lluvia nos permite proponer soluciones duraderas y estéticas.",
            'svc2_tags': '<span class="service-tag">Piscinas y spas</span><span class="service-tag">Terrazas y pavimentos</span><span class="service-tag">Pérgolas y parasoles</span><span class="service-tag">Vallas y portones</span><span class="service-tag">Jardines paisajísticos</span><span class="service-tag">Iluminación exterior</span><span class="service-tag">Cisternas y recuperación de agua</span><span class="service-tag">Accesos y aparcamientos</span>',
            'svc2_i1': "Construcción de piscina de desbordamiento con terraza de 200 m² en Terres Basses",
            'svc2_i2': "Acondicionamiento completo de jardín tropical con pérgola, valla e iluminación en Grand Case",
            'svc2_i3': "Instalación de portón automático y valla a medida para villa protegida en Philipsburg",
            'svc2_i4': "Creación de zona BBQ, lounges y cochera en Maho Beach",
            'svc3_tag': 'Acabados interiores',
            'svc3_box_h': 'Lo que nuestros clientes nos confían',
            'svc3_p1': "El segundo cuerpo de obra engloba todos los trabajos de acabado interior que dan vida a su inmueble. FTFL CARAÏBES gestiona la totalidad de estos oficios, asegurando una coordinación completa entre los distintos gremios — lo que le evita tener que gestionar múltiples interlocutores.",
            'svc3_p2': "Carpintería, fontanería, instalación eléctrica, alicatado, pintura, cerrajería: cada prestación es ejecutada por profesionales formados en las normativas locales de ambos lados de la isla. Intervenimos tanto en obra nueva como en rehabilitación de villas.",
            'svc3_tags': '<span class="service-tag">Carpintería de madera y aluminio</span><span class="service-tag">Fontanería y sanitarios</span><span class="service-tag">Electricidad y domótica</span><span class="service-tag">Alicatado y revestimientos</span><span class="service-tag">Pintura interior/exterior</span><span class="service-tag">Cerrajería y metalistería</span><span class="service-tag">Aislamiento térmico</span><span class="service-tag">Reforma integral</span>',
            'svc3_i1': "Reforma integral de una villa de 280 m² en Anse Marcel: fontanería, electricidad, alicatado, pintura",
            'svc3_i2': "Instalación de carpintería de aluminio anticiclónica para un inmueble comercial en Marigot",
            'svc3_i3': "Actualización a normativa eléctrica y de fontanería para un alquiler vacacional en Simpson Bay",
            'svc3_i4': "Colocación de revestimiento de gran formato y ducha italiana para un hotel boutique en Dutch Quarter",
            'svc4_tag': 'Multiservicios',
            'svc4_box_h': 'Nuestros contratos de mantenimiento',
            'svc4_p1': "En Saint-Martin, son numerosos los propietarios que residen en el extranjero parte del año. FTFL CARAÏBES ofrece un servicio de multiservicios especialmente diseñado para ellos: un único interlocutor disponible, que supervisa, mantiene y hace intervenir a los profesionales adecuados en el momento justo.",
            'svc4_p2': "También gestionamos las urgencias: fuga de agua, problema eléctrico, daños tras tormenta. Nuestra red de socios locales nos permite intervenir con rapidez, con un informe fotográfico sistemático enviado al propietario. Ideal para inversores, hoteleros y expatriados.",
            'svc4_tags': '<span class="service-tag">Mantenimiento preventivo</span><span class="service-tag">Asistencia de urgencia</span><span class="service-tag">Limpieza y puesta a punto</span><span class="service-tag">Pequeñas obras</span><span class="service-tag">Conserjería de propiedad</span><span class="service-tag">Seguimiento fotográfico remoto</span>',
            'svc4_i1': '<strong style="color:#fff;">Contrato estacional</strong> — visita mensual, informe de estado, pequeñas obras incluidas',
            'svc4_i2': '<strong style="color:#fff;">Preparación ciclónica</strong> — protección de huecos, retirada de mobiliario exterior',
            'svc4_i3': '<strong style="color:#fff;">Puesta a punto tras el paso</strong> — intervención rápida después de temporales tropicales',
            'svc4_i4': '<strong style="color:#fff;">Conserjería de obras</strong> — gestión completa durante la ausencia de los propietarios',
            'faq_h': 'Preguntas frecuentes',
            'faq1_q': "¿Intervienen también en el lado holandés (Sint Maarten)?",
            'faq1_a': "Sí, intervenimos en toda la isla — parte francesa (Saint-Martin, colectividad 97150) y parte holandesa (Sint Maarten). Nuestros equipos dominan ambos marcos normativos y le simplifican todos los trámites administrativos.",
            'faq2_q': "¿Cuál es el plazo para obtener un presupuesto?",
            'faq2_a': "Nos comprometemos a contactarle en un plazo de 24 horas hábiles tras la recepción de su solicitud. Para proyectos complejos que requieran una visita a la obra, fijamos una cita en 48 horas y le remitimos un presupuesto detallado en 5 días.",
            'faq3_q': "¿Pueden gestionar la totalidad de la obra, de principio a fin?",
            'faq3_a': "Esa es exactamente nuestra propuesta de valor. FTFL CARAÏBES puede hacerse cargo de la totalidad de un proyecto: movimiento de tierras, estructura, acondicionamiento exterior, acabados y mantenimiento. Un solo contrato, un solo interlocutor, un solo responsable.",
            'faq4_q': "¿Trabajan con propietarios que están fuera de la isla?",
            'faq4_a': "Sí, hemos desarrollado una oferta específica para los propietarios no residentes: seguimiento fotográfico diario, informes por WhatsApp o correo electrónico, coordinación con los gestores locales. Usted estará informado en cada etapa sin necesidad de desplazarse.",
            'cta': "Solicitar presupuesto gratuito — Respuesta en 24h",
        },
        'nl': {
            'svc1_tag': 'Grondwerken &amp; Infrastructuur',
            'svc1_box_h': 'Projectreferenties',
            'svc1_p1': "Vóór elke bouw moet de grond nauwkeurig worden voorbereid. FTFL CARAÏBES beheerst alle grondwerkzaamheden afgestemd op de eilandspecifieke omstandigheden van Saint-Martin: kleibodems, steile hellingen, kustligging en orkaankansen.",
            'svc1_p2': "Onze ploegen verzorgen de fundering, ontgravingen, regenwaterafvoer en wegenwerken. Wij nemen ook rioleringen, taludbeveiliging en afvoer van vrijgekomen grond voor onze rekening.",
            'svc1_tags': '<span class="service-tag">Algemene grondwerken</span><span class="service-tag">Ontgraving</span><span class="service-tag">Funderingen &amp; sleuven</span><span class="service-tag">Wegen &amp; toegangen</span><span class="service-tag">Rioleringssystemen</span><span class="service-tag">Steenbestorting &amp; taluds</span><span class="service-tag">Regenwaterafvoer</span><span class="service-tag">Ondergrondse netwerken</span>',
            'svc1_i1': "Grondwerken voor een villa in Orient Bay (1.200 m²) met aanleg van toegangsweg en plaatsing van watertanks",
            'svc1_i2': "Infrastructuurnetwerken voor een woonwijk in Terres Basses: riolering, water, elektriciteit",
            'svc1_i3': "Drainage en stabilisatie van een talud in Oyster Pond na tropische stortregens",
            'svc1_i4': "Aanleg van wegen en parkings voor een hotelcomplex in Simpson Bay",
            'svc2_tag': 'Buitenaanleg',
            'svc2_box_h': 'Kenmerkende realisaties',
            'svc2_p1': "De buitenkant is de eerste indruk van uw eigendom. FTFL CARAÏBES ontwerpt en realiseert buitenruimtes die passen bij de Caribische omgeving: zwembaden, terrassen, pergola's, tuinen en omheiningen, allemaal ontworpen om tropische winden en intense uv-straling op Saint-Martin te weerstaan.",
            'svc2_p2': "Wij voeren projecten uit van elk formaat — van kleine tuinaanleg tot grootschalige ontwikkelingen (hotelcomplexen, verkavelingen, prestigieuze villa's). Onze kennis van lokale planten, klimaatbestendige materialen en regenwaterbeheer stelt ons in staat duurzame en esthetische oplossingen te bieden.",
            'svc2_tags': '<span class="service-tag">Zwembaden &amp; spa\'s</span><span class="service-tag">Terrassen &amp; bestrating</span><span class="service-tag">Pergola\'s &amp; schaduwstructuren</span><span class="service-tag">Omheiningen &amp; poorten</span><span class="service-tag">Aangelegde tuinen</span><span class="service-tag">Buitenverlichting</span><span class="service-tag">Regenwatertanks</span><span class="service-tag">Opritten &amp; parkings</span>',
            'svc2_i1': "Bouw van een overloopzwembad met 200 m² terras in Terres Basses",
            'svc2_i2': "Volledige aanleg van tropische tuin met pergola, omheining en verlichting in Grand Case",
            'svc2_i3': "Plaatsing van automatische poort en maatwerkafscheiding voor beveiligde villa in Philipsburg",
            'svc2_i4': "Aanleg van BBQ-ruimte, loungegebieden en carport in Maho Beach",
            'svc3_tag': 'Afbouwwerken',
            'svc3_box_h': 'Wat onze klanten ons toevertrouwen',
            'svc3_p1': "Afbouwwerken omvatten alle binnenafwerkingen die uw gebouw tot leven brengen. FTFL CARAÏBES neemt de volledige scope op zich en zorgt voor totale coördinatie tussen de vakdisciplines — zodat u niet tientallen aannemers hoeft te beheren.",
            'svc3_p2': "Schrijnwerk, loodgieterij, elektriciteit, tegelwerk, schilderwerk, sleutelwerk: elke specialiteit wordt uitgevoerd door professionals opgeleid aan de lokale normen van beide kanten van het eiland. Wij werken zowel op nieuwbouw als op renovatie van villa's.",
            'svc3_tags': '<span class="service-tag">Hout- &amp; aluminiumschrijwerk</span><span class="service-tag">Loodgieterij &amp; sanitair</span><span class="service-tag">Elektriciteit &amp; domotica</span><span class="service-tag">Tegelwerk &amp; wandbekleding</span><span class="service-tag">Binnen-/buitenschilderwerk</span><span class="service-tag">Hang-, sluit- &amp; metaalwerk</span><span class="service-tag">Thermische isolatie</span><span class="service-tag">Volledige renovatie</span>',
            'svc3_i1': "Volledige renovatie van een villa van 280 m² in Anse Marcel: loodgieterij, elektriciteit, tegelwerk, schilderwerk",
            'svc3_i2': "Installatie van anti-orkaan aluminium schrijnwerk voor een commercieel gebouw in Marigot",
            'svc3_i3': "Elektrische en loodgieterijconformiteitsupgrade voor een vakantieverhuurwoning in Simpson Bay",
            'svc3_i4': "Plaatsing van grootformaat tegels en inloopdouche voor een boutique hotel in Dutch Quarter",
            'svc4_tag': 'Multidiensten',
            'svc4_box_h': 'Onze onderhoudscontracten',
            'svc4_p1': "Op Saint-Martin wonen veel eigenaren een deel van het jaar in het buitenland. FTFL CARAÏBES biedt een op maat gemaakt multidiensten-pakket speciaal voor hen: één beschikbaar aanspreekpunt dat toeziet, onderhoudt en de juiste vaklieden op het juiste moment inschakelt.",
            'svc4_p2': "Wij behandelen ook noodgevallen: waterlekkages, elektrische problemen, stormbeschadigingen. Ons netwerk van lokale partners stelt ons in staat snel in te grijpen, met systematisch fotoverslag rechtstreeks naar de eigenaar. Ideaal voor investeerders, hoteliers en expats.",
            'svc4_tags': '<span class="service-tag">Preventief onderhoud</span><span class="service-tag">Dringende interventie</span><span class="service-tag">Reiniging &amp; herstel</span><span class="service-tag">Kleine werken</span><span class="service-tag">Vastgoedconciërge</span><span class="service-tag">Fotobeheer op afstand</span>',
            'svc4_i1': '<strong style="color:#fff;">Seizoenscontract</strong> — maandelijkse inspectie, toestandsrapport, kleine werken inbegrepen',
            'svc4_i2': '<strong style="color:#fff;">Orkaanvoorbereiding</strong> — afdichten van openingen, wegzetten van buitenmeubilair',
            'svc4_i3': '<strong style="color:#fff;">Herstel na doortocht</strong> — snelle interventie na tropische stormen',
            'svc4_i4': '<strong style="color:#fff;">Werkenconciërge</strong> — volledig vastgoedbeheer tijdens afwezigheid van eigenaren',
            'faq_h': 'Veelgestelde vragen',
            'faq1_q': "Werkt u ook aan de Nederlandse kant (Sint Maarten)?",
            'faq1_a': "Ja, wij werken op het hele eiland — Frans gedeelte (Saint-Martin, collectivité 97150) en Nederlands gedeelte (Sint Maarten). Onze teams zijn vertrouwd met beide regelgevingskaders en regelen alle administratieve stappen voor u.",
            'faq2_q': "Hoe lang duurt het om een offerte te ontvangen?",
            'faq2_a': "Wij verbinden er ons toe u binnen 24 werkuren na ontvangst van uw aanvraag terug te contacteren. Voor complexe projecten waarvoor een plaatsbezoek nodig is, plannen we een afspraak binnen 48 uur en leveren we een gedetailleerde offerte binnen 5 werkdagen.",
            'faq3_q': "Kunt u het volledige project van A tot Z beheren?",
            'faq3_a': "Dat is precies onze toegevoegde waarde. FTFL CARAÏBES kan de volledige verantwoordelijkheid nemen voor een project: grondwerken, ruwbouw, buitenaanleg, afbouwwerken en onderhoud. Eén contract, één aanspreekpunt, één verantwoordelijke partner.",
            'faq4_q': "Werkt u samen met eigenaren die niet op het eiland aanwezig zijn?",
            'faq4_a': "Ja, wij hebben een specifieke dienst ontwikkeld voor niet-residerende eigenaren: dagelijkse fotoupdates, WhatsApp of e-mailrapporten, coördinatie met lokale vastgoedbeheerders. U wordt in elke fase op de hoogte gehouden zonder dat u zelf aanwezig moet zijn.",
            'cta': "Gratis offerte aanvragen — Antwoord binnen 24u",
        },
        'pt': {
            'svc1_tag': 'Terraplenagem e infraestruturas',
            'svc1_box_h': 'Projetos em destaque',
            'svc1_p1': "Antes de qualquer construção, o solo deve ser preparado com rigor. A FTFL CARAÏBES domina todas as operações de terraplenagem adaptadas às condições insulares de Saint-Martin: solos argilosos, declives acentuados, proximidade do mar e riscos ciclónicos.",
            'svc1_p2': "As nossas equipas intervêm na preparação de fundações, na escavação dos volumes necessários, na drenagem de águas pluviais e no arranjo de acessos. Tratamos também das redes de saneamento, da proteção de taludes e da gestão de terras escavadas.",
            'svc1_tags': '<span class="service-tag">Terraplenagem geral</span><span class="service-tag">Escavação</span><span class="service-tag">Valas e fundações</span><span class="service-tag">Arruamentos e acessos</span><span class="service-tag">Saneamento</span><span class="service-tag">Enrocamento e taludes</span><span class="service-tag">Drenagem pluvial</span><span class="service-tag">Redes enterradas</span>',
            'svc1_i1': "Terraplenagem de uma moradia em Orient Bay (1 200 m²) com criação de via de acesso e colocação de cisternas",
            'svc1_i2': "Redes de infraestruturas para um loteamento em Terres Basses: saneamento, água, eletricidade",
            'svc1_i3': "Drenagem e estabilização de um talude em Oyster Pond após chuvas ciclónicas",
            'svc1_i4': "Criação de arruamentos e estacionamentos para um complexo hoteleiro em Simpson Bay",
            'svc2_tag': 'Obras exteriores e paisagismo',
            'svc2_box_h': 'Realizações emblemáticas',
            'svc2_p1': "O exterior é a primeira impressão do seu imóvel. A FTFL CARAÏBES concebe e realiza espaços exteriores à altura do enquadramento caribenho: piscinas, terraços, pérgolas, jardins e vedações — tudo concebido para resistir aos ventos tropicais e à intensa radiação UV em Saint-Martin.",
            'svc2_p2': "Intervenimos tanto em pequenos arranjos como em projetos de grande envergadura (complexos hoteleiros, urbanizações, villas de prestígio). O nosso conhecimento das plantas locais, dos materiais adaptados ao clima tropical e das técnicas de gestão de águas pluviais permite-nos propor soluções duradouras e esteticamente cuidadas.",
            'svc2_tags': '<span class="service-tag">Piscinas e spas</span><span class="service-tag">Terraços e pavimentos</span><span class="service-tag">Pérgolas e coberturas</span><span class="service-tag">Vedações e portões</span><span class="service-tag">Jardins paisagísticos</span><span class="service-tag">Iluminação exterior</span><span class="service-tag">Cisternas e recuperação de água</span><span class="service-tag">Acessos e estacionamentos</span>',
            'svc2_i1': "Construção de piscina de transbordo com terraço de 200 m² em Terres Basses",
            'svc2_i2': "Arranjo completo de jardim tropical com pérgola, vedação e iluminação em Grand Case",
            'svc2_i3': "Montagem de portão automático e vedação à medida para moradia segura em Philipsburg",
            'svc2_i4': "Criação de espaço BBQ, lounges e cobertura de automóvel em Maho Beach",
            'svc3_tag': 'Obras de Acabamento',
            'svc3_box_h': 'O que os nossos clientes nos confiam',
            'svc3_p1': "As obras de acabamento englobam todos os trabalhos de conclusão interior que dão vida ao seu edifício. A FTFL CARAÏBES gere a totalidade destas especialidades, assegurando uma coordenação completa entre artesãos e ofícios — poupando-lhe a gestão de múltiplos intervenientes.",
            'svc3_p2': "Carpintaria, canalização, eletricidade, revestimentos, pintura, serralharia: cada especialidade é executada por profissionais formados de acordo com as normas locais dos dois lados da ilha. Trabalhamos tanto em construção nova como em renovação de moradias.",
            'svc3_tags': '<span class="service-tag">Carpintaria em madeira e alumínio</span><span class="service-tag">Canalização e sanitários</span><span class="service-tag">Eletricidade e domótica</span><span class="service-tag">Revestimentos e cerâmica</span><span class="service-tag">Pintura interior/exterior</span><span class="service-tag">Serralharia e trabalhos em metal</span><span class="service-tag">Isolamento térmico</span><span class="service-tag">Renovação completa</span>',
            'svc3_i1': "Renovação completa de uma moradia de 280 m² em Anse Marcel: canalização, eletricidade, revestimentos, pintura",
            'svc3_i2': "Instalação de caixilharia de alumínio anticiclone para um edifício comercial em Marigot",
            'svc3_i3': "Atualização de conformidade elétrica e de canalização para um alojamento de férias em Simpson Bay",
            'svc3_i4': "Assentamento de revestimento de grande formato e duche italiano para um hotel boutique em Dutch Quarter",
            'svc4_tag': 'Multisserviços',
            'svc4_box_h': 'Os nossos contratos de manutenção',
            'svc4_p1': "Em Saint-Martin, muitos proprietários residem no estrangeiro durante parte do ano. A FTFL CARAÏBES oferece um serviço de multisserviços especialmente concebido para eles: um único interlocutor disponível, que monitoriza, mantém e chama os profissionais certos no momento adequado.",
            'svc4_p2': "Tratamos também das urgências: fuga de água, problema elétrico, danos após tempestade. A nossa rede de parceiros locais permite intervir rapidamente, com relatório fotográfico sistemático enviado diretamente ao proprietário. Ideal para investidores, hoteleiros e expatriados.",
            'svc4_tags': '<span class="service-tag">Manutenção preventiva</span><span class="service-tag">Assistência de urgência</span><span class="service-tag">Limpeza e reposição</span><span class="service-tag">Pequenos trabalhos</span><span class="service-tag">Conciergerie imobiliária</span><span class="service-tag">Acompanhamento fotográfico remoto</span>',
            'svc4_i1': '<strong style="color:#fff;">Contrato sazonal</strong> — visita mensal, relatório de estado, pequenos trabalhos incluídos',
            'svc4_i2': '<strong style="color:#fff;">Preparação ciclónica</strong> — proteção de aberturas, remoção do mobiliário exterior',
            'svc4_i3': '<strong style="color:#fff;">Reposição pós-ciclone</strong> — intervenção rápida após intempéries tropicais',
            'svc4_i4': '<strong style="color:#fff;">Conciergerie de obras</strong> — gestão completa durante a ausência dos proprietários',
            'faq_h': 'Perguntas frequentes',
            'faq1_q': "Também intervêm do lado holandês (Sint Maarten)?",
            'faq1_a': "Sim, intervimos em toda a ilha — lado francês (Saint-Martin, coletividade 97150) e lado holandês (Sint Maarten). As nossas equipas dominam ambos os quadros regulamentares e simplificam todos os procedimentos administrativos.",
            'faq2_q': "Qual é o prazo para obter um orçamento?",
            'faq2_a': "Comprometemo-nos a responder no prazo de 24 horas úteis após a receção do seu pedido. Para projetos complexos que exijam uma visita ao local, marcamos uma reunião em 48 horas e entregamos um orçamento detalhado em 5 dias.",
            'faq3_q': "Podem gerir toda a obra do início ao fim?",
            'faq3_a': "Essa é exatamente a nossa mais-valia. A FTFL CARAÏBES pode assumir a responsabilidade total de um projeto: terraplenagem, obra bruta, arranjos exteriores, acabamentos e manutenção. Um único contrato, um único interlocutor, um único responsável.",
            'faq4_q': "Trabalham com proprietários que estão ausentes da ilha?",
            'faq4_a': "Sim, desenvolvemos uma oferta específica para proprietários não residentes: acompanhamento fotográfico diário, relatórios por WhatsApp ou e-mail, coordenação com os gestores locais. É mantido informado em cada etapa sem necessidade de se deslocar.",
            'cta': "Pedir orçamento gratuito — Resposta em 24h",
        },
    }
    t = T[lang]
    return f"""<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="{home}">{home_label}</a><span>›</span><span>{breadcrumb}</span>
    </nav>
    <span class="section-tag" data-i18n="services.tag">Nos Métiers</span>
    <h1 data-i18n="services.title">Une réponse complète<br/>à <span class="highlight">chaque besoin.</span></h1>
    <p data-i18n="services.sub">Du terrassement aux finitions, FTFL couvre l'ensemble des corps d'état avec les mêmes standards d'exigence.</p>
    <a href="{contact}" class="btn btn-primary" style="margin-top:12px;">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg>
      <span data-i18n="nav.cta">Demander un devis gratuit</span>
    </a>
  </div>
</section>

<!-- ── SERVICE 01 ─────────────────────────────────────────── -->
<section class="section" id="services" style="padding-bottom:0;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding-bottom:80px;border-bottom:1px solid rgba(255,255,255,.07);" data-aos="fade-up">
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <span style="font-family:var(--font-head);font-size:3rem;font-weight:900;color:rgba(61,168,100,.2);line-height:1;">01</span>
          <span class="section-tag" style="margin:0;">{t['svc1_tag']}</span>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.9rem;font-weight:800;margin-bottom:16px;" data-i18n="svc1.h">Terrassement &amp; VRD</h2>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:20px;">{t['svc1_p1']}</p>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:24px;">{t['svc1_p2']}</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          {t['svc1_tags']}
        </div>
      </div>
      <div style="background:rgba(61,168,100,.05);border:1px solid rgba(61,168,100,.15);border-radius:20px;padding:36px;">
        <h3 style="font-family:var(--font-head);font-size:1.1rem;font-weight:700;margin-bottom:20px;color:var(--orange);">{t['svc1_box_h']}</h3>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px;">
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc1_i1']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc1_i2']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc1_i3']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc1_i4']}</span></li>
        </ul>
      </div>
    </div>

    <!-- ── SERVICE 02 ─────────────────────────────────────── -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding:80px 0;border-bottom:1px solid rgba(255,255,255,.07);" data-aos="fade-up">
      <div style="background:rgba(61,168,100,.05);border:1px solid rgba(61,168,100,.15);border-radius:20px;padding:36px;">
        <h3 style="font-family:var(--font-head);font-size:1.1rem;font-weight:700;margin-bottom:20px;color:var(--orange);">{t['svc2_box_h']}</h3>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px;">
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc2_i1']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc2_i2']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc2_i3']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc2_i4']}</span></li>
        </ul>
      </div>
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <span style="font-family:var(--font-head);font-size:3rem;font-weight:900;color:rgba(61,168,100,.2);line-height:1;">02</span>
          <span class="section-tag" style="margin:0;">{t['svc2_tag']}</span>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.9rem;font-weight:800;margin-bottom:16px;" data-i18n="svc2.h">Aménagement Extérieur</h2>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:20px;">{t['svc2_p1']}</p>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:24px;">{t['svc2_p2']}</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          {t['svc2_tags']}
        </div>
      </div>
    </div>

    <!-- ── SERVICE 03 ─────────────────────────────────────── -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding:80px 0;border-bottom:1px solid rgba(255,255,255,.07);" data-aos="fade-up">
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <span style="font-family:var(--font-head);font-size:3rem;font-weight:900;color:rgba(61,168,100,.2);line-height:1;">03</span>
          <span class="section-tag" style="margin:0;">{t['svc3_tag']}</span>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.9rem;font-weight:800;margin-bottom:16px;" data-i18n="svc3.h">Travaux de Second Œuvre</h2>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:20px;">{t['svc3_p1']}</p>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:24px;">{t['svc3_p2']}</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          {t['svc3_tags']}
        </div>
      </div>
      <div style="background:rgba(61,168,100,.05);border:1px solid rgba(61,168,100,.15);border-radius:20px;padding:36px;">
        <h3 style="font-family:var(--font-head);font-size:1.1rem;font-weight:700;margin-bottom:20px;color:var(--orange);">{t['svc3_box_h']}</h3>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px;">
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc3_i1']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc3_i2']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc3_i3']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc3_i4']}</span></li>
        </ul>
      </div>
    </div>

    <!-- ── SERVICE 04 ─────────────────────────────────────── -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding:80px 0;" data-aos="fade-up">
      <div style="background:rgba(61,168,100,.05);border:1px solid rgba(61,168,100,.15);border-radius:20px;padding:36px;">
        <h3 style="font-family:var(--font-head);font-size:1.1rem;font-weight:700;margin-bottom:20px;color:var(--orange);">{t['svc4_box_h']}</h3>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px;">
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc4_i1']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc4_i2']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc4_i3']}</span></li>
          <li style="display:flex;gap:12px;align-items:flex-start;"><svg style="flex-shrink:0;margin-top:2px;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="color:var(--gray-light);line-height:1.6;">{t['svc4_i4']}</span></li>
        </ul>
      </div>
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <span style="font-family:var(--font-head);font-size:3rem;font-weight:900;color:rgba(61,168,100,.2);line-height:1;">04</span>
          <span class="section-tag" style="margin:0;">{t['svc4_tag']}</span>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.9rem;font-weight:800;margin-bottom:16px;" data-i18n="svc4.h">Multiservices &amp; Maintenance</h2>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:20px;">{t['svc4_p1']}</p>
        <p style="color:var(--gray-light);line-height:1.85;margin-bottom:24px;">{t['svc4_p2']}</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          {t['svc4_tags']}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── FAQ SERVICES ──────────────────────────────────────────── -->
<section class="section" style="background:rgba(255,255,255,.02);padding:80px 0;">
  <div class="container" style="max-width:800px;">
    <h2 style="font-family:var(--font-head);font-size:1.8rem;font-weight:800;text-align:center;margin-bottom:48px;" data-aos="fade-up">{t['faq_h']}</h2>
    <div style="display:flex;flex-direction:column;gap:16px;" data-aos="fade-up">
      <details style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px;">
        <summary style="font-family:var(--font-head);font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">{t['faq1_q']} <span style="color:var(--orange);font-size:1.4rem;line-height:1;">+</span></summary>
        <p style="color:var(--gray-light);margin-top:16px;line-height:1.8;">{t['faq1_a']}</p>
      </details>
      <details style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px;">
        <summary style="font-family:var(--font-head);font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">{t['faq2_q']} <span style="color:var(--orange);font-size:1.4rem;line-height:1;">+</span></summary>
        <p style="color:var(--gray-light);margin-top:16px;line-height:1.8;">{t['faq2_a']}</p>
      </details>
      <details style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px;">
        <summary style="font-family:var(--font-head);font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">{t['faq3_q']} <span style="color:var(--orange);font-size:1.4rem;line-height:1;">+</span></summary>
        <p style="color:var(--gray-light);margin-top:16px;line-height:1.8;">{t['faq3_a']}</p>
      </details>
      <details style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px;">
        <summary style="font-family:var(--font-head);font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">{t['faq4_q']} <span style="color:var(--orange);font-size:1.4rem;line-height:1;">+</span></summary>
        <p style="color:var(--gray-light);margin-top:16px;line-height:1.8;">{t['faq4_a']}</p>
      </details>
    </div>
    <div style="text-align:center;margin-top:48px;" data-aos="fade-up">
      <a href="{contact}" class="btn btn-primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        {t['cta']}
      </a>
    </div>
  </div>
</section>"""


def content_approche(lc):
    home = lc['home']
    home_label = lc['home_label']
    breadcrumb = PAGE_META['approche'][lc['lang']]['breadcrumb']
    _cs = SLUG_TRANSLATIONS['contact'][lc['lang']]
    contact = f'{lc["prefix"]}/{_cs}/' if lc['lang'] != 'fr' else f'/{_cs}/'
    return f"""<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="{home}">{home_label}</a>
      <span>›</span>
      <span>{breadcrumb}</span>
    </nav>
    <span class="section-tag" data-i18n="approach.tag">Notre Approche</span>
    <h1 data-i18n="approach.title">Un processus <span class="highlight">rigoureux</span><br/>à chaque étape.</h1>
    <p data-i18n="approach.sub">De la première rencontre à la remise des clés, nous vous accompagnons avec méthode, rigueur et transparence totale.</p>
  </div>
</section>

<section class="section approach" id="approach">
  <div class="container">
    <div class="approach-steps">
      <div class="approach-step" data-aos="fade-up" data-aos-delay="0">
        <div class="step-circle"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg></div>
        <h2 class="step-title" data-i18n="step1.h">01 · Écoute</h2>
        <p class="step-desc" data-i18n="step1.p">Nous prenons le temps de comprendre votre projet dans ses moindres détails — contraintes techniques, budget, calendrier.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="100">
        <div class="step-circle"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
        <h2 class="step-title" data-i18n="step2.h">02 · Étude</h2>
        <p class="step-desc" data-i18n="step2.p">Chiffrage précis, planning prévisionnel, identification des risques : notre étude vous donne une vision claire avant tout démarrage.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="200">
        <div class="step-circle"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div>
        <h2 class="step-title" data-i18n="step3.h">03 · Exécution</h2>
        <p class="step-desc" data-i18n="step3.p">Nos équipes s'engagent avec rigueur. Un chef de chantier dédié coordonne chaque intervention et vous tient informé en temps réel.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="300">
        <div class="step-circle"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>
        <h2 class="step-title" data-i18n="step4.h">04 · Livraison</h2>
        <p class="step-desc" data-i18n="step4.p">Nous ne rendons les clés qu'une fois chaque détail achevé à votre satisfaction, dans le strict respect des règles de l'art.</p>
      </div>
    </div>
    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;" data-i18n="approach.seo.h">Un engagement total du premier contact à la livraison</h2>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;" data-i18n="approach.seo.p">Chez FTFL CARAÏBES, notre méthode repose sur une conviction : un projet bien préparé est un projet réussi. Cette rigueur initiale permet d'établir un devis précis, un planning réaliste et d'anticiper les risques avant le premier coup de pelleteuse.</p>
      <div style="margin-top:28px;text-align:center;">
        <a href="{contact}" class="btn btn-primary" data-i18n="approach.cta">Démarrer votre projet avec FTFL</a>
      </div>
    </div>
  </div>
</section>"""


def content_valeurs(lc):
    home = lc['home']
    home_label = lc['home_label']
    breadcrumb = PAGE_META['valeurs'][lc['lang']]['breadcrumb']
    _cs = SLUG_TRANSLATIONS['contact'][lc['lang']]
    contact = f'{lc["prefix"]}/{_cs}/' if lc['lang'] != 'fr' else f'/{_cs}/'
    _ss = SLUG_TRANSLATIONS['services'][lc['lang']]
    services = f'{lc["prefix"]}/{_ss}/' if lc['lang'] != 'fr' else f'/{_ss}/'
    return f"""<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="{home}">{home_label}</a>
      <span>›</span>
      <span>{breadcrumb}</span>
    </nav>
    <span class="section-tag" data-i18n="values.tag">Nos Valeurs</span>
    <h1 data-i18n="values.title">Ce qui nous <span class="highlight">distingue.</span></h1>
    <p data-i18n="values.sub">Quatre piliers fondateurs qui guident chacune de nos interventions, du premier devis à la livraison finale.</p>
  </div>
</section>

<section class="section values" id="values">
  <div class="container">
    <div class="grid-4">
      <div class="value-card" data-aos="fade-up" data-aos-delay="0">
        <div class="value-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val1.h">Ancrage Local</h2>
        <p data-i18n="val1.p">Implantés à Saint-Martin depuis nos débuts, nous connaissons chaque quartier, chaque fournisseur, chaque contrainte du terrain.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="80">
        <div class="value-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val2.h">Fiabilité</h2>
        <p data-i18n="val2.p">Un chantier qui démarre à l'heure, un budget maîtrisé, des engagements tenus jusqu'au bout. Notre réputation se construit projet après projet.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="160">
        <div class="value-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg></div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val3.h">Polyvalence</h2>
        <p data-i18n="val3.p">Du terrassement aux finitions, nos équipes couvrent tous les corps d'état. Un seul interlocuteur, zéro coordination à gérer.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="240">
        <div class="value-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val4.h">Exigence</h2>
        <p data-i18n="val4.p">Mêmes standards sur chaque chantier, quelle que soit son envergure. Les normes locales, les délais, la sécurité : rien n'est laissé au hasard.</p>
      </div>
    </div>
    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;" data-i18n="values.seo.h">Des valeurs forgées sur le terrain caribéen</h2>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;" data-i18n="values.seo.p">Ces quatre valeurs reflètent ce que nous avons appris au fil des années de chantiers à Saint-Martin et Sint Maarten. L'ancrage local nous permet de réagir vite et de comprendre les particularités d'un territoire insulaire. La fiabilité est ce qui nous a permis de fidéliser nos clients.</p>
      <div style="margin-top:28px;text-align:center;">
        <a href="{contact}" class="btn btn-primary" data-i18n="values.cta">Travailler avec FTFL CARAÏBES</a>
        <a href="{services}" class="btn btn-outline" style="margin-left:16px;" data-i18n="values.svc">Voir nos services</a>
      </div>
    </div>
  </div>
</section>"""


def content_zone(lc):
    home = lc['home']
    home_label = lc['home_label']
    breadcrumb = PAGE_META['zone'][lc['lang']]['breadcrumb']
    _cs = SLUG_TRANSLATIONS['contact'][lc['lang']]
    contact = f'{lc["prefix"]}/{_cs}/' if lc['lang'] != 'fr' else f'/{_cs}/'
    return f"""<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="{home}">{home_label}</a>
      <span>›</span>
      <span>{breadcrumb}</span>
    </nav>
    <span class="section-tag" data-i18n="zone.tag">Zone d'Intervention</span>
    <h1 data-i18n="zone.title">Une île, deux pays,<br/><span class="highlight">une seule équipe.</span></h1>
    <p data-i18n="zone.sub">FTFL opère sur l'intégralité de l'île de Saint-Martin, côté français comme côté hollandais. Une double maîtrise réglementaire au service de vos projets.</p>
  </div>
</section>

<section class="section zone" id="zone" style="background:var(--navy-mid);">
  <div class="zone-bg-photo">
    <img src="/images/FTFL-WEB-1.webp" alt="Vue aérienne île Saint-Martin Sint Maarten" loading="lazy" width="1400" height="900"/>
  </div>
  <div class="container">
    <div class="zone-visual">
      <div class="zone-card zone-card-fr" data-aos="fade-right">
        <div class="zone-flag">🇫🇷</div>
        <h2 style="font-family:var(--font-head);font-size:1.15rem;font-weight:800;margin-bottom:8px;">Saint-Martin</h2>
        <p style="color:rgba(0,85,164,.9);font-weight:600;" data-i18n="zone.fr.side">Partie Française</p>
        <p data-i18n="zone.fr.desc">Maîtrise complète du cadre administratif français. Permis de construire, déclarations de travaux, normes RT : nous gérons tout.</p>
        <div class="zone-places">
          <span class="zone-place">Orient Bay</span><span class="zone-place">Mont Vernon</span>
          <span class="zone-place">Terres Basses</span><span class="zone-place">Oyster Pond</span>
          <span class="zone-place">Anse Marcel</span><span class="zone-place">Marigot</span>
          <span class="zone-place">Sandy Ground</span><span class="zone-place">Grand Case</span>
          <span class="zone-place">Cul-de-Sac</span><span class="zone-place">Quartier d'Orléans</span>
        </div>
      </div>
      <div class="zone-card zone-card-nl" data-aos="fade-left">
        <div class="zone-flag">🇸🇽</div>
        <h2 style="font-family:var(--font-head);font-size:1.15rem;font-weight:800;margin-bottom:8px;">Sint Maarten</h2>
        <p style="color:rgba(174,28,40,.9);font-weight:600;" data-i18n="zone.nl.side">Partie Hollandaise</p>
        <p data-i18n="zone.nl.desc">Connaissance approfondie du système réglementaire néerlandais. Nos équipes opèrent sur Sint Maarten avec la même efficacité.</p>
        <div class="zone-places">
          <span class="zone-place">Philipsburg</span><span class="zone-place">Simpson Bay</span>
          <span class="zone-place">Cole Bay</span><span class="zone-place">Maho</span>
          <span class="zone-place">Cupecoy</span><span class="zone-place">Dutch Quarter</span>
          <span class="zone-place">Cay Bay</span>
        </div>
      </div>
    </div>
    <p class="zone-tagline" data-aos="fade-up" data-i18n="zone.tagline">+ interventions ponctuelles sur <span>Saint-Barthélemy</span> & <span>Anguilla</span></p>
    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;position:relative;z-index:1;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;" data-i18n="zone.seo.h">L'avantage d'un opérateur bi-frontalier</h2>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;" data-i18n="zone.seo.p">Saint-Martin est une île partagée entre la France et les Pays-Bas. FTFL CARAÏBES est l'un des rares prestataires à opérer avec la même efficacité <strong style="color:#fff;">des deux côtés de la frontière</strong>, avec une maîtrise complète des réglementations locales de chaque partie.</p>
      <div style="margin-top:28px;text-align:center;">
        <a href="{contact}" class="btn btn-primary" data-i18n="zone.cta">Discuter de votre projet à Saint-Martin</a>
      </div>
    </div>
  </div>
</section>"""


def content_contact(lc):
    home = lc['home']
    home_label = lc['home_label']
    breadcrumb = PAGE_META['contact'][lc['lang']]['breadcrumb']
    lang = lc['lang']
    CT = {
        'fr': {
            'subject': 'Nouvelle demande de devis — FTFL CARAÏBES',
            'autoresponse': "Merci pour votre demande. L'équipe FTFL CARAÏBES vous contactera dans les 24h.",
            'ph_email': 'votre@email.com',
            'ph_msg': 'Décrivez votre projet : nature des travaux, superficie, délais souhaités, contraintes particulières…',
            'budget_lt5': 'Moins de 5 000 €',
            'budget_5_20': '5 000 – 20 000 €',
            'budget_20_50': '20 000 – 50 000 €',
            'budget_50_100': '50 000 – 100 000 €',
            'budget_gt100': 'Plus de 100 000 €',
        },
        'en': {
            'subject': 'New quote request — FTFL CARAÏBES',
            'autoresponse': 'Thank you for your message. The FTFL CARAÏBES team will contact you within 24 hours.',
            'ph_email': 'your@email.com',
            'ph_msg': 'Tell us about your project: type of works, approximate area, preferred timeline, any specific requirements…',
            'budget_lt5': 'Less than 5,000 €',
            'budget_5_20': '5,000 – 20,000 €',
            'budget_20_50': '20,000 – 50,000 €',
            'budget_50_100': '50,000 – 100,000 €',
            'budget_gt100': 'Over 100,000 €',
        },
        'es': {
            'subject': 'Nueva solicitud de presupuesto — FTFL CARAÏBES',
            'autoresponse': 'Gracias por su solicitud. El equipo de FTFL CARAÏBES se pondrá en contacto con usted en las próximas 24 horas.',
            'ph_email': 'su@email.com',
            'ph_msg': 'Cuéntenos su proyecto: tipo de obras, superficie aproximada, plazos deseados, requisitos especiales…',
            'budget_lt5': 'Menos de 5.000 €',
            'budget_5_20': '5.000 – 20.000 €',
            'budget_20_50': '20.000 – 50.000 €',
            'budget_50_100': '50.000 – 100.000 €',
            'budget_gt100': 'Más de 100.000 €',
        },
        'nl': {
            'subject': 'Nieuwe offerteaanvraag — FTFL CARAÏBES',
            'autoresponse': 'Bedankt voor uw aanvraag. Het team van FTFL CARAÏBES neemt binnen 24 uur contact met u op.',
            'ph_email': 'uw@email.com',
            'ph_msg': 'Vertel ons over uw project: type werken, geschatte oppervlakte, gewenste planning, bijzondere vereisten…',
            'budget_lt5': 'Minder dan 5.000 €',
            'budget_5_20': '5.000 – 20.000 €',
            'budget_20_50': '20.000 – 50.000 €',
            'budget_50_100': '50.000 – 100.000 €',
            'budget_gt100': 'Meer dan 100.000 €',
        },
        'pt': {
            'subject': 'Novo pedido de orçamento — FTFL CARAÏBES',
            'autoresponse': 'Obrigado pelo seu pedido. A equipa FTFL CARAÏBES entrará em contacto consigo nas próximas 24 horas.',
            'ph_email': 'o.seu@email.com',
            'ph_msg': 'Descreva o seu projeto: tipo de obras, área aproximada, prazos pretendidos, requisitos especiais…',
            'budget_lt5': 'Menos de 5 000 €',
            'budget_5_20': '5 000 – 20 000 €',
            'budget_20_50': '20 000 – 50 000 €',
            'budget_50_100': '50 000 – 100 000 €',
            'budget_gt100': 'Mais de 100 000 €',
        },
    }
    ct = CT[lang]
    return f"""<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="{home}">{home_label}</a>
      <span>›</span>
      <span>{breadcrumb}</span>
    </nav>
    <span class="section-tag" data-i18n="contact.tag">Contact</span>
    <h1 data-i18n="contact.title">Construisons ensemble<br/><span class="highlight">votre projet.</span></h1>
    <p data-i18n="contact.sub">Un projet de construction, de rénovation ou d'aménagement ? Notre équipe étudie votre demande et vous soumet un devis détaillé, gratuit et sans engagement.</p>
  </div>
</section>

<section class="section contact" id="contact">
  <div class="container">
    <div class="contact-grid">
      <div data-aos="fade-right">
        <div class="contact-items">
          <a class="contact-item" href="https://wa.me/590690432818" target="_blank" rel="noopener">
            <div class="contact-item-icon" style="color:#25D366;"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12 0C5.373 0 0 5.373 0 12c0 2.117.549 4.175 1.594 5.994L0 24l6.188-1.563A11.944 11.944 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.926 0-3.82-.509-5.486-1.473l-.394-.23-4.075 1.03 1.072-3.94-.256-.407A9.944 9.944 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg></div>
            <div class="contact-item-text"><span class="ci-label" data-i18n="ci.whatsapp">WhatsApp</span><span>+590 690 43 28 18</span></div>
          </a>
          <a class="contact-item" href="tel:+590690432818">
            <div class="contact-item-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg></div>
            <div class="contact-item-text"><span class="ci-label" data-i18n="ci.phone">Téléphone</span><span>+590 690 43 28 18</span></div>
          </a>
          <a class="contact-item" href="mailto:contact@ftfl-sxm.com">
            <div class="contact-item-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>
            <div class="contact-item-text"><span class="ci-label">Email</span><span>contact@ftfl-sxm.com</span></div>
          </a>
          <div class="contact-item">
            <div class="contact-item-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <div class="contact-item-text"><label data-i18n="ci.loc">Localisation</label><span>Saint-Martin / Sint Maarten · SXM 97150</span></div>
          </div>
          <a class="contact-item" href="https://www.linkedin.com/company/ftfl-cara%C3%AFbes/" target="_blank" rel="noopener">
            <div class="contact-item-icon" style="color:#0A66C2;"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></div>
            <div class="contact-item-text"><span class="ci-label" data-i18n="ci.linkedin">LinkedIn</span><span>FTFL CARAÏBES</span></div>
          </a>
        </div>
      </div>
      <div data-aos="fade-left" data-aos-delay="100">
        <div class="contact-form">
          <h2 class="form-title" data-i18n="form.title">Demande de devis gratuit</h2>
          <form id="contactForm" onsubmit="handleSubmit(event)">
            <input type="hidden" name="_subject" value="{ct['subject']}"/>
            <input type="hidden" name="_template" value="box"/>
            <input type="hidden" name="_color" value="1a6b35"/>
            <input type="hidden" name="_captcha" value="false"/>
            <input type="hidden" name="_autoresponse" value="{ct['autoresponse']}"/>
            <input type="hidden" name="Heure (Saint-Martin)" id="sxmTime" value=""/>
            <div class="form-row">
              <div class="form-group"><label data-i18n="f.name">Prénom & Nom *</label><input type="text" name="Nom complet" placeholder="Jean Dupont" required/></div>
              <div class="form-group"><label data-i18n="f.phone">Téléphone *</label><input type="tel" name="Telephone" placeholder="+590 690 43 28 18" required/></div>
            </div>
            <div class="form-group"><label>Email *</label><input type="email" name="Email" placeholder="{ct['ph_email']}" required/></div>
            <div class="form-group">
              <label data-i18n="f.svc">Type de prestation *</label>
              <select name="Service demande" id="selectService" required>
                <option value="" disabled selected data-i18n="f.svc.ph">Sélectionnez un service</option>
                <option value="Terrassement VRD" data-i18n="svc1.h">Terrassement & VRD</option>
                <option value="Amenagement Exterieur" data-i18n="svc2.h">Aménagement Extérieur</option>
                <option value="Second Oeuvre" data-i18n="svc3.h">Travaux de Second Œuvre</option>
                <option value="Multiservices Maintenance" data-i18n="svc4.h">Multiservices & Maintenance</option>
                <option value="Autre / Plusieurs services" data-i18n="f.svc.other">Autre / Plusieurs services</option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label data-i18n="f.loc">Localisation du chantier</label>
                <select name="Localisation" id="selectLocation">
                  <option value="" disabled selected data-i18n="f.loc.ph">Partie française ou NL ?</option>
                  <option value="Saint-Martin FR" data-i18n="f.loc.fr">Saint-Martin (FR)</option>
                  <option value="Sint Maarten NL" data-i18n="f.loc.nl">Sint Maarten (NL)</option>
                  <option value="Les deux cotes" data-i18n="f.loc.both">Les deux</option>
                  <option value="Autre ile" data-i18n="f.loc.other">Autre île</option>
                </select>
              </div>
              <div class="form-group">
                <label data-i18n="f.budget">Budget estimé</label>
                <select name="Budget" id="selectBudget">
                  <option value="" disabled selected data-i18n="f.budget.ph">Budget indicatif</option>
                  <option value="Moins de 5000">{ct['budget_lt5']}</option>
                  <option value="5000-20000">{ct['budget_5_20']}</option>
                  <option value="20000-50000">{ct['budget_20_50']}</option>
                  <option value="50000-100000">{ct['budget_50_100']}</option>
                  <option value="Plus de 100000">{ct['budget_gt100']}</option>
                </select>
              </div>
            </div>
            <div class="form-group"><label data-i18n="f.msg">Description de votre projet *</label><textarea name="Description" id="msgTextarea" placeholder="{ct['ph_msg']}" required></textarea></div>
            <button type="submit" class="form-submit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              <span data-i18n="f.submit">Envoyer ma demande</span>
            </button>
          </form>
          <div class="form-success" id="formSuccess"><span data-i18n="f.success">Merci ! Votre demande a bien été reçue. Notre équipe vous contacte sous 24h.</span></div>
        </div>
      </div>
    </div>
  </div>
</section>"""


CONTENT_BUILDERS = {
    'services': content_services,
    'approche': content_approche,
    'valeurs':  content_valeurs,
    'zone':     content_zone,
    'contact':  content_contact,
}


def content_mentions_legales(lc):
    home = lc['home']
    home_label = lc['home_label']
    bc = LEGAL_META['mentions-legales'][lc['lang']]['breadcrumb']
    return f"""<section class="page-hero" style="min-height:280px;">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb"><a href="{home}">{home_label}</a><span>›</span><span>{bc}</span></nav>
    <span class="section-tag">{bc}</span>
    <h1 style="font-size:2rem;">{bc}</h1>
  </div>
</section>
<section class="section" style="padding:80px 0;">
  <div class="container" style="max-width:800px;">
    <div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:48px;">
      <div data-legal-lang="fr" {'style="display:none"' if lc['lang'] != 'fr' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Mentions légales</h2>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Éditeur</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Raison sociale</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">FTFL CARAÏBES</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">SIREN</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">102 641 339</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">SIRET</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">102 641 339 00010</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Forme juridique</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">Société par actions simplifiée (SAS)</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Siège social</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Email</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);"><a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Téléphone</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);"><a href="tel:+590690432818" style="color:var(--orange);">+590 690 43 28 18</a></td></tr>
        </table>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Hébergement</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Site hébergé par Cloudflare Pages — Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Propriété intellectuelle</h3>
        <p style="color:var(--gray-light);line-height:1.8;">L'ensemble des contenus (textes, images, logo) est la propriété exclusive de FTFL CARAÏBES. Toute reproduction sans autorisation écrite préalable est strictement interdite.</p>
      </div>
      <div data-legal-lang="en" {'style="display:none"' if lc['lang'] != 'en' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Legal Notice</h2>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Publisher</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Company name</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">FTFL CARAÏBES</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">SIREN</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">102 641 339</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Legal form</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">Simplified joint-stock company (SAS)</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Registered office</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);">34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</td></tr>
          <tr><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);color:var(--gray-light);">Email</td><td style="padding:8px 12px;border:1px solid rgba(255,255,255,.1);"><a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></td></tr>
        </table>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Hosting</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Site hosted by Cloudflare Pages — Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Intellectual Property</h3>
        <p style="color:var(--gray-light);line-height:1.8;">All content (text, images, logo) is the exclusive property of FTFL CARAÏBES. Any reproduction without prior written authorization is strictly prohibited.</p>
      </div>
      <div data-legal-lang="es" {'style="display:none"' if lc['lang'] != 'es' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Aviso Legal</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;"><strong>FTFL CARAÏBES</strong> — SAS — SIREN 102 641 339 — SIRET 102 641 339 00010 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin — <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a> — <a href="tel:+590690432818" style="color:var(--orange);">+590 690 43 28 18</a></p>
        <p style="color:var(--gray-light);line-height:1.8;">Todos los contenidos son propiedad exclusiva de FTFL CARAÏBES. Queda prohibida su reproducción sin autorización previa por escrito.</p>
      </div>
      <div data-legal-lang="nl" {'style="display:none"' if lc['lang'] != 'nl' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Juridische Informatie</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;"><strong>FTFL CARAÏBES</strong> — SAS — SIREN 102 641 339 — SIRET 102 641 339 00010 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin — <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a> — <a href="tel:+590690432818" style="color:var(--orange);">+590 690 43 28 18</a></p>
        <p style="color:var(--gray-light);line-height:1.8;">Alle inhoud is het exclusieve eigendom van FTFL CARAÏBES. Reproductie zonder voorafgaande schriftelijke toestemming is verboden.</p>
      </div>
      <div data-legal-lang="pt" {'style="display:none"' if lc['lang'] != 'pt' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Menções Legais</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;"><strong>FTFL CARAÏBES</strong> — SAS — SIREN 102 641 339 — SIRET 102 641 339 00010 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin — <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a> — <a href="tel:+590690432818" style="color:var(--orange);">+590 690 43 28 18</a></p>
        <p style="color:var(--gray-light);line-height:1.8;">Todo o conteúdo é propriedade exclusiva da FTFL CARAÏBES. É proibida qualquer reprodução sem autorização prévia por escrito.</p>
      </div>
    </div>
  </div>
</section>"""


def content_confidentialite(lc):
    home = lc['home']
    home_label = lc['home_label']
    bc = LEGAL_META['confidentialite'][lc['lang']]['breadcrumb']
    return f"""<section class="page-hero" style="min-height:280px;">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb"><a href="{home}">{home_label}</a><span>›</span><span>{bc}</span></nav>
    <span class="section-tag">{bc}</span>
    <h1 style="font-size:2rem;">{bc}</h1>
  </div>
</section>
<section class="section" style="padding:80px 0;">
  <div class="container" style="max-width:800px;">
    <div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:48px;">
      <div {'style="display:none"' if lc['lang'] != 'fr' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Politique de confidentialité</h2>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Données collectées</h3>
        <p style="color:var(--gray-light);line-height:1.8;">FTFL CARAÏBES collecte uniquement les données que vous nous transmettez via le formulaire de contact : nom, téléphone, email, description de projet. Ces données sont utilisées exclusivement pour répondre à vos demandes de devis et ne sont jamais cédées à des tiers.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Durée de conservation</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Vos données sont conservées pendant 3 ans à compter de votre dernier contact, conformément à la réglementation française.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Vos droits (RGPD)</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Conformément au Règlement Général sur la Protection des Données (RGPD), vous disposez d'un droit d'accès, de rectification, d'effacement et de portabilité de vos données. Pour exercer ces droits : <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Cookies</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Ce site n'utilise pas de cookies de traçage ou publicitaires. Seules des données techniques essentielles au bon fonctionnement du site peuvent être utilisées.</p>
      </div>
      <div {'style="display:none"' if lc['lang'] != 'en' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Privacy Policy</h2>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Data collected</h3>
        <p style="color:var(--gray-light);line-height:1.8;">FTFL CARAÏBES only collects data you submit via the contact form: name, phone, email, project description. This data is used exclusively to respond to your quote requests and is never shared with third parties.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Retention period</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Your data is retained for 3 years from your last contact, in accordance with French regulations.</p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Your rights (GDPR)</h3>
        <p style="color:var(--gray-light);line-height:1.8;">Under the General Data Protection Regulation (GDPR), you have the right to access, rectify, delete and port your data. To exercise these rights: <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></p>
        <h3 style="font-size:1rem;font-weight:700;margin:24px 0 12px;">Cookies</h3>
        <p style="color:var(--gray-light);line-height:1.8;">This site does not use tracking or advertising cookies. Only essential technical data for site operation may be used.</p>
      </div>
      <div {'style="display:none"' if lc['lang'] != 'es' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Política de Privacidad</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;">FTFL CARAÏBES recopila únicamente los datos que usted transmite mediante el formulario de contacto (nombre, teléfono, email, descripción del proyecto), utilizados exclusivamente para responder a sus solicitudes de presupuesto.</p>
        <p style="color:var(--gray-light);line-height:1.8;">Para ejercer sus derechos de acceso, rectificación o supresión según el RGPD: <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></p>
      </div>
      <div {'style="display:none"' if lc['lang'] != 'nl' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Privacybeleid</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;">FTFL CARAÏBES verzamelt uitsluitend de gegevens die u via het contactformulier indient (naam, telefoon, e-mail, projectomschrijving), uitsluitend gebruikt om te reageren op uw offerteverzoeken.</p>
        <p style="color:var(--gray-light);line-height:1.8;">Voor het uitoefenen van uw rechten onder de AVG: <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></p>
      </div>
      <div {'style="display:none"' if lc['lang'] != 'pt' else ''}>
        <h2 style="font-family:var(--font-head);font-size:1.4rem;font-weight:800;margin-bottom:24px;">Política de Privacidade</h2>
        <p style="color:var(--gray-light);line-height:1.8;margin-bottom:16px;">A FTFL CARAÏBES recolhe apenas os dados que transmite através do formulário de contacto (nome, telefone, email, descrição do projeto), utilizados exclusivamente para responder às suas solicitações de orçamento.</p>
        <p style="color:var(--gray-light);line-height:1.8;">Para exercer os seus direitos ao abrigo do RGPD: <a href="mailto:contact@ftfl-sxm.com" style="color:var(--orange);">contact@ftfl-sxm.com</a></p>
      </div>
    </div>
  </div>
</section>"""


LEGAL_CONTENT_BUILDERS = {
    'mentions-legales': content_mentions_legales,
    'confidentialite':  content_confidentialite,
}


# ── Générateur de page ────────────────────────────────────────────

def generate_sitemap():
    """Generate sitemap.xml with today's date as lastmod for all 40 URLs."""
    today = datetime.date.today().isoformat()

    def hreflang_block(slug, indent='    '):
        lines = []
        for lk in LANG_ORDER:
            url = slug_url(lk, slug)
            lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="{lk}" href="{url}"/>')
        fr_slug = SLUG_TRANSLATIONS[slug]['fr']
        lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/{fr_slug}/"/>')
        return '\n'.join(lines)

    def home_hreflang(indent='    '):
        lines = []
        for lk in LANG_ORDER:
            url = f'{BASE_URL}/{lk}/' if lk != 'fr' else f'{BASE_URL}/'
            lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="{lk}" href="{url}"/>')
        lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>')
        return '\n'.join(lines)

    urls = []

    # Home pages
    home_prios = {'fr': '1.0', 'en': '0.9', 'es': '0.9', 'nl': '0.9', 'pt': '0.9'}
    for lk in LANG_ORDER:
        loc = f'{BASE_URL}/{lk}/' if lk != 'fr' else f'{BASE_URL}/'
        prio = home_prios[lk]
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority>
{home_hreflang()}
  </url>""")

    # SEO pages (5 slugs × 5 langs)
    for slug in PAGE_SLUGS:
        for lk in LANG_ORDER:
            loc = slug_url(lk, slug)
            urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority>
{hreflang_block(slug)}
  </url>""")

    # Legal pages (2 slugs × 5 langs)
    for slug in LEGAL_SLUGS:
        for lk in LANG_ORDER:
            loc = slug_url(lk, slug)
            urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority>
{hreflang_block(slug)}
  </url>""")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    xml += '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n\n'
    xml += '\n'.join(urls)
    xml += '\n</urlset>\n'

    out_path = os.path.join(BASE_DIR, 'sitemap.xml')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f'[OK] sitemap.xml  ({len(urls)} URLs, lastmod={today})')


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

        result.append(html[pos:open_end])
        result.append(translations[key])
        result.append(close_m.group(0))
        pos = close_m.end()

    return ''.join(result)


def build_page(lc, slug, meta, og_image, content_html, breadcrumb_schema_html):
    lang     = lc['lang']
    canonical = slug_url(lang, slug)
    return f"""<!DOCTYPE html>
<html lang="{lang}" prefix="og: https://ogp.me/ns#">
<head>
{build_head(lc, slug, meta, og_image)}

{breadcrumb_schema_html}
</head>
<body>

{build_navbar(lc, slug)}

{content_html}

{build_footer(lc)}

<script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
<script src="/js/scripts.js"></script>
</body>
</html>"""


# ── Écriture des fichiers ─────────────────────────────────────────

def write_page(rel_dir, html):
    out_dir  = os.path.join(BASE_DIR, *rel_dir.strip('/').split('/'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return out_path


if __name__ == '__main__':

    # ── 25 pages SEO ────────────────────────────────────────────
    for slug in PAGE_SLUGS:
        for lang_code in LANG_ORDER:
            lc       = LANG_CONFIGS[lang_code]
            meta     = PAGE_META[slug][lang_code]
            og_image = OG_IMAGES[slug]
            canonical = slug_url(lang_code, slug)
            bc_schema = build_breadcrumb_schema(lc, slug, meta, canonical)
            content   = CONTENT_BUILDERS[slug](lc)
            html      = build_page(lc, slug, meta, og_image, content, bc_schema)
            if lang_code != 'fr':
                html = apply_i18n(html, lang_code)

            translated = SLUG_TRANSLATIONS[slug][lang_code]
            rel = f'/{translated}/' if lang_code == 'fr' else f'/{lang_code}/{translated}/'
            write_page(rel, html)
            print(f'[OK] {rel}')

    # ── 10 pages légales ────────────────────────────────────────
    for slug in LEGAL_SLUGS:
        for lang_code in LANG_ORDER:
            lc       = LANG_CONFIGS[lang_code]
            meta     = LEGAL_META[slug][lang_code]
            meta_full = {
                'title': meta['title'], 'desc': meta['desc'],
                'og_title': meta['title'], 'og_desc': meta['desc'],
                'tw_title': meta['title'], 'tw_desc': meta['desc'],
                'breadcrumb': meta['breadcrumb'],
            }
            og_image  = OG_IMAGES[slug]
            canonical = slug_url(lang_code, slug)
            bc_schema = build_breadcrumb_schema(lc, slug, meta_full, canonical)
            content   = LEGAL_CONTENT_BUILDERS[slug](lc)
            html      = build_page(lc, slug, meta_full, og_image, content, bc_schema)
            if lang_code != 'fr':
                html = apply_i18n(html, lang_code)

            translated = SLUG_TRANSLATIONS[slug][lang_code]
            rel = f'/{translated}/' if lang_code == 'fr' else f'/{lang_code}/{translated}/'
            write_page(rel, html)
            print(f'[OK] {rel}')

    print(f'\n[DONE] {len(PAGE_SLUGS)*len(LANG_ORDER)} SEO pages + {len(LEGAL_SLUGS)*len(LANG_ORDER)} legal pages generated.')

    # ── Sitemap auto-généré ──────────────────────────────────────
    generate_sitemap()
    print('Pensez a commit + push sur GitHub.')

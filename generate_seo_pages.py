"""
generate_seo_pages.py
Génère les 5 pages SEO supplémentaires :
  /services/, /approche/, /valeurs/, /zone/, /contact/

Ces pages sont ADDITIONNELLES à index.html (one-page intact).
À relancer si le contenu de base change.

Usage : python generate_seo_pages.py
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Blocs partagés ────────────────────────────────────────────

HEAD_COMMON = """  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>
  <meta name="author"    content="FTFL CARAÏBES"/>
  <meta name="copyright" content="FTFL CARAÏBES 2025"/>

  <!-- GEO -->
  <meta name="geo.region"     content="FR-MF"/>
  <meta name="geo.placename"  content="Saint-Martin, Caraïbes"/>
  <meta name="geo.position"   content="18.0735;-63.0820"/>
  <meta name="ICBM"           content="18.0735, -63.0820"/>

  <!-- HREFLANG -->
  <link rel="alternate" hreflang="fr"        href="https://www.ftfl-sxm.com/"/>
  <link rel="alternate" hreflang="en"        href="https://www.ftfl-sxm.com/en/"/>
  <link rel="alternate" hreflang="es"        href="https://www.ftfl-sxm.com/es/"/>
  <link rel="alternate" hreflang="nl"        href="https://www.ftfl-sxm.com/nl/"/>
  <link rel="alternate" hreflang="pt"        href="https://www.ftfl-sxm.com/pt/"/>
  <link rel="alternate" hreflang="x-default" href="https://www.ftfl-sxm.com/"/>

  <!-- FAVICON -->
  <link rel="icon"             type="image/png" href="/images/Logo FTFL.png"/>
  <link rel="apple-touch-icon" href="/images/Logo FTFL.png"/>
  <meta name="theme-color"     content="#1B6B35"/>

  <!-- FONTS & CSS -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link rel="dns-prefetch" href="https://unpkg.com"/>
  <meta name="color-scheme" content="dark"/>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="https://unpkg.com/aos@2.3.4/dist/aos.css"/>
  <link rel="stylesheet" href="/css/styles.css"/>"""

SCRIPTS = """<script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
<script src="/js/scripts.js"></script>"""

NAVBAR = """<!-- PRELOADER -->
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
  <a href="/" onclick="closeMobileNav()" data-i18n="nav.about">À propos</a>
  <a href="/services/" onclick="closeMobileNav()" data-i18n="nav.services">Services</a>
  <a href="/approche/" onclick="closeMobileNav()" data-i18n="nav.approach">Approche</a>
  <a href="/valeurs/" onclick="closeMobileNav()" data-i18n="nav.values">Valeurs</a>
  <a href="/zone/" onclick="closeMobileNav()" data-i18n="nav.zone">Zone</a>
  <a href="/contact/" onclick="closeMobileNav()" data-i18n="nav.cta">Contactez-nous</a>
</div>

<!-- NAVBAR -->
<nav class="navbar" id="navbar">
  <div class="container">
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/" class="navbar-logo">
        <img src="/images/Logo FTFL.png" alt="FTFL CARAÏBES" width="140" height="56"/>
      </a>
      <div class="lang-switcher" id="langSwitcher">
        <div class="lang-btn" onclick="toggleLang()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span id="langCurrent">FR</span>
          <svg class="chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="lang-dropdown" id="langDropdown">
          <a class="lang-option active" data-lang="fr" href="/"><span class="lang-flag">🇫🇷</span> Français</a>
          <a class="lang-option" data-lang="en" href="/en/"><span class="lang-flag">🇺🇸</span> English</a>
          <a class="lang-option" data-lang="es" href="/es/"><span class="lang-flag">🇪🇸</span> Español</a>
          <a class="lang-option" data-lang="nl" href="/nl/"><span class="lang-flag">🇳🇱</span> Nederlands</a>
          <a class="lang-option" data-lang="pt" href="/pt/"><span class="lang-flag">🇵🇹</span> Português</a>
        </div>
      </div>
    </div>
    <ul class="nav-links">
      <li><a href="/" data-i18n="nav.about">À propos</a></li>
      <li><a href="/services/" data-i18n="nav.services">Services</a></li>
      <li><a href="/approche/" data-i18n="nav.approach">Approche</a></li>
      <li><a href="/valeurs/" data-i18n="nav.values">Valeurs</a></li>
      <li><a href="/zone/" data-i18n="nav.zone">Zone</a></li>
    </ul>
    <div class="navbar-cta">
      <a href="/contact/" class="btn btn-primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg>
        <span data-i18n="nav.cta">Contactez-nous</span>
      </a>
    </div>
    <div class="burger" onclick="openMobileNav()">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="footer-logo"><img src="/images/Logo FTFL.png" alt="FTFL CARAÏBES"/></div>
        <p data-i18n="ft.desc">Un seul partenaire pour tous vos travaux à Saint-Martin. Terrassement, VRD, aménagement extérieur, second œuvre et multiservices.</p>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.svc">Services</h4>
        <ul>
          <li><a href="/services/" data-i18n="ft.svc1">Terrassement & VRD</a></li>
          <li><a href="/services/" data-i18n="ft.svc2">Aménagement Extérieur</a></li>
          <li><a href="/services/" data-i18n="ft.svc3">Second Œuvre</a></li>
          <li><a href="/services/" data-i18n="ft.svc4">Multiservices</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.co">Entreprise</h4>
        <ul>
          <li><a href="/" data-i18n="ft.about">À propos</a></li>
          <li><a href="/valeurs/" data-i18n="ft.vals">Nos valeurs</a></li>
          <li><a href="/approche/" data-i18n="ft.app">Notre approche</a></li>
          <li><a href="/" data-i18n="ft.team">L'équipe</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 data-i18n="ft.h.ct">Contact</h4>
        <ul>
          <li><a href="tel:+590690432818">+590 690 43 28 18</a></li>
          <li><a href="https://wa.me/590690432818" target="_blank" rel="noopener">WhatsApp : +590 690 43 28 18</a></li>
          <li><a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></li>
          <li><a href="https://www.linkedin.com/company/ftfl-cara%C3%AFbes/" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="/contact/" data-i18n="ft.quote">Demander un devis</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span data-i18n="ft.copy">© 2025 FTFL CARAÏBES — Tous droits réservés</span>
      <div class="footer-legal-links">
        <a href="#" onclick="openLegalModal('modalMentions');return false;" data-i18n="ft.legal1">Mentions légales</a>
        <span aria-hidden="true">·</span>
        <a href="#" onclick="openLegalModal('modalPrivacy');return false;" data-i18n="ft.legal2">Politique de confidentialité</a>
      </div>
      <span data-i18n="ft.slogan">Saint-Martin · Sint Maarten · Caraïbes 🌴</span>
    </div>
  </div>
</footer>"""

LEGAL_MODALS = """<div class="legal-modal" id="modalMentions" role="dialog" aria-modal="true">
  <div class="legal-modal-overlay" onclick="closeLegalModal('modalMentions')"></div>
  <div class="legal-modal-box">
    <button class="legal-close" onclick="closeLegalModal('modalMentions')" aria-label="Fermer">✕</button>
    <div data-legal-lang="fr"><h2>Mentions légales</h2>
      <div class="legal-section"><h3>Éditeur</h3><table class="legal-table">
        <tr><td>Raison sociale</td><td>FTFL CARAÏBES</td></tr>
        <tr><td>SIREN</td><td>102 641 339</td></tr><tr><td>SIRET</td><td>102 641 339 00010</td></tr>
        <tr><td>Forme juridique</td><td>Société par actions simplifiée (SAS)</td></tr>
        <tr><td>Siège social</td><td>34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</td></tr>
        <tr><td>Email</td><td><a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></td></tr>
        <tr><td>Téléphone</td><td><a href="tel:+590690432818">+590 690 43 28 18</a></td></tr>
      </table></div>
      <div class="legal-section"><h3>Propriété intellectuelle</h3><p>L'ensemble des contenus est la propriété exclusive de FTFL CARAÏBES. Toute reproduction sans autorisation est interdite.</p></div>
    </div>
    <div data-legal-lang="en" style="display:none"><h2>Legal Notice</h2>
      <div class="legal-section"><h3>Publisher</h3><table class="legal-table">
        <tr><td>Company name</td><td>FTFL CARAÏBES</td></tr>
        <tr><td>SIREN</td><td>102 641 339</td></tr><tr><td>SIRET</td><td>102 641 339 00010</td></tr>
        <tr><td>Legal form</td><td>Simplified joint-stock company (SAS)</td></tr>
        <tr><td>Registered office</td><td>34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</td></tr>
        <tr><td>Email</td><td><a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></td></tr>
      </table></div>
    </div>
    <div data-legal-lang="es" style="display:none"><h2>Aviso legal</h2>
      <div class="legal-section"><h3>Editor</h3><p>FTFL CARAÏBES — SAS — SIREN 102 641 339 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</p></div>
    </div>
    <div data-legal-lang="nl" style="display:none"><h2>Juridische informatie</h2>
      <div class="legal-section"><h3>Uitgever</h3><p>FTFL CARAÏBES — SAS — SIREN 102 641 339 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</p></div>
    </div>
    <div data-legal-lang="pt" style="display:none"><h2>Menções legais</h2>
      <div class="legal-section"><h3>Editor</h3><p>FTFL CARAÏBES — SAS — SIREN 102 641 339 — 34 rue de l'Escale, Oyster Pond, 97150 Saint-Martin</p></div>
    </div>
  </div>
</div>
<div class="legal-modal" id="modalPrivacy" role="dialog" aria-modal="true">
  <div class="legal-modal-overlay" onclick="closeLegalModal('modalPrivacy')"></div>
  <div class="legal-modal-box">
    <button class="legal-close" onclick="closeLegalModal('modalPrivacy')" aria-label="Fermer">✕</button>
    <div data-legal-lang="fr"><h2>Politique de confidentialité</h2>
      <div class="legal-section"><h3>Données collectées</h3><p>FTFL CARAÏBES collecte uniquement les données que vous nous transmettez via le formulaire de contact (nom, téléphone, email, description de projet). Ces données sont utilisées exclusivement pour répondre à vos demandes de devis.</p></div>
      <div class="legal-section"><h3>Vos droits</h3><p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification et de suppression de vos données. Contactez-nous : <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></p></div>
    </div>
    <div data-legal-lang="en" style="display:none"><h2>Privacy Policy</h2>
      <div class="legal-section"><h3>Data collected</h3><p>FTFL CARAÏBES only collects data you submit via the contact form (name, phone, email, project description). This data is used exclusively to respond to your quote requests.</p></div>
      <div class="legal-section"><h3>Your rights</h3><p>Under GDPR, you have the right to access, rectify and delete your data. Contact us: <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></p></div>
    </div>
    <div data-legal-lang="es" style="display:none"><h2>Política de privacidad</h2>
      <div class="legal-section"><p>FTFL CARAÏBES recopila únicamente los datos que usted nos transmite mediante el formulario de contacto. Para ejercer sus derechos: <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></p></div>
    </div>
    <div data-legal-lang="nl" style="display:none"><h2>Privacybeleid</h2>
      <div class="legal-section"><p>FTFL CARAÏBES verzamelt uitsluitend de gegevens die u via het contactformulier indient. Voor uw rechten: <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></p></div>
    </div>
    <div data-legal-lang="pt" style="display:none"><h2>Política de privacidade</h2>
      <div class="legal-section"><p>A FTFL CARAÏBES recolhe apenas os dados que nos transmite através do formulário de contacto. Para exercer os seus direitos: <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a></p></div>
    </div>
  </div>
</div>"""

# ── Pages définitions ──────────────────────────────────────────

PAGES = {
    'services': {
        'dir': 'services',
        'canonical': 'https://www.ftfl-sxm.com/services/',
        'og_image': 'https://www.ftfl-sxm.com/images/FTFL-WEB-2.jpg',
        'title': 'FTFL CARAÏBES | Services de Construction Saint-Martin | Terrassement, Aménagement, Second Œuvre',
        'desc': 'Découvrez les services de construction de FTFL CARAÏBES à Saint-Martin : terrassement et VRD, aménagement extérieur, travaux de second œuvre, multiservices et maintenance. Devis gratuit.',
        'keywords': 'services construction Saint-Martin, terrassement Saint-Martin, VRD Saint-Martin, aménagement extérieur Saint-Martin, second oeuvre Saint-Martin, piscine Saint-Martin, clôtures Saint-Martin, plomberie Saint-Martin, peinture Saint-Martin, renovation Saint-Martin, multiservices Saint-Martin, maintenance Saint-Martin, entreprise BTP SXM',
        'breadcrumb': 'Services',
        'schema_type': 'Service',
        'content': lambda: SERVICES_CONTENT,
    },
    'approche': {
        'dir': 'approche',
        'canonical': 'https://www.ftfl-sxm.com/approche/',
        'og_image': 'https://www.ftfl-sxm.com/images/FTFL-WEB-3.webp',
        'title': 'FTFL CARAÏBES | Notre Méthode de Travail | Processus Construction Saint-Martin',
        'desc': 'La méthode FTFL CARAÏBES : 4 étapes clés pour mener vos projets de construction à Saint-Martin avec rigueur et transparence — écoute, étude, exécution, livraison.',
        'keywords': 'méthode construction Saint-Martin, processus BTP Saint-Martin, gestion chantier Saint-Martin, chef de chantier Saint-Martin, suivi travaux Saint-Martin, devis construction Saint-Martin, planning chantier SXM',
        'breadcrumb': 'Notre Méthode',
        'schema_type': 'HowTo',
        'content': lambda: APPROCHE_CONTENT,
    },
    'valeurs': {
        'dir': 'valeurs',
        'canonical': 'https://www.ftfl-sxm.com/valeurs/',
        'og_image': 'https://www.ftfl-sxm.com/images/FTFL-WEB-3.webp',
        'title': 'FTFL CARAÏBES | Nos Valeurs | Entreprise de Construction Saint-Martin',
        'desc': 'Les valeurs fondatrices de FTFL CARAÏBES : ancrage local, fiabilité, polyvalence et exigence. Découvrez ce qui fait la différence de votre partenaire BTP à Saint-Martin.',
        'keywords': 'valeurs entreprise construction Saint-Martin, BTP Saint-Martin fiable, partenaire construction SXM, qualité construction Saint-Martin, engagement BTP Saint-Martin',
        'breadcrumb': 'Nos Valeurs',
        'schema_type': 'Organization',
        'content': lambda: VALEURS_CONTENT,
    },
    'zone': {
        'dir': 'zone',
        'canonical': 'https://www.ftfl-sxm.com/zone/',
        'og_image': 'https://www.ftfl-sxm.com/images/FTFL-WEB-1.webp',
        'title': "FTFL CARAÏBES | Zone d'Intervention Saint-Martin Sint Maarten | Construction SXM",
        'desc': "FTFL CARAÏBES intervient sur toute l'île de Saint-Martin / Sint Maarten : Orient Bay, Marigot, Grand Case, Philipsburg, Simpson Bay et plus. Construction côté français et hollandais.",
        'keywords': "zone intervention construction Saint-Martin, travaux Sint Maarten, chantier côté français Saint-Martin, chantier côté hollandais Sint Maarten, entreprise BTP toute l'île SXM, Orient Bay, Marigot, Philipsburg, construction SXM",
        'breadcrumb': "Zone d'Intervention",
        'schema_type': 'Place',
        'content': lambda: ZONE_CONTENT,
    },
    'contact': {
        'dir': 'contact',
        'canonical': 'https://www.ftfl-sxm.com/contact/',
        'og_image': 'https://www.ftfl-sxm.com/images/Logo%20FTFL.png',
        'title': 'FTFL CARAÏBES | Contact & Devis Gratuit | Construction Saint-Martin Sint Maarten',
        'desc': 'Contactez FTFL CARAÏBES pour votre projet de construction à Saint-Martin. Devis gratuit et sans engagement. Réponse sous 24h. Téléphone, WhatsApp, email et formulaire en ligne.',
        'keywords': 'contact FTFL CARAÏBES, devis gratuit construction Saint-Martin, demander devis BTP SXM, contacter entreprise construction Saint-Martin, téléphone construction Saint-Martin, WhatsApp BTP SXM',
        'breadcrumb': 'Contact',
        'schema_type': 'ContactPage',
        'content': lambda: CONTACT_CONTENT,
    },
}

# ── Contenu des sections ───────────────────────────────────────

SERVICES_CONTENT = """<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="/">Accueil</a>
      <span>›</span>
      <span>Services</span>
    </nav>
    <span class="section-tag" data-i18n="services.tag">Nos Métiers</span>
    <h1 data-i18n="services.title">Une réponse complète<br/>à <span class="highlight">chaque besoin.</span></h1>
    <p data-i18n="services.sub">Du terrassement aux finitions, FTFL couvre l'ensemble des corps d'état avec les mêmes standards d'exigence.</p>
    <a href="/contact/" class="btn btn-primary" style="margin-top:12px;">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg>
      Demander un devis gratuit
    </a>
  </div>
</section>

<section class="section services" id="services">
  <div class="container">
    <div class="grid-4">
      <div class="service-card" data-aos="fade-up" data-aos-delay="0">
        <div class="service-number">01</div>
        <div class="service-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 22h20"/><path d="M6.87 2h10.26L20 7H4L6.87 2Z"/><path d="M4 7h16v15H4V7Z"/><path d="M9 22V12h6v10"/></svg>
        </div>
        <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:12px;font-family:var(--font-head);" data-i18n="svc1.h">Terrassement & VRD</h2>
        <p data-i18n="svc1.p">Nous préparons le terrain pour vos projets avec des moyens adaptés aux spécificités de l'île.</p>
        <div class="service-tags" data-i18n="svc1.tags">
          <span class="service-tag">Terrassement général</span><span class="service-tag">Décaissement</span>
          <span class="service-tag">Fouilles</span><span class="service-tag">Voiries</span>
          <span class="service-tag">Assainissement</span><span class="service-tag">Enrochement</span><span class="service-tag">Drainage</span>
        </div>
      </div>
      <div class="service-card" data-aos="fade-up" data-aos-delay="80">
        <div class="service-number">02</div>
        <div class="service-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        </div>
        <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:12px;font-family:var(--font-head);" data-i18n="svc2.h">Aménagement Extérieur</h2>
        <p data-i18n="svc2.p">Nous concevons et réalisons vos espaces extérieurs pour sublimer vos propriétés.</p>
        <div class="service-tags" data-i18n="svc2.tags">
          <span class="service-tag">Clôtures & portails</span><span class="service-tag">Terrasses</span>
          <span class="service-tag">Pergolas</span><span class="service-tag">Piscines</span>
          <span class="service-tag">Paysager</span><span class="service-tag">Éclairage ext.</span><span class="service-tag">Citernes</span>
        </div>
      </div>
      <div class="service-card" data-aos="fade-up" data-aos-delay="160">
        <div class="service-number">03</div>
        <div class="service-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        </div>
        <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:12px;font-family:var(--font-head);" data-i18n="svc3.h">Travaux de Second Œuvre</h2>
        <p data-i18n="svc3.p">FTFL prend en charge l'ensemble des travaux de finition et de réhabilitation pour mener vos projets à leur terme.</p>
        <div class="service-tags" data-i18n="svc3.tags">
          <span class="service-tag">Menuiserie</span><span class="service-tag">Plomberie</span>
          <span class="service-tag">Carrelage</span><span class="service-tag">Peinture</span>
          <span class="service-tag">Serrurerie</span><span class="service-tag">Métallerie</span><span class="service-tag">Rénovation</span>
        </div>
      </div>
      <div class="service-card" data-aos="fade-up" data-aos-delay="240">
        <div class="service-number">04</div>
        <div class="service-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>
        </div>
        <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:12px;font-family:var(--font-head);" data-i18n="svc4.h">Multiservices & Maintenance</h2>
        <p data-i18n="svc4.p">Un interlocuteur unique pour l'entretien courant, la maintenance et les interventions rapides sur votre patrimoine.</p>
        <div class="service-tags" data-i18n="svc4.tags">
          <span class="service-tag">Maintenance préventive</span><span class="service-tag">Dépannage</span>
          <span class="service-tag">Nettoyage chantier</span><span class="service-tag">Petits travaux</span>
          <span class="service-tag">Contrats maintenance</span><span class="service-tag">Urgences 24h</span>
        </div>
      </div>
    </div>

    <!-- Texte SEO enrichi -->
    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;">Pourquoi confier vos travaux à FTFL CARAÏBES ?</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;">
        <div>
          <p style="color:var(--gray-light);line-height:1.85;margin-bottom:16px;">
            Entreprise de construction implantée à Saint-Martin, FTFL CARAÏBES intervient sur l'ensemble de l'île — côté français (collectivité de Saint-Martin) comme côté hollandais (Sint Maarten). Notre polyvalence est notre force : en confiant votre chantier à FTFL, vous bénéficiez d'un <strong style="color:#fff;">interlocuteur unique</strong> pour l'ensemble de vos travaux, des terrassements jusqu'aux finitions intérieures.
          </p>
          <p style="color:var(--gray-light);line-height:1.85;">
            Que vous soyez un particulier en quête d'une rénovation complète, un promoteur immobilier, un hôtelier ou une collectivité locale, nos équipes adaptent leur intervention à votre projet et à vos contraintes budgétaires.
          </p>
        </div>
        <div>
          <p style="color:var(--gray-light);line-height:1.85;margin-bottom:16px;">
            Spécialistes des <strong style="color:#fff;">conditions de chantier caribéennes</strong> (climat tropical, logistique insulaire, normes locales), nous maîtrisons les défis propres à Saint-Martin : approvisionnement en matériaux, gestion des saisons cycloniques, réglementation des deux côtés de la frontière.
          </p>
          <p style="color:var(--gray-light);line-height:1.85;">
            Chaque projet bénéficie d'un <strong style="color:#fff;">chef de chantier dédié</strong>, d'un suivi quotidien et d'une communication transparente. Du devis gratuit à la livraison, FTFL s'engage à respecter les délais et les budgets convenus.
          </p>
        </div>
      </div>
      <div style="margin-top:28px;text-align:center;">
        <a href="/contact/" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          Demander un devis gratuit — Réponse sous 24h
        </a>
      </div>
    </div>
  </div>
</section>"""

APPROCHE_CONTENT = """<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="/">Accueil</a>
      <span>›</span>
      <span>Notre Méthode</span>
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
        <div class="step-circle">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg>
        </div>
        <h2 class="step-title" data-i18n="step1.h">01 · Écoute</h2>
        <p class="step-desc" data-i18n="step1.p">Nous prenons le temps de comprendre votre projet dans ses moindres détails — contraintes techniques, budget, calendrier — pour construire avec vous la stratégie la plus adaptée.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="100">
        <div class="step-circle">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <h2 class="step-title" data-i18n="step2.h">02 · Étude</h2>
        <p class="step-desc" data-i18n="step2.p">Chiffrage précis, planning prévisionnel, identification des risques : notre étude technique et financière vous donne une vision claire avant tout démarrage.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="200">
        <div class="step-circle">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        </div>
        <h2 class="step-title" data-i18n="step3.h">03 · Exécution</h2>
        <p class="step-desc" data-i18n="step3.p">Nos équipes s'engagent avec rigueur et savoir-faire. Un chef de chantier dédié coordonne chaque intervention et vous tient informé en temps réel.</p>
      </div>
      <div class="approach-step" data-aos="fade-up" data-aos-delay="300">
        <div class="step-circle">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        </div>
        <h2 class="step-title" data-i18n="step4.h">04 · Livraison</h2>
        <p class="step-desc" data-i18n="step4.p">Nous ne rendons les clés qu'une fois chaque détail achevé à votre satisfaction, dans le strict respect des règles de l'art et des délais convenus.</p>
      </div>
    </div>

    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;">Un engagement total du premier contact à la livraison</h2>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;">
        Chez FTFL CARAÏBES, notre méthode de travail repose sur une conviction : un projet bien préparé est un projet réussi. C'est pourquoi nous investissons du temps dès la phase d'écoute pour comprendre précisément vos attentes, vos contraintes techniques et votre budget. Cette rigueur initiale nous permet d'établir un devis précis, un planning réaliste et d'anticiper les risques avant que le premier coup de pelleteuse ne soit donné.
      </p>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;margin-top:16px;">
        Sur chantier, nos équipes travaillent sous la supervision d'un chef de chantier dédié qui assure le suivi quotidien des travaux et vous tient informé de l'avancement en temps réel. À Saint-Martin, les conditions locales (logistique insulaire, aléas climatiques tropicaux, approvisionnements) exigent une capacité d'adaptation permanente — une compétence que nous avons forgée au fil des années.
      </p>
      <div style="margin-top:28px;text-align:center;">
        <a href="/contact/" class="btn btn-primary">Démarrer votre projet avec FTFL</a>
      </div>
    </div>
  </div>
</section>"""

VALEURS_CONTENT = """<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="/">Accueil</a>
      <span>›</span>
      <span>Nos Valeurs</span>
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
        <div class="value-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val1.h">Ancrage Local</h2>
        <p data-i18n="val1.p">Implantés à Saint-Martin depuis nos débuts, nous connaissons chaque quartier, chaque fournisseur, chaque contrainte du terrain. Cette proximité nous rend réactifs et efficaces là où d'autres tâtonnent.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="80">
        <div class="value-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val2.h">Fiabilité</h2>
        <p data-i18n="val2.p">Un chantier qui démarre à l'heure, un budget maîtrisé, des engagements tenus jusqu'au bout. Chez FTFL, notre réputation se construit projet après projet, sur la force de notre parole.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="160">
        <div class="value-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val3.h">Polyvalence</h2>
        <p data-i18n="val3.p">Du terrassement aux finitions, de la villa privée au bâtiment commercial, nos équipes couvrent tous les corps d'état. Un seul interlocuteur, zéro coordination à gérer.</p>
      </div>
      <div class="value-card" data-aos="fade-up" data-aos-delay="240">
        <div class="value-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </div>
        <h2 style="font-family:var(--font-head);font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px;" data-i18n="val4.h">Exigence</h2>
        <p data-i18n="val4.p">Nous appliquons les mêmes standards de qualité sur chaque chantier, quelle que soit son envergure. Les normes locales, les délais, la sécurité : rien n'est laissé au hasard.</p>
      </div>
    </div>

    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;">Des valeurs forgées sur le terrain caribéen</h2>
      <p style="color:var(--gray-light);line-height:1.85;max-width:800px;">
        Ces quatre valeurs ne sont pas des slogans : elles reflètent ce que nous avons appris au fil des années de chantiers à Saint-Martin et Sint Maarten. L'<strong style="color:#fff;">ancrage local</strong> nous permet de réagir vite, d'avoir les bons contacts, et de comprendre les particularités d'un territoire insulaire où chaque projet représente un défi logistique. La <strong style="color:#fff;">fiabilité</strong> est ce qui nous a permis de fidéliser nos clients — particuliers, promoteurs, hôteliers — qui nous recommandent pour leur cohérence et leur sérieux.
      </p>
      <div style="margin-top:28px;text-align:center;">
        <a href="/contact/" class="btn btn-primary">Travailler avec FTFL CARAÏBES</a>
        <a href="/services/" class="btn btn-outline" style="margin-left:16px;">Voir nos services</a>
      </div>
    </div>
  </div>
</section>"""

ZONE_CONTENT = """<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="/">Accueil</a>
      <span>›</span>
      <span>Zone d'Intervention</span>
    </nav>
    <span class="section-tag" data-i18n="zone.tag">Zone d'Intervention</span>
    <h1 data-i18n="zone.title">Une île, deux pays,<br/><span class="highlight">une seule équipe.</span></h1>
    <p data-i18n="zone.sub">FTFL opère sur l'intégralité de l'île de Saint-Martin, côté français comme côté hollandais. Une double maîtrise réglementaire et logistique au service de vos projets.</p>
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
        <p data-i18n="zone.fr.desc">Maîtrise complète du cadre administratif et réglementaire français. Permis de construire, déclarations de travaux, normes RT : nous gérons tout.</p>
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
        <p data-i18n="zone.nl.desc">Connaissance approfondie du système réglementaire néerlandais. Nos équipes opèrent sur Sint Maarten avec la même efficacité qu'en partie française.</p>
        <div class="zone-places">
          <span class="zone-place">Philipsburg</span><span class="zone-place">Simpson Bay</span>
          <span class="zone-place">Cole Bay</span><span class="zone-place">Maho</span>
          <span class="zone-place">Cupecoy</span><span class="zone-place">Dutch Quarter</span>
          <span class="zone-place">Cay Bay</span>
        </div>
      </div>
    </div>
    <p class="zone-tagline" data-aos="fade-up" data-i18n="zone.tagline">
      + interventions ponctuelles sur <span>Saint-Barthélemy</span> & <span>Anguilla</span>
    </p>

    <div style="margin-top:80px;padding:48px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;position:relative;z-index:1;" data-aos="fade-up">
      <h2 style="font-family:var(--font-head);font-size:1.6rem;font-weight:800;margin-bottom:20px;">L'avantage d'un opérateur bi-frontalier</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;">
        <div>
          <p style="color:var(--gray-light);line-height:1.85;margin-bottom:16px;">
            Saint-Martin est une île unique en son genre : partagée entre la France et les Pays-Bas, elle offre deux cadres réglementaires distincts que peu d'entreprises maîtrisent vraiment. FTFL CARAÏBES est l'un des rares prestataires à opérer avec la même efficacité des <strong style="color:#fff;">deux côtés de la frontière</strong>.
          </p>
          <p style="color:var(--gray-light);line-height:1.85;">
            Côté français (collectivité de Saint-Martin, code INSEE 97150), nous gérons les permis de construire, les déclarations préalables de travaux, les normes RT et les règles d'urbanisme locales. Nos équipes connaissent parfaitement les délais administratifs et les interlocuteurs clés.
          </p>
        </div>
        <div>
          <p style="color:var(--gray-light);line-height:1.85;margin-bottom:16px;">
            Côté hollandais (Sint Maarten), nous maîtrisons le système de permis de construire néerlandais, les normes de construction locales et les pratiques du marché. Cette double expertise représente un gain de temps et de sérénité considérable pour nos clients qui ont des propriétés ou des projets des deux côtés de l'île.
          </p>
          <p style="color:var(--gray-light);line-height:1.85;">
            Des interventions ponctuelles peuvent également être organisées sur <strong style="color:#fff;">Saint-Barthélemy</strong> et <strong style="color:#fff;">Anguilla</strong> pour nos clients qui nous font confiance sur l'île principale.
          </p>
        </div>
      </div>
      <div style="margin-top:28px;text-align:center;">
        <a href="/contact/" class="btn btn-primary">Discuter de votre projet à Saint-Martin</a>
      </div>
    </div>
  </div>
</section>"""

CONTACT_CONTENT = """<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb">
      <a href="/">Accueil</a>
      <span>›</span>
      <span>Contact</span>
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
            <div class="contact-item-icon" style="color:#25D366;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12 0C5.373 0 0 5.373 0 12c0 2.117.549 4.175 1.594 5.994L0 24l6.188-1.563A11.944 11.944 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.926 0-3.82-.509-5.486-1.473l-.394-.23-4.075 1.03 1.072-3.94-.256-.407A9.944 9.944 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
            </div>
            <div class="contact-item-text">
              <span class="ci-label" data-i18n="ci.whatsapp">WhatsApp</span>
              <span>+590 690 43 28 18</span>
            </div>
          </a>
          <a class="contact-item" href="tel:+590690432818">
            <div class="contact-item-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.2a16 16 0 0 0 6 6l1.56-1.88a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.56z"/></svg>
            </div>
            <div class="contact-item-text">
              <span class="ci-label">Téléphone</span>
              <span>+590 690 43 28 18</span>
            </div>
          </a>
          <a class="contact-item" href="mailto:contact@ftfl-sxm.com">
            <div class="contact-item-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            </div>
            <div class="contact-item-text">
              <span class="ci-label">Email</span>
              <a href="mailto:contact@ftfl-sxm.com">contact@ftfl-sxm.com</a>
            </div>
          </a>
          <div class="contact-item">
            <div class="contact-item-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div class="contact-item-text">
              <label data-i18n="ci.loc">Localisation</label>
              <span>Saint-Martin / Sint Maarten · SXM 97150</span>
            </div>
          </div>
          <a class="contact-item" href="https://www.linkedin.com/company/ftfl-cara%C3%AFbes/" target="_blank" rel="noopener">
            <div class="contact-item-icon" style="color:#0A66C2;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </div>
            <div class="contact-item-text">
              <span class="ci-label" data-i18n="ci.linkedin">LinkedIn</span>
              <span>FTFL CARAÏBES</span>
            </div>
          </a>
        </div>
      </div>

      <div data-aos="fade-left" data-aos-delay="100">
        <div class="contact-form">
          <h2 class="form-title" data-i18n="form.title">Demande de devis gratuit</h2>
          <form id="contactForm" onsubmit="handleSubmit(event)">
            <input type="hidden" name="_subject"      value="Nouvelle demande de devis — FTFL CARAÏBES"/>
            <input type="hidden" name="_template"     value="box"/>
            <input type="hidden" name="_color"        value="1a6b35"/>
            <input type="hidden" name="_captcha"      value="false"/>
            <input type="hidden" name="_autoresponse" value="Merci pour votre demande. L'équipe FTFL CARAÏBES vous contactera dans les 24h. / Thank you for your request. FTFL CARAÏBES team will contact you within 24h."/>
            <input type="hidden" name="Heure (Saint-Martin)" id="sxmTime" value=""/>
            <div class="form-row">
              <div class="form-group">
                <label data-i18n="f.name">Prénom & Nom *</label>
                <input type="text" name="Nom complet" placeholder="Jean Dupont" required/>
              </div>
              <div class="form-group">
                <label data-i18n="f.phone">Téléphone *</label>
                <input type="tel" name="Téléphone" placeholder="+590 690 43 28 18" required/>
              </div>
            </div>
            <div class="form-group">
              <label>Email *</label>
              <input type="email" name="Email" placeholder="votre@email.com" required/>
            </div>
            <div class="form-group">
              <label data-i18n="f.svc">Type de prestation *</label>
              <select name="Service demandé" id="selectService" required>
                <option value="" disabled selected>Sélectionnez un service</option>
                <option value="Terrassement & VRD">Terrassement & VRD</option>
                <option value="Aménagement Extérieur">Aménagement Extérieur</option>
                <option value="Travaux de Second Œuvre">Travaux de Second Œuvre</option>
                <option value="Multiservices & Maintenance">Multiservices & Maintenance</option>
                <option value="Autre / Plusieurs services">Autre / Plusieurs services</option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label data-i18n="f.loc">Localisation du chantier</label>
                <select name="Localisation du chantier" id="selectLocation">
                  <option value="" disabled selected>Partie française ou NL ?</option>
                  <option value="Saint-Martin — Partie Française">Saint-Martin (FR)</option>
                  <option value="Sint Maarten — Partie Néerlandaise">Sint Maarten (NL)</option>
                  <option value="Les deux côtés">Les deux</option>
                  <option value="Autre île">Autre île</option>
                </select>
              </div>
              <div class="form-group">
                <label data-i18n="f.budget">Budget estimé</label>
                <select name="Budget estimé" id="selectBudget">
                  <option value="" disabled selected>Budget indicatif</option>
                  <option value="Moins de 5 000 €">Moins de 5 000 €</option>
                  <option value="5 000 – 20 000 €">5 000 – 20 000 €</option>
                  <option value="20 000 – 50 000 €">20 000 – 50 000 €</option>
                  <option value="50 000 – 100 000 €">50 000 – 100 000 €</option>
                  <option value="Plus de 100 000 €">Plus de 100 000 €</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label data-i18n="f.msg">Description de votre projet *</label>
              <textarea name="Description du projet" id="msgTextarea" placeholder="Décrivez votre projet : nature des travaux, superficie approximative, délais souhaités, contraintes particulières…" required></textarea>
            </div>
            <button type="submit" class="form-submit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              <span data-i18n="f.submit">Envoyer ma demande</span>
            </button>
          </form>
          <div class="form-success" id="formSuccess">
            <span data-i18n="f.success">✅ Merci ! Votre demande a bien été reçue. Notre équipe vous contacte sous 24h.</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

# ── Générateur ────────────────────────────────────────────────

def build_page(slug, page):
    content = page['content']()
    return f"""<!DOCTYPE html>
<html lang="fr" prefix="og: https://ogp.me/ns#">
<head>
{HEAD_COMMON}
  <title id="seo-title">{page['title']}</title>
  <meta id="seo-desc" name="description" content="{page['desc']}"/>
  <meta id="seo-keys" name="keywords" content="{page['keywords']}"/>
  <link id="seo-canonical" rel="canonical" href="{page['canonical']}"/>

  <!-- OPEN GRAPH -->
  <meta id="og-title"  property="og:title"       content="FTFL CARAÏBES | {page['breadcrumb']}"/>
  <meta id="og-desc"   property="og:description"  content="{page['desc']}"/>
  <meta id="og-locale" property="og:locale"       content="fr_FR"/>
  <meta property="og:type"   content="website"/>
  <meta property="og:url"    content="{page['canonical']}"/>
  <meta property="og:image"  content="{page['og_image']}"/>
  <meta property="og:site_name" content="FTFL CARAÏBES"/>

  <!-- TWITTER CARD -->
  <meta name="twitter:card"  content="summary_large_image"/>
  <meta id="tw-title" name="twitter:title"       content="FTFL CARAÏBES | {page['breadcrumb']}"/>
  <meta id="tw-desc"  name="twitter:description"  content="{page['desc']}"/>
  <meta name="twitter:image" content="{page['og_image']}"/>

  <!-- SCHEMA.ORG BREADCRUMB -->
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"Accueil","item":"https://www.ftfl-sxm.com/"}},
      {{"@type":"ListItem","position":2,"name":"{page['breadcrumb']}","item":"{page['canonical']}"}}
    ]
  }}
  </script>

  <script src="https://unpkg.com/aos@2.3.4/dist/aos.js" defer></script>
</head>
<body>

{NAVBAR}

{content}

{FOOTER}

{LEGAL_MODALS}

<script src="/js/scripts.js"></script>
</body>
</html>"""

if __name__ == '__main__':
    for slug, page in PAGES.items():
        out_dir = os.path.join(BASE_DIR, page['dir'])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        html = build_page(slug, page)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'[OK] {page["dir"]}/index.html  —  {page["canonical"]}')

    print('\nDone. Pensez a commit + push sur GitHub.')

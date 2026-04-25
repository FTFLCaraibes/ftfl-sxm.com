// ── AOS INIT ────────────────────────────────────────────────
AOS.init({ duration: 700, once: true, offset: 60, easing: 'ease-out-cubic' });

// ── NAVBAR SCROLL ───────────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
});

// ── MOBILE NAV ──────────────────────────────────────────────
function openMobileNav()  { document.getElementById('mobileNav').classList.add('open'); }
function closeMobileNav() { document.getElementById('mobileNav').classList.remove('open'); }

// ── PARTICLE CANVAS ─────────────────────────────────────────
(function() {
  const canvas = document.getElementById('particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width  = canvas.parentElement.offsetWidth;
    H = canvas.height = canvas.parentElement.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class P {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.r = Math.random() * 1.5 + .3;
      this.vx = (Math.random() - .5) * .4;
      this.vy = (Math.random() - .5) * .4;
      this.a  = Math.random() * .25 + .05;
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
      ctx.fillStyle = `rgba(61,168,100,${this.a})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < 80; i++) particles.push(new P());

  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i+1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d  = Math.sqrt(dx*dx + dy*dy);
        if (d < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(61,168,100,${.06 * (1 - d/120)})`;
          ctx.lineWidth = .5;
          ctx.stroke();
        }
      }
    }
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => { p.update(); p.draw(); });
    drawLines();
    requestAnimationFrame(loop);
  }
  loop();
})();

// ── COUNTER ANIMATION ───────────────────────────────────────
const counters = document.querySelectorAll('.counter');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = +el.dataset.target;
    const step = target / 40;
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = Math.round(current);
      if (current >= target) clearInterval(timer);
    }, 40);
    counterObserver.unobserve(el);
  });
}, { threshold: .5 });
counters.forEach(c => counterObserver.observe(c));

// ── HERO TITLE ENTRANCE ─────────────────────────────────────
document.querySelectorAll('.hero-title .line').forEach((line, i) => {
  line.style.cssText = `opacity:0;transform:translateY(40px);transition:opacity .8s cubic-bezier(.4,0,.2,1) ${i*.2}s,transform .8s cubic-bezier(.4,0,.2,1) ${i*.2}s`;
  setTimeout(() => {
    line.style.opacity = '1';
    line.style.transform = 'translateY(0)';
  }, 200 + i * 150);
});

// ── CONTACT FORM ────────────────────────────────────────────
function handleSubmit(e) {
  e.preventDefault();
  const form   = document.getElementById('contactForm');
  const success= document.getElementById('formSuccess');
  const btn    = form.querySelector('.form-submit');
  const span   = btn.querySelector('span[data-i18n]');

  // Heure locale Saint-Martin (UTC−4, pas de DST)
  const sxmField = document.getElementById('sxmTime');
  if (sxmField) {
    sxmField.value = new Date().toLocaleString('fr-FR', {
      timeZone: 'America/Anguilla',
      weekday: 'long', day: '2-digit', month: 'long', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  if(span) span.textContent = '…';
  btn.disabled = true;

  const data = new FormData(form);

  fetch('https://formsubmit.co/ajax/contact@ftfl-sxm.com', {
    method : 'POST',
    headers: { 'Accept': 'application/json' },
    body   : data
  })
  .then(r => r.json())
  .then(res => {
    if(res.success === 'true' || res.success === true) {
      form.style.display  = 'none';
      success.style.display = 'block';
    } else { throw new Error(); }
  })
  .catch(() => {
    btn.disabled = false;
    if(span) span.textContent = i18nData[currentLang]?.['f.submit'] || 'Envoyer';
    alert('Une erreur est survenue. Veuillez réessayer ou nous écrire directement à contact@ftfl-sxm.com');
  });
}

// ── LANGUAGE SWITCHER ────────────────────────────────────────
// Priorité : window.__LANG (injecté par les pages /en/ /es/ etc.)
//            puis localStorage, puis langue navigateur, puis 'fr'
const urlLang = new URLSearchParams(window.location.search).get('lang');
const supported = ['fr','en','es','nl','pt'];
// window.__LANG est injecté par les pages statiques /en/ /es/ /nl/ /pt/
// Sans injection, on est sur une page française — on force 'fr'
let currentLang = (window.__LANG && supported.includes(window.__LANG)) ? window.__LANG
                : supported.includes(urlLang)                          ? urlLang
                : 'fr';

const i18nData = {
  fr: {
    // NAV
    'nav.about':'À propos','nav.services':'Services','nav.approach':'Approche',
    'nav.values':'Valeurs','nav.zone':'Zone','nav.cta':'Contactez-nous',
    // HERO
    'hero.line1':'Un seul partenaire',
    'hero.line2':'pour tous vos <span class="orange-word">travaux.</span>',
    'hero.subtitle':'FTFL CARAÏBES, votre entreprise de construction polyvalente présente des deux côtés de l\'île. Terrassement, aménagement extérieur, second œuvre et multiservices.',
    'hero.cta1':'Demander un devis','hero.cta2':'Découvrir nos métiers',
    'hero.stat1':'Local & ancré à Saint-Martin','hero.stat2':'Terrassement, Second œuvre…',
    'hero.stat2unit':'métiers','hero.stat3unit':'pays','hero.stat3':'Partie FR & NL couverte',
    'hero.scroll':'Défiler',
    // ABOUT
    'about.tag':'À propos',
    'about.title':'Née d\'une conviction simple,<br/><span class="highlight">enracinée dans les Caraïbes.</span>',
    'about.p1':'FTFL CARAÏBES est née d\'une conviction simple : à Saint-Martin, les projets de construction et d\'aménagement méritent un <strong>partenaire local fiable, réactif et polyvalent</strong>.',
    'about.p2':'Fondée par des professionnels du BTP enracinés dans le tissu caribéen, notre entreprise intervient des deux côtés de l\'île — partie française comme partie hollandaise — avec une parfaite connaissance du terrain, des acteurs locaux et des contraintes propres à notre territoire.',
    'about.p3':'Notre ambition : devenir le <strong>partenaire de référence</strong> des particuliers, des professionnels et des institutionnels pour tous leurs projets travaux à Saint-Martin.',
    'about.badge1':'Réactivité & disponibilité','about.badge2':'Respect des délais & budgets',
    'about.badge3':'Qualité d\'exécution','about.badge4':'Transparence client',
    'about.clients.h':'Nos clients',
    'about.clients.list':'<div class="client-item">Particuliers</div><div class="client-item">Copropriétés</div><div class="client-item">Promoteurs & Investisseurs</div><div class="client-item">Hôteliers & Commerces</div><div class="client-item">Collectivités & Institutionnels</div>',
    'about.commit.h':'Nos engagements',
    'about.commit.list':'<div class="client-item">Un interlocuteur unique</div><div class="client-item">Chantier suivi au quotidien</div><div class="client-item">Devis précis & détaillé</div><div class="client-item">Livraison aux règles de l\'art</div><div class="client-item">Interventions FR & NL</div>',
    // SERVICES
    'services.tag':'Nos Métiers',
    'services.title':'Une réponse complète<br/>à <span class="highlight">chaque besoin.</span>',
    'services.sub':'Du terrassement aux finitions, FTFL couvre l\'ensemble des corps d\'état avec les mêmes standards d\'exigence.',
    'svc1.h':'Terrassement & VRD',
    'svc1.p':'Nous préparons le terrain pour vos projets avec des moyens adaptés aux spécificités de l\'île.',
    'svc1.tags':'<span class="service-tag">Terrassement général</span><span class="service-tag">Décaissement</span><span class="service-tag">Fouilles</span><span class="service-tag">Voiries</span><span class="service-tag">Assainissement</span><span class="service-tag">Enrochement</span><span class="service-tag">Drainage</span>',
    'svc2.h':'Aménagement Extérieur',
    'svc2.p':'Nous concevons et réalisons vos espaces extérieurs pour sublimer vos propriétés.',
    'svc2.tags':'<span class="service-tag">Clôtures & portails</span><span class="service-tag">Terrasses</span><span class="service-tag">Pergolas</span><span class="service-tag">Piscines</span><span class="service-tag">Paysager</span><span class="service-tag">Éclairage ext.</span><span class="service-tag">Citernes</span>',
    'svc3.h':'Travaux de Second Œuvre',
    'svc3.p':'FTFL prend en charge l\'ensemble des travaux de finition et de réhabilitation pour mener vos projets à leur terme.',
    'svc3.tags':'<span class="service-tag">Menuiserie</span><span class="service-tag">Plomberie</span><span class="service-tag">Carrelage</span><span class="service-tag">Peinture</span><span class="service-tag">Serrurerie</span><span class="service-tag">Métallerie</span><span class="service-tag">Rénovation</span>',
    'svc4.h':'Multiservices & Maintenance',
    'svc4.p':'Un interlocuteur unique pour l\'entretien courant, la maintenance et les interventions rapides sur votre patrimoine.',
    'svc4.tags':'<span class="service-tag">Maintenance préventive</span><span class="service-tag">Dépannage</span><span class="service-tag">Nettoyage chantier</span><span class="service-tag">Petits travaux</span><span class="service-tag">Contrats maintenance</span><span class="service-tag">Urgences 24h</span>',
    // APPROACH
    'approach.tag':'Notre Approche',
    'approach.title':'Un processus <span class="highlight">rigoureux</span><br/>à chaque étape.',
    'approach.sub':'De la première rencontre à la remise des clés, nous vous accompagnons avec méthode, rigueur et transparence totale.',
    'step1.h':'01 · Écoute',
    'step1.p':'Nous prenons le temps de comprendre votre projet dans ses moindres détails — contraintes techniques, budget, calendrier — pour construire avec vous la stratégie la plus adaptée.',
    'step2.h':'02 · Étude',
    'step2.p':'Chiffrage précis, planning prévisionnel, identification des risques : notre étude technique et financière vous donne une vision claire avant tout démarrage.',
    'step3.h':'03 · Exécution',
    'step3.p':'Nos équipes s\'engagent avec rigueur et savoir-faire. Un chef de chantier dédié coordonne chaque intervention et vous tient informé en temps réel.',
    'step4.h':'04 · Livraison',
    'step4.p':'Nous ne rendons les clés qu\'une fois chaque détail achevé à votre satisfaction, dans le strict respect des règles de l\'art et des délais convenus.',
    // VALUES
    'values.tag':'Nos Valeurs',
    'values.title':'Ce qui nous <span class="highlight">distingue.</span>',
    'values.sub':'Quatre piliers fondateurs qui guident chacune de nos interventions, du premier devis à la livraison finale.',
    'val1.h':'Ancrage Local',
    'val1.p':'Implantés à Saint-Martin depuis nos débuts, nous connaissons chaque quartier, chaque fournisseur, chaque contrainte du terrain. Cette proximité nous rend réactifs et efficaces là où d\'autres tâtonnent.',
    'val2.h':'Fiabilité',
    'val2.p':'Un chantier qui démarre à l\'heure, un budget maîtrisé, des engagements tenus jusqu\'au bout. Chez FTFL, notre réputation se construit projet après projet, sur la force de notre parole.',
    'val3.h':'Polyvalence',
    'val3.p':'Du terrassement aux finitions, de la villa privée au bâtiment commercial, nos équipes couvrent tous les corps d\'état. Un seul interlocuteur, zéro coordination à gérer.',
    'val4.h':'Exigence',
    'val4.p':'Nous appliquons les mêmes standards de qualité sur chaque chantier, quelle que soit son envergure. Les normes locales, les délais, la sécurité : rien n\'est laissé au hasard.',
    // ZONE
    'zone.tag':'Zone d\'Intervention',
    'zone.title':'Une île, deux pays,<br/><span class="highlight">une seule équipe.</span>',
    'zone.sub':'FTFL opère sur l\'intégralité de l\'île de Saint-Martin, côté français comme côté hollandais. Une double maîtrise réglementaire et logistique au service de vos projets.',
    'zone.fr.side':'Partie Française',
    'zone.fr.desc':'Maîtrise complète du cadre administratif et réglementaire français. Permis de construire, déclarations de travaux, normes RT : nous gérons tout.',
    'zone.nl.side':'Partie hollandaise',
    'zone.nl.desc':'Connaissance approfondie du système réglementaire néerlandais. Nos équipes opèrent sur Sint Maarten avec la même efficacité qu\'en partie française.',
    'zone.tagline':'+ interventions ponctuelles sur <span>Saint-Barthélemy</span> & <span>Anguilla</span>',
    // TEAM
    'team.tag':'L\'Équipe',
    'team.title':'Des hommes de terrain,<br/><span class="highlight">au service de votre territoire.</span>',
    'team.sub':'L\'équipe fondatrice de FTFL réunit des professionnels du BTP aguerris aux chantiers caribéens les plus exigeants, avec une connaissance unique des réalités locales.',
    'team.p1.h':'Expérience Terrain',
    'team.p1.p':'Des années de chantiers à Saint-Martin forgent une connaissance béton des contraintes locales : conditions climatiques, logistique insulaire, circuits d\'approvisionnement.',
    'team.p2.h':'Équipe Structurée',
    'team.p2.p':'Chefs de chantier expérimentés, compagnons qualifiés, coordinateurs projet. Chaque chantier dispose d\'un référent unique — votre interlocuteur du début à la fin.',
    'team.p3.h':'Réseau Local Solide',
    'team.p3.p':'Fournisseurs premium, sous-traitants certifiés, loueurs d\'engins fiables des deux côtés de la frontière : notre réseau est votre garantie de continuité.',
    'team.cta.h':'Prêt à démarrer votre projet ?',
    'team.cta.p':'Contactez-nous dès aujourd\'hui pour une étude gratuite, sans engagement. Nous répondons dans les 24h.',
    'team.cta.btn':'Nous contacter',
    // CONTACT
    'contact.tag':'Contact',
    'contact.title':'Construisons ensemble<br/><span class="highlight">votre projet.</span>',
    'contact.sub':'Un projet de construction, de rénovation ou d\'aménagement ? Notre équipe étudie votre demande et vous soumet un devis détaillé, gratuit et sans engagement.',
    'ci.whatsapp':'WhatsApp','ci.linkedin':'LinkedIn','ci.web':'Site web','ci.loc':'Localisation',
    'f.name':'Prénom & Nom *','f.phone':'Téléphone *',
    'f.svc':'Type de prestation *','f.loc':'Localisation du chantier',
    'f.budget':'Budget estimé','f.msg':'Description de votre projet *',
    'f.msg.ph':'Décrivez votre projet : nature des travaux, superficie approximative, délais souhaités, contraintes particulières…',
    'f.submit':'Envoyer ma demande',
    'f.success':'✅ Merci ! Votre demande a bien été reçue. Notre équipe vous contacte sous 24h.',
    'form.title':'Demande de devis gratuit',
    // FOOTER
    'ft.desc':'Un seul partenaire pour tous vos travaux à Saint-Martin. Terrassement, VRD, aménagement extérieur, second œuvre et multiservices.',
    'ft.h.svc':'Services','ft.h.co':'Entreprise','ft.h.ct':'Contact',
    'ft.svc1':'Terrassement & VRD','ft.svc2':'Aménagement Extérieur',
    'ft.svc3':'Second Œuvre','ft.svc4':'Multiservices',
    'ft.about':'À propos','ft.vals':'Nos valeurs',
    'ft.app':'Notre approche','ft.team':'L\'équipe',
    'ft.copy':'© 2025 FTFL CARAÏBES — Tous droits réservés',
    'ft.legal1':'Mentions légales','ft.legal2':'Politique de confidentialité',
    'ft.slogan':'Saint-Martin · Sint Maarten · Caraïbes 🌴',
    'showcase.h':'L\'excellence au service de <span class="highlight">chaque chantier.</span>',
    'showcase.p':'Équipements professionnels, équipes qualifiées, maîtrise totale du territoire : chaque projet FTFL est conduit avec le même niveau d\'exigence.',
    'showcase.cta':'Demander un devis',
    'ft.quote':'Demander un devis',
  },
  en: {
    'nav.about':'About','nav.services':'Services','nav.approach':'Approach',
    'nav.values':'Values','nav.zone':'Coverage','nav.cta':'Contact us',
    'hero.line1':'One trusted partner',
    'hero.line2':'for all your <span class="orange-word">projects.</span>',
    'hero.subtitle':'FTFL CARAÏBES is the go-to construction company on Saint Martin island, covering both the French and Dutch sides. Earthworks, outdoor development, finishing works and property maintenance.',
    'hero.cta1':'Get a free quote','hero.cta2':'Explore our services',
    'hero.stat1':'Local & rooted in Saint Martin','hero.stat2':'Earthworks, Finishing works…',
    'hero.stat2unit':'trades','hero.stat3unit':'countries','hero.stat3':'FR & NL sides covered',
    'hero.scroll':'Scroll',
    'about.tag':'About us',
    'about.title':'Built on a simple belief,<br/><span class="highlight">rooted in the Caribbean.</span>',
    'about.p1':'FTFL CARAÏBES was built on one simple belief: construction and development projects in Saint Martin deserve a <strong>reliable, responsive and versatile local partner</strong> — not a distant contractor.',
    'about.p2':'Founded by seasoned construction professionals embedded in the Caribbean landscape, we operate on both sides of the island — French and Dutch — with an insider knowledge of the territory, its stakeholders and its specific challenges.',
    'about.p3':'Our goal: to become the <strong>reference partner</strong> for homeowners, developers, hotel groups and public institutions for every construction project on Saint Martin.',
    'about.badge1':'Fast response & availability','about.badge2':'On time & on budget',
    'about.badge3':'Proven workmanship','about.badge4':'Full client transparency',
    'about.clients.h':'Our clients',
    'about.clients.list':'<div class="client-item">Private homeowners</div><div class="client-item">Co-ownership associations</div><div class="client-item">Developers & Investors</div><div class="client-item">Hotels & Businesses</div><div class="client-item">Public bodies & Institutions</div>',
    'about.commit.h':'Our commitments',
    'about.commit.list':'<div class="client-item">Single point of contact</div><div class="client-item">Daily site monitoring</div><div class="client-item">Detailed, accurate quotes</div><div class="client-item">Delivered to the highest standard</div><div class="client-item">Operations on FR & NL side</div>',
    'services.tag':'Our Expertise',
    'services.title':'A complete solution<br/>for <span class="highlight">every project.</span>',
    'services.sub':'From groundbreaking to final finishing, FTFL covers every construction trade with the same uncompromising standards.',
    'svc1.h':'Earthworks & Civil Works',
    'svc1.p':'We prepare the ground for your project using equipment and methods tailored to the specific conditions of Saint Martin island.',
    'svc1.tags':'<span class="service-tag">Site clearance</span><span class="service-tag">Excavation</span><span class="service-tag">Trenching</span><span class="service-tag">Road works</span><span class="service-tag">Drainage</span><span class="service-tag">Retaining walls</span><span class="service-tag">Land levelling</span>',
    'svc2.h':'Exterior Works',
    'svc2.p':'We design and build your outdoor spaces to enhance the value and appeal of your property — from pools to landscaping.',
    'svc2.tags':'<span class="service-tag">Fencing & gates</span><span class="service-tag">Terraces</span><span class="service-tag">Pergolas</span><span class="service-tag">Swimming pools</span><span class="service-tag">Landscaping</span><span class="service-tag">Outdoor lighting</span><span class="service-tag">Rainwater tanks</span>',
    'svc3.h':'Finishing & Interior Works',
    'svc3.p':'FTFL handles all interior finishing and renovation trades, taking your project from shell to move-in-ready.',
    'svc3.tags':'<span class="service-tag">Carpentry</span><span class="service-tag">Plumbing</span><span class="service-tag">Tiling</span><span class="service-tag">Painting</span><span class="service-tag">Locksmithing</span><span class="service-tag">Metalwork</span><span class="service-tag">Renovation</span>',
    'svc4.h':'Multiservices & Maintenance',
    'svc4.p':'Your single point of contact for day-to-day upkeep, preventive maintenance and fast-response repairs on your property.',
    'svc4.tags':'<span class="service-tag">Preventive maintenance</span><span class="service-tag">Emergency repairs</span><span class="service-tag">Site clean-up</span><span class="service-tag">Minor works</span><span class="service-tag">Service contracts</span><span class="service-tag">24h response</span>',
    'approach.tag':'How We Work',
    'approach.title':'A <span class="highlight">structured</span> process<br/>at every stage.',
    'approach.sub':'From the first meeting to final handover, we guide every project with a proven method, rigorous execution and full transparency.',
    'step1.h':'01 · Discovery',
    'step1.p':'We take the time to fully understand your project — technical requirements, budget, timeline and priorities — so we can build the right plan together from day one.',
    'step2.h':'02 · Study',
    'step2.p':'Accurate costing, detailed schedule, risk assessment: our technical and financial study gives you a clear, commitment-ready picture before a single shovel hits the ground.',
    'step3.h':'03 · Execution',
    'step3.p':'Our crews deliver with precision and professionalism. A dedicated site manager oversees every day on site and keeps you informed in real time.',
    'step4.h':'04 · Handover',
    'step4.p':'We don\'t hand over the keys until every last detail has been completed to your full satisfaction — on time, to spec, and built to last.',
    'values.tag':'Our Values',
    'values.title':'What makes us <span class="highlight">different.</span>',
    'values.sub':'Four core principles that shape every decision we make, from the first quote to the final walkthrough.',
    'val1.h':'Local Roots',
    'val1.p':'We\'ve been embedded in Saint Martin since day one. We know every neighbourhood, every supplier, every island-specific challenge — and we use that knowledge to move faster and smarter than anyone else.',
    'val2.h':'Reliability',
    'val2.p':'Projects that start on schedule. Budgets that stay on track. Commitments that are kept without exception. At FTFL, our word is our bond — and our reputation is built project by project.',
    'val3.h':'Versatility',
    'val3.p':'From earthworks to finishing touches, from private villas to commercial buildings, we cover every trade in-house. One team, one contract, zero coordination headaches.',
    'val4.h':'High Standards',
    'val4.p':'We apply the same exacting standards on every job, regardless of scale. Local regulations, safety, timelines — nothing is left to chance on any FTFL site.',
    'zone.tag':'Coverage',
    'zone.title':'One island, two countries,<br/><span class="highlight">one team.</span>',
    'zone.sub':'FTFL operates across the entire island of Saint Martin, covering both the French and Dutch sides. Dual regulatory expertise and seamless cross-border operations for your projects.',
    'zone.fr.side':'French Side',
    'zone.fr.desc':'Full command of French administrative and building regulations. Building permits, compliance filings and technical standards — we handle it all.',
    'zone.nl.side':'Dutch Side',
    'zone.nl.desc':'Deep knowledge of the Dutch regulatory framework on Sint Maarten. Our crews operate across the border with the same efficiency as on the French side.',
    'zone.tagline':'+ occasional projects on <span>Saint-Barthélemy</span> & <span>Anguilla</span>',
    'team.tag':'The Team',
    'team.title':'Field professionals,<br/><span class="highlight">built for this island.</span>',
    'team.sub':'FTFL\'s founding team brings together construction veterans who have delivered some of the most demanding projects across the Caribbean — with a deep understanding of what it takes to build here.',
    'team.p1.h':'Field Experience',
    'team.p1.p':'Years of active sites on Saint Martin mean we understand the island\'s real challenges: tropical climate, island logistics, material supply chains and local labour.',
    'team.p2.h':'Structured Team',
    'team.p2.p':'Experienced site managers, skilled tradespeople, project coordinators. Every project gets a dedicated lead — your single point of contact from start to finish.',
    'team.p3.h':'Strong Local Network',
    'team.p3.p':'Trusted suppliers, certified subcontractors, reliable equipment hire — on both sides of the border. Our network is your project\'s backbone.',
    'team.cta.h':'Ready to get started?',
    'team.cta.p':'Reach out today for a free, no-obligation site assessment. We respond within 24 hours.',
    'team.cta.btn':'Get in touch',
    'contact.tag':'Contact',
    'contact.title':'Let\'s build your<br/><span class="highlight">project together.</span>',
    'contact.sub':'Planning a construction, renovation or landscaping project? Our team reviews every enquiry and provides a detailed, free quote — usually within 24 hours.',
    'ci.whatsapp':'WhatsApp','ci.linkedin':'LinkedIn','ci.web':'Website','ci.loc':'Location',
    'f.name':'Full name *','f.phone':'Phone number *',
    'f.svc':'Service required *','f.loc':'Site location',
    'f.budget':'Estimated budget','f.msg':'Project description *',
    'f.msg.ph':'Tell us about your project: type of works, approximate area, preferred timeline, any specific requirements…',
    'f.submit':'Send my request',
    'f.success':'✅ Thank you! Your request has been received. Our team will get back to you within 24 hours.',
    'form.title':'Request a free quote',
    'ft.desc':'Your trusted construction partner on Saint Martin island. Earthworks, civil works, exterior works, finishing works and maintenance services.',
    'ft.h.svc':'Services','ft.h.co':'Company','ft.h.ct':'Contact',
    'ft.svc1':'Earthworks & Civil Works','ft.svc2':'Exterior Works',
    'ft.svc3':'Finishing Works','ft.svc4':'Multiservices',
    'ft.about':'About us','ft.vals':'Our values',
    'ft.app':'Our approach','ft.team':'The team',
    'ft.copy':'© 2025 FTFL CARAÏBES — All rights reserved',
    'ft.legal1':'Legal Notice','ft.legal2':'Privacy Policy',
    'ft.slogan':'Saint Martin · Sint Maarten · Caribbean 🌴',
    'showcase.h':'Excellence delivered on <span class="highlight">every project.</span>',
    'showcase.p':'Professional equipment, expert teams and deep local knowledge — every FTFL project is delivered to the same uncompromising standard.',
    'showcase.cta':'Get a free quote',
    'ft.quote':'Request a quote',
  },
  es: {
    'nav.about':'Quiénes somos','nav.services':'Servicios','nav.approach':'Método',
    'nav.values':'Valores','nav.zone':'Cobertura','nav.cta':'Contáctenos',
    'hero.line1':'Un único socio',
    'hero.line2':'para todas sus <span class="orange-word">obras.</span>',
    'hero.subtitle':'FTFL CARAÏBES es la empresa de construcción de referencia en Saint-Martin, presente en ambos lados de la isla. Movimiento de tierras, acondicionamiento exterior, acabados y mantenimiento.',
    'hero.cta1':'Solicitar presupuesto','hero.cta2':'Ver nuestros servicios',
    'hero.stat1':'Empresa local, arraigada en Saint-Martin','hero.stat2':'Movimiento de tierras, acabados…',
    'hero.stat2unit':'oficios','hero.stat3unit':'países','hero.stat3':'Lados FR y NL cubiertos',
    'hero.scroll':'Deslizar',
    'about.tag':'Quiénes somos',
    'about.title':'Nacida de una convicción,<br/><span class="highlight">arraigada en el Caribe.</span>',
    'about.p1':'FTFL CARAÏBES nació de una convicción: en Saint-Martin, los proyectos de construcción merecen un <strong>socio local serio, ágil y polivalente</strong>, no un contratista de paso.',
    'about.p2':'Fundada por profesionales de la construcción con raíces en el Caribe, nuestra empresa opera en ambos lados de la isla — francés y holandés — con un conocimiento profundo del territorio, sus actores y sus particularidades.',
    'about.p3':'Nuestra ambición: ser el <strong>socio de referencia</strong> de particulares, promotores, hoteles y administraciones para todos sus proyectos en Saint-Martin.',
    'about.badge1':'Rapidez y disponibilidad','about.badge2':'Plazos y presupuestos cumplidos',
    'about.badge3':'Calidad de ejecución','about.badge4':'Transparencia total',
    'about.clients.h':'Nuestros clientes',
    'about.clients.list':'<div class="client-item">Particulares</div><div class="client-item">Comunidades de propietarios</div><div class="client-item">Promotores e Inversores</div><div class="client-item">Hoteles y Comercios</div><div class="client-item">Instituciones y Organismos públicos</div>',
    'about.commit.h':'Nuestros compromisos',
    'about.commit.list':'<div class="client-item">Un solo interlocutor</div><div class="client-item">Seguimiento diario de obra</div><div class="client-item">Presupuesto detallado y preciso</div><div class="client-item">Entrega según las normas del arte</div><div class="client-item">Intervenciones FR y NL</div>',
    'services.tag':'Nuestros Servicios',
    'services.title':'Una respuesta global<br/>a <span class="highlight">cada necesidad.</span>',
    'services.sub':'Desde el movimiento de tierras hasta los acabados, FTFL cubre todos los oficios de la construcción con el mismo nivel de exigencia.',
    'svc1.h':'Movimiento de tierras, urbanización y redes',
    'svc1.p':'Preparamos el terreno para sus proyectos con medios adaptados a las especificidades de la isla.',
    'svc1.tags':'<span class="service-tag">Movimiento de tierras general</span><span class="service-tag">Excavación</span><span class="service-tag">Zanjas</span><span class="service-tag">Viales</span><span class="service-tag">Saneamiento</span><span class="service-tag">Escollera</span><span class="service-tag">Drenaje</span>',
    'svc2.h':'Obras exteriores',
    'svc2.p':'Diseñamos y ejecutamos sus espacios exteriores para realzar el valor y el atractivo de sus propiedades.',
    'svc2.tags':'<span class="service-tag">Vallas y portones</span><span class="service-tag">Terrazas</span><span class="service-tag">Pérgolas</span><span class="service-tag">Piscinas</span><span class="service-tag">Jardinería</span><span class="service-tag">Iluminación ext.</span><span class="service-tag">Cisternas</span>',
    'svc3.h':'Acabados interiores',
    'svc3.p':'FTFL gestiona todos los trabajos de acabado y rehabilitación para llevar sus proyectos hasta la entrega final.',
    'svc3.tags':'<span class="service-tag">Carpintería</span><span class="service-tag">Fontanería</span><span class="service-tag">Alicatado</span><span class="service-tag">Pintura</span><span class="service-tag">Cerrajería</span><span class="service-tag">Metalistería</span><span class="service-tag">Reformas</span>',
    'svc4.h':'Multiservicios y Mantenimiento',
    'svc4.p':'Un único interlocutor para el mantenimiento ordinario, el mantenimiento preventivo y las intervenciones de urgencia en su inmueble.',
    'svc4.tags':'<span class="service-tag">Mantenimiento preventivo</span><span class="service-tag">Averías</span><span class="service-tag">Limpieza de obra</span><span class="service-tag">Pequeñas obras</span><span class="service-tag">Contratos mantenimiento</span><span class="service-tag">Urgencias 24h</span>',
    'approach.tag':'Nuestro Método',
    'approach.title':'Un proceso <span class="highlight">riguroso</span><br/>en cada etapa.',
    'approach.sub':'Desde el primer encuentro hasta la entrega de llaves, le acompañamos con método, rigor y transparencia absoluta.',
    'step1.h':'01 · Escucha',
    'step1.p':'Nos tomamos el tiempo de entender su proyecto en profundidad — necesidades técnicas, presupuesto, plazos — para definir juntos la mejor estrategia desde el principio.',
    'step2.h':'02 · Estudio',
    'step2.p':'Presupuesto detallado, calendario preliminar, análisis de riesgos: nuestro estudio técnico-económico le da visibilidad total antes de cualquier inicio de obra.',
    'step3.h':'03 · Ejecución',
    'step3.p':'Nuestros equipos actúan con precisión y profesionalidad. Un jefe de obra dedicado coordina cada intervención y le mantiene informado en tiempo real.',
    'step4.h':'04 · Entrega',
    'step4.p':'No entregamos las llaves hasta que cada detalle esté terminado a su entera satisfacción, respetando tanto las normas de la construcción como los plazos acordados.',
    'values.tag':'Nuestros Valores',
    'values.title':'Lo que nos <span class="highlight">define.</span>',
    'values.sub':'Cuatro principios fundacionales que guían cada una de nuestras decisiones, del primer presupuesto a la entrega final.',
    'val1.h':'Arraigo Local',
    'val1.p':'Presentes en Saint-Martin desde el primer día, conocemos cada barrio, cada proveedor y cada condicionante local. Esa proximidad nos hace más ágiles y eficaces allí donde otros aún están buscando referencias.',
    'val2.h':'Fiabilidad',
    'val2.p':'Obras que comienzan a tiempo. Presupuestos que se respetan. Compromisos que se cumplen sin excepción. En FTFL, nuestra reputación se construye obra a obra, sobre hechos.',
    'val3.h':'Polivalencia',
    'val3.p':'Del movimiento de tierras a los acabados, de la villa privada al local comercial, cubrimos todos los gremios de obra. Un solo interlocutor, cero coordinación adicional que gestionar.',
    'val4.h':'Exigencia',
    'val4.p':'Aplicamos los mismos estándares de calidad en cada obra, sea cual sea su envergadura. Normativa local, seguridad, plazos: nada se deja al azar en un proyecto FTFL.',
    'zone.tag':'Zona de Intervención',
    'zone.title':'Una isla, dos países,<br/><span class="highlight">un solo equipo.</span>',
    'zone.sub':'FTFL opera en toda la isla de Saint-Martin, tanto en el lado francés como en el holandés. Doble dominio normativo y logístico al servicio de sus proyectos.',
    'zone.fr.side':'Lado Francés',
    'zone.fr.desc':'Dominio completo del marco administrativo y normativo francés. Permisos de obra, declaraciones, normativas técnicas: lo gestionamos todo.',
    'zone.nl.side':'Lado Holandés',
    'zone.nl.desc':'Conocimiento profundo del sistema normativo neerlandés. Nuestros equipos operan en Sint Maarten con la misma eficacia que en el lado francés.',
    'zone.tagline':'+ intervenciones puntuales en <span>Saint-Barthélemy</span> & <span>Anguilla</span>',
    'team.tag':'El Equipo',
    'team.title':'Profesionales de campo,<br/><span class="highlight">comprometidos con su territorio.</span>',
    'team.sub':'El equipo fundador de FTFL reúne veteranos de la construcción que han ejecutado los proyectos más exigentes del Caribe, con un conocimiento único de la realidad local.',
    'team.p1.h':'Experiencia de Campo',
    'team.p1.p':'Años de obras en Saint-Martin nos han dado un conocimiento concreto de sus retos: clima tropical, logística insular, cadenas de suministro locales.',
    'team.p2.h':'Equipo Estructurado',
    'team.p2.p':'Jefes de obra experimentados, operarios cualificados, coordinadores de proyecto. Cada obra tiene un responsable único — su interlocutor del inicio al fin.',
    'team.p3.h':'Red Local Sólida',
    'team.p3.p':'Proveedores de confianza, subcontratistas certificados, empresas de alquiler de maquinaria en ambos lados de la frontera: nuestra red es la columna vertebral de sus proyectos.',
    'team.cta.h':'¿Listo para iniciar su proyecto?',
    'team.cta.p':'Contáctenos hoy mismo para un estudio gratuito y sin compromiso. Respondemos en menos de 24 horas.',
    'team.cta.btn':'Contáctenos',
    'contact.tag':'Contacto',
    'contact.title':'Construyamos juntos<br/><span class="highlight">su proyecto.</span>',
    'contact.sub':'¿Tiene un proyecto de construcción, reforma o acondicionamiento? Nuestro equipo analiza su solicitud y le presenta un presupuesto detallado, gratuito y sin compromiso.',
    'ci.whatsapp':'WhatsApp','ci.linkedin':'LinkedIn','ci.web':'Sitio web','ci.loc':'Ubicación',
    'f.name':'Nombre y apellido *','f.phone':'Teléfono *',
    'f.svc':'Tipo de servicio *','f.loc':'Ubicación de la obra',
    'f.budget':'Presupuesto estimado','f.msg':'Descripción del proyecto *',
    'f.msg.ph':'Cuéntenos su proyecto: tipo de obras, superficie aproximada, plazos deseados, requisitos especiales…',
    'f.submit':'Enviar mi solicitud',
    'f.success':'✅ ¡Gracias! Su solicitud ha sido recibida. Nuestro equipo se pondrá en contacto con usted en menos de 24 horas.',
    'form.title':'Solicitar presupuesto gratuito',
    'ft.desc':'Su socio de construcción de referencia en Saint-Martin. Movimiento de tierras, urbanización y redes, obras exteriores, acabados y multiservicios.',
    'ft.h.svc':'Servicios','ft.h.co':'Empresa','ft.h.ct':'Contacto',
    'ft.svc1':'Movimiento de tierras y redes','ft.svc2':'Obras exteriores',
    'ft.svc3':'Obras de Acabado','ft.svc4':'Multiservicios',
    'ft.about':'Quiénes somos','ft.vals':'Nuestros valores',
    'ft.app':'Nuestro método','ft.team':'El equipo',
    'ft.copy':'© 2025 FTFL CARAÏBES — Todos los derechos reservados',
    'ft.legal1':'Aviso legal','ft.legal2':'Política de privacidad',
    'ft.slogan':'Saint-Martin · Sint Maarten · Caribe 🌴',
    'showcase.h':'La excelencia al servicio de <span class="highlight">cada obra.</span>',
    'showcase.p':'Maquinaria profesional, equipos expertos y profundo conocimiento del territorio: cada proyecto FTFL se lleva a cabo con el mismo nivel de exigencia.',
    'showcase.cta':'Solicitar presupuesto',
    'ft.quote':'Solicitar presupuesto',
  },
  nl: {
    'nav.about':'Over ons','nav.services':'Diensten','nav.approach':'Werkwijze',
    'nav.values':'Waarden','nav.zone':'Werkgebied','nav.cta':'Neem contact op',
    'hero.line1':'Eén betrouwbare partner',
    'hero.line2':'voor al uw <span class="orange-word">bouwprojecten.</span>',
    'hero.subtitle':'FTFL CARAÏBES is hét bouwbedrijf van Saint-Martin, actief op zowel de Franse als de Nederlandse kant. Grondwerken, buitenaanleg, afbouwwerken en onderhoud.',
    'hero.cta1':'Offerte aanvragen','hero.cta2':'Bekijk onze diensten',
    'hero.stat1':'Lokaal verankerd in Saint-Martin','hero.stat2':'Grondwerken, Afbouw…',
    'hero.stat2unit':'vakgebieden','hero.stat3unit':'landen','hero.stat3':'Franse & Nederlandse kant gedekt',
    'hero.scroll':'Scrollen',
    'about.tag':'Over ons',
    'about.title':'Gebouwd op een eenvoudige overtuiging,<br/><span class="highlight">geworteld in het Caribisch gebied.</span>',
    'about.p1':'FTFL CARAÏBES is opgericht vanuit één overtuiging: bouw- en inrichtingsprojecten op Saint-Martin verdienen een <strong>betrouwbare, snelle en veelzijdige lokale partner</strong> — geen aannemer van elders.',
    'about.p2':'Opgericht door ervaren bouwprofessionals die geworteld zijn in de Caribische omgeving, werken wij aan beide kanten van het eiland met een grondige kennis van het terrein, de lokale spelers en de specifieke beperkingen.',
    'about.p3':'Onze ambitie: de <strong>referentiepartner</strong> worden voor particulieren, projectontwikkelaars, hotels en overheden voor al hun bouwprojecten op Saint-Martin.',
    'about.badge1':'Snelheid & beschikbaarheid','about.badge2':'Planning & budget gerespecteerd',
    'about.badge3':'Kwaliteit van uitvoering','about.badge4':'Volledige transparantie',
    'about.clients.h':'Onze klanten',
    'about.clients.list':'<div class="client-item">Particulieren</div><div class="client-item">Verenigingen van eigenaars</div><div class="client-item">Projectontwikkelaars & Investeerders</div><div class="client-item">Hotels & Bedrijven</div><div class="client-item">Overheden & Instellingen</div>',
    'about.commit.h':'Onze beloften',
    'about.commit.list':'<div class="client-item">Eén aanspreekpunt</div><div class="client-item">Dagelijkse werfopvolging</div><div class="client-item">Nauwkeurige offerte op maat</div><div class="client-item">Oplevering volgens de regels van de kunst</div><div class="client-item">Actief aan Franse & Nederlandse kant</div>',
    'services.tag':'Onze Diensten',
    'services.title':'Een volledig aanbod<br/>voor <span class="highlight">elk project.</span>',
    'services.sub':'Van grondwerken tot afwerking, FTFL dekt alle bouwdisciplines met dezelfde hoge kwaliteitsstandaard.',
    'svc1.h':'Grondwerken & Infrastructuur',
    'svc1.p':'Wij bereiden de bouwplaats voor uw project voor met middelen die zijn afgestemd op de specifieke kenmerken van het eiland.',
    'svc1.tags':'<span class="service-tag">Algemene grondwerken</span><span class="service-tag">Ontgraving</span><span class="service-tag">Uitgravingen</span><span class="service-tag">Wegenbouw</span><span class="service-tag">Riolering</span><span class="service-tag">Steenbestorting</span><span class="service-tag">Drainage</span>',
    'svc2.h':'Buitenaanleg',
    'svc2.p':'Wij ontwerpen en realiseren uw buitenruimtes om de waarde en aantrekkelijkheid van uw eigendom te verhogen.',
    'svc2.tags':'<span class="service-tag">Omheiningen & poorten</span><span class="service-tag">Terrassen</span><span class="service-tag">Pergola\'s</span><span class="service-tag">Zwembaden</span><span class="service-tag">Tuinaanleg</span><span class="service-tag">Buitenverlichting</span><span class="service-tag">Regenwatertanks</span>',
    'svc3.h':'Afbouwwerken',
    'svc3.p':'FTFL verzorgt alle afbouw- en renovatiewerken om uw project tot aan de oplevering te brengen.',
    'svc3.tags':'<span class="service-tag">Schrijnwerk</span><span class="service-tag">Loodgieterij</span><span class="service-tag">Tegelwerk</span><span class="service-tag">Schilderwerk</span><span class="service-tag">Hang- en sluitwerk</span><span class="service-tag">Metaalwerk</span><span class="service-tag">Renovatie</span>',
    'svc4.h':'Multidiensten & Onderhoud',
    'svc4.p':'Uw enige aanspreekpunt voor dagelijks onderhoud, preventief onderhoud en snelle herstellingen aan uw vastgoed.',
    'svc4.tags':'<span class="service-tag">Preventief onderhoud</span><span class="service-tag">Dringende herstellingen</span><span class="service-tag">Werfopruiming</span><span class="service-tag">Kleine werken</span><span class="service-tag">Onderhoudscontracten</span><span class="service-tag">24u-interventie</span>',
    'approach.tag':'Onze Werkwijze',
    'approach.title':'Een <span class="highlight">gestructureerd</span> proces<br/>bij elke stap.',
    'approach.sub':'Van de eerste ontmoeting tot de sleuteloverdracht begeleiden wij elk project met een bewezen methode, nauwkeurige uitvoering en volledige transparantie.',
    'step1.h':'01 · Luisteren',
    'step1.p':'Wij nemen de tijd om uw project grondig te begrijpen — technische vereisten, budget, planning — zodat wij samen de juiste strategie vanaf dag één kunnen opbouwen.',
    'step2.h':'02 · Studie',
    'step2.p':'Nauwkeurige prijsraming, gedetailleerde planning, risicoanalyse: onze technisch-financiële studie geeft u volledige duidelijkheid vóór de eerste schop de grond in gaat.',
    'step3.h':'03 · Uitvoering',
    'step3.p':'Onze ploegen werken met precisie en vakmanschap. Een toegewijde werfleider coördineert elke interventie en houdt u in real time op de hoogte.',
    'step4.h':'04 · Oplevering',
    'step4.p':'Wij overhandigen de sleutels pas wanneer elk detail naar uw volledige tevredenheid is afgewerkt — op tijd, conform de specificaties en duurzaam uitgevoerd.',
    'values.tag':'Onze Waarden',
    'values.title':'Wat ons <span class="highlight">onderscheidt.</span>',
    'values.sub':'Vier kernprincipes die elke beslissing sturen die wij nemen, van de eerste offerte tot de definitieve oplevering.',
    'val1.h':'Lokale Verankering',
    'val1.p':'Wij zijn geworteld in Saint-Martin en kennen elke wijk, elke leverancier, elke lokale beperking. Die nabijheid maakt ons sneller en slimmer dan wie dan ook.',
    'val2.h':'Betrouwbaarheid',
    'val2.p':'Werven die op tijd starten. Budgetten die op koers blijven. Beloften die zonder uitzondering worden nagekomen. Bij FTFL wordt reputatie gebouwd werf na werf.',
    'val3.h':'Veelzijdigheid',
    'val3.p':'Van grondwerken tot afwerking, van privévilla tot handelsgebouw: wij dekken alle bouwdisciplines intern. Eén contract, geen coördinatiezorgen.',
    'val4.h':'Kwaliteitseisen',
    'val4.p':'Wij leggen op elke werf dezelfde strenge normen op, ongeacht de omvang. Lokale regelgeving, veiligheid, planning: niets wordt aan het toeval overgelaten.',
    'zone.tag':'Werkgebied',
    'zone.title':'Eén eiland, twee landen,<br/><span class="highlight">één team.</span>',
    'zone.sub':'FTFL is actief op het volledige eiland Saint-Martin — zowel aan de Franse als aan de Nederlandse kant. Dubbele regelgevende en logistieke expertise ten dienste van uw projecten.',
    'zone.fr.side':'Franse Kant',
    'zone.fr.desc':'Volledige beheersing van het Franse administratieve kader en de bouwregelgeving. Bouwvergunningen, aangiftes en technische normen: wij regelen alles.',
    'zone.nl.side':'Nederlandse Kant',
    'zone.nl.desc':'Grondige kennis van het Nederlandse regelgevingskader op Sint Maarten. Onze ploegen werken aan de Nederlandse kant met dezelfde efficiëntie.',
    'zone.tagline':'+ occasionele projecten op <span>Saint-Barthélemy</span> & <span>Anguilla</span>',
    'team.tag':'Het Team',
    'team.title':'Vakmensen op het terrein,<br/><span class="highlight">ten dienste van uw eiland.</span>',
    'team.sub':'Het oprichtersteam van FTFL brengt bouwveteranen samen die de meest veeleisende projecten in het Caribisch gebied hebben gerealiseerd, met een unieke kennis van de lokale werkelijkheid.',
    'team.p1.h':'Terreinervaring',
    'team.p1.p':'Jaren van actieve werven op Saint-Martin geven ons een concreet inzicht in de uitdagingen: tropisch klimaat, eilandlogistiek, lokale bevoorradingsketens.',
    'team.p2.h':'Gestructureerd Team',
    'team.p2.p':'Ervaren werfleiders, vakkundige arbeiders, projectcoördinatoren. Elke werf krijgt een vaste verantwoordelijke — uw enige aanspreekpunt van begin tot einde.',
    'team.p3.h':'Sterk Lokaal Netwerk',
    'team.p3.p':'Betrouwbare leveranciers, gecertificeerde onderaannemers, solide machineverhuurbedrijven aan beide kanten van de grens: ons netwerk is de ruggengraat van uw project.',
    'team.cta.h':'Klaar om te starten?',
    'team.cta.p':'Neem vandaag nog contact op voor een gratis en vrijblijvende studie. Wij antwoorden binnen 24 uur.',
    'team.cta.btn':'Contacteer ons',
    'contact.tag':'Contact',
    'contact.title':'Laten we samen<br/><span class="highlight">bouwen.</span>',
    'contact.sub':'Een bouw-, renovatie- of buitenaanlegproject? Ons team bestudeert uw aanvraag en bezorgt u een gedetailleerde, gratis en vrijblijvende offerte.',
    'ci.whatsapp':'WhatsApp','ci.linkedin':'LinkedIn','ci.web':'Website','ci.loc':'Locatie',
    'f.name':'Voor- & achternaam *','f.phone':'Telefoonnummer *',
    'f.svc':'Gevraagde dienst *','f.loc':'Locatie van de werf',
    'f.budget':'Geschat budget','f.msg':'Beschrijving van uw project *',
    'f.msg.ph':'Vertel ons over uw project: type werken, geschatte oppervlakte, gewenste planning, bijzondere vereisten…',
    'f.submit':'Verstuur mijn aanvraag',
    'f.success':'✅ Bedankt! Uw aanvraag is goed ontvangen. Ons team neemt binnen 24 uur contact met u op.',
    'form.title':'Gratis offerte aanvragen',
    'ft.desc':'Uw betrouwbare bouwpartner op Saint-Martin. Grondwerken, infrastructuurwerken, buitenaanleg, afbouwwerken en multidiensten.',
    'ft.h.svc':'Diensten','ft.h.co':'Bedrijf','ft.h.ct':'Contact',
    'ft.svc1':'Grondwerken & Infra','ft.svc2':'Buitenaanleg',
    'ft.svc3':'Afbouwwerken','ft.svc4':'Multidiensten',
    'ft.about':'Over ons','ft.vals':'Onze waarden',
    'ft.app':'Onze werkwijze','ft.team':'Het team',
    'ft.copy':'© 2025 FTFL CARAÏBES — Alle rechten voorbehouden',
    'ft.legal1':'Juridische informatie','ft.legal2':'Privacybeleid',
    'ft.slogan':'Saint-Martin · Sint Maarten · Caraïben 🌴',
    'showcase.h':'Uitmuntendheid voor <span class="highlight">elk bouwproject.</span>',
    'showcase.p':'Professioneel materieel, vakkundige ploegen, volledige terreinbeheersing: elk FTFL-project wordt met dezelfde hoge standaard uitgevoerd.',
    'ft.quote':'Offerte aanvragen',
    'showcase.cta':'Offerte aanvragen',
  },
  pt: {
    'nav.about':'Sobre nós','nav.services':'Serviços','nav.approach':'Método',
    'nav.values':'Valores','nav.zone':'Cobertura','nav.cta':'Contacte-nos',
    'hero.line1':'Um parceiro de confiança',
    'hero.line2':'para todas as suas <span class="orange-word">obras.</span>',
    'hero.subtitle':'FTFL CARAÏBES é a empresa de construção de referência em Saint-Martin, presente nos dois lados da ilha. Terraplenagem, arranjos exteriores, obras de acabamento e manutenção.',
    'hero.cta1':'Pedir orçamento','hero.cta2':'Ver os nossos serviços',
    'hero.stat1':'Local e enraizado em Saint-Martin','hero.stat2':'Terraplenagem, Acabamentos…',
    'hero.stat2unit':'áreas','hero.stat3unit':'países','hero.stat3':'Lados FR e NL cobertos',
    'hero.scroll':'Rolar',
    'about.tag':'Sobre nós',
    'about.title':'Nascida de uma convicção,<br/><span class="highlight">enraizada nas Caraíbas.</span>',
    'about.p1':'A FTFL CARAÏBES nasceu de uma convicção: em Saint-Martin, os projetos de construção merecem um <strong>parceiro local fiável, ágil e polivalente</strong> — não um empreiteiro de fora.',
    'about.p2':'Fundada por profissionais da construção enraizados nas Caraíbas, a nossa empresa atua nos dois lados da ilha — francês e holandês — com um conhecimento profundo do território, dos atores locais e das suas especificidades.',
    'about.p3':'A nossa ambição: tornarmo-nos o <strong>parceiro de referência</strong> de particulares, promotores, hotéis e instituições para todos os seus projetos em Saint-Martin.',
    'about.badge1':'Reatividade & disponibilidade','about.badge2':'Prazos e orçamentos respeitados',
    'about.badge3':'Qualidade de execução','about.badge4':'Transparência total',
    'about.clients.h':'Os nossos clientes',
    'about.clients.list':'<div class="client-item">Particulares</div><div class="client-item">Condomínios</div><div class="client-item">Promotores & Investidores</div><div class="client-item">Hotéis & Empresas</div><div class="client-item">Autarquias & Instituições</div>',
    'about.commit.h':'Os nossos compromissos',
    'about.commit.list':'<div class="client-item">Um único interlocutor</div><div class="client-item">Acompanhamento diário da obra</div><div class="client-item">Orçamento preciso e detalhado</div><div class="client-item">Entrega segundo as regras da arte</div><div class="client-item">Intervenções FR & NL</div>',
    'services.tag':'Os Nossos Serviços',
    'services.title':'Uma resposta global<br/>para <span class="highlight">cada projeto.</span>',
    'services.sub':'Da terraplenagem aos acabamentos, a FTFL cobre todos os ofícios da construção com os mesmos padrões de exigência.',
    'svc1.h':'Terraplenagem e infraestruturas',
    'svc1.p':'Preparamos o terreno para os seus projetos com meios adaptados às especificidades da ilha.',
    'svc1.tags':'<span class="service-tag">Terraplenagem geral</span><span class="service-tag">Escavação</span><span class="service-tag">Valas</span><span class="service-tag">Arruamentos</span><span class="service-tag">Saneamento</span><span class="service-tag">Enrocamento</span><span class="service-tag">Drenagem</span>',
    'svc2.h':'Obras exteriores e paisagismo',
    'svc2.p':'Concebemos e realizamos os seus espaços exteriores para valorizar e embelezar o seu imóvel.',
    'svc2.tags':'<span class="service-tag">Vedações & portões</span><span class="service-tag">Terraços</span><span class="service-tag">Pérgolas</span><span class="service-tag">Piscinas</span><span class="service-tag">Paisagismo</span><span class="service-tag">Iluminação ext.</span><span class="service-tag">Cisternas</span>',
    'svc3.h':'Obras de Acabamento',
    'svc3.p':'A FTFL gere todas as obras de acabamento e reabilitação para levar os seus projetos até à entrega final.',
    'svc3.tags':'<span class="service-tag">Carpintaria</span><span class="service-tag">Canalização</span><span class="service-tag">Revestimentos</span><span class="service-tag">Pintura</span><span class="service-tag">Serralharia</span><span class="service-tag">Trabalhos em metal</span><span class="service-tag">Renovações</span>',
    'svc4.h':'Multisserviços e Manutenção',
    'svc4.p':'Um único interlocutor para a manutenção corrente, as revisões preventivas e as intervenções de emergência no seu património.',
    'svc4.tags':'<span class="service-tag">Manutenção preventiva</span><span class="service-tag">Reparações urgentes</span><span class="service-tag">Limpeza de obra</span><span class="service-tag">Pequenos trabalhos</span><span class="service-tag">Contratos manutenção</span><span class="service-tag">Urgências 24h</span>',
    'approach.tag':'O Nosso Método',
    'approach.title':'Um processo <span class="highlight">rigoroso</span><br/>em cada etapa.',
    'approach.sub':'Da primeira reunião à entrega das chaves, acompanhamos cada projeto com método, rigor e transparência total.',
    'step1.h':'01 · Escuta',
    'step1.p':'Dedicamos tempo a compreender o seu projeto em pormenor — requisitos técnicos, orçamento, prazos — para definirmos juntos a estratégia mais adequada desde o início.',
    'step2.h':'02 · Estudo',
    'step2.p':'Estimativa detalhada, planeamento preliminar, análise de riscos: o nosso estudo técnico-financeiro dá-lhe visibilidade total antes de qualquer início de obra.',
    'step3.h':'03 · Execução',
    'step3.p':'As nossas equipas intervêm com rigor e profissionalismo. Um diretor de obra dedicado coordena cada intervenção e mantém-no informado em tempo real.',
    'step4.h':'04 · Entrega',
    'step4.p':'Só entregamos as chaves quando cada detalhe estiver concluído à sua inteira satisfação — no prazo acordado, segundo as normas e construído para durar.',
    'values.tag':'Os Nossos Valores',
    'values.title':'O que nos <span class="highlight">define.</span>',
    'values.sub':'Quatro princípios fundamentais que orientam cada uma das nossas decisões, do primeiro orçamento à entrega final.',
    'val1.h':'Presença Local',
    'val1.p':'Presentes em Saint-Martin desde o início, conhecemos cada bairro, cada fornecedor e cada condicionante local. Essa proximidade torna-nos mais ágeis e eficazes onde outros ainda procuram referências.',
    'val2.h':'Fiabilidade',
    'val2.p':'Obras que começam a tempo. Orçamentos que se respeitam. Compromissos que se cumprem sem exceção. Na FTFL, a nossa reputação constrói-se obra a obra, sobre factos.',
    'val3.h':'Polivalência',
    'val3.p':'Da terraplenagem aos acabamentos, da moradia privada ao edifício comercial, cobrimos todos os ofícios internamente. Um só contrato, zero coordenação extra.',
    'val4.h':'Exigência',
    'val4.p':'Aplicamos os mesmos padrões rigorosos em cada obra, independentemente da sua dimensão. Regulamentação local, segurança, prazos: nada é deixado ao acaso num projeto FTFL.',
    'zone.tag':'Zona de Intervenção',
    'zone.title':'Uma ilha, dois países,<br/><span class="highlight">uma única equipa.</span>',
    'zone.sub':'A FTFL opera em toda a ilha de Saint-Martin — lados francês e holandês. Duplo domínio regulamentar e logístico ao serviço dos seus projetos.',
    'zone.fr.side':'Lado Francês',
    'zone.fr.desc':'Domínio completo do quadro administrativo e regulamentar francês. Licenças de obra, declarações e normas técnicas: tratamos de tudo.',
    'zone.nl.side':'Lado Holandês',
    'zone.nl.desc':'Conhecimento profundo do sistema regulamentar neerlandês em Sint Maarten. As nossas equipas operam do lado holandês com a mesma eficácia.',
    'zone.tagline':'+ intervenções pontuais em <span>Saint-Barthélemy</span> & <span>Anguilla</span>',
    'team.tag':'A Equipa',
    'team.title':'Profissionais de terreno,<br/><span class="highlight">ao serviço da ilha.</span>',
    'team.sub':'A equipa fundadora da FTFL reúne veteranos da construção que realizaram os projetos mais exigentes das Caraíbas, com um conhecimento único da realidade local.',
    'team.p1.h':'Experiência de Terreno',
    'team.p1.p':'Anos de obras ativas em Saint-Martin traduzem-se num conhecimento concreto dos desafios locais: clima tropical, logística insular, cadeias de abastecimento locais.',
    'team.p2.h':'Equipa Estruturada',
    'team.p2.p':'Diretores de obra experientes, operários qualificados, coordenadores de projeto. Cada obra tem um responsável único — o seu interlocutor do início ao fim.',
    'team.p3.h':'Rede Local Sólida',
    'team.p3.p':'Fornecedores de confiança, subempreiteiros certificados, empresas de aluguer de equipamento nos dois lados da fronteira: a nossa rede é a espinha dorsal dos seus projetos.',
    'team.cta.h':'Pronto para começar o seu projeto?',
    'team.cta.p':'Contacte-nos hoje para um estudo gratuito e sem compromisso. Respondemos em menos de 24 horas.',
    'team.cta.btn':'Falar connosco',
    'contact.tag':'Contacto',
    'contact.title':'Vamos construir juntos<br/><span class="highlight">o seu projeto.</span>',
    'contact.sub':'Tem um projeto de construção, remodelação ou arranjo? A nossa equipa analisa o seu pedido e apresenta um orçamento detalhado, gratuito e sem compromisso.',
    'ci.whatsapp':'WhatsApp','ci.linkedin':'LinkedIn','ci.web':'Website','ci.loc':'Localização',
    'f.name':'Nome completo *','f.phone':'Telefone *',
    'f.svc':'Tipo de serviço *','f.loc':'Localização da obra',
    'f.budget':'Orçamento estimado','f.msg':'Descrição do projeto *',
    'f.msg.ph':'Descreva o seu projeto: tipo de obras, área aproximada, prazos pretendidos, requisitos especiais…',
    'f.submit':'Enviar o meu pedido',
    'f.success':'✅ Obrigado! O seu pedido foi recebido. A nossa equipa entrará em contacto consigo em menos de 24 horas.',
    'form.title':'Pedir orçamento gratuito',
    'ft.desc':'O seu parceiro de construção de referência em Saint-Martin. Terraplenagem, infraestruturas e redes, obras exteriores, acabamentos e multisserviços.',
    'ft.h.svc':'Serviços','ft.h.co':'Empresa','ft.h.ct':'Contacto',
    'ft.svc1':'Terraplenagem & Infraestruturas','ft.svc2':'Arranjos Exteriores',
    'ft.svc3':'Obras de Acabamento','ft.svc4':'Multisserviços',
    'ft.about':'Sobre nós','ft.vals':'Os nossos valores',
    'ft.app':'O nosso método','ft.team':'A equipa',
    'ft.copy':'© 2025 FTFL CARAÏBES — Todos os direitos reservados',
    'ft.legal1':'Menções legais','ft.legal2':'Política de privacidade',
    'ft.slogan':'Saint-Martin · Sint Maarten · Caraíbas 🌴',
    'showcase.h':'Excelência ao serviço de <span class="highlight">cada obra.</span>',
    'showcase.p':'Equipamentos profissionais, equipas qualificadas e conhecimento profundo do território: cada projeto FTFL é conduzido com o mesmo nível de exigência.',
    'showcase.cta':'Pedir orçamento',
    'ft.quote':'Pedir orçamento',
  }
};

// ── SEO META DATA PAR LANGUE ─────────────────────────────────
const seoMeta = {
  fr: {
    htmlLang:   'fr',
    ogLocale:   'fr_FR',
    title:      'FTFL CARAÏBES | Entreprise de Construction Saint-Martin | Terrassement VRD BTP SXM',
    desc:       'FTFL CARAÏBES, votre entreprise BTP de référence à Saint-Martin (SXM). Terrassement, VRD, aménagement extérieur, second œuvre, multiservices. Interventions côté français et hollandais. Devis gratuit.',
    keywords:   'construction Saint-Martin, BTP Saint-Martin, terrassement Saint-Martin, travaux Saint-Martin, VRD SXM, aménagement extérieur Saint-Martin, rénovation Saint-Martin, second oeuvre Saint-Martin, entreprise travaux SXM, maçonnerie Saint-Martin, piscine Saint-Martin, menuiserie Saint-Martin, plomberie Saint-Martin, peinture Saint-Martin, devis construction Saint-Martin, Sint Maarten bouw, FTFL Caraïbes, construction piscine Saint-Martin, rénovation villa Saint-Martin, terrassement Sint Maarten, entreprise BTP SXM 97150, travaux bâtiment Saint-Martin, constructeur Saint-Martin, devis travaux gratuit Saint-Martin',
    ogTitle:    'FTFL CARAÏBES | Entreprise de Construction Saint-Martin',
    ogDesc:     'Un seul partenaire pour tous vos travaux à Saint-Martin. Terrassement, VRD, aménagement extérieur, second œuvre et multiservices.',
    twTitle:    'FTFL CARAÏBES | Construction Saint-Martin',
    twDesc:     'Un seul partenaire pour tous vos travaux à Saint-Martin. Terrassement, VRD, second œuvre, multiservices.',
  },
  en: {
    htmlLang:   'en',
    ogLocale:   'en_US',
    title:      'FTFL CARAÏBES | Construction Company Saint Martin Island | Earthworks Civil Works SXM',
    desc:       'FTFL CARAÏBES, your trusted construction company on Saint Martin island (SXM). Earthworks, civil works, exterior works, finishing works and maintenance services on both the French and Dutch sides. Free quote.',
    keywords:   'construction company Saint Martin island, building contractor SXM, earthworks Saint Martin, civil works Sint Maarten, renovation Saint Martin, landscaping Saint Martin, pool construction Saint Martin, outdoor development SXM, carpentry plumbing Saint Martin, maintenance Saint Martin island, FTFL Caribbeans, villa renovation Saint Martin, construction quote Saint Martin, property maintenance Sint Maarten, trusted builder Saint Martin island',
    ogTitle:    'FTFL CARAÏBES | Construction Company Saint Martin',
    ogDesc:     'One trusted partner for all your construction projects in Saint Martin. Earthworks, civil works, exterior works, finishing works and maintenance services.',
    twTitle:    'FTFL CARAÏBES | Construction Saint Martin Island',
    twDesc:     'One trusted partner for your construction projects in Saint Martin SXM. Earthworks, finishing works and maintenance services.',
  },
  es: {
    htmlLang:   'es',
    ogLocale:   'es_ES',
    title:      'FTFL CARAÏBES | Empresa de Construcción Saint-Martin | Movimiento de Tierras y Obras SXM',
    desc:       'FTFL CARAÏBES, su empresa de construcción de referencia en Saint-Martin (SXM). Movimiento de tierras, urbanización y redes, obras exteriores, acabados y multiservicios. Lado francés y holandés. Presupuesto gratuito.',
    keywords:   'empresa construcción Saint-Martin, obras Saint-Martin, constructora Sint Maarten, terraplenaje Saint-Martin, renovación Saint-Martin, piscina Saint-Martin, jardinería Saint-Martin, fontanería Saint-Martin, pintura Saint-Martin, FTFL Caribe, obras Caribe francés, construcción piscina Saint-Martin, reforma villa Saint-Martin, empresa constructora SXM, presupuesto obras Saint-Martin, mantenimiento inmueble Sint Maarten',
    ogTitle:    'FTFL CARAÏBES | Empresa de Construcción Saint-Martin',
    ogDesc:     'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acondicionamiento exterior, acabados y multiservicios.',
    twTitle:    'FTFL CARAÏBES | Construcción Saint-Martin SXM',
    twDesc:     'Un solo socio para todas sus obras en Saint-Martin. Movimiento de tierras, acabados y multiservicios.',
  },
  nl: {
    htmlLang:   'nl',
    ogLocale:   'nl_NL',
    title:      'FTFL CARAÏBES | Bouwbedrijf Sint Maarten Saint-Martin | Grondwerken en Infrastructuur SXM',
    desc:       'FTFL CARAÏBES, uw betrouwbare bouwpartner op Sint Maarten / Saint-Martin (SXM). Grondwerken, infrastructuurwerken, buitenaanleg, afbouwwerken en multidiensten aan de Franse en Nederlandse kant. Gratis offerte.',
    keywords:   'bouwbedrijf Sint Maarten, aannemer Sint Maarten, grondwerken Sint Maarten, verbouwing Sint Maarten, tuinaanleg Sint Maarten, zwembad Sint Maarten, schilderwerk Sint Maarten, loodgieter Sint Maarten, FTFL Caribbeans, bouw Saint-Martin Frans Carib, zwembad bouwen Sint Maarten, villa renovatie Sint Maarten, aannemer SXM, bouwofferte Sint Maarten, vastgoedonderhoud Sint Maarten',
    ogTitle:    'FTFL CARAÏBES | Bouwbedrijf Sint Maarten / Saint-Martin',
    ogDesc:     'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, buitenaanleg, afbouwwerken en multidiensten.',
    twTitle:    'FTFL CARAÏBES | Bouwbedrijf Sint Maarten SXM',
    twDesc:     'Eén partner voor al uw bouwprojecten op Sint Maarten. Grondwerken, afbouw en multidiensten.',
  },
  pt: {
    htmlLang:   'pt',
    ogLocale:   'pt_PT',
    title:      'FTFL CARAÏBES | Empresa de Construção Saint-Martin | Terraplenagem Obras SXM',
    desc:       'FTFL CARAÏBES, a sua empresa de construção de referência em Saint-Martin (SXM). Terraplenagem, infraestruturas e redes, obras exteriores, acabamentos e multisserviços nos lados francês e holandês. Orçamento gratuito.',
    keywords:   'empresa construção Saint-Martin, obras Saint-Martin, empreiteiro Sint Maarten, terraplenagem Saint-Martin, remodelação Saint-Martin, piscina Saint-Martin, jardinagem Saint-Martin, canalização Saint-Martin, pintura Saint-Martin, FTFL Caribe, construção Caribe francês, construção piscina Saint-Martin, renovação moradia Saint-Martin, empreiteiro SXM, orçamento obras Saint-Martin, manutenção imóvel Sint Maarten',
    ogTitle:    'FTFL CARAÏBES | Empresa de Construção Saint-Martin',
    ogDesc:     'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, obras exteriores, acabamentos e multisserviços.',
    twTitle:    'FTFL CARAÏBES | Construção Saint-Martin SXM',
    twDesc:     'Um único parceiro para todas as suas obras em Saint-Martin. Terraplenagem, acabamentos e multisserviços.',
  }
};

function updateSEOMeta(lang) {
  const m = seoMeta[lang] || seoMeta.fr;
  document.documentElement.lang = m.htmlLang;
  document.title = m.title;
  document.getElementById('seo-title').textContent = m.title;
  const setMeta = (id, attr, val) => { const el = document.getElementById(id); if(el) el.setAttribute(attr, val); };
  setMeta('seo-desc',  'content', m.desc);
  setMeta('seo-keys',  'content', m.keywords);
  setMeta('og-title',  'content', m.ogTitle);
  setMeta('og-desc',   'content', m.ogDesc);
  setMeta('og-locale', 'content', m.ogLocale);
  setMeta('tw-title',  'content', m.twTitle);
  setMeta('tw-desc',   'content', m.twDesc);
  const _langUrls = {fr:'https://www.ftfl-sxm.com/',en:'https://www.ftfl-sxm.com/en/',es:'https://www.ftfl-sxm.com/es/',nl:'https://www.ftfl-sxm.com/nl/',pt:'https://www.ftfl-sxm.com/pt/'};
  const canonical = document.getElementById('seo-canonical');
  if(canonical) canonical.href = _langUrls[lang] || 'https://www.ftfl-sxm.com/';
  document.querySelector('html').setAttribute('lang', m.htmlLang);
}

function updateSelectOptions(lang) {
  const opts = {
    fr: {
      service: [
        ['','Sélectionnez un service',true],
        ['Terrassement & VRD','Terrassement & VRD'],
        ['Aménagement Extérieur','Aménagement Extérieur'],
        ['Travaux de Second Œuvre','Travaux de Second Œuvre'],
        ['Multiservices & Maintenance','Multiservices & Maintenance'],
        ['Autre / Plusieurs services','Autre / Plusieurs services']
      ],
      location: [
        ['','Partie française ou NL ?',true],
        ['Saint-Martin — Partie Française','Saint-Martin (FR)'],
        ['Sint Maarten — Partie Néerlandaise','Sint Maarten (NL)'],
        ['Les deux côtés','Les deux'],
        ['Autre île','Autre île']
      ],
      budget: [
        ['','Budget indicatif',true],
        ['Moins de 5 000 €','Moins de 5 000 €'],['5 000 – 20 000 €','5 000 – 20 000 €'],
        ['20 000 – 50 000 €','20 000 – 50 000 €'],['50 000 – 100 000 €','50 000 – 100 000 €'],['Plus de 100 000 €','Plus de 100 000 €']
      ]
    },
    en: {
      service: [
        ['','Select a service',true],
        ['Earthworks & Civil Works','Earthworks & Civil Works'],
        ['Exterior Works','Exterior Works'],
        ['Finishing & Interior Works','Finishing & Interior Works'],
        ['Multiservices & Maintenance','Multiservices & Maintenance'],
        ['Other / Multiple services','Other / Multiple services']
      ],
      location: [
        ['','French or Dutch side?',true],
        ['Saint-Martin — French Side','Saint-Martin (FR)'],
        ['Sint Maarten — Dutch Side','Sint Maarten (NL)'],
        ['Both sides','Both sides'],
        ['Another island','Another island']
      ],
      budget: [
        ['','Indicative budget',true],
        ['Under €5,000','Under €5,000'],['€5,000 – €20,000','€5,000 – €20,000'],
        ['€20,000 – €50,000','€20,000 – €50,000'],['€50,000 – €100,000','€50,000 – €100,000'],['Over €100,000','Over €100,000']
      ]
    },
    es: {
      service: [
        ['','Seleccione un servicio',true],
        ['Movimiento de tierras, urbanización y redes','Movimiento de tierras, urbanización y redes'],
        ['Obras exteriores','Obras exteriores'],
        ['Acabados interiores','Acabados interiores'],
        ['Multiservicios & Mantenimiento','Multiservicios & Mantenimiento'],
        ['Otro / Varios servicios','Otro / Varios servicios']
      ],
      location: [
        ['','¿Lado francés o holandés?',true],
        ['Saint-Martin — Lado Francés','Saint-Martin (FR)'],
        ['Sint Maarten — Lado Holandés','Sint Maarten (NL)'],
        ['Ambos lados','Ambos lados'],
        ['Otra isla','Otra isla']
      ],
      budget: [
        ['','Presupuesto estimado',true],
        ['Menos de 5.000 €','Menos de 5.000 €'],['5.000 – 20.000 €','5.000 – 20.000 €'],
        ['20.000 – 50.000 €','20.000 – 50.000 €'],['50.000 – 100.000 €','50.000 – 100.000 €'],['Más de 100.000 €','Más de 100.000 €']
      ]
    },
    nl: {
      service: [
        ['','Selecteer een dienst',true],
        ['Grondwerken & Infrastructuur','Grondwerken & Infrastructuur'],
        ['Buitenaanleg','Buitenaanleg'],
        ['Afbouwwerken','Afbouwwerken'],
        ['Multidiensten & Onderhoud','Multidiensten & Onderhoud'],
        ['Andere / Meerdere diensten','Andere / Meerdere diensten']
      ],
      location: [
        ['','Franse of Nederlandse kant?',true],
        ['Saint-Martin — Franse kant','Saint-Martin (FR)'],
        ['Sint Maarten — Nederlandse kant','Sint Maarten (NL)'],
        ['Beide kanten','Beide kanten'],
        ['Ander eiland','Ander eiland']
      ],
      budget: [
        ['','Indicatief budget',true],
        ['Minder dan € 5.000','Minder dan € 5.000'],['€ 5.000 – € 20.000','€ 5.000 – € 20.000'],
        ['€ 20.000 – € 50.000','€ 20.000 – € 50.000'],['€ 50.000 – € 100.000','€ 50.000 – € 100.000'],['Meer dan € 100.000','Meer dan € 100.000']
      ]
    },
    pt: {
      service: [
        ['','Selecione um serviço',true],
        ['Terraplenagem e infraestruturas','Terraplenagem e infraestruturas'],
        ['Obras exteriores e paisagismo','Obras exteriores e paisagismo'],
        ['Obras de Acabamento','Obras de Acabamento'],
        ['Multisserviços & Manutenção','Multisserviços & Manutenção'],
        ['Outro / Vários serviços','Outro / Vários serviços']
      ],
      location: [
        ['','Lado francês ou holandês?',true],
        ['Saint-Martin — lado francês','Saint-Martin (FR)'],
        ['Sint Maarten — lado holandês','Sint Maarten (NL)'],
        ['Ambos os lados','Ambos os lados'],
        ['Outra ilha','Outra ilha']
      ],
      budget: [
        ['','Orçamento estimado',true],
        ['Menos de 5.000 €','Menos de 5.000 €'],['5.000 – 20.000 €','5.000 – 20.000 €'],
        ['20.000 – 50.000 €','20.000 – 50.000 €'],['50.000 – 100.000 €','50.000 – 100.000 €'],['Mais de 100.000 €','Mais de 100.000 €']
      ]
    }
  };
  const d = opts[lang] || opts.fr;
  const rebuild = (id, arr) => {
    const sel = document.getElementById(id);
    if(!sel) return;
    const cur = sel.value;
    sel.innerHTML = arr.map(([v,t,dis]) =>
      `<option value="${v}"${dis?' disabled selected':''}${v===cur?' selected':''}>${t}</option>`
    ).join('');
  };
  rebuild('selectService', d.service);
  rebuild('selectLocation', d.location);
  rebuild('selectBudget', d.budget);
}

function applyLang(lang) {
  const dict = i18nData[lang] || i18nData.fr;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key] !== undefined) el.innerHTML = dict[key];
  });
  const ta = document.getElementById('msgTextarea');
  if(ta && dict['f.msg.ph']) ta.placeholder = dict['f.msg.ph'];
  updateSelectOptions(lang);
  document.getElementById('langCurrent').textContent = lang.toUpperCase();
  document.querySelectorAll('.lang-option').forEach(opt => {
    opt.classList.toggle('active', opt.dataset.lang === lang);
  });
  document.querySelectorAll('[data-legal-lang]').forEach(function(el) {
    el.style.display = el.dataset.legalLang === lang ? '' : 'none';
  });
  localStorage.setItem('ftfl-lang', lang);
  currentLang = lang;
  updateSEOMeta(lang);
  document.querySelectorAll('.hero-title .line').forEach(line => {
    line.style.opacity = '1'; line.style.transform = 'translateY(0)';
  });
}

function setLang(lang) {
  const langPaths = { fr:'/', en:'/en/', es:'/es/', nl:'/nl/', pt:'/pt/' };
  const target = langPaths[lang] || '/';
  const path = location.pathname;
  let curLang = 'fr';
  if (/^\/en(\/|$)/.test(path)) curLang = 'en';
  else if (/^\/es(\/|$)/.test(path)) curLang = 'es';
  else if (/^\/nl(\/|$)/.test(path)) curLang = 'nl';
  else if (/^\/pt(\/|$)/.test(path)) curLang = 'pt';
  localStorage.setItem('ftfl-lang', lang);
  if (curLang !== lang) {
    window.location.href = target;
    return;
  }
  applyLang(lang);
  closeLang();
}

function toggleLang() {
  document.getElementById('langSwitcher').classList.toggle('open');
}
function closeLang() {
  document.getElementById('langSwitcher').classList.remove('open');
}

// Close dropdown when clicking outside
document.addEventListener('click', e => {
  if (!e.target.closest('#langSwitcher')) closeLang();
});

// Init on load
applyLang(currentLang);

// ════════════════════════════════════════════════════════════
//   DYNAMIC EFFECTS — PREMIUM WEBMASTER LAYER
// ════════════════════════════════════════════════════════════

// ── PRELOADER ────────────────────────────────────────────────
(function(){
  const pl = document.getElementById('preloader');
  if(!pl) return;
  const dismiss = () => { pl.classList.add('done'); setTimeout(()=>pl.remove(),700); };
  if(document.readyState==='complete') { setTimeout(dismiss,500); }
  else { window.addEventListener('load',()=>setTimeout(dismiss,1700)); }
})();

// ── SCROLL PROGRESS BAR ──────────────────────────────────────
(function(){
  const bar = document.getElementById('scrollProgress');
  if(!bar) return;
  window.addEventListener('scroll',()=>{
    const pct = window.scrollY/(document.documentElement.scrollHeight-window.innerHeight)*100;
    bar.style.width = Math.min(pct,100)+'%';
  },{passive:true});
})();

// ── ACTIVE NAV SECTION ───────────────────────────────────────
(function(){
  const secs = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.nav-links a, .mobile-nav a');
  const obs = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting)
        links.forEach(l=>l.classList.toggle('is-active', l.getAttribute('href')==='#'+e.target.id));
    });
  },{threshold:.3, rootMargin:'-70px 0px -38% 0px'});
  secs.forEach(s=>obs.observe(s));
})();

// ── NAVBAR CTA PULSE (appears after scroll) ───────────────────
(function(){
  const cta = document.querySelector('.navbar-cta .btn-primary');
  if(!cta) return;
  let done=false;
  window.addEventListener('scroll',()=>{
    if(!done && window.scrollY>450){ cta.classList.add('pulsing'); done=true; }
  },{passive:true});
})();

// ── BUTTON RIPPLE ────────────────────────────────────────────
document.querySelectorAll('.btn').forEach(btn=>{
  btn.style.position='relative';
  btn.addEventListener('click',e=>{
    const r=btn.getBoundingClientRect();
    const d=Math.max(r.width,r.height)*1.9;
    const rpl=document.createElement('span');
    rpl.className='btn-ripple';
    rpl.style.cssText=`position:absolute;width:${d}px;height:${d}px;left:${e.clientX-r.left-d/2}px;top:${e.clientY-r.top-d/2}px`;
    btn.appendChild(rpl);
    rpl.addEventListener('animationend',()=>rpl.remove());
  });
});

// ── MAGNETIC BUTTONS ─────────────────────────────────────────
if(window.matchMedia('(pointer:fine)').matches){
  document.querySelectorAll('.btn-primary,.btn-outline').forEach(btn=>{
    btn.addEventListener('mousemove',e=>{
      const r=btn.getBoundingClientRect();
      const x=(e.clientX-r.left-r.width/2)*.28;
      const y=(e.clientY-r.top-r.height/2)*.28;
      btn.style.cssText+='transition:transform .05s;transform:translate('+x+'px,'+y+'px) scale(1.02)';
    });
    btn.addEventListener('mouseleave',()=>{
      btn.style.transition='transform .45s cubic-bezier(.4,0,.2,1)';
      btn.style.transform='translate(0,0) scale(1)';
    });
  });
}

// ── 3D CARD TILT ─────────────────────────────────────────────
if(window.matchMedia('(hover:hover) and (pointer:fine)').matches){
  document.querySelectorAll('.service-card,.value-card,.team-pillar,.about-card').forEach(card=>{
    card.addEventListener('mouseenter',()=>{ card.style.transition='none'; });
    card.addEventListener('mousemove',e=>{
      const r=card.getBoundingClientRect();
      const x=(e.clientX-r.left)/r.width-.5;
      const y=(e.clientY-r.top)/r.height-.5;
      card.style.transform=`perspective(700px) rotateX(${y*-9}deg) rotateY(${x*9}deg) translateY(-6px) scale(1.025)`;
    });
    card.addEventListener('mouseleave',()=>{
      card.style.transition='transform .5s cubic-bezier(.4,0,.2,1)';
      card.style.transform='';
      setTimeout(()=>card.style.transition='',500);
    });
  });
}

// ── PARALLAX HERO PHOTO ──────────────────────────────────────
(function(){
  const img=document.querySelector('.hero-photo img');
  if(!img) return;
  window.addEventListener('scroll',()=>{
    const y=window.scrollY;
    if(y<window.innerHeight*1.3) img.style.transform='translateY('+(y*.1)+'px)';
  },{passive:true});
})();

// ── PARALLAX SHOWCASE STRIP ──────────────────────────────────
(function(){
  const img=document.querySelector('.showcase-strip img');
  const strip=img && img.closest('.showcase-strip');
  if(!strip) return;
  window.addEventListener('scroll',()=>{
    const r=strip.getBoundingClientRect();
    if(r.bottom<0 || r.top>window.innerHeight) return;
    const offset=(window.innerHeight/2-r.top-r.height/2)*.1;
    img.style.transform='translateY('+offset+'px)';
  },{passive:true});
})();

// ── CUSTOM CURSOR ────────────────────────────────────────────
(function(){
  if(!window.matchMedia('(pointer:fine)').matches) return;
  const dot=document.getElementById('cursorDot');
  const ring=document.getElementById('cursorRing');
  if(!dot||!ring) return;
  let mx=window.innerWidth/2, my=window.innerHeight/2,
      rx=mx, ry=my;
  window.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;},{passive:true});
  (function tick(){
    dot.style.left=mx+'px'; dot.style.top=my+'px';
    rx+=(mx-rx)*.13; ry+=(my-ry)*.13;
    ring.style.left=Math.round(rx)+'px'; ring.style.top=Math.round(ry)+'px';
    requestAnimationFrame(tick);
  })();
  const targets='a,button,.btn,.service-card,.lang-option,.burger,.about-card,.team-pillar,.value-card';
  document.querySelectorAll(targets).forEach(el=>{
    el.addEventListener('mouseenter',()=>ring.classList.add('hovered'));
    el.addEventListener('mouseleave',()=>ring.classList.remove('hovered'));
  });
  document.addEventListener('mousedown',()=>{ring.classList.add('clicked');dot.style.transform='translate(-50%,-50%) scale(.55)';});
  document.addEventListener('mouseup',()=>{ring.classList.remove('clicked');dot.style.transform='translate(-50%,-50%) scale(1)';});
  document.addEventListener('mouseleave',()=>{dot.style.opacity='0';ring.style.opacity='0';});
  document.addEventListener('mouseenter',()=>{dot.style.opacity='1';ring.style.opacity='1';});
})();

// ── SMOOTH SCROLL ───────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) {
      e.preventDefault();
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── LEGAL MODALS ─────────────────────────────────────────────
function openLegalModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
  const closeBtn = modal.querySelector('.legal-close');
  if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
}

function closeLegalModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.remove('open');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.legal-modal.open').forEach(function(m) {
      m.classList.remove('open');
      document.body.style.overflow = '';
    });
  }
});

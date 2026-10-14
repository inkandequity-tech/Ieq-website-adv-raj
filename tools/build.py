#!/usr/bin/env python3
"""Builds the static site into the repository root.

    python3 tools/build.py

Pages are plain HTML so that GitHub Pages can serve them as they are. Edit the
content in this file, run the script, commit the generated pages.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ieqlaw.com"
NAME = "Ink & Equity"
PHONE = "+91 9450 72 7289"
PHONE_TEL = "+919450727289"
EMAIL = "ChamberLko@gmail.com"
STREET = "1, Moti Mahal Marg, Hazratganj"
CITY = "Lucknow, Uttar Pradesh 226001"
MODIFIED = "2026-10-13"
REVIEWED = "13 October 2026"

PRACTICE = [
    ("constitutional-and-writ", "Constitutional and writ matters",
     "Challenging state action in the High Court and the Supreme Court."),
    ("service-matters", "Service matters",
     "Promotion, seniority, discipline, pension and recruitment disputes."),
    ("property-and-real-estate", "Property and real estate",
     "Title, possession, tenancy, development authorities and RERA."),
    ("cyber-crime-and-online-fraud", "Cyber crime and online fraud",
     "Reporting, evidence, bank disputes and criminal proceedings."),
]
# Extra practice areas live in tools/practice_content.py (one page each).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from practice_content import NEW_PRACTICE, NEW_PAGES
import mapdata
PRACTICE = PRACTICE + NEW_PRACTICE
HOME_PRACTICE = PRACTICE[:4]
OTHER_AREAS = []

# Case library: hypothetical scenarios (tools/content/scenarios.json). Every page carries
# the notice below. Nothing in the library states or implies that the practice handled a matter.
_SC = json.loads((ROOT / "tools" / "content" / "scenarios.json").read_text(encoding="utf-8"))
SCEN_NOTICE = _SC["notice"]
SCEN_DATE, SCEN_DATE_HUMAN = "2026-10-14", "14 October 2026"
SCEN_STATUS = "Draft for general information"
LIB = [x for x in _SC["scenarios"] if x["publish"]]
for _i, _x in enumerate(LIB, 1):
    _x["ref"] = f"CL-{_i:02d}"
SCEN_BY_PRACTICE = {}
for _x in LIB:
    SCEN_BY_PRACTICE.setdefault(_x["practice"], []).append(_x)

TEAM = [
    ("rishabh", "Rishabh Raj", "Founding partner", "Constitutional and writ matters, property, service matters, cyber crime."),
    ("vedant", "Vedant Bhargav", "Managing partner", "Family law, criminal law, contract and civil litigation."),
    ("radhika", "Radhika Singh", "Partner", "Tax, constitutional and service matters."),
    ("hanumant", "Hanumant Lal Srivastava", "Partner", "Civil and criminal matters in the trial courts."),
    ("gokel", "Gokel Seth", "Junior partner", "Property and real estate, RERA, development authority and tenancy matters."),
    ("richa", "Richa Mishra", "Junior partner", "Tax, constitutional and service matters."),
    ("kanchan", "Kanchan Srivastava", "Junior partner", "Civil and criminal matters in the trial courts."),
]

LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6 58 32 32 58 6 32Z" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-dasharray="4 5"/><path d="M32 17 47 32 32 47 17 32Z" fill="var(--accent)"/>'
        '<circle cx="32" cy="32" r="4.2" fill="var(--warm)"/></svg>')
MOON = '<svg class="theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5Z"/></svg>'
SUN = '<svg class="theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>'

SCALES = '''<div class="scales-wrap">
<button class="scales-btn" type="button" aria-label="Add a weight to the scales">
<svg class="scales" viewBox="0 0 400 340" role="img" aria-label="A pair of brass scales">
<path class="metal" d="M200 62V318M128 318H272"/>
<circle cx="200" cy="56" r="8" fill="var(--warm)" stroke="none"/>
<g class="beam"><path class="metal" d="M70 70H330"/><circle cx="200" cy="70" r="6" fill="var(--bg)" class="metal"/></g>
<g class="panl" style="transform:translate(70px,70px)"><path class="metal" d="M0 0L-56 122M0 0L56 122"/><path class="pan" d="M-72 122Q0 182 72 122Z"/></g>
<g class="panr" style="transform:translate(330px,70px)"><path class="metal" d="M0 0L-56 122M0 0L56 122"/><path class="pan" d="M-72 122Q0 182 72 122Z"/></g>
</svg>
</button>
<p class="scales-cap" aria-live="polite">Tap the scales.</p>
</div>'''

# ---------------------------------------------------------------- shell

def rel(depth, path):
    """Link from a page at `depth` to a root-relative path."""
    if path == "":
        return "../" * depth if depth else "./"
    return "../" * depth + path


def head(*, depth, path, title, desc, og_type="website", noindex=False, ld=None, og_alt=None):
    p = lambda x: rel(depth, x)
    canon = BASE + "/" + path if path else BASE + "/"
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{canon}">',
    ]
    if noindex:
        tags.append('<meta name="robots" content="noindex, follow">')
    tags += [
        '<meta name="theme-color" content="#0a0f2e">',
        '<meta name="color-scheme" content="dark light">',
        f'<link rel="icon" href="{p("assets/favicon.svg")}" type="image/svg+xml">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{canon}">',
        f'<meta property="og:image" content="{BASE}/assets/og-image.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(og_alt or "Ink & Equity, advocates and legal consultants, Lucknow")}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{BASE}/assets/og-image.png">',
        f'<link rel="preload" href="{p("assets/fonts/fraunces.woff2")}" as="font" type="font/woff2" crossorigin>',
        f'<link rel="preload" href="{p("assets/fonts/instrument-sans.woff2")}" as="font" type="font/woff2" crossorigin>',
        f'<link rel="stylesheet" href="{p("css/nexus.css")}">',
        "<script>(function(){var d=document.documentElement;try{var t=localStorage.getItem('ie-theme');"
        "if(!t)t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';d.dataset.theme=t;var p=localStorage.getItem('ie-palette');if(p&&/^(noir|emerald|burgundy)$/.test(p))d.dataset.palette=p}"
        "catch(e){d.dataset.theme='dark'}d.classList.add('js')})()</script>",
    ]
    for block in ld or []:
        tags.append('<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False, separators=(",", ":")) + "</script>")
    return "\n".join(tags)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


NAV = [
    ("practice", "practice-areas.html", "Practice"),
    ("map", "map.html", "Map"),
    ("about", "about.html", "About"),
    ("insights", "insights.html", "Insights"),
    ("library", "case-library.html", "Library"),
    ("careers", "careers.html", "Careers"),
    ("contact", "contact.html", "Contact"),
]

PALETTE_OPTIONS = ('<option value="ink">Ink</option>'
    '<option value="noir">Noir</option>'
    '<option value="emerald">Emerald</option>'
    '<option value="burgundy">Burgundy</option>')


def header(depth, current):
    p = lambda x: rel(depth, x)
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{p(h)}"{cur if k == current else ""}>{t}</a>' for k, h, t in NAV
    )
    return f'''<header class="site-header"><div class="wrap bar">
<a class="logo" href="{p("")}" aria-label="{NAME}, home">{LOGO}<span><b>{NAME}</b><small>Advocates and legal consultants</small></span></a>
<nav class="nav" id="nav" aria-label="Main">{links}<label class="palette-mobile"><span>Colour theme</span><select class="palette-select" data-palette-select>{PALETTE_OPTIONS}</select></label></nav>
<label class="theme-studio"><span class="visually-hidden">Colour theme</span><select class="palette-select" data-palette-select>{PALETTE_OPTIONS}</select></label>
<button class="icon-btn" id="theme" type="button" aria-label="Switch between dark and light theme" aria-pressed="false">{MOON}{SUN}</button>
<button class="icon-btn menu-btn" id="menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{MENU}</button>
</div></header>'''


def footer(depth):
    p = lambda x: rel(depth, x)
    areas = "".join(f'<li><a href="{p("practice/" + s + ".html")}">{t}</a></li>' for s, t, _ in HOME_PRACTICE)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot">
<div><h2>{NAME}</h2>
<address class="muted" style="font-style:normal">{STREET}<br>{CITY}<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address></div>
<div><h2>Areas of practice</h2><ul>{areas}<li><a href="{p("practice-areas.html")}">All areas</a></li></ul></div>
<div><h2>The practice</h2><ul>
<li><a href="{p("about.html")}">About</a></li>
<li><a href="{p("rishabh-raj.html")}">Rishabh Raj, Advocate</a></li>
<li><a href="{p("map.html")}">Map of the areas</a></li>
<li><a href="{p("insights.html")}">Insights</a></li>
<li><a href="{p("case-library.html")}">Case library</a></li>
<li><a href="{p("careers.html")}">Careers</a></li>
<li><a href="{p("contact.html")}">Contact</a></li>
<li><a href="{p("disclaimer.html")}">Disclaimer</a></li>
<li><a href="{p("privacy.html")}">Privacy</a></li></ul></div>
</div>
<div class="maxim"><button id="maxim" type="button" aria-label="Show another legal maxim">Audi alteram partem.</button><small id="maxim-gloss" aria-live="polite">Hear the other side.</small></div>
<p class="legal">This website gives general information about the advocates and the practice. It is not an advertisement or a solicitation, and it is not legal advice. See the <a href="{p("disclaimer.html")}">disclaimer</a>. &copy; <span id="year">2026</span> {NAME}.</p>
</div></footer>'''


def shell(*, depth, path, current, title, desc, body, ld=None, og_type="website", noindex=False, og_alt=None):
    p = lambda x: rel(depth, x)
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
{head(depth=depth, path=path, title=title, desc=desc, og_type=og_type, noindex=noindex, ld=ld, og_alt=og_alt)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="lattice" aria-hidden="true"></div><div class="lattice-lit" aria-hidden="true"></div><div class="progress" aria-hidden="true"></div>
{header(depth, current)}
<main id="main">
{body}
</main>
{footer(depth)}
<div class="notice" id="notice" role="region" aria-label="Notice" hidden><p>This website is for information only. It is not an advertisement or a solicitation, and nothing on it is legal advice. <a href="{p("disclaimer.html")}">Read the disclaimer</a>.</p><button class="btn small solid" id="notice-ok" type="button">I understand</button></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{p("js/nexus.js")}" defer></script>
</body>
</html>
'''


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def write(rel_path, html):
    out = ROOT / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


PAGES = []  # (path, lastmod) for the sitemap

ORG = {"@type": "LegalService", "@id": BASE + "/#firm", "name": NAME, "alternateName": "IEQ Law", "url": BASE + "/",
       "image": BASE + "/assets/og-image.png", "telephone": PHONE_TEL, "email": EMAIL,
       "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Lucknow",
                   "addressRegion": "Uttar Pradesh", "postalCode": "226001", "addressCountry": "IN"},
       "knowsAbout": [t for _, t, _ in PRACTICE] + OTHER_AREAS}

PERSON = {"@type": "Person", "@id": BASE + "/rishabh-raj.html#person", "name": "Rishabh Raj", "jobTitle": "Advocate",
          "url": BASE + "/rishabh-raj.html", "image": BASE + "/assets/team/rishabh.webp",
          "worksFor": {"@id": BASE + "/#firm"},
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Symbiosis Law School, Noida"},
          "memberOf": [{"@type": "Organization", "name": n} for n in (
              "Oudh Bar Association", "Supreme Court Bar Association", "Central Bar Association, Lucknow")],
          "knowsAbout": ["Constitutional law", "Writ jurisdiction", "Service law", "Property law", "Cyber law"]}

# ---------------------------------------------------------------- pages

def home():
    d = 0
    p = lambda x: rel(d, x)
    rows = "".join(
        f'<li><a class="row" href="{p("practice/" + s + ".html")}"><h3>{t}</h3><p>{blurb}</p><span class="go" aria-hidden="true">Read more</span></a></li>'
        for s, t, blurb in HOME_PRACTICE)
    body = f'''<section class="hero"><div class="wrap">
<p class="site-name">{NAME}, advocates and legal consultants in Lucknow</p>
<div class="hero-grid">
<h1 class="display" data-ink>Plain law, set in ink.</h1>
<div class="hero-aside">
<p class="lede">A law practice in Lucknow. Its advocates appear in the Allahabad High Court, the Supreme Court of India and the courts of Uttar Pradesh.</p>
<div class="hero-actions"><a class="btn solid" href="{p("practice-areas.html")}">Areas of practice</a><a class="btn" href="{p("contact.html")}">Contact the chamber</a></div>
<p class="hint">The headline bleeds where you point.</p>
</div></div>
</div></section>

<section class="section reveal ways" id="ways"><div class="wrap">
<h2 class="ways-h">Three ways to look around</h2>
<div class="ways-grid">
<div><h3>Get to know the practice</h3><p>Its history, its advocates and the profile of Rishabh Raj.</p><p><a class="link" href="{p("about.html")}">About</a> <span aria-hidden="true">&middot;</span> <a class="link" href="{p("rishabh-raj.html")}">Profile</a></p></div>
<div><h3>Find a topic</h3><p>{len(PRACTICE)} areas of practice, drawn as a map that shows how they group and which forums the worked scenarios name.</p><p><a class="link" href="{p("map.html")}">Open the map</a> <span aria-hidden="true">&middot;</span> <a class="link" href="{p("practice-areas.html")}">List of areas</a></p></div>
<div><h3>Read in depth</h3><p>Worked hypothetical scenarios, and commentary on judgments.</p><p><a class="link" href="{p("case-library.html")}">Case library</a> <span aria-hidden="true">&middot;</span> <a class="link" href="{p("insights.html")}">Insights</a></p></div>
</div>
</div></section>

<section class="section reveal" id="practice"><div class="wrap">
<h2>Areas of practice</h2>
<p class="lede">Each page explains the law in plain terms: what the area covers, where matters are heard, and which papers usually matter.</p>
<ul class="index">{rows}</ul>
<p class="also">The practice covers {len(PRACTICE)} areas in total. See <a class="link" href="{p("practice-areas.html")}">all areas</a>, or read worked examples in the <a class="link" href="{p("case-library.html")}">case library</a>.</p>
</div></section>

<section class="section reveal" id="advocate"><div class="wrap founder">
<div class="arch"><img src="{p("assets/team/rishabh.webp")}" width="480" height="600" alt="Portrait of Rishabh Raj, advocate" loading="lazy" decoding="async"></div>
<div>
<h2>Rishabh Raj, Advocate</h2>
<p class="lede">Founding partner of {NAME}. Enrolled with the Bar Council of Uttar Pradesh in 2018 and practising in Lucknow.</p>
<dl class="facts">
<dt>Qualification</dt><dd>BBA.LLB, Symbiosis Law School, Noida</dd>
<dt>Bar associations</dt><dd>Oudh Bar Association; Supreme Court Bar Association; Central Bar Association, Lucknow (civil courts)</dd>
<dt>Areas of practice</dt><dd>Constitutional and writ matters, service matters, property and real estate, cyber crime</dd>
</dl>
<p style="margin-top:1.6rem"><a class="link" href="{p("rishabh-raj.html")}">Full profile</a></p>
</div></div></section>

<section class="section" id="notes"><div class="wrap feature">
<div><h2>From the notes</h2><p class="lede">Short commentary on judgments and the law, written for readers who are not lawyers.</p></div>
<div>
<h3><a class="link" href="{p("insights/pregnancy-pet-allahabad-hc.html")}">Pregnancy and public jobs: the Allahabad High Court on Komal Jaiswal v. State of U.P.</a></h3>
<p class="muted">A Division Bench of the Lucknow Bench held that a candidate who is nine months pregnant cannot be refused a postponed physical test only because the rules are silent. A reading of the judgment of 22 July 2026.</p>
</div></div></section>

<section class="section" id="contact"><div class="wrap contact-grid">
<div>
<h2>Visit the chamber</h2>
<address class="address">{STREET}<br>{CITY}<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
<p class="muted">Visits are by appointment. Please call or write before you come. <a class="link" href="{p("contact.html")}">Hours and what to bring</a>.</p>
</div>
{SCALES}
</div></section>'''
    ld = [{"@context": "https://schema.org", "@graph": [
        ORG,
        {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": NAME, "publisher": {"@id": BASE + "/#firm"}}]}]
    PAGES.append(("", MODIFIED))
    write("index.html", shell(depth=0, path="", current="", title="Ink & Equity | Rishabh Raj, Advocates, Lucknow",
        desc="Ink & Equity is a law practice in Lucknow. Read about its areas of practice, its advocates and the courts they appear in. Address and contact details.",
        body=body, ld=ld))


def about():
    d = 0
    p = lambda x: rel(d, x)
    def nm(k, n):
        return f'<a class="link" href="{p("rishabh-raj.html")}">{n}</a>' if k == "rishabh" else n
    team = "".join(
        f'<li><div class="arch"><img src="{p("assets/team/" + k + ".webp")}" width="480" height="600" alt="Portrait of {n}" loading="lazy" decoding="async"></div>'
        f'<h3>{nm(k, n)}</h3><p class="role">{r}</p><p>{a}</p></li>'
        for k, n, r, a in TEAM)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">About</p>
<h1>A practice that began as one advocate's chamber.</h1>
<p class="lede">{NAME} is a law practice in Lucknow, formerly Rishabh Raj &amp; Associates. It took its present name on 29 March 2024.</p>
</div></section>

<section class="section"><div class="wrap narrow prose">
<h2>The name</h2>
<p>Ink is the written record: the petition, the affidavit, the order. Much of litigation is decided on paper, and the practice treats drafting as the core of the work.</p>
<p>Equity is the older idea behind it: that the law should be applied with attention to what is fair in the case in front of the court.</p>
</div></section>

<section class="section"><div class="wrap narrow prose">
<h2>How the practice grew</h2>
<ol class="timeline">
<li><time>2018</time><h3>Enrolment and civil practice</h3><p>Rishabh Raj enrolled with the Bar Council of Uttar Pradesh and began practice in Lucknow in the chambers of Shri Brijesh Kumar Saxena, appearing in civil courts.</p></li>
<li><time>2021 to 2022</time><h3>Rishabh Raj &amp; Associates</h3><p>With guidance from Shri Ram Raj Singh, advocate, he set up his own practice. Work widened to constitutional, service and family matters.</p></li>
<li><time>2023 to 2024</time><h3>Vedant Bhargav joins</h3><p>Vedant Bhargav joined the practice, adding family, criminal and contract matters.</p></li>
<li><time>29 March 2024</time><h3>Ink &amp; Equity</h3><p>The practice took its present name.</p></li>
</ol>
</div></section>

<section class="section" id="team"><div class="wrap">
<h2>The advocates</h2>
<p class="lede">Seven advocates, each with their own areas of practice.</p>
<ul class="team">{team}</ul>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("About", BASE + "/about.html")])]
    PAGES.append(("about.html", MODIFIED))
    write("about.html", shell(depth=0, path="about.html", current="about", title="About Ink & Equity | Lucknow Advocates",
        desc="Ink & Equity is a law practice in Lucknow, formerly Rishabh Raj & Associates. How the practice grew, and the advocates who work in it.", body=body, ld=ld))


def rishabh():
    d = 0
    p = lambda x: rel(d, x)
    areas = "".join(f"<li>{x}</li>" for x in [
        "Constitutional and writ matters (Articles 226 and 32 of the Constitution)",
        "Service matters", "Property and real estate, including RERA", "Cyber crime and online fraud",
        "Civil and criminal matters"])
    body = f'''<section class="page-head"><div class="wrap founder">
<div class="arch"><img src="{p("assets/team/rishabh.webp")}" width="480" height="600" alt="Portrait of Rishabh Raj, advocate" decoding="async"></div>
<div>
<p class="site-name">Advocate, Lucknow</p>
<h1>Rishabh Raj</h1>
<p class="lede">Advocate and founding partner of {NAME}, practising in Lucknow since enrolling with the Bar Council of Uttar Pradesh in 2018.</p>
<dl class="facts">
<dt>Qualification</dt><dd>BBA.LLB, Symbiosis Law School, Noida</dd>
<dt>Enrolled</dt><dd>Bar Council of Uttar Pradesh, 2018</dd>
<dt>Bar associations</dt><dd>Oudh Bar Association; Supreme Court Bar Association; Central Bar Association, Lucknow (civil courts)</dd>
<dt>Courts</dt><dd>Supreme Court of India; Allahabad High Court, Lucknow Bench and Prayagraj; Delhi High Court; civil and criminal courts in Uttar Pradesh</dd>
<dt>Chamber</dt><dd>{STREET}, {CITY}</dd>
</dl>
</div></div></section>

<section class="section"><div class="wrap narrow prose">
<h2>Areas of practice</h2>
<ul>{areas}</ul>
<p>Each of the first four has a page that explains the law in plain terms: <a href="{p("practice/constitutional-and-writ.html")}">constitutional and writ matters</a>, <a href="{p("practice/service-matters.html")}">service matters</a>, <a href="{p("practice/property-and-real-estate.html")}">property and real estate</a> and <a href="{p("practice/cyber-crime-and-online-fraud.html")}">cyber crime and online fraud</a>.</p>
<h2>Background</h2>
<p>After law school at Symbiosis in Noida, Rishabh Raj worked in corporate legal roles before enrolling in 2018. He then returned to Lucknow, trained in civil practice and, in 2021 to 2022, set up Rishabh Raj &amp; Associates. The practice became {NAME} on 29 March 2024. Read the <a href="{p("about.html")}">history of the practice</a>.</p>
<div class="aside-note"><strong>A note on names.</strong> More than one advocate in India is called Rishabh Raj. This page is about the advocate who practises in Lucknow at {NAME}, {STREET}.</div>
<h2>Contact</h2>
<p><a href="tel:{PHONE_TEL}">{PHONE}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a>. <a href="{p("contact.html")}">Hours and directions</a>.</p>
</div></section>'''
    ld = [{"@context": "https://schema.org", "@graph": [
              {"@type": "ProfilePage", "url": BASE + "/rishabh-raj.html", "mainEntity": {"@id": BASE + "/rishabh-raj.html#person"}},
              PERSON]},
          crumbs([("Home", BASE + "/"), ("Rishabh Raj, Advocate", BASE + "/rishabh-raj.html")])]
    PAGES.append(("rishabh-raj.html", MODIFIED))
    write("rishabh-raj.html", shell(depth=0, path="rishabh-raj.html", current="about", title="Rishabh Raj, Advocate, Lucknow | Ink & Equity",
        desc="Rishabh Raj is an advocate in Lucknow and founding partner of Ink & Equity. Qualification, bar associations, courts and areas of practice.",
        body=body, ld=ld, og_type="profile", og_alt="Rishabh Raj, advocate, Lucknow"))


def forum_map(p):
    """Simplified map of the forums most matters pass through. Clickable; draws in on scroll."""
    def node(x, y, w, h, title, sub, href=None, cls=""):
        inner = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="fnode {cls}"/>'
                 f'<text x="{x + w/2}" y="{y + 26}" text-anchor="middle" class="ftitle">{title}</text>'
                 f'<text x="{x + w/2}" y="{y + 44}" text-anchor="middle" class="fsub">{sub}</text>')
        if href:
            return f'<a href="{href}" class="fnode-link"><title>{title}: {sub}</title>{inner}</a>'
        return f'<g><title>{title}: {sub}</title>{inner}</g>'
    sc = node(250, 20, 220, 56, "Supreme Court of India", "Article 32 writs and appeals", cls="top")
    hc = node(70, 160, 270, 56, "High Court at Allahabad", "Lucknow bench \u00b7 Article 226 writs and appeals", href=p("practice/constitutional-and-writ.html"))
    tr = node(400, 160, 270, 56, "Tribunals", "CAT, NCLT, NGT and similar bodies", href=p("practice/service-matters.html"))
    dc = node(70, 300, 270, 56, "District and civil courts", "Suits, criminal trials, first appeals", href=p("practice/criminal-law.html"))
    cm = node(400, 300, 270, 56, "Commissions and regulators", "Consumer, RERA and sector forums", href=p("practice/consumer-protection.html"))
    lines = (
        '<path class="flink" d="M205 160 L360 76" />'
        '<path class="flink" d="M405 160 L360 76" />'
        '<path class="flink dash" d="M205 216 L205 300" />'
        '<path class="flink dash" d="M535 216 L535 300" />'
        '<path class="flink dash" d="M340 188 L400 188" />'
    )
    return f"""<figure class="forum-map reveal" aria-labelledby="forum-map-title">
<figcaption id="forum-map-title"><span class="kicker">Simplified map</span>Where most matters are heard</figcaption>
<svg viewBox="0 0 720 390" role="img" aria-label="Diagram of the Supreme Court, the High Court, tribunals, district courts and commissions. Solid lines show usual routes; dashed lines show routes that depend on the statute.">
{lines}{sc}{hc}{tr}{dc}{cm}
</svg>
<p class="forum-note">Solid lines show the usual route. Dashed lines apply only where the statute allows. The right forum depends on the subject, the relief sought and the order being challenged, so check the relevant page before relying on any route.</p>
</figure>
"""


def practice_index():
    d = 0
    p = lambda x: rel(d, x)
    rows = "".join(
        f'<li><a class="row" href="{p("practice/" + s + ".html")}"><h3>{t}</h3><p>{b}</p><span class="go" aria-hidden="true">Read more</span></a></li>'
        for s, t, b in PRACTICE)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">Areas of practice</p>
<h1>What the practice handles.</h1>
<p class="lede">{len(PRACTICE)} areas have their own pages, from constitutional and writ matters to cross-border and NRI work.</p>
</div></section>
<section class="section"><div class="wrap">
{forum_map(p)}
<ul class="index">{rows}</ul>
<p class="also">Worked hypothetical scenarios for many of these areas are in the <a class="link" href="{p("case-library.html")}">case library</a>.</p>
<div class="aside-note">These pages give general information and are reviewed from time to time. The law changes, and every matter turns on its own facts. Nothing here is legal advice.</div>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Areas of practice", BASE + "/practice-areas.html")])]
    PAGES.append(("practice-areas.html", MODIFIED))
    write("practice-areas.html", shell(depth=0, path="practice-areas.html", current="practice", title="Areas of Practice | Ink & Equity",
        desc="Areas of practice at Ink & Equity, Lucknow: constitutional and writ matters, service matters, property and real estate, cyber crime and online fraud.",
        body=body, ld=ld))


# --- practice pages (content written for general readers; reviewed against statute names, not case outcomes)
PAGES_CONTENT = {
"constitutional-and-writ": dict(
    title="Writ Petitions and Constitutional Law | Ink & Equity",
    desc="A plain guide to writ petitions under Articles 226 and 32: what they cover, where they are heard, and what courts expect. Ink & Equity, Lucknow.",
    h1="Constitutional and writ matters",
    lede="Challenging action by the State in the High Court or the Supreme Court, under Articles 226 and 32 of the Constitution.",
    sections=[
        ("What this covers", """<ul>
<li>Orders, notices and inaction of government departments, local bodies and other public authorities.</li>
<li>Claims that a fundamental right has been violated, including the rights to equality (Article 14), to freedom (Article 19) and to life and personal liberty (Article 21).</li>
<li>Challenges to the validity of rules, notifications and executive orders.</li>
<li>Habeas corpus, where a person is said to be detained unlawfully.</li>
<li>Public interest litigation, where a petitioner raises a matter of wider public concern.</li>
</ul>"""),
        ("Where these matters are heard", """<p>Under Article 226, the High Court can issue writs for the enforcement of fundamental rights and for any other legal right. The Allahabad High Court sits at Prayagraj and at Lucknow, and the Lucknow Bench hears matters arising from the districts assigned to it.</p>
<p>Under Article 32, a person can go directly to the Supreme Court of India for the enforcement of fundamental rights. Appeals from High Courts, including by special leave under Article 136, also lie to the Supreme Court.</p>
<p>The five classic writs are habeas corpus, mandamus, prohibition, certiorari and quo warranto. A court can also pass any other direction that suits the case.</p>"""),
        ("What courts look at first", """<ul>
<li><strong>Alternative remedy.</strong> If the law gives an effective appeal or tribunal, the High Court may ask the petitioner to use it first. This is a rule of discretion, not an absolute bar.</li>
<li><strong>Delay.</strong> No fixed limitation period applies to a writ petition, but unexplained delay can lead a court to refuse relief.</li>
<li><strong>Who is the respondent.</strong> Writs are aimed at the State and at bodies that perform public functions. A purely private dispute is ordinarily not a matter for a writ.</li>
</ul>"""),
        ("Papers that usually matter", """<ul>
<li>The order or letter being challenged, with the date it was received.</li>
<li>Any representation already sent and any reply.</li>
<li>Documents that show the right claimed: an appointment letter, a licence, an allotment, a rule or notification.</li>
<li>A short chronology of events in date order.</li>
</ul>"""),
    ],
    faq=[
        ("Is there a fixed time limit for a writ petition?", "No fixed period is prescribed. Courts expect a petition to be filed promptly, and a long, unexplained delay can be a reason to refuse relief."),
        ("Can a writ be filed against a private company?", "Ordinarily not for a private dispute. Writs are directed at the State and at bodies that perform public functions. Whether a particular body qualifies depends on its facts."),
        ("What is the difference between Article 226 and Article 32?", "Article 32 gives a direct route to the Supreme Court for fundamental rights. Article 226 gives access to the High Court for fundamental rights and for other legal rights, so its reach is wider."),
    ]),
"service-matters": dict(
    title="Service Matters in Uttar Pradesh | Ink & Equity",
    desc="A plain guide to service disputes: promotion, seniority, discipline, pension and recruitment, and the forums that hear them. Ink & Equity, Lucknow.",
    h1="Service matters",
    lede="Disputes between employees and public employers, from recruitment and promotion to disciplinary action and pension.",
    sections=[
        ("What this covers", """<ul>
<li>Recruitment and selection: eligibility, results, and decisions of selection bodies.</li>
<li>Promotion, seniority and pay fixation.</li>
<li>Suspension, departmental inquiries and punishment.</li>
<li>Termination, removal and reinstatement.</li>
<li>Pension, gratuity, family pension and other retirement benefits.</li>
<li>Transfers and compassionate appointment.</li>
</ul>"""),
        ("Where these matters are heard", """<p>The forum depends on the employer. Many central government employees go first to the Central Administrative Tribunal, which was set up under the Administrative Tribunals Act, 1985. Other public employees usually approach the High Court under Article 226. Orders of a tribunal can be challenged in the High Court.</p>
<p>Before going to court, an employee is usually expected to use the remedies inside the department, such as an appeal or a representation.</p>"""),
        ("Time limits to keep in mind", """<p>An application to the Central Administrative Tribunal generally has to be made within one year of the final order (Section 21 of the 1985 Act). The Tribunal can condone delay for sufficient cause. For a High Court writ, no fixed period applies, but delay can still count against the petitioner.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The appointment letter and service book entries.</li>
<li>The order challenged, with proof of the date it was received.</li>
<li>For disciplinary matters: the charge sheet, the reply, the inquiry report and the punishment order.</li>
<li>For pension: the pension payment order and the service and salary records the department used.</li>
<li>Every representation sent and every reply.</li>
</ul>"""),
    ],
    faq=[
        ("Can a recruitment result be challenged?", "A candidate can approach the court where the selection rules were not followed or a decision was arbitrary. Courts generally look at the advertisement and the rules in force when the process began."),
        ("What is a departmental inquiry?", "It is the process by which an employer examines a charge of misconduct. The employee is entitled to notice of the charges and a fair chance to reply, as the applicable conduct rules require and, for civil servants, as Article 311 requires where it applies."),
        ("Does a pending representation stop the time limit?", "Not automatically. Where a representation has been made, the Tribunal's Act has its own rule on how time is counted. Anyone relying on a representation should have the dates checked early."),
    ]),
"property-and-real-estate": dict(
    title="Property and RERA Matters, Lucknow | Ink & Equity",
    desc="A plain guide to title, possession, tenancy, development authority and RERA matters in Uttar Pradesh. Ink & Equity, advocates in Lucknow.",
    h1="Property and real estate",
    lede="Title, possession, tenancy, development authority matters and disputes between buyers and builders, in Lucknow and across Uttar Pradesh.",
    sections=[
        ("What this covers", """<ul>
<li>Checking title before a purchase, and drafting and registering sale deeds, gift deeds and wills.</li>
<li>Suits for possession, partition, injunction and specific performance.</li>
<li>Tenancy and eviction, including matters under the Uttar Pradesh Urban Buildings (Regulation of Letting, Rent and Eviction) Act, 1972.</li>
<li>Disputes between home buyers and builders under the Real Estate (Regulation and Development) Act, 2016.</li>
<li>Allotment, cancellation, map sanction and demolition matters involving development authorities.</li>
<li>Revenue records and agricultural land, including proceedings before revenue courts under the Uttar Pradesh Revenue Code, 2006.</li>
</ul>"""),
        ("Where these matters are heard", """<ul>
<li>Civil courts, for title, possession, partition, injunction and specific performance.</li>
<li>The Uttar Pradesh Real Estate Regulatory Authority and its Appellate Tribunal, for registered projects.</li>
<li>Consumer commissions, for deficiency in service by a builder, under the Consumer Protection Act, 2019.</li>
<li>The High Court, by writ, for action by development authorities and other public bodies.</li>
<li>Revenue courts, for mutation and other revenue disputes.</li>
</ul>"""),
        ("Time limits to keep in mind", """<p>Under the Limitation Act, 1963, a suit for possession of immovable property based on title generally has to be filed within twelve years from when the possession of the other side became adverse. A suit for specific performance of a contract generally has to be filed within three years of the date fixed for performance, or of when the plaintiff learned that performance was refused. Which rule applies depends on the facts, so dates should be checked early.</p>"""),
        ("Two points that are often misunderstood", """<ul>
<li>A power of attorney lets someone act for the owner. It does not by itself transfer ownership. A sale of immovable property worth ₹100 or more needs a registered deed (Section 54, Transfer of Property Act, 1882), and the Supreme Court said in <em>Suraj Lamps and Industries v. State of Haryana</em> (2011) that title does not pass by a general power of attorney, an agreement to sell or a will alone.</li>
<li>Mutation in the revenue records shows who pays the land revenue or tax. It is not, on its own, proof of ownership.</li>
</ul>"""),
        ("Papers that usually matter", """<ul>
<li>The chain of title: every earlier registered deed, in order.</li>
<li>An encumbrance certificate and the revenue records (khatauni or khasra).</li>
<li>Tax receipts, the sanctioned map and any allotment letter.</li>
<li>For a flat or plot in a project: the builder-buyer agreement, the RERA registration number, payment receipts and correspondence.</li>
</ul>"""),
    ],
    faq=[
        ("Does a power of attorney transfer ownership?", "No. It authorises another person to act for the owner. Ownership of immovable property passes through a registered conveyance, such as a sale deed."),
        ("Where can a flat buyer complain about delay?", "A buyer in a registered project can complain to the Uttar Pradesh RERA. A consumer commission is another route. Which one suits a case depends on the relief sought and the facts."),
        ("Is a mutation entry proof of ownership?", "No. It records who is in the revenue records for tax purposes. Title is decided on the documents and the law."),
    ]),
"cyber-crime-and-online-fraud": dict(
    title="Cyber Crime and Online Fraud in India | Ink & Equity",
    desc="A plain guide to online fraud and cyber crime in India: what to do first, which laws apply, and where cases are heard. Ink & Equity, Lucknow.",
    h1="Cyber crime and online fraud",
    lede="Online fraud, impersonation, account takeover and other offences committed through computers and phones, from the first report to the court case.",
    sections=[
        ("What this covers", """<ul>
<li>UPI, card and net-banking fraud, including phishing and calls that ask for an OTP.</li>
<li>Fake investment schemes, job offers and online shops.</li>
<li>Identity theft and impersonation.</li>
<li>Unauthorised access to accounts and devices.</li>
<li>Online harassment, defamation and the sharing of private images.</li>
</ul>"""),
        ("What to do in the first hours", """<ol>
<li>Tell the bank or wallet provider at once, by phone and then in writing, and ask them to block the card, account or UPI handle.</li>
<li>Report the fraud on the National Cyber Crime Reporting Portal (cybercrime.gov.in) or call the helpline, 1930. Quick reports give the system a better chance to hold the money.</li>
<li>Keep the evidence: screenshots, transaction IDs and UTR numbers, phone numbers, links, emails with their full headers, and bank statements. Do not delete chats.</li>
<li>Give a written complaint to the police station or the cyber crime police station, and keep the acknowledgement number.</li>
</ol>"""),
        ("Laws that commonly apply", """<p>The Information Technology Act, 2000 covers unauthorised access and damage to computers (Section 43), identity theft (Section 66C) and cheating by personation using a computer resource (Section 66D). The Bharatiya Nyaya Sanhita, 2023 covers cheating (Section 318) and cheating by personation (Section 319). The Bharatiya Nagarik Suraksha Sanhita, 2023 governs the procedure, including how information about an offence is recorded.</p>
<p>The Reserve Bank of India's 2017 framework on unauthorised electronic banking transactions ties a customer's liability to who was at fault and how quickly the transaction was reported. The bank's current policy should be checked.</p>"""),
        ("Where these matters are heard", """<ul>
<li>The police and the Magistrate's court, for criminal proceedings.</li>
<li>The adjudicating officer under Section 46 of the Information Technology Act, for compensation claims up to ₹5 crore. Larger claims go to the civil court.</li>
<li>The banking ombudsman and consumer commissions, for disputes with banks and service providers.</li>
<li>The High Court, for bail, quashing of proceedings and writs.</li>
</ul>"""),
    ],
    faq=[
        ("How quickly should a fraud be reported?", "Immediately. Banks and the 1930 helpline can sometimes place a hold on funds if they are told quickly."),
        ("Do I need a lawyer to file a complaint?", "No. A complaint can be made on the portal or at a police station without one."),
        ("Can I get my money back?", "It depends on how fast the fraud was reported, where the money moved and the bank's policy. No outcome can be promised."),
    ]),
}


PAGES_CONTENT.update(NEW_PAGES)


def practice_pages():
    d = 1
    p = lambda x: rel(d, x)
    for slug, t, _ in PRACTICE:
        c = PAGES_CONTENT[slug]
        secs = "".join(f"<h2>{h}</h2>{b}" for h, b in c["sections"])
        faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faq"])
        others = "".join(f'<li><a href="{p("practice/" + s + ".html")}">{tt}</a></li>' for s, tt, _ in PRACTICE if s != slug)
        sc = SCEN_BY_PRACTICE.get(slug, [])
        onmap = f'<p class="onmap"><a class="link" href="{p("map.html")}#map-{slug}">See this area on the map</a></p>'
        scen = ('<h2>Illustrative scenarios</h2><p>Worked hypothetical scenarios in this area. They are general information and do not describe actual matters.</p><ul class="related">'
                + "".join(f'<li><a href="{p("library/" + x["slug"] + ".html")}">{esc(x["title"])}</a></li>' for x in sc) + "</ul>") if sc else ""
        body = f'''<section class="page-head"><div class="wrap">
<p class="site-name"><a class="link" href="{p("practice-areas.html")}">Areas of practice</a></p>
<h1>{c["h1"]}</h1>
<p class="lede">{c["lede"]}</p>
<p class="meta-line">General information, last reviewed {REVIEWED}.</p>
</div></section>
<section class="prose"><div class="wrap narrow">
{secs}
<h2>Common questions</h2>
<div class="faq">{faq}</div>
{scen}
{onmap}
<div class="aside-note">This page gives general information. It is not legal advice, the law changes, and every matter turns on its own facts. Advocates cannot solicit work, and nothing here is an invitation to instruct. Contact details are on the <a href="{p("contact.html")}">contact page</a>.</div>
<h2>Other areas</h2>
<ul class="related">{others}</ul>
</div></section>'''
        path = f"practice/{slug}.html"
        ld = [crumbs([("Home", BASE + "/"), ("Areas of practice", BASE + "/practice-areas.html"), (t, f"{BASE}/{path}")]),
              {"@context": "https://schema.org", "@type": "WebPage", "url": f"{BASE}/{path}", "name": c["h1"],
               "description": c["desc"], "dateModified": MODIFIED, "publisher": {"@id": BASE + "/#firm"}}]
        PAGES.append((path, MODIFIED))
        write(path, shell(depth=1, path=path, current="practice", title=c["title"], desc=c["desc"], body=body, ld=ld))


def article():
    d = 1
    p = lambda x: rel(d, x)
    # Body of the article, already edited for the site (no counsel names, no press roundup).
    inner = (ROOT / "tools" / "content" / "komal-jaiswal.html").read_text(encoding="utf-8").strip()
    h1 = "Pregnancy Cannot Bar a Woman from Public Employment: the Allahabad High Court in Komal Jaiswal"
    path = "insights/pregnancy-pet-allahabad-hc.html"
    body = f'''<section class="page-head"><div class="wrap narrow">
<p class="site-name"><a class="link" href="{p("insights.html")}">Insights</a></p>
<h1 style="max-width:none;font-size:clamp(2rem,5vw,3.6rem)">{h1}</h1>
<p class="meta-line">By the IEQ Editorial Team. Published 31 July 2026, updated {REVIEWED}. Constitutional and service law.</p>
</div></section>
<article class="prose"><div class="wrap narrow">
<div class="aside-note">Prepared from the judgment of 22 July 2026 in Special Appeal No. 318 of 2026. Read it for yourself: <a href="{p("assets/judgments/komal-jaiswal-v-state-of-up-spla-318-2026.pdf")}">the judgment (PDF)</a>. Quotations and dates should be checked against the judgment before anyone relies on them.</div>
{inner}
<div class="aside-note">This article is general commentary on a published judgment. It is not legal advice and not an advertisement. The law may have changed since it was written.</div>
</div></article>'''
    ld = [crumbs([("Home", BASE + "/"), ("Insights", BASE + "/insights.html"), ("Komal Jaiswal v. State of U.P.", f"{BASE}/{path}")]),
          {"@context": "https://schema.org", "@type": "Article", "headline": h1, "datePublished": "2026-07-31",
           "dateModified": MODIFIED, "author": {"@type": "Organization", "name": "IEQ Editorial Team"},
           "publisher": {"@id": BASE + "/#firm"}, "mainEntityOfPage": f"{BASE}/{path}",
           "description": "A reading of the Allahabad High Court's judgment on a pregnant candidate's request to postpone a physical efficiency test."}]
    PAGES.append((path, MODIFIED))
    write(path, shell(depth=1, path=path, current="insights", title="Komal Jaiswal v. State of U.P.: Pregnancy and Public Jobs",
        desc="A reading of the Allahabad High Court's 22 July 2026 judgment on a pregnant candidate's request to postpone a physical efficiency test for public employment.",
        body=body, ld=ld, og_type="article"))


def insights():
    d = 0
    p = lambda x: rel(d, x)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">Insights</p>
<h1>Notes on the law.</h1>
<p class="lede">Commentary on judgments, written for readers who are not lawyers.</p>
</div></section>
<section class="section"><div class="wrap">
<ul class="index"><li><a class="row" href="{p("insights/pregnancy-pet-allahabad-hc.html")}"><h3>Pregnancy and public jobs</h3><p>The Allahabad High Court on Komal Jaiswal v. State of U.P. Constitutional and service law, 31 July 2026.</p><span class="go" aria-hidden="true">Read</span></a></li></ul>
<p class="also">New notes are added as they are written. Worked hypothetical scenarios are in the <a class="link" href="{p("case-library.html")}">case library</a>.</p>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Insights", BASE + "/insights.html")])]
    PAGES.append(("insights.html", MODIFIED))
    write("insights.html", shell(depth=0, path="insights.html", current="insights", title="Insights | Ink & Equity",
        desc="Plain-language notes on judgments and the law from Ink & Equity, advocates in Lucknow.", body=body, ld=ld))


def contact():
    d = 0
    p = lambda x: rel(d, x)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">Contact</p>
<h1>The chamber, Hazratganj.</h1>
</div></section>
<section class="section"><div class="wrap contact-grid">
<div>
<address class="address">{NAME}<br>{STREET}<br>{CITY}<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
<p><a class="link" href="https://wa.me/{PHONE_TEL.lstrip("+")}" rel="noopener">WhatsApp</a> &nbsp; <a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=1+Moti+Mahal+Marg+Hazratganj+Lucknow" rel="noopener">Open in maps</a></p>
<h2 style="font-size:1.4rem;margin-top:2rem">Hours</h2>
<ul class="hours"><li><span>Monday to Friday</span><span>6:30 to 9:00 pm</span></li><li><span>Saturday</span><span>11:00 am to 1:00 pm</span></li><li><span>Sunday</span><span>11:00 am to 4:00 pm</span></li></ul>
<p class="muted" style="margin-top:1rem">Visits are by appointment. Please call or write before you come.</p>
</div>
{SCALES}
</div></section>
<section class="section"><div class="wrap">
<h2>Before a first meeting</h2>
<p class="lede">A few things make a first meeting more useful.</p>
<ol class="steps">
<li><h3>Call or write</h3><p>Say what the matter is about and, if a case is pending, the court and the next date.</p></li>
<li><h3>Gather the papers</h3><p>Orders, notices, agreements and receipts, in date order. Copies are enough.</p></li>
<li><h3>Meet the advocate</h3><p>The advocate explains the forum, the time limits and the options.</p></li>
<li><h3>Decide</h3><p>If you choose to engage the advocate, the terms are agreed in writing.</p></li>
</ol>
<div class="aside-note">Advocates in India may not solicit work. This page lists contact details for people who have chosen to get in touch. It is not an invitation to instruct, and writing to the chamber does not by itself create an advocate-client relationship.</div>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Contact", BASE + "/contact.html")]),
          {"@context": "https://schema.org", "@type": "ContactPage", "url": BASE + "/contact.html", "about": {"@id": BASE + "/#firm"}}]
    PAGES.append(("contact.html", MODIFIED))
    write("contact.html", shell(depth=0, path="contact.html", current="contact", title="Contact | Ink & Equity, Hazratganj, Lucknow",
        desc="Address, telephone, email and office hours of Ink & Equity, advocates at 1, Moti Mahal Marg, Hazratganj, Lucknow. Visits are by appointment.", body=body, ld=ld))


def careers():
    d = 0
    p = lambda x: rel(d, x)
    roles = [("Junior advocate, High Court practice", "Lucknow. Full time. Up to two years since enrolment. Writ and service matters, research and drafting."),
             ("Junior advocate, trial court practice", "Lucknow. Full time. Up to three years since enrolment. Civil and criminal matters, bail and property."),
             ("Law clerk or research associate", "Lucknow. Full time. Final-year students and recent graduates. Research and drafting across all areas."),
             ("Internship", "Lucknow. Four to eight weeks, rolling. Second year and above. Court visits, research and drafting.")]
    items = "".join(f"<li><h3>{r}</h3><p>{t}</p></li>" for r, t in roles)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">Careers</p>
<h1>Work in the chamber.</h1>
<p class="lede">{NAME} takes on junior advocates, research associates and interns in Lucknow.</p>
</div></section>
<section class="prose"><div class="wrap narrow">
<h2>Roles</h2>
<ul style="list-style:none;padding:0">{items}</ul>
<h2>How to apply</h2>
<p>Write to <a href="mailto:{EMAIL}?subject=Application%20-%20Role%20name">{EMAIL}</a> with the role in the subject line. Send a CV of up to two pages, a cover note of up to 300 words, proof of enrolment if you are enrolled, and a writing sample if you have one.</p>
<p>Every application is read. This page is about hiring only and is not an invitation to instruct.</p>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Careers", BASE + "/careers.html")])]
    PAGES.append(("careers.html", MODIFIED))
    write("careers.html", shell(depth=0, path="careers.html", current="careers", title="Careers | Ink & Equity, Lucknow",
        desc="Openings for junior advocates, research associates and interns at Ink & Equity in Lucknow, and how to apply.", body=body, ld=ld))


def disclaimer():
    body = '''<section class="page-head"><div class="wrap"><p class="site-name">Disclaimer</p><h1>Information only.</h1></div></section>
<section class="prose"><div class="wrap narrow">
<p>Under the rules of the Bar Council of India, advocates may not solicit work or advertise. This website is meant to give information about Ink &amp; Equity and its advocates. It is not an advertisement and it is not a solicitation.</p>
<ul>
<li>Nothing on this website is legal advice. Content is general and may be out of date.</li>
<li>Visiting the site, reading it or writing to the chamber does not create an advocate-client relationship.</li>
<li>No outcome is promised or implied. Past matters, where mentioned, say nothing about any other matter.</li>
<li>Links to other sites are for convenience. The advocates are not responsible for what those sites say.</li>
<li>Please take advice on your own facts before acting.</li>
</ul>
<p>Questions about this notice can be sent to the email address on the contact page.</p>
</div></section>'''
    PAGES.append(("disclaimer.html", MODIFIED))
    write("disclaimer.html", shell(depth=0, path="disclaimer.html", current="", title="Disclaimer | Ink & Equity",
        desc="Disclaimer for the Ink & Equity website: information only, not advertising or solicitation, and not legal advice.", body=body,
        ld=[crumbs([("Home", BASE + "/"), ("Disclaimer", BASE + "/disclaimer.html")])]))


def privacy():
    body = '''<section class="page-head"><div class="wrap"><p class="site-name">Privacy</p><h1>What this site keeps.</h1></div></section>
<section class="prose"><div class="wrap narrow">
<p>This site has no forms, accounts, analytics or advertising. It does not set cookies.</p>
<h2>In your browser</h2>
<p>Your browser may store two small settings on your own device: your light or dark mode, your colour theme, and whether you have dismissed the notice at the bottom of the page. They are never sent to us.</p>
<h2>On the server</h2>
<p>The site is delivered through third-party hosting. Like most hosts, they may keep standard server logs, such as IP addresses and the pages requested. We do not control those logs.</p>
<h2>If you write or call</h2>
<p>If you send an email or call the chamber, the details you give are used to reply to you and are kept confidential. Please do not send documents until an advocate has asked for them.</p>
<h2>Changes</h2>
<p>If the site starts using analytics or other tools, this page will be updated first.</p>
</div></section>'''
    PAGES.append(("privacy.html", MODIFIED))
    write("privacy.html", shell(depth=0, path="privacy.html", current="", title="Privacy | Ink & Equity",
        desc="What the Ink & Equity website stores and what it does not: no forms, analytics, advertising or cookies.", body=body,
        ld=[crumbs([("Home", BASE + "/"), ("Privacy", BASE + "/privacy.html")])]))


def not_found():
    body = '''<section class="gone"><div class="wrap">
<h1 class="display" data-ink>Not on the record.</h1>
<p class="lede">That page does not exist, or it has moved.</p>
<div class="hero-actions"><a class="btn solid" href="/">Go to the home page</a><a class="btn" href="/practice-areas.html">Areas of practice</a></div>
</div></section>'''
    # the 404 is served from any depth, so it uses root-absolute asset paths
    html = shell(depth=0, path="404.html", current="", title="Page not found | Ink & Equity",
                 desc="This page could not be found.", body=body, noindex=True)
    for a in ('href="css/', 'href="assets/', 'src="js/', 'href="about', 'href="rishabh', 'href="insights', 'href="careers', 'href="contact',
              'href="practice', 'href="disclaimer', 'href="privacy', 'href="./"'):
        html = html.replace(a, a.replace('"', '"/', 1) if a != 'href="./"' else 'href="/"')
    write("404.html", html)


# --- case library: law-report style pages for the hypothetical scenarios
SC_SECTIONS = [
    ("facts", "Hypothetical facts"), ("problem", "The practical problem"), ("issues", "Issues"),
    ("framework", "Legal framework"), ("strategy", "Possible steps, in sequence"),
    ("docs", "Documents and evidence"), ("forum", "Proceedings and forum"), ("outcomes", "How it could go"),
    ("lessons", "Misconceptions and lessons"), ("faq", "Common questions"),
    ("notcovered", "What this scenario does not cover"), ("sources", "Primary sources to consult"),
]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"]
URL_RE = re.compile(r"(https?://[^\s<>\"]+[^\s<>\".,;)])")


def rich(t):
    out, last = [], 0
    for m in URL_RE.finditer(t):
        out.append(esc(t[last:m.start()]))
        u = m.group(1)
        out.append(f'<a href="{esc(u)}" rel="noopener">{esc(u)}</a>')
        last = m.end()
    out.append(esc(t[last:]))
    return "".join(out)


def blocks_html(bl):
    out = []
    for b in bl:
        t = b["t"]
        if t == "p":
            out.append(f"<p>{rich(b['x'])}</p>")
        elif t == "h":
            out.append(f"<h3>{esc(b['x'])}</h3>")
        elif t == "ul":
            out.append("<ul>" + "".join(f"<li>{rich(i)}</li>" for i in b["items"]) + "</ul>")
        elif t == "ol":
            cls = ' class="alpha"' if b.get("alpha") else ""
            out.append(f"<ol{cls}>" + "".join(f"<li>{rich(i)}</li>" for i in b["items"]) + "</ol>")
    return "".join(out)


def case_library():
    d = 0
    p = lambda x: rel(d, x)
    areas = sorted({x["area"] for x in LIB})
    chips = '<button class="chip" type="button" data-area="" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-area="{esc(a)}" aria-pressed="false">{esc(a)}</button>' for a in areas)
    rows = "".join(
        f'<tr data-area="{esc(x["area"])}" data-text="{esc((x["title"] + " " + x["area"] + " " + x["forum"] + " " + x["question"]).lower())}">'
        f'<td class="ref">{x["ref"]}</td>'
        f'<td><a href="{p("library/" + x["slug"] + ".html")}">{esc(x["title"])}</a><small>{esc(x["question"])}</small></td>'
        f'<td>{esc(x["area"])}</td><td>{esc(x["forum"])}</td></tr>' for x in LIB)
    body = f'''<section class="page-head"><div class="wrap">
<p class="site-name">Case library</p>
<h1>Worked scenarios in Indian law.</h1>
<p class="lede">{len(LIB)} hypothetical scenarios. Each sets out the facts, the issues, the legal framework, the steps in sequence, the forums, and how the matter could go.</p>
<p class="meta-line">General information, prepared {SCEN_DATE_HUMAN}. Scenarios are grouped by area of practice and carry a reference number.</p>
</div></section>
<section class="section"><div class="wrap">
<div class="notice-box" role="note"><strong>Illustrative scenarios.</strong> {esc(SCEN_NOTICE)}</div>
<div class="lib-tools"><label class="sr" for="lib-q">Search the library</label><input id="lib-q" type="search" placeholder="Search, for example bail, GST or RERA" autocomplete="off"><span id="lib-count" class="muted" aria-live="polite"></span></div>
<div class="chips" role="group" aria-label="Filter by area of practice">{chips}</div>
<table class="lib"><thead><tr><th scope="col">Ref.</th><th scope="col">Scenario</th><th scope="col">Area</th><th scope="col">Forum</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Case library", BASE + "/case-library.html")]),
          {"@context": "https://schema.org", "@type": "CollectionPage", "url": BASE + "/case-library.html", "name": "Case library",
           "dateModified": SCEN_DATE,
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/library/{x['slug']}.html", "name": x["title"]}
               for i, x in enumerate(LIB)]}}]
    PAGES.append(("case-library.html", SCEN_DATE))
    write("case-library.html", shell(depth=0, path="case-library.html", current="library",
          title="Case Library | Ink & Equity",
          desc="Worked hypothetical scenarios in Indian law from Ink & Equity, Lucknow: facts, issues, framework, steps, forums and outcomes. General information only.",
          body=body, ld=ld))


def library_pages():
    d = 1
    p = lambda x: rel(d, x)
    for x in LIB:
        path = f"library/{x['slug']}.html"
        sec = x["sections"]
        present = [(k, h) for k, h in SC_SECTIONS if sec.get(k)]
        toc = "".join(f'<li><a href="#{k}">{h}</a></li>' for k, h in present)
        parts = []
        for n, (k, h) in enumerate(present):
            if k == "faq":
                inner = '<div class="faq">' + "".join(
                    f"<details><summary>{rich(q)}</summary><p>{rich(a)}</p></details>" for q, a in sec[k]) + "</div>"
            else:
                inner = blocks_html(sec[k])
            parts.append(f'<h2 id="{k}"><span class="no">{ROMAN[n]}</span>{h}</h2>{inner}')
        same = [y for y in LIB if y["practice"] == x["practice"] and y is not x]
        more = ('<h2>More in this area</h2><ul class="related">' + "".join(
            f'<li><a href="{p("library/" + y["slug"] + ".html")}">{esc(y["title"])}</a></li>' for y in same) + "</ul>") if same else ""
        ptitle = next((t for s_, t, _ in PRACTICE if s_ == x["practice"]), "")
        plink = f'<li><a href="{p("practice/" + x["practice"] + ".html")}">{esc(ptitle)}: area overview</a></li>' if ptitle else ""
        mlink = f'<li><a href="{p("map.html")}#map-{x["practice"]}">See this area on the map</a></li>'
        cite = [("Ref.", x["ref"]), ("Type", "Illustrative scenario"), ("Area", x["area"]), ("Jurisdiction", x["jurisdiction"]),
                ("Forum", x["forum"]), ("Audience", x["audience"]), ("Prepared", SCEN_DATE_HUMAN), ("Status", SCEN_STATUS)]
        cite_html = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in cite if b)
        body = f'''<section class="page-head report-head"><div class="wrap">
<p class="site-name"><a class="link" href="{p("case-library.html")}">Case library</a> &middot; {esc(x["area"])}</p>
<h1>{esc(x["title"])}</h1>
<p class="lede">{esc(x["question"])}</p>
<dl class="cite">{cite_html}</dl>
</div></section>
<section class="prose report"><div class="wrap rpt">
<nav class="toc" aria-label="On this page"><p class="toc-h">Contents</p><ol>{toc}</ol></nav>
<article class="rpt-body">
<div class="notice-box" role="note"><strong>Illustrative scenario.</strong> {esc(SCEN_NOTICE)}</div>
{"".join(parts)}
<h2>Related</h2>
<ul class="related">{plink}{mlink}<li><a href="{p("case-library.html")}">Back to the case library</a></li></ul>
{more}
<div class="aside-note">This page gives general information. It is not legal advice, the law changes, and every matter turns on its own facts. Contact details are on the <a href="{p("contact.html")}">contact page</a>.</div>
</article></div></section>'''
        ld = [crumbs([("Home", BASE + "/"), ("Case library", BASE + "/case-library.html"), (x["title"], f"{BASE}/{path}")]),
              {"@context": "https://schema.org", "@type": "Article", "headline": x["title"], "url": f"{BASE}/{path}",
               "description": x["meta_desc"], "dateModified": SCEN_DATE, "inLanguage": "en-IN",
               "isPartOf": {"@type": "CollectionPage", "url": BASE + "/case-library.html"}}]
        PAGES.append((path, SCEN_DATE))
        write(path, shell(depth=1, path=path, current="library", title=x["meta_title"], desc=x["meta_desc"],
                          body=body, ld=ld, og_type="article"))


def map_page():
    """The thread map: areas of practice, their worked scenarios and the forums those scenarios name."""
    d = 0
    p = lambda x: rel(d, x)
    m = mapdata.render(PRACTICE, LIB, p)
    body = f'''<section class="page-head map-head"><div class="wrap map-head-grid">
<div><p class="site-name">Map of the areas of practice</p>
<h1>How the areas connect.</h1></div>
<div class="map-head-aside"><p class="lede">{m["n_areas"]} areas in {m["n_fams"]} families. Each small bead is a worked, hypothetical scenario from the case library. Choose a forum to see which areas name it.</p>
<p class="meta-line">General information, prepared {SCEN_DATE_HUMAN}.</p></div>
</div></section>
<section class="map-stage" aria-labelledby="map-h"><div class="wrap">
<h2 class="sr" id="map-h">The map</h2>
<div class="map-grid">
<figure class="map" id="map">{m["svg"]}<div class="map-tip" id="map-tip" hidden></div>
<figcaption>Each diamond is an area of practice, grouped into families around the centre. Filled diamonds have a worked scenario, shown as a bead. Hollow ones do not yet. The list below the map holds the same information as text.</figcaption></figure>
<div class="map-side">
<div class="map-filter" id="map-filter" hidden><p class="map-filter-h" id="map-filter-h">Forum named in a scenario</p><div class="chips" role="group" aria-labelledby="map-filter-h">{m["chips"]}</div></div>
<p class="map-status" id="map-status" role="status" aria-live="polite"></p>
<aside class="map-read" id="map-read" aria-label="Selected area" hidden></aside>
</div>
</div>
<div class="aside-note">The map shows how the pages of this website relate to one another. A forum appears on it only because a hypothetical scenario names it. It does not show where the advocates appear, and it is not legal advice.</div>
</div></section>
<section class="section" id="list"><div class="wrap">
<h2>All areas, as a list</h2>
<p class="lede">Grouped by family, with the scenarios and forums for each area.</p>
<div class="map-list">{m["list"]}</div>
</div></section>'''
    ld = [crumbs([("Home", BASE + "/"), ("Map of the areas of practice", BASE + "/map.html")]),
          {"@context": "https://schema.org", "@type": "WebPage", "url": BASE + "/map.html", "name": "Map of the areas of practice",
           "dateModified": SCEN_DATE, "publisher": {"@id": BASE + "/#firm"}}]
    PAGES.append(("map.html", SCEN_DATE))
    write("map.html", shell(depth=0, path="map.html", current="map", title="Map of the Areas of Practice | Ink & Equity",
        desc=f"An interactive map of the {m['n_areas']} areas of practice at Ink & Equity, Lucknow, with worked hypothetical scenarios and the forums they name. General information.",
        body=body, ld=ld))


def sitemap_and_robots():
    urls = "\n".join(
        f"  <url><loc>{BASE}/{path}</loc><lastmod>{mod}</lastmod></url>" for path, mod in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


if __name__ == "__main__":
    home(); about(); rishabh(); practice_index(); practice_pages(); article(); insights(); case_library(); library_pages(); map_page(); contact(); careers()
    disclaimer(); privacy(); not_found(); sitemap_and_robots()
    print(f"built {len(PAGES)} indexable pages + 404")

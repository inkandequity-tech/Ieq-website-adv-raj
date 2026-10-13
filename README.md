# aequitas-nexus

The website of Ink & Equity, advocates and legal consultants, Lucknow: <https://ieqlaw.com>.

A static site with no build step to deploy and no runtime dependencies. Plain HTML, one stylesheet, one script.

## Structure

```
index.html, about.html, rishabh-raj.html, practice-areas.html,
insights.html, contact.html, careers.html, disclaimer.html, privacy.html, 404.html
practice/      four area pages
insights/      long-form commentary
css/nexus.css  the whole design system
js/nexus.js    enhancement only; the site reads fine with it off
assets/        fonts (self-hosted), team portraits (WebP), favicon, share image, judgment PDF
tools/         build.py, lint.py, make_og.py, content/
robots.txt, sitemap.xml, CNAME, .nojekyll
```

## Editing

Page text lives in `tools/build.py`; the long article lives in `tools/content/komal-jaiswal.html`.

```
python3 tools/build.py   # regenerates every page, sitemap.xml and robots.txt
python3 tools/lint.py    # title/description length, canonicals, JSON-LD, links, wording, enrolment-number scan
```

Commit the generated pages. `tools/make_og.py` redraws `assets/og-image.png` (needs Pillow and static instances of the two fonts).

## Deploying

GitHub Pages, branch `main`, root folder. `CNAME` holds `ieqlaw.com`.
Only one repository should have Pages enabled for that domain at a time. Disable it on the old repository before enabling it here.

## Design

Indigo ink and vellum, with lapis and zafran accents; light and dark themes. Fraunces (variable) for display, Instrument Sans for text.
Motifs come from Lucknow: a chikan-thread lattice that the pointer lights up, and Nawabi arches for portraits.

Quirks, all optional and all off under `prefers-reduced-motion`:
- the headline bleeds ink around the pointer (and once, by itself, on touch screens);
- the theme toggle spills ink from the button (View Transitions API);
- tap the scales on the home and contact pages;
- tap the maxim in the footer;
- Konami code, or tap the logo five times;
- the tab title changes when you switch away.

## SEO

- One canonical per page, `https://ieqlaw.com/...`; the home page is `/`.
- `LegalService`, `Person`/`ProfilePage`, `Article` and `BreadcrumbList` JSON-LD. No review or rating markup.
- `404.html` is `noindex`; every other page is in `sitemap.xml`.
- Content is in the HTML, not injected by script.

## Professional conduct (Bar Council of India, Rule 36 and its 2008 proviso)

The site keeps to information about the advocates and the practice: name, address, contact details, qualification, areas of practice, bar associations.
It contains no testimonials, ratings, outcome claims, comparative or superlative wording, named clients, case boards, contact forms or fee offers.
`tools/lint.py` fails the build if banned wording appears. The Bar enrolment ID is deliberately not published anywhere; the lint fails if an ID-like pattern appears.
This is a working checklist, not legal advice. Have the final text reviewed against the current Rule 36 and any State Bar Council circulars.

## Licences

Code: the owner's. Fonts: Fraunces and Instrument Sans, SIL Open Font License 1.1 (texts in `assets/fonts/`).

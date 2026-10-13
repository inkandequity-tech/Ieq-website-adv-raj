# Ink & Equity website (Nexus design)

The public website of **Ink & Equity**, advocates and legal consultants at 1, Moti Mahal Marg, Hazratganj, Lucknow (formerly Rishabh Raj & Associates), served at <https://ieqlaw.com>.

This repository is a ground-up rebuild of the earlier `v5-ink-and-equity-website`. It keeps that site's facts (address, hours, team, history) but replaces its design, code, structure and wording. Where everything came from is listed in [PROVENANCE.md](PROVENANCE.md).

---

## 1. What the site is for

1. Give a visitor who searches for the practice, or for Rishabh Raj, Advocate, Lucknow, an accurate page with address, telephone, email and hours.
2. Explain 26 areas of practice in plain language: what each covers, where matters are heard, which time limits and papers matter.
3. Offer a **case library** of 28 labelled, hypothetical scenarios that show how a legal problem is analysed (facts, issues, framework, steps, forums, outcomes). They are general information, not accounts of real matters.
4. Publish occasional commentary on judgments (one article so far).
5. Do all of that within the Bar Council of India's limits on advocates' websites (see section 8).

It is a **static site**. There is no database, no form handler, no analytics and no cookies.

## 2. Pages

| URL | Purpose | Indexed |
|---|---|---|
| `/` | Home: headline, areas of practice, profile of Rishabh Raj, latest note, address and the scales toy | yes |
| `/about.html` | Name, history of the practice (timeline), the seven advocates | yes |
| `/rishabh-raj.html` | Profile page for name searches: qualification, enrolment year, bar associations, courts, areas of practice, a note separating him from other advocates of the same name | yes |
| `/practice-areas.html` | Index of all areas of practice | yes |
| `/practice/<slug>.html` (26 pages) | One page per area: what it covers, forums, papers, time limits, FAQ, links to related scenarios. The original four are constitutional and writ, service matters, property and real estate, and cyber crime and online fraud; 22 more were added from the practice-area taxonomy | yes |
| `/case-library.html` | Index of the 28 hypothetical scenarios: search box, filter by area, reference numbers CL-01 to CL-28 | yes |
| `/library/<slug>.html` (28 pages) | One scenario each, in a law-report layout (see section 3a) | yes |
| `/insights.html`, `/insights/pregnancy-pet-allahabad-hc.html` | Commentary index and the Komal Jaiswal article | yes |
| `/contact.html` | Address, telephone, email, WhatsApp, hours, what to bring | yes |
| `/careers.html` | Roles and how to apply (hiring only) | yes |
| `/disclaimer.html`, `/privacy.html` | Information-only notice; what the site stores | yes |
| `/404.html` | Not-found page | no (`noindex`) |

## 3. Repository layout

```
.
├── index.html … privacy.html, 404.html   generated pages (committed)
├── practice/                             26 area pages (generated)
├── library/                              28 scenario pages (generated)
├── case-library.html                     scenario index (generated)
├── insights/                             article (generated from tools/content)
├── css/nexus.css                         the entire design system (about 24 KB)
├── js/nexus.js                           all behaviour, including the library filter; progressive enhancement only
├── assets/
│   ├── fonts/                            Fraunces + Instrument Sans (WOFF2) and their OFL texts
│   ├── team/                             seven portraits, WebP, 480x600
│   ├── judgments/                        the judgment PDF the article is based on
│   ├── favicon.svg, og-image.png         icon and 1200x630 share image
├── .github/workflows/pages.yml           lint, then deploy to GitHub Pages on push to main
├── tools/
│   ├── build.py                          page generator (site copy, library renderer)
│   ├── practice_content.py               copy for the 22 added practice pages (NEW_PRACTICE, NEW_PAGES)
│   ├── lint.py                           SEO, conduct and link checks
│   ├── make_og.py                        redraws the share image
│   └── content/
│       ├── komal-jaiswal.html            article body, already edited
│       └── scenarios.json               the case-library scenarios and the mandatory notice
├── robots.txt, sitemap.xml               generated
├── CNAME                                 ieqlaw.com
├── .nojekyll                             serve files as they are
├── README.md, PROVENANCE.md
```

### 3a. The case library

Source: `tools/content/scenarios.json`, shaped as `{"notice": "...", "scenarios": [...]}`. `build.py` renders it; do not edit the generated `library/` pages.

Each scenario has `key`, `slug`, `title`, `meta_title`, `meta_desc`, `area`, `practice` (slug of the related practice page), `forum`, `jurisdiction`, `audience`, `question`, `publish` and `sections`. `sections` holds lists of blocks (`{"t":"p"}`, `"ul"`, `"ol"`, `"h"`) under these keys, shown in this order with Roman numerals: `facts`, `problem`, `issues`, `framework`, `strategy`, `docs`, `forum`, `outcomes`, `lessons`, `faq` (list of `[question, answer]`), `notcovered`, `sources`. Empty sections are skipped.

Rules the library follows:

- **Every scenario page and the index carry the notice** from `scenarios.json`: hypothetical, not an actual client matter, no guaranteed outcome, not legal advice. Never remove it, and never attribute a scenario to the firm, an advocate or a client.
- **Status.** Each page shows the status in `SCEN_STATUS` (currently "Draft for general information"). The source drafts were marked not approved for publication, so change this label only after an advocate has reviewed the page.
- **`publish: false`** keeps a scenario out of the build. CL numbering is assigned in file order among published scenarios, so adding or hiding one renumbers the rest.
- B4-10 (a complaint about an advocate's conduct) is held back with `publish: false` pending a professional-conduct review.
- Pages carry `Article` and `BreadcrumbList` JSON-LD with no author; the index uses `CollectionPage` and `ItemList`.
- Each practice page lists the scenarios mapped to it through `practice`.
- Adding a scenario: append to `scenarios.json`, rebuild, lint. Bump `SCEN_DATE` and `SCEN_DATE_HUMAN` in `build.py` when scenario content changes.

## 4. Working on it

```bash
python3 tools/build.py    # regenerate every page, sitemap.xml and robots.txt
python3 tools/lint.py     # must print OK before you commit
python3 -m http.server 8000   # preview at http://localhost:8000
```

- Change wording, team, address or hours at the top of `tools/build.py`, then rebuild. Do not hand-edit generated pages; the next build overwrites them.
- Add an area page by adding a row to `NEW_PRACTICE` and an entry to `NEW_PAGES` in `tools/practice_content.py` (the original four live in `PRACTICE` and `PAGES_CONTENT` in `build.py`).
- Add an article by writing its body to `tools/content/` and adding a function like `article()`.
- Bump `MODIFIED` and `REVIEWED` in `build.py` when content changes, so `lastmod` and the "last reviewed" lines stay honest. Scenario pages use `SCEN_DATE` instead.
- Workflow: branch, change, build, lint, open a pull request. Merging to `main` deploys.
- Needs only Python 3.9+ for the build. Pillow is needed only for `make_og.py`.

## 5. Design

**Concept.** Lucknow craft, set in ink: *chikan* thread-work and *Nawabi* arches, in an indigo-ink and vellum palette.

| Token | Dark | Light |
|---|---|---|
| Background | `#0a0f2e` ink | `#eef1f8` |
| Text | `#f1ead9` vellum | `#0a0f2e` |
| Accent | `#7a93ff` lapis | `#2a3fd0` |
| Warm | `#ffb454` zafran | `#9a5800` |

- **Type.** Fraunces (variable: weight, optical size, SOFT, WONK) for headings; Instrument Sans for text. Both self-hosted, no third-party font requests.
- **Layout.** Left-aligned, 62-character text measure, one wide index list instead of card grids. Numbers appear only where content is a real sequence (steps before a first meeting; the practice timeline).
- **Themes.** Follows the system setting, remembered after a toggle.
- **Accessibility.** Skip link, visible focus, `aria-current`, reduced-motion support, semantic landmarks, alt text on portraits, content readable with JavaScript off.

**Case library layout.** Citation bar (Ref., Type, Area, Jurisdiction, Forum, Audience, Prepared, Status), a notice box, a sticky contents column, Roman-numbered sections and a 74-character text measure. On screens under 860 px the contents column folds above the text and the index table stacks into rows.

### Motion and quirks (all optional, all off under reduced motion)

| Where | What happens |
|---|---|
| Home headline | Letters fade in from ink; the pointer then makes nearby letters bleed (stroke, glow, softer shapes). Letter widths are pinned so nothing reflows. On touch screens a pen sweeps across once. |
| Background | A stitched lattice; the area around the pointer is lit. |
| Theme button | Ink spills outward from the button (View Transitions API; falls back to an instant switch). |
| Portraits | Arch shapes that open upward as they scroll into view; colour returns on hover. |
| Index rows | A stitched underline draws in; the title softens. |
| Scales (home, contact) | Tap to drop weights; the beam tilts with physics-like easing and turns gold when balanced. |
| Footer | Tap the Latin maxim: it types out the next one with its translation. |
| Anywhere | Konami code, or five taps on the logo, rains § symbols. |
| Tab | Title changes to "Court is in recess" when you switch away. |
| Console | A short greeting for people reading the source. |

## 6. SEO

- Canonical on every page, `https://ieqlaw.com/…`; the home page is `/`. Internal links to the home page use `/`, never `/index.html`.
- Titles are 62 characters or fewer (counted as served, so `&` counts as `&amp;`), descriptions 160 or fewer (enforced by lint). One `h1` per page.
- Open Graph and Twitter tags with a 1200x630 image.
- JSON-LD: `LegalService` and `WebSite` (home), `Person` + `ProfilePage` (profile), `Article` (commentary), `ContactPage`, `WebPage` (practice pages), `CollectionPage` + `ItemList` (case library index), `Article` (scenario pages), and `BreadcrumbList` on inner pages. No review, rating or offer markup.
- `sitemap.xml` lists the 65 indexable pages with `lastmod` (practice and library pages included); `robots.txt` allows all and points to it.
- Everything is in the served HTML (no content injected by script). Fonts are preloaded; images have width and height set.
- Not done here, to do after launch: add the site in Google Search Console and Bing Webmaster Tools, submit the sitemap, check the Google Business Profile matches the address and hours, and measure real page speed.

## 7. Deploying

GitHub Pages, deployed by `.github/workflows/pages.yml`: every push to `main` runs `python3 tools/lint.py`, and the deploy stops if lint fails. The whole repository directory is published, so everything under `tools/` (including `scenarios.json`) is publicly reachable; keep nothing private there. The `CNAME` file holds `ieqlaw.com`. Only one repository may be serving that domain at a time, so switch Pages off on the old repository first. Keep "Enforce HTTPS" on.

## 8. Professional conduct (Bar Council of India)

Advocates in India may not advertise or solicit work (Rule 36 of the BCI Rules, and the 2008 proviso that lets an advocate's website give limited information). The site is built to stay inside that:

- It states name, address, telephone, email, qualification, enrolment year, areas of practice and bar associations.
- It has **no** testimonials, ratings, outcome or "win" claims, comparative or superlative wording, named clients, case boards, fee offers, booking forms or "hire us" calls to action.
- The case library is labelled as hypothetical on every page. It contains no real clients, no results and no claim that the practice handled any matter.
- Each practice page and the contact page say they are information and not an invitation to instruct.
- The Bar enrolment ID is deliberately not published anywhere. `tools/lint.py` fails the build if an ID-like pattern appears, and also fails on banned promotional words.
- The profile lists courts the advocate appears in. That item is not one of the fields the rule is generally read as allowing; have it confirmed or remove it.

The rule text was checked through secondary sources only. This is a working checklist and not legal advice. Have the final text reviewed against the current rule and any State Bar Council circulars.

## 9. Content that needs a human check before relying on it

- The practice pages are plain-language summaries written for this site from the statutes and well-known decisions they name. A practising advocate should read them for accuracy. They carry a "last reviewed" date.
- The Komal Jaiswal article was carried over from the earlier site and edited. It has not been checked line by line against the judgment PDF. The page says so.
- The 22 practice pages added from the taxonomy were published on the owner's confirmation that the practice undertakes these areas. They still need a read-through by an advocate. Foreign-law, tax and cross-border pages in particular should be checked by the right professional.
- The 28 library scenarios are drafts. Their source files were marked not approved for publication, and inline verification flags were removed during import. Statutory references, thresholds and limitation periods need checking against primary sources before the status label is changed. GST, FEMA, environmental and insurance scenarios need specialist review.
- The four original practice areas follow what the old site listed; they were not re-confirmed.

## 10. Privacy

No forms, accounts, analytics, advertising or cookies. The browser stores two settings locally (theme and "notice dismissed"). Hosting may keep standard server logs. If analytics is ever added, update `privacy.html` first.

## 11. Credits and licences

- Design, code and copy: written for this repository.
- Fonts: **Fraunces** (Undercase Type) and **Instrument Sans** (Instrument), SIL Open Font License 1.1, delivered via the `@fontsource-variable` packages. Licence texts are in `assets/fonts/`.
- Portraits belong to the individuals shown and the practice.
- The judgment PDF is a public court document.

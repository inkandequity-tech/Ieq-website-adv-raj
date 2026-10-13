# Provenance: where this site came from

Last updated 13 October 2026.

## Source repository

| | |
|---|---|
| Repository | <https://github.com/ieraHQ/v5-ink-and-equity-website> (public) |
| Commit used | `e21fb12` (last push 31 July 2026) |
| What it was | The "v5" site: static HTML with `css/base.css`, `components.css`, `layouts.css`, `variables.css`, `js/global.js`, `forms.js`, a courts/eCourts search tool and a browser game. |
| Where it was staged | `https://inkandequity-tech.github.io/v5-ink-and-equity-website` (the old canonical and Open Graph URLs pointed here instead of `ieqlaw.com`). |
| Live domain | `ieqlaw.com` via the `CNAME` file. |

That snapshot is the first commit of this repository's history (`d4932f4`, "Baseline"). Everything described below can be compared against it with `git diff d4932f4 HEAD`.

## What was kept, and in what form

| Item | From the source | In this repository |
|---|---|---|
| Name, address, telephone, email | footer and contact page | same details, rebuilt in `tools/build.py` |
| Office hours | contact page | same hours; "by appointment" kept |
| Practice history | `about.html` timeline | shortened to enrolment (2018), Rishabh Raj & Associates (2021-22), Vedant Bhargav joins (2023-24), renamed 29 March 2024 |
| Team and roles | `about.html` | seven advocates, names and roles kept; descriptions shortened to areas of practice |
| Portraits | `assets/team/*.jpg/png` (up to 2 MB each) | resized to 480x600 WebP (10-15 KB each) |
| Rishabh Raj's details | `about.html` | BBA.LLB, Symbiosis Law School, Noida; enrolled with the Bar Council of Uttar Pradesh in 2018; the three bar associations were supplied by him in this session |
| Komal Jaiswal article | `insights/pregnancy-pet-allahabad-hc.html` | body kept in `tools/content/komal-jaiswal.html` after edits (below) |
| Judgment PDF | `assets/judgments/komal-jaiswal-v-state-of-up-spla-318-2026.pdf` | unchanged |
| `CNAME` | `ieqlaw.com` | unchanged |
| Technical fixes | commit `85b46a2` on top of the baseline | canonicals, `robots.txt`, `sitemap.xml`, removal of the staging host |

## What was removed, and why

| Removed | Reason |
|---|---|
| Testimonial-style and "formidable", "most", "pioneered", "consistent success" wording | not permitted promotional claims for advocates |
| Named client and government-body lists | client confidentiality and promotion |
| Free-first-consultation offer, "Book Consultation" buttons, booking and application forms, WhatsApp floating button | solicitation, and forms that collected personal data without a privacy basis |
| Court boards and the eCourts search tool, the "Law Empire" game | not suitable for a conduct-compliant site; they relied on placeholder data. Still available in the baseline commit |
| In the article: counsel names (both sides), the "About Ink & Equity" paragraph, the press-coverage section, the timeline line about newspapers | would attribute the firm to a reported case and rely on unverified media claims |
| Claim that practice began in 2017 | the advocate enrolled in 2018 |
| Two clerks' portraits and biographies | not needed to describe the advocates' practice |
| The `docs/` folder of internal session notes | not for public serving |
| Old CSS and JavaScript | replaced by `css/nexus.css` and `js/nexus.js` |

## What is new (not copied from anywhere)

- All visual design, layout, animation and the interactive details (lattice, ink-bleed headline, arches, scales, maxims).
- The profile page, four practice pages, disclaimer and privacy pages, the 404 page, the contact "before a first meeting" steps.
- Practice-page text: written for this site as general summaries of the Constitution of India, the Administrative Tribunals Act 1985, the Transfer of Property Act 1882, the Limitation Act 1963, RERA 2016, the Information Technology Act 2000, the Bharatiya Nyaya Sanhita 2023 and the Bharatiya Nagarik Suraksha Sanhita 2023, and the Supreme Court decision in *Suraj Lamps and Industries v. State of Haryana* (2011). No text was copied from other law-firm sites or from statute commentaries.
- Build and lint tooling in `tools/`.
- The favicon and share image, drawn with Pillow from the shipped fonts.

## Third-party material

- Fonts: Fraunces and Instrument Sans, SIL OFL 1.1, from the `@fontsource-variable` npm packages.
- No stock photography, icon packs, JavaScript libraries or tracking scripts.

## Supplied by the owner in this session

- The repository to start from, and instructions to keep the Bar enrolment ID off the site.
- The bar associations (Oudh Bar Association, Supreme Court Bar Association, Central Bar Association Lucknow, civil courts).
- A clarification that other advocates share his name, which is why the profile page includes a neutral note about it.

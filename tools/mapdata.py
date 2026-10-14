"""Data and markup for map.html (the thread map).

Everything on the map comes from content that already exists on the site:
the area pages (PRACTICE), the hypothetical scenarios (LIB) and the editorial grouping in
tools/content/map.json. Nothing here is typed by hand per area, so the map cannot drift
from the pages it links to. build.py fails if a scenario forum label or an area is not covered.
"""
import json, math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
CFG = json.loads((HERE / "content" / "map.json").read_text(encoding="utf-8"))

W = 800                 # square viewBox
C = W / 2
R_HUB, R_AREA, R_BEAD, R_ARC, R_LAB = 118, 262, 300, 232, 350
GAP_DEG = 7.0
LAB_HALF = 42   # degrees of arc each side of a family's middle that its name may use


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def pt(r, deg):
    a = math.radians(deg)
    return round(C + r * math.cos(a), 1), round(C + r * math.sin(a), 1)


def collect(practice, lib):
    """Validate the editorial config against the live content and return the model."""
    slugs = [s for s, _, _ in practice]
    placed = [a for f in CFG["families"] for a in f["areas"]]
    missing = [s for s in slugs if s not in placed]
    extra = [a for a in placed if a not in slugs]
    dupes = sorted({a for a in placed if placed.count(a) > 1})
    if missing or extra or dupes:
        raise SystemExit(f"map.json does not match the area pages: missing={missing} unknown={extra} duplicated={dupes}")
    fmap = CFG["forum_map"]
    unmapped = sorted({x["forum"] for x in lib if x["forum"] not in fmap})
    if unmapped:
        raise SystemExit(f"map.json forum_map has no entry for scenario forum label(s): {unmapped}")
    known = {f["id"] for f in CFG["forums"]}
    bad = sorted({i for v in fmap.values() for i in v if i not in known})
    if bad:
        raise SystemExit(f"map.json forum_map uses unknown forum id(s): {bad}")

    info = {s: {"slug": s, "title": t, "blurb": b, "scen": [], "forums": []} for s, t, b in practice}
    for x in lib:
        a = info[x["practice"]]
        a["scen"].append(x)
        for fid in fmap[x["forum"]]:
            if fid not in a["forums"]:
                a["forums"].append(fid)
    order = [f["id"] for f in CFG["forums"]]
    for a in info.values():
        a["forums"].sort(key=order.index)
    return info


def layout(info):
    """Deterministic polar layout: one sector per family, sized by its number of areas."""
    fams = CFG["families"]
    total = sum(len(f["areas"]) for f in fams)
    step = (360 - GAP_DEG * len(fams)) / total
    ang = -90.0
    out = []
    for f in fams:
        ang += GAP_DEG / 2
        span = step * len(f["areas"])
        areas = []
        for i, slug in enumerate(f["areas"]):
            areas.append((slug, ang + step * (i + 0.5)))
        out.append({"id": f["id"], "label": f["label"], "mid": ang + span / 2, "a0": ang + 1.2, "a1": ang + span - 1.2, "areas": areas})
        ang += span + GAP_DEG / 2
    return out


def svg(info, fams, forum_label):
    s = []
    a = s.append
    a(f'<svg viewBox="0 0 {W} {W}" aria-hidden="true" focusable="false" id="map-svg">')
    # orbits
    a(f'<circle class="m-orbit" cx="{C}" cy="{C}" r="{R_HUB}"/>'
      f'<circle class="m-orbit" cx="{C}" cy="{C}" r="{R_AREA}"/>')
    # family arcs (under the points) and curved family names (outside the beads)
    for f in fams:
        x0, y0 = pt(R_ARC, f["a0"]); x1, y1 = pt(R_ARC, f["a1"])
        a(f'<path class="m-arc" data-family="{f["id"]}" d="M{x0} {y0}A{R_ARC} {R_ARC} 0 0 1 {x1} {y1}"/>')
    defs = []
    for f in fams:
        top = math.sin(math.radians(f["mid"])) < 0
        r = R_LAB if top else R_LAB + 11           # bottom names read from the inside out, so sit a little further out
        x0, y0 = pt(r, f["mid"] - LAB_HALF); x1, y1 = pt(r, f["mid"] + LAB_HALF)
        d = f"M{x0} {y0}A{r} {r} 0 0 1 {x1} {y1}" if top else f"M{x1} {y1}A{r} {r} 0 0 0 {x0} {y0}"
        defs.append(f'<path id="fl-{f["id"]}" d="{d}"/>')
    a("<defs>" + "".join(defs) + "</defs>")
    for f in fams:
        a(f'<text class="m-flab" data-family="{f["id"]}"><textPath href="#fl-{f["id"]}" startOffset="50%" text-anchor="middle">{esc(f["label"])}</textPath></text>')
    # threads: centre -> hub, hub -> area
    for f in fams:
        hx, hy = pt(R_HUB, f["mid"])
        a(f'<line class="m-e m-e0" data-family="{f["id"]}" x1="{C}" y1="{C}" x2="{hx}" y2="{hy}"/>')
        for slug, deg in f["areas"]:
            x, y = pt(R_AREA - 11, deg)
            a(f'<line class="m-e m-e1" data-family="{f["id"]}" data-area="{slug}" x1="{hx}" y1="{hy}" x2="{x}" y2="{y}"/>')
    # beads: one per worked scenario, beyond the area point
    for f in fams:
        for slug, deg in f["areas"]:
            scen = info[slug]["scen"]
            k = len(scen)
            for j, x in enumerate(scen):
                d = deg + (j - (k - 1) / 2) * 3.4
                bx, by = pt(R_BEAD, d)
                nx, ny = pt(R_AREA + 11, deg)
                a(f'<line class="m-bl" data-area="{slug}" x1="{nx}" y1="{ny}" x2="{bx}" y2="{by}"/>'
                  f'<circle class="m-b" data-area="{slug}" cx="{bx}" cy="{by}" r="4"/>')
    # hubs
    for f in fams:
        hx, hy = pt(R_HUB, f["mid"])
        a(f'<g class="m-h" data-family="{f["id"]}" transform="translate({hx} {hy})"><circle class="m-hit" r="26"/>'
          f'<circle class="m-hub" r="7"/></g>')
    # area points
    for f in fams:
        for slug, deg in f["areas"]:
            x, y = pt(R_AREA, deg)
            ai = info[slug]
            cls = "m-n has-scen" if ai["scen"] else "m-n"
            a(f'<g class="{cls}" data-area="{slug}" data-family="{f["id"]}" data-forums="{" ".join(ai["forums"])}" '
              f'transform="translate({x} {y})"><circle class="m-hit" r="26"/><path class="m-dot" d="M0 -10.5L10.5 0L0 10.5L-10.5 0Z"/></g>')
    # centre mark (the logo)
    a(f'<g class="m-core" transform="translate({C} {C}) scale(1.3) translate(-32 -32)">'
      '<path class="m-core-ring" d="M32 6 58 32 32 58 6 32Z"/><path class="m-core-fill" d="M32 17 47 32 32 47 17 32Z"/>'
      '<circle class="m-core-dot" cx="32" cy="32" r="4.2"/></g>')
    a("</svg>")
    return "".join(s)


def lists(info, fams, forum_label, p):
    """The text version: every area, grouped by family, with its scenarios and forums."""
    fam_label = {f["id"]: f["label"] for f in CFG["families"]}
    out = []
    for f in fams:
        items = []
        for slug, _ in f["areas"]:
            ai = info[slug]
            meta = []
            if ai["scen"]:
                links = ", ".join(
                    f'<a href="{p("library/" + x["slug"] + ".html")}">{esc(x["ref"])} {esc(x["title"])}</a>' for x in ai["scen"])
                n = len(ai["scen"])
                meta.append(f'<p class="map-meta"><span>Worked scenario{"s" if n > 1 else ""} (hypothetical):</span> {links}</p>')
                if ai["forums"]:
                    meta.append('<p class="map-meta map-forums"><span>Forum{} named in {}:</span> {}</p>'.format(
                        "s" if len(ai["forums"]) > 1 else "", "it" if n == 1 else "them",
                        esc(", ".join(forum_label[i] for i in ai["forums"]))))
            else:
                meta.append('<p class="map-meta"><span>No worked scenario for this area yet.</span></p>')
            items.append(
                f'<li class="map-item" data-area="{slug}" data-family-label="{esc(fam_label[f["id"]])}" '
                f'data-forums="{" ".join(ai["forums"])}">'
                f'<a class="map-title" href="{p("practice/" + slug + ".html")}">{esc(ai["title"])}</a>'
                f'<p class="map-blurb">{esc(ai["blurb"])}</p>{"".join(meta)}'
                f'<span class="map-flag" aria-hidden="true">Named in the forum selected above</span></li>')
        out.append(f'<div class="map-fam" data-family="{f["id"]}"><h3>{esc(f["label"])} <small>{len(f["areas"])}</small></h3>'
                   f'<ul class="map-items">{"".join(items)}</ul></div>')
    return "".join(out)


def render(practice, lib, p):
    info = collect(practice, lib)
    fams = layout(info)
    forum_label = {f["id"]: f["label"] for f in CFG["forums"]}
    used = {i for a in info.values() for i in a["forums"]}
    chips = "".join(
        f'<button class="chip" type="button" data-forum="{f["id"]}" aria-pressed="false">{esc(f["label"])}</button>'
        for f in CFG["forums"] if f["id"] in used)
    n_scen = sum(len(a["scen"]) for a in info.values())
    n_with = sum(1 for a in info.values() if a["scen"])
    return {
        "svg": svg(info, fams, forum_label),
        "chips": chips,
        "list": lists(info, fams, forum_label, p),
        "n_areas": len(info), "n_scen": n_scen, "n_with": n_with, "n_fams": len(fams),
    }
